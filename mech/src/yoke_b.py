"""ORGA rev B: HS35-style horseshoe yoke (own geometry, not a copy of any part).

Mechanism (same principle as the Corsair HS35 the user showed, our own dimensions):
  * YOKE: a horseshoe band that wraps the UPPER half of the cup, radially outside the shell side wall,
    from a front pivot (y = 0) over the crown to a rear pivot (y = 0). It snaps over two plastic studs
    moulded on the shell (no metal near the antenna). Tilt = rotation about the stud axis (X_B).
    The radial gap grows from 0.6 mm at the pivots to 2.6 mm at the crown, because the crown region of the
    cup swings outward when it tilts; that crown gap is also the tilt stop.
  * SWIVEL: a pin on the yoke crown turns in a collar at the lower end of the slider (the visible ring),
    retained by an M2 set screw that rides in an arc groove (+/- yaw limit), as in rev A.4.
  * S-ARM: the slider's lower end bends out and back down into the collar (the HS35 S-bend).
  * HARNESS: free loop from the collar to a grommet hole in the shell's outer face near the top, outside
    the yoke, so the yoke can never pinch it in tilt.

Left-cup frame (X rear, Y up, Z outward from the baffle rear face); the right cup uses the mirror image.
"""
import math
from orga_common import *  # noqa: F401,F403
from orga_common import v
from build123d import Polyline, Spline, sweep, Line, Wire

T, W = v("yk_t"), v("yk_w")
GS, GT = v("yk_gap_side"), v("yk_gap_top")
ZP = v("yk_pivot_z")
A_IN, B_IN = A_OUT + GS, B_OUT + GT            # yoke inner face (superellipse)
A_YO, B_YO = A_IN + T, B_IN + T                # yoke outer face
Y_CROWN = B_YO                                 # crown outer face at x = 0
PIN_Z = v("pivot_z")                           # swivel-pin axis (unchanged slider socket plane, Y_H = Y_ZC0 + 8)
COL_D, COL_L = v("swivel_collar")
AG = v("swivel_axial_gap")
Y_BOSS = Y_CROWN + 1.0                         # top of the crown boss
Y_COL0 = Y_BOSS + AG                           # collar bottom (cup frame y == Z_H)
Y_COL1 = Y_COL0 + COL_L                        # collar top
Y_GROOVE = (Y_COL0 + Y_COL1) / 2               # set-screw / arc-groove height


def _upper(solid, y0=0.0):
    return solid & Pos(0, y0 + 60, 0) * Box(200, 120, 100)


