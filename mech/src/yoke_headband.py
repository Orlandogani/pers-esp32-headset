"""ORGA headband (rev B: slider ends in the S-arm + swivel collar, see yoke_b.py; fork() is the obsolete rev A yoke) and: sliders + top band (head frame H, arc in the Y-Z plane)."""
import math
from orga_common import *  # noqa: F401,F403
from orga_common import v
from build123d import ThreePointArc, Line


# ============================================================== fork (left cup frame; mirror for right)
def fork():
    """Oval fork (rev A.1): an arch that follows the cup outline (same superellipse exponent),
    from the front pivot over the top to the rear pivot; swivel pin on top."""
    aw, at = v("fork_arm"); clr = v("fork_clear"); pz = v("pivot_z")
    xi = A_OUT + v("pivot_boss")[1] + clr          # inner face at the pivots (clears the pivot bosses)
    yi = v("fork_bar_y")                           # inner face at the top (clears the cup in tilt)
    xo, yo = xi + aw, yi + aw
    y_pin0, y_pin1 = v("fork_pin_y")
    z0 = pz - at / 2
    ring = Pos(0, 0, z0) * (extrude(se_face(xo, yo, phase_deg=45), at) - extrude(se_face(xi, yi, phase_deg=45), at))
    f = ring & Pos(0, 50, z0 - 1) * Box(200, 100, at + 2, align=CA)          # keep the upper half
    for sgn in (-1, 1):                                                       # round pivot ends
        f = f + Pos(sgn * (xi + xo) / 2, 0, z0) * Cylinder(aw / 2, at, align=CA)
    # stem from the arch crown to the swivel pin, flared into the arch
    f = f + Pos(0, (yo - 1 + y_pin0) / 2, z0) * Box(10, y_pin0 - yo + 1, at, align=CA)
    for sgn in (-1, 1):
        g = Pos(sgn * 7, yo + 1, z0) * Box(6, 4, at, align=CA)
        g = g - Pos(sgn * 10, yo + 4, z0 - 1) * Cylinder(4, at + 2, align=CA)
        f = f + g
    # swivel pin (axis +Y) with retention groove for the slider's M2 set screw
    pin_d = v("swivel_pin_d")
    pin = along((0, y_pin0 - 0.5, pz), (0, 1, 0), Cylinder(pin_d / 2, y_pin1 - y_pin0 + 0.5, align=CA))
    groove = along((0, (y_pin0 + y_pin1) / 2 - 0.5, pz), (0, 1, 0),
                   Cylinder(pin_d / 2 + 1, 1.0, align=CA) - Cylinder(pin_d / 2 - 0.6, 1.0, align=CA))
    f = f + pin - groove
    # pivot pins (inward); the rear one is hollow for the 5-wire harness
    pd = v("pivot_pin_d"); plen = xi - (A_CAV + 0.2)
    for sgn in (-1, 1):
        f = f + along((sgn * xi, 0, pz), (-sgn, 0, 0), Cylinder(pd / 2, plen, align=CA))
    hb = v("harness_bore_d")
    f = f - along((A_CAV, 0, pz), (1, 0, 0), Cylinder(hb / 2, xo - A_CAV + 1, align=CA))
    # harness channel along the outer edge of the rear arm, from the pivot to the crown
    ch = Pos(0, 0, pz - (hb + 0.2) / 2) * (extrude(se_face(xo + 1, yo + 1, phase_deg=45), hb + 0.2) -
                                          extrude(se_face(xo - hb - 0.7, yo - hb - 0.7, phase_deg=45), hb + 0.2))
    ch = ch & Pos(50, 50, pz - 5) * Box(100, 100, 10, align=CA)
    ch = ch + Pos((xi + xo) / 2 + 1.0, 0, pz - (hb + 0.2) / 2) * Box(hb + 1.2, hb + 0.2, hb + 0.2, align=CA)
    f = f - ch
    return f


# ============================================================== headband (head frame H)
R = v("band_r"); CZ = v("band_center_z")


def _pt(theta_deg, r):
    t = math.radians(theta_deg)
    return (0.0, r * math.sin(t), CZ + r * math.cos(t))


def sector(t0, t1, r0, r1, half_w):
    """Annular sector in the Y-Z plane between angles t0..t1 (deg from +Z toward +Y), extruded +/- half_w in X."""
    tm = (t0 + t1) / 2
    w = Wire([ThreePointArc(_pt(t0, r1), _pt(tm, r1), _pt(t1, r1)), Line(_pt(t1, r1), _pt(t1, r0)),
              ThreePointArc(_pt(t1, r0), _pt(tm, r0), _pt(t0, r0)), Line(_pt(t0, r0), _pt(t0, r1))])
    face = make_face(w)
    return Pos(-half_w, 0, 0) * extrude(face, 2 * half_w, dir=(1, 0, 0))


