"""Shared geometry for ORGA rev A (build123d). All numbers come from params/orga_params.py.

Left-cup local frame == board frame B (M1-A): X rear, Y up, Z outward, origin on the driver
axis at the baffle rear face. Right-cup parts are mirrored (x -> -x) and placed with their own map.
"""
import math, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "params"))
from orga_params import v  # noqa: E402
from build123d import (Spline, Wire, Vector, Plane, Axis, Pos, Rot, Box, Cylinder, Sphere,  # noqa: F401
                       extrude, make_face, offset, split, fillet, chamfer, Keep, Align, Location,
                       Compound, Part, mirror, Polyline, Rectangle, Circle, RectangleRounded, Sketch)

REV = "B"
WALL = v("wall_fdm")
A_CAV = (v("pad_open_w") + 2 * v("pad_ring_w")) / 2 - WALL      # 37.0  cavity half width  (X)
B_CAV = (v("pad_open_h") + 2 * v("pad_ring_w")) / 2 - WALL      # 50.5  cavity half height (Y)
A_OUT, B_OUT = A_CAV + WALL, B_CAV + WALL
N = v("cup_n")
BOARD_BOT = v("board_bot_z")
BOARD_TOP = BOARD_BOT + v("pcb_t")
CA = (Align.CENTER, Align.CENTER, Align.MIN)   # cylinder/box sitting on its local XY plane


# ---------------------------------------------------------------- superellipse helpers
def se_xy(a, b, t, n=N):
    c, s = math.cos(t), math.sin(t)
    return a * math.copysign(abs(c) ** (2 / n), c), b * math.copysign(abs(s) ** (2 / n), s)


def se_normal(a, b, x, y, n=N):
    gx = math.copysign((abs(x) / a) ** (n - 1), x) / a if x else 0.0
    gy = math.copysign((abs(y) / b) ** (n - 1), y) / b if y else 0.0
    L = math.hypot(gx, gy)
    return gx / L, gy / L


def se_x_at_y(a, b, y, side=+1, n=N):
    """x on the superellipse for a given y (side=+1 rear, -1 front)."""
    return side * a * max(0.0, 1 - (abs(y) / b) ** n) ** (1 / n)


def rim_point(y, side, inset=0.0, a=A_CAV, b=B_CAV):
    """Point on the cavity wall at height y, moved `inset` mm inward along the normal; returns (x, y, nx, ny)."""
    x = se_x_at_y(a, b, y, side)
    nx, ny = se_normal(a, b, x, y)
    return x - inset * nx, y - inset * ny, nx, ny


def rim_point_t(t_deg, inset=0.0, a=A_CAV, b=B_CAV):
    x, y = se_xy(a, b, math.radians(t_deg))
    nx, ny = se_normal(a, b, x, y)
    return x - inset * nx, y - inset * ny, nx, ny


def _rim_table(a=A_CAV, b=B_CAV, n=N, m=3601):
    ts = [180 + 180 * i / (m - 1) for i in range(m)]
    pts = [se_xy(a, b, math.radians(t), n) for t in ts]
    s = [0.0]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        s.append(s[-1] + math.hypot(x1 - x0, y1 - y0))
    return ts, s


_TS, _SS = _rim_table()


def t_at_s(s_mm):
    """Superellipse angle [deg] at arc length s along the LOWER half of the cavity, starting at the front pivot."""
    import bisect
    i = min(bisect.bisect_left(_SS, s_mm), len(_SS) - 1)
    return _TS[i]


def rim_point_s(s_mm, inset=0.0):
    return rim_point_t(t_at_s(s_mm), inset)


def se_face(a, b, n=N, z=0.0, m=96, phase_deg=0.0):
    ph = math.radians(phase_deg)   # moves the spline seam away from features cut at y = 0
    pts = [Vector(*se_xy(a, b, ph + 2 * math.pi * i / m, n), z) for i in range(m)]
    return make_face(Wire([Spline(*pts, periodic=True)]))


def depth_at(x):
    """Outer-face depth (Zc) of the left shell at rear-coordinate x (wedge)."""
    return v("shell_d0") + v("shell_slope") * x


def wedge_plane(offset_in=0.0):
    """Plane of the shell outer face (offset_in > 0 moves it inward, i.e. the inner face)."""
    nrm = Vector(-v("shell_slope"), 0, 1).normalized()
    return Plane(origin=(0, 0, v("shell_d0") - offset_in / nrm.Z), z_dir=nrm)


def along(origin, direction, solid):
    """Place `solid` (built on its local XY plane, axis +Z) with its axis along `direction`."""
    d = Vector(*direction).normalized()
    x_dir = Vector(0, 0, 1).cross(d)
    if x_dir.length < 1e-6:
        x_dir = Vector(1, 0, 0)
    return Plane(origin=origin, x_dir=x_dir.normalized(), z_dir=d) * solid


def radial_box(x, y, nx, ny, z_c, length, w_tan, h_z, start=0.0):
    """Box whose long axis runs along the in-plane normal (nx, ny), starting `start` mm from (x, y),
    width w_tan along the tangent, height h_z centred at z_c."""
    pl = Plane(origin=(x + start * nx, y + start * ny, z_c), x_dir=(-ny, nx, 0), z_dir=(nx, ny, 0))
    return pl * Box(w_tan, h_z, length, align=CA)


# ---------------------------------------------------------------- frames -> head frame H
PAD_STACK = v("padring_t") + v("pad_t") + v("skirt_len") + v("baffle_t")  # Zc of pad face = -PAD_STACK
Y_ZC0 = v("pad_face_y_h") + PAD_STACK                                      # Y_H of Zc = 0 (left)


def to_head_left(obj):
    """(x_B, y_B, z_B) -> (X_H, Y_H, Z_H) = (-x_B, z_B + Y_ZC0, y_B)."""
    loc = Location(Plane(origin=(0, Y_ZC0, 0), x_dir=(-1, 0, 0), z_dir=(0, 1, 0)))
    return loc * obj


def to_head_right(obj_mirrored):
    """Right-cup local frame (X fwd, Y up, Z outward = -Y_H): (x, y, z) -> (x, -Y_ZC0 - z, y)."""
    loc = Location(Plane(origin=(0, -Y_ZC0, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0)))
    return loc * obj_mirrored


def mirror_x(obj):
    return mirror(obj, about=Plane.YZ)