# ---------------------------------------------------------------- the yoke
def yoke():
    z0 = ZP - W / 2
    band = Pos(0, 0, z0) * (extrude(se_face(A_YO, B_YO, phase_deg=45), W) - extrude(se_face(A_IN, B_IN, phase_deg=45), W))
    y = _upper(band)
    ed = v("yk_end_d")
    for s in (-1, 1):                                                         # round ends with the pivot holes
        y = y + along((s * A_IN, 0, ZP), (s, 0, 0), Cylinder(ed / 2, T, align=CA))
    # cosmetic side panels (recess on the outer face), stopping short of the ends and the crown
    pw, pd, py0 = v("yk_pocket")
    ring = Pos(0, 0, ZP - pw / 2) * (extrude(se_face(A_YO + 1, B_YO + 1, phase_deg=45), pw) -
                                    extrude(se_face(A_YO - pd, B_YO - pd, phase_deg=45), pw))
    for s in (-1, 1):
        y = y - (ring & Pos(s * 30, py0 + (B_IN - 14 - py0) / 2, ZP) * Box(60, B_IN - 14 - py0, 20))
    # crown boss and swivel pin (axis +Y at z = PIN_Z)
    boss = Pos(0, (Y_CROWN - 2.0 + Y_BOSS) / 2, ZP) * Box(14.0, Y_BOSS - Y_CROWN + 2.0, W)
    boss = boss + along((0, Y_CROWN - 2.0, PIN_Z), (0, 1, 0), Cylinder(COL_D / 2, Y_BOSS - Y_CROWN + 2.0, align=CA))
    y = y + (boss - extrude(se_face(A_IN + 0.01, B_IN + 0.01, phase_deg=45), 100))
    pin_d = v("swivel_pin_d")
    y = y + along((0, Y_BOSS - 0.5, PIN_Z), (0, 1, 0), Cylinder(pin_d / 2, Y_COL1 - 0.3 - Y_BOSS + 0.5, align=CA))
    # retention + yaw stop: ARC groove on the +x_B (= -X_H) side of the pin, for the collar's set screw
    yl = v("yaw_limit_deg") + 3.0
    r_ = pin_d
    pts = [(0.0, 0.0)] + [(r_ * math.cos(math.radians(yl * (2 * i / 12 - 1))), r_ * math.sin(math.radians(yl * (2 * i / 12 - 1)))) for i in range(13)] + [(0.0, 0.0)]
    pie = Plane(origin=(0, Y_GROOVE - 1.0, PIN_Z), x_dir=(1, 0, 0), z_dir=(0, 1, 0)) * extrude(make_face(Polyline(*pts)), 2.0)
    gring = along((0, Y_GROOVE - 0.5, PIN_Z), (0, 1, 0), Cylinder(pin_d / 2 + 1, 1.0, align=CA) - Cylinder(pin_d / 2 - 0.6, 1.0, align=CA))
    y = y - (gring & pie)
    # pivot holes with a lead-in chamfer on the inside (snap-on over the studs)
    hd = v("yk_hole_d")
    for s in (-1, 1):
        y = y - along((s * (A_IN - 1), 0, ZP), (s, 0, 0), Cylinder(hd / 2, T + 2, align=CA))
        y = y - along((s * (A_IN - 0.01), 0, ZP), (s, 0, 0), _cone(hd / 2 + 0.8, hd / 2, 0.8))
        # arc slot for the stud's stop lug: lug half-angle + stop angle, through the end boss
        lh, lr, lc = v("yk_lug")
        r1 = v("yk_stud_d") / 2 + lr + lc
        y = y - _stud_plane(s, s * (A_IN - 1)) * extrude(_pie(hd / 2 - 0.1, r1, lh + v("yk_tilt_stop")), T + 2)
    return y