def tangent_plane(theta_deg, r):
    t = math.radians(theta_deg)
    return Plane(origin=_pt(theta_deg, r), x_dir=(1, 0, 0), z_dir=(0, math.sin(t), math.cos(t)))


SOCKET_Y = Y_ZC0 + v("pivot_z")
TAB_DEG = 36.0
_SKIN_R = ((R - 3.5) + (R - v("rail_section")[1] / 2 - 0.2)) / 2
BUMP_DEG = TAB_DEG + math.degrees(3.0 / _SKIN_R)          # bump sits 3 mm from the tab centre
DETENT_DEG = math.degrees(v("band_detent_pitch") / (R - 2.0))


def slider():
    """Left slider (Y_H > 0). Mirror about XZ for the right one."""
    rw, rt = v("rail_section")
    y_pin0, y_pin1 = v("fork_pin_y")
    t_bot = v("sarm_start_deg") + 0.5          # rev B: the rail ends where the S-arm starts
    s = sector(v("slider_top_deg"), t_bot, R - rt / 2, R + rt / 2, rw / 2)
    # rev B: the slider ends in an S-arm that drops to the swivel collar at the yoke crown (HS35-style)
    import yoke_b as _yb
    s = s + _yb.sarm_and_collar(R, CZ, SOCKET_Y, v("sarm_start_deg"))
    # detent notches on the rail inner face (pitch 5 mm, +/- 3 steps)
    for k in range(-3, 4):
        th = BUMP_DEG + k * DETENT_DEG
        if th < v("slider_top_deg") + 0.5:
            continue
        s = s - tangent_plane(th, R - rt / 2) * Rot(45, 0, 0) * Box(rw + 1, 0.9, 0.9)
        if k == -3:   # last notch = pull-out STOP: square wall on its -theta side, so the bump cannot ramp out
            s = s - tangent_plane(th, R - rt / 2) * Box(rw + 1, 0.64, 0.64, align=(Align.CENTER, Align.MAX, Align.MIN))
    # lead-in chamfer at the rail tip so the band's detent bump rides up on insertion
    s = s - tangent_plane(v("slider_top_deg"), R - rt / 2) * Rot(45, 0, 0) * Box(rw + 1, 1.4, 1.4)
    # harness: groove along the +X face of the rail, notch down the outer side of the socket
    gw, gd = v("harness_groove")
    s = s - Pos(rw / 2 - gd / 2 + 0.01, 0, 0) * sector(v("slider_top_deg") - 1, t_bot + 1, R - gw / 2, R + gw / 2, gd / 2 + 0.01)
    return s


def band_top():
    bw, br = v("band_section"); half = v("band_half_deg")
    rw, rt = v("rail_section"); sw, st = v("steel_slot")
    r0, r1 = R - 3.5, R - 3.5 + br
    b = sector(-half, half, r0, r1, bw / 2)
    for sgn in (1, -1):
        sl = sector(22.0, half + 1, R - rt / 2 - 0.2, R + rt / 2 + 0.2, rw / 2 + 0.2)
        b = b - (sl if sgn > 0 else mirror(sl, about=Plane.XZ))
    b = b - sector(-30.0, half + 1, R + 2.8, R + 2.8 + st, sw / 2)     # steel band slot, open at the +Y end face
    # cross pin that closes the slot after the steel band is pushed in
    tp = math.radians(v("steel_pin_deg")); rp = R + 2.8 + st / 2
    b = b - Pos(-bw / 2 - 1, rp * math.sin(tp), CZ + rp * math.cos(tp)) * along((0, 0, 0), (1, 0, 0), Cylinder(v("steel_pin_d") / 2, bw + 2, align=CA))
    b = b - Pos(bw / 2 - 1.1, 0, 0) * sector(-half - 1, half + 1, R - 1.6, R + 1.6, 2.1)  # harness groove (+X face)
    # lightening pockets on the cushion side (|theta| < 19 deg), ribs every ~6 deg
    for a0 in range(-19, 19, 6):
        b = b - sector(a0 + 0.6, min(a0 + 6, 19) - 0.6, r0 - 0.1, R + 1.8, 8.5)
    # detent flexure tabs in the inner skin under each sleeve
    skin_r = (r0 + R - rt / 2 - 0.2) / 2
    skin_t = (R - rt / 2 - 0.2) - r0
    for sgn in (1, -1):
        pl = tangent_plane(TAB_DEG, skin_r)
        slit = pl * (Pos(0, 0.3, 0) * Box(6.2, 8.6, skin_t + 0.2) - Pos(0, -0.5, 0) * Box(5.0, 9.0, skin_t + 0.4))
        # V-shaped bump (matches the rail notches), 0.6 proud of the sleeve floor
        bump = tangent_plane(BUMP_DEG, R - rt / 2 - 0.2) * Rot(45, 0, 0) * Box(3.0, 0.85, 0.85)
        if sgn < 0:
            slit, bump = mirror(slit, about=Plane.XZ), mirror(bump, about=Plane.XZ)
        b = b - slit + bump
    return b
