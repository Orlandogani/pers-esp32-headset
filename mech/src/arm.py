"""ORGA rev A.3: Sony-style single arm (replaces the fork).

The arm drops from the slider's swivel pin, enters the cup through a slot in the top-front rim and runs
down a sealed tunnel along the front wall to a tilt pivot at the cup's centre height (y = 0), so the pad
pressure stays centred (same principle as the XM5, own geometry). Pivot = M3 shoulder screw through the
front wall, the arm lug and a heat-set insert in the tunnel's inner wall.

All in the LEFT cup frame (X rear, Y up, Z outward); the right cup uses the mirror image.
"""
import math
from orga_common import *  # noqa: F401,F403
from orga_common import v
from build123d import Polyline


def P(name):
    return v(name)


def _wedge(t0, t1, r=200.0):
    """2D wedge (face) between superellipse PARAMETER angles t0..t1 [deg] (converted to polar), apex at the origin."""
    pts = [(0.0, 0.0)]
    n = 24
    for i in range(n + 1):
        x, y = se_xy(A_CAV, B_CAV, math.radians(t0 + (t1 - t0) * i / n))
        t = math.atan2(y, x)
        pts.append((r * math.cos(t), r * math.sin(t)))
    pts.append((0.0, 0.0))
    return make_face(Polyline(*pts))


def _band(inset_out, inset_in, t0, t1):
    """2D band along the cavity wall: between (cavity - inset_out) and (cavity - inset_in), angles t0..t1."""
    outer = se_face(A_CAV - inset_out, B_CAV - inset_out, phase_deg=90)
    inner = se_face(A_CAV - inset_in, B_CAV - inset_in, phase_deg=90)
    return (outer - inner) & _wedge(t0, t1)


def _zclip(solid, h, k):
    """Keep zp - h - k*y <= z <= zp + h + k*y (the tilt wedge)."""
    zp = P("arm_pivot_z")
    s = split(solid, bisect_by=Plane(origin=(0, 0, zp + h), z_dir=Vector(0, -k, 1).normalized()), keep=Keep.BOTTOM)
    s = split(s, bisect_by=Plane(origin=(0, 0, zp - h), z_dir=Vector(0, k, 1).normalized()), keep=Keep.TOP)
    return s


K = math.tan(math.radians(P("arm_tilt_deg")))
TE = P("arm_t_e")
I0, AW, AT = P("arm_inset0"), P("arm_w"), P("arm_t")
CLR, TW = P("arm_clr"), P("tunnel_wall")
ZP = P("arm_pivot_z")
LUG_R = P("arm_lug_r")
LUG_X0, LUG_X1 = -(A_CAV - I0), -(A_CAV - I0 - AW)          # lug spans the arm width at y = 0 (front wall)


def _lug(r, grow=0.0):
    x0, x1 = LUG_X0 - grow, LUG_X1 + grow
    return along((x0, 0, ZP), (1, 0, 0), Cylinder(r, x1 - x0, align=CA))


def _exit_stub(start, length, w_tan, h_z):
    xw, yw, nx, ny = rim_point_t(TE)
    return radial_box(xw, yw, nx, ny, ZP, length, w_tan, h_z, start=start)