def _pie(r0, r1, half_deg, centre_deg=90.0, n=12):
    """2D annular sector in the y-z plane of a stud (local x = cup y, local y = cup z), centred on +y."""
    a0, a1 = math.radians(centre_deg - half_deg), math.radians(centre_deg + half_deg)
    outer = [(r1 * math.cos(a0 + (a1 - a0) * i / n), r1 * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    inner = [(r0 * math.cos(a1 - (a1 - a0) * i / n), r0 * math.sin(a1 - (a1 - a0) * i / n)) for i in range(n + 1)]
    return make_face(Polyline(*(outer + inner + [outer[0]])))


def _stud_plane(s, x):
    """Plane on the stud axis at cup x, local x = cup +y, local z = outward (s * X_B)."""
    return Plane(origin=(x, 0, ZP), x_dir=(0, 1, 0), z_dir=(s, 0, 0))


def _cone(r0, r1, h):
    from build123d import Cone
    return Cone(r0, r1, h, align=CA)


# ---------------------------------------------------------------- shell features (both cups)
def shell_add(inner):
    """Studs on the outer side wall + reinforcing bosses inside the wall behind them."""
    sd, ch = v("yk_stud_d"), v("yk_stud_chamfer")
    L = GS + T                                     # stud reaches the yoke's outer face
    add = None
    for s in (-1, 1):
        stud = along((s * (A_OUT - 0.6), 0, ZP), (s, 0, 0), Cylinder(sd / 2, 0.6 + L - ch, align=CA))
        stud = stud + along((s * (A_OUT + L - ch), 0, ZP), (s, 0, 0), _cone(sd / 2, sd / 2 - ch * 0.8, ch))
        bd, bh = v("yk_inner_boss")
        boss = along((s * (A_CAV + 0.6), 0, ZP), (-s, 0, 0), Cylinder(bd / 2, 0.6 + bh, align=CA))
        boss = boss & Pos(0, 0, ZP) * Box(200, 200, 2 * (ZP - 0.5))          # stays above the frame lip
        lh, lr, lc = v("yk_lug")                    # tilt-stop lug inside the yoke-end thickness
        lug = _stud_plane(s, s * (A_IN + 0.2)) * extrude(_pie(sd / 2 - 0.3, sd / 2 + lr, lh), T - 0.6)
        part = stud + boss + lug
        add = part if add is None else add + part
    return add


def shell_cut():
    """Harness grommet hole in the outer face near the top (outside the yoke) + the cap-disc ring groove."""
    hx, hy, hd, gd = v("harness_entry")
    zo = depth_at(hx)
    cut = Pos(hx, hy, zo - WALL - 2) * Cylinder(hd / 2, WALL + 4, align=CA)
    cut = cut + Pos(hx, hy, zo - 0.8) * Cylinder(gd / 2, 2, align=CA)
    dd, cy, gw, gdp = v("cap_disc")
    ring = Pos(0, cy, 0) * (Cylinder(dd / 2 + gw / 2, 40, align=CA) - Cylinder(dd / 2 - gw / 2, 40, align=CA))
    ring = split(ring, bisect_by=wedge_plane(gdp), keep=Keep.TOP)
    return cut + ring


# ---------------------------------------------------------------- slider S-arm + collar (head frame H)
def sarm_and_collar(R, CZ, socket_y, t_start_deg):
    """S-arm from the rail end (angle t_start on the band arc) down to the swivel collar at the yoke crown.
    Head frame H: the collar axis is vertical (Z_H) at Y_H = socket_y."""
    sw, st = v("sarm_section")
    t = math.radians(t_start_deg)
    p0 = Vector(0, R * math.sin(t), CZ + R * math.cos(t))
    d0 = Vector(0, math.cos(t), -math.sin(t))
    p1 = Vector(0, socket_y, Y_COL1 - 0.01)
    my, mz = v("sarm_mid")
    path = Wire([Spline(p0, Vector(0, my, mz), p1, tangents=[d0, Vector(0, 0, -1)])])
    prof_pl = Plane(origin=p0, x_dir=(1, 0, 0), z_dir=d0)
    prof = prof_pl * Rectangle(sw, st)
    arm = sweep(prof, path=path)
    col = Pos(0, socket_y, Y_COL0) * Cylinder(COL_D / 2, COL_L, align=CA)
    s = arm + col + Pos(0, socket_y, Y_COL1 - 1.0) * Box(sw, st + 2.0, 2.0, align=CA)
    s = s - Pos(0, socket_y, Y_COL0 - 1) * Cylinder(v("swivel_pin_d") / 2 + 0.2, COL_L + 1.2, align=CA)
    # M2 set-screw pilot from the -X_H side (rides in the pin's arc groove)
    s = s - along((0, socket_y, Y_GROOVE), (-1, 0, 0), Cylinder(0.8, 8, align=CA))
    # harness groove along the +X_H face of the S-arm and down the collar
    gw, gd = v("harness_groove")
    gprof = Plane(origin=p0 + Vector(sw / 2 - gd / 2 + 0.01, 0, 0), x_dir=(1, 0, 0), z_dir=d0) * Rectangle(gd + 0.02, gw)
    s = s - sweep(gprof, path=Pos(sw / 2 - gd / 2 + 0.01, 0, 0) * path)
    s = s - Pos(COL_D / 2 - gd / 2 + 0.01, socket_y, Y_COL0 - 1) * Box(gd + 0.02, gw, COL_L + 2, align=CA)
    return s


# ---------------------------------------------------------------- envelopes for the checks
def tilt_axis_y_h():
    return Y_ZC0 + ZP