# ---------------------------------------------------------------- the arm
def arm():
    band = Pos(0, 0, ZP - AT / 2) * extrude(_band(I0, I0 + AW, TE - 4, 180.0), AT)
    a = band + _lug(LUG_R)
    EX = WALL + 5.5
    a = a + _exit_stub(-(I0 + AW), I0 + AW + EX, 7.0, AT)
    # external bar: stub end -> swivel pin
    xw, yw, nx, ny = rim_point_t(TE)
    p1 = (xw + EX * nx, yw + EX * ny)
    y_pin0, y_pin1 = v("fork_pin_y")
    pz = v("pivot_z")
    p2 = (0.0, y_pin0 - 4.0)
    ew, et = P("arm_ext")
    z0 = min(ZP - AT / 2, pz - 3.0)
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    ang = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))
    bar = Pos((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, z0) * Rot(0, 0, ang) * Box(L, ew, et, align=CA)
    a = a + bar + Pos(p1[0], p1[1], z0) * Cylinder(ew / 2, et, align=CA) + Pos(p2[0], p2[1], z0) * Cylinder(ew / 2, et, align=CA)
    # harness groove on the outward (+Z) face of the external bar
    gw, gd = P("harness_groove")
    a = a - Pos((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, z0 + et - gd) * Rot(0, 0, ang) * Box(L + ew, gw, gd + 1, align=CA)
    a = a + Pos(0, (p2[1] + y_pin0 - 0.3) / 2, pz - 3.0) * Box(9.0, y_pin0 - 0.3 - p2[1], 6.0, align=CA)
    # swivel pin (axis +Y) with retention groove for the slider's set screw (unchanged interface)
    pin_d = v("swivel_pin_d")
    a = a + along((0, y_pin0 - 0.5, pz), (0, 1, 0), Cylinder(pin_d / 2, y_pin1 - y_pin0 + 0.5, align=CA))
    # retention + yaw stop: the slider's set screw rides in an ARC groove (±yaw limit) on the +X_H side of the pin
    yl = v("yaw_limit_deg") + 3.0                                   # + half the set-screw tip width
    ring = along((0, (y_pin0 + y_pin1) / 2 - 0.5, pz), (0, 1, 0),
                 Cylinder(pin_d / 2 + 1, 1.0, align=CA) - Cylinder(pin_d / 2 - 0.6, 1.0, align=CA))
    r_ = pin_d
    pts = [(0.0, 0.0)] + [(r_ * math.cos(math.radians(180 + yl * (2 * i / 12 - 1))), r_ * math.sin(math.radians(180 + yl * (2 * i / 12 - 1)))) for i in range(13)] + [(0.0, 0.0)]
    pie = Plane(origin=(0, (y_pin0 + y_pin1) / 2 - 1.0, pz), x_dir=(1, 0, 0), z_dir=(0, 1, 0)) * extrude(make_face(Polyline(*pts)), 2.0)
    a = a - (ring & pie)
    # pivot bore
    a = a - along((LUG_X0 - 1, 0, ZP), (1, 0, 0), Cylinder(P("arm_lug_hole_d") / 2, AW + 2, align=CA))
    return a


# ---------------------------------------------------------------- the tunnel (added to both outer shells)
def tunnel_void():
    """Space the arm sweeps over the tilt range, OPEN DOWN TO THE FRAME so the arm drops in from the open
    side of the shell; the frame's baffle closes the tunnel floor (foam strip seal)."""
    zp = P("arm_pivot_z")
    h = AT / 2 + CLR
    band = Pos(0, 0, -1) * extrude(_band(0.3, I0 + AW + CLR, TE - 10, 183.0), 40)
    void = split(band, bisect_by=Plane(origin=(0, 0, zp + h), z_dir=Vector(0, -K, 1).normalized()), keep=Keep.BOTTOM)
    r = LUG_R + CLR
    lug = _lug(r, CLR) + along((LUG_X0 - CLR, 0, ZP), (1, 0, 0), Box(2 * r, ZP + 1.0, AW + 2 * CLR, align=(Align.MAX, Align.CENTER, Align.MIN)))
    return void + lug


def tunnel_walls(inner):
    """Full-height inner wall of the tunnel (shell plate = ceiling, frame baffle = floor). No tilted planes
    touch the shell plate (that made an invalid print mesh in rev A.3)."""
    band = Pos(0, 0, -1) * extrude(_band(-0.5, I0 + AW + CLR + TW, TE - 13, 186.0), 40)
    g = 1.0     # clip to the cavity grown 1 mm into the shell wall so the union overlaps instead of sharing faces
    grown = Pos(0, 0, -1) * extrude(se_face(A_CAV + g, B_CAV + g, phase_deg=90), 41)
    grown = split(grown, bisect_by=wedge_plane(WALL - g), keep=Keep.BOTTOM)
    return band & grown & Pos(0, 0, 0.1) * Box(200, 200, 40, align=CA)


def rim_slot():
    """Notch in the top-front rim for the arm: tall enough for the full tilt and OPEN AT THE BOTTOM EDGE,
    so the arm drops into the tunnel from the open side of the shell before the frame closes it."""
    xw, yw, nx, ny = rim_point_t(TE)
    s = radial_box(xw, yw, nx, ny, 15.0, WALL + 8.0, 7.0 + 2 * CLR, 40.0, start=-2.0)
    zp = P("arm_pivot_z")
    return split(s, bisect_by=Plane(origin=(0, 0, zp + AT / 2 + CLR), z_dir=Vector(0, -K, 1).normalized()), keep=Keep.BOTTOM)


def pivot_features(shell):
    """Through-hole + counterbore in the front wall, insert boss on the tunnel's inner wall."""
    hd, cb = P("arm_wall_hole_d"), P("arm_screw_head")
    xo = -A_OUT
    shell = shell - along((xo - 1, 0, ZP), (1, 0, 0), Cylinder(hd / 2, WALL + 2, align=CA))
    shell = shell - along((xo - 1, 0, ZP), (1, 0, 0), Cylinder(cb[0] / 2, 1 + cb[1], align=CA))
    bx0 = LUG_X1 + CLR
    bod, blen = P("arm_insert_boss")
    shell = shell + along((bx0, 0, ZP), (1, 0, 0), Cylinder(bod / 2, blen, align=CA))
    shell = shell - along((bx0 - 0.1, 0, ZP), (1, 0, 0), Cylinder(v("m3_clear_d") / 2, blen + 0.2, align=CA))
    # M3 nut trap, open toward the cavity (+X): push the nut in along the screw axis before closing the cup
    af, nt = v("m3_nut")
    hexa = make_face(Polyline(*[(af / math.sqrt(3) * math.cos(math.radians(30 + 60 * i)),
                                 af / math.sqrt(3) * math.sin(math.radians(30 + 60 * i))) for i in range(7)]))
    trap = Plane(origin=(bx0 + blen - nt, 0, ZP), x_dir=(0, 1, 0), z_dir=(1, 0, 0)) * extrude(hexa, nt + 1.0)
    shell = shell - trap
    # harness passage from the tunnel into the cavity, just above the pivot
    shell = shell - along((bx0 - 1, 8.0, ZP), (1, 0, 0), Cylinder(P("harness_bore_d") / 2, blen + 3, align=CA))
    return shell


def board_trim():
    """2D region the PCB must avoid (tunnel + insert boss), in board frame B."""
    t = _band(-3.0, I0 + AW + CLR + TW + 0.5, TE - 14, 187.0)
    bod, blen = P("arm_insert_boss")
    x0, x1 = -A_CAV - 2.0, LUG_X1 + CLR + blen + 1.5   # nut + screw tip + tweezer room
    t = t + Pos((x0 + x1) / 2, 0, 0) * Rectangle(x1 - x0, bod + 1.0)
    return t


def frame_lip_cut():
    """Region removed from the frame's locating lip where the tunnel walls sit."""
    return extrude(_band(-1.0, I0 + AW + CLR + TW + 0.3, TE - 14, 187.0), 5.0)
