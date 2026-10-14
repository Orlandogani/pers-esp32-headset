"""ORGA rev A small printed parts: side keys, thumbwheel, light guide. Built in place (left frame B)."""
import math
from orga_common import *  # noqa: F401,F403
from orga_common import v
from cups import LAY


def _key_plane(k):
    (xw, yw), (nx, ny) = k["wall"], k["n"]
    return Plane(origin=(xw, yw, k["z"]), x_dir=(-ny, nx, 0), z_dir=(nx, ny, 0))


def key_local(name):
    """Key in local frame: Z = outward normal (0 at inner wall), X = rim tangent, Y = cup Z."""
    act, pre, ot = v("key_act_from_wall"), v("key_pretravel"), v("key_overtravel")
    gap = pre + v("sidekey_travel") + ot                      # cap underside to outer surface
    fo = 0.45                                                 # flange stand-off: curved wall clearance
    plunger = Pos(0, 0, -(act - pre)) * Box(2.0, 1.0, (act - pre) - 0.8 - fo, align=CA)
    flange = Pos(0, 0, -0.8 - fo) * Box(8.4, 4.2, 0.8, align=CA)
    body = Pos(0, 0, -fo) * Box(6.4, 2.6, WALL + gap + fo, align=CA)
    cap = Pos(0, 0, WALL + gap) * Box(7.2, 3.4, 1.2, align=CA)
    cap = fillet(cap.edges().filter_by_position(Axis.Z, WALL + gap + 1.19, WALL + gap + 1.21), 0.5)
    k = plunger + flange + body + cap
    top = WALL + gap + 1.2
    if name == "PWR":     # concave dimple: find POWER blind
        k = k - Pos(0, 0, top + 0.5) * Sphere(1.1)
    else:                 # MFB: two raised ridges
        for dx in (-1.6, 1.6):
            k = k + Pos(dx, 0, top) * Box(0.6, 2.6, 0.5, align=CA)
    return k


def key(name):
    return _key_plane(LAY["keys"][name]) * key_local(name)


def wheel():
    W = LAY["wheel"]; r = v("wheel_d") / 2; t = v("wheel_t")
    w = Cylinder(r, t, align=CA)
    n = 36
    for i in range(n):
        a = 2 * math.pi * i / n
        w = w - Pos(r * math.cos(a), r * math.sin(a), -1) * Rot(0, 0, math.degrees(a)) * Box(0.8, 0.7, t + 2, align=CA)
    w = w - Pos(0, 0, -1) * Cylinder(v("wheel_bore_d") / 2, t + 2, align=CA)
    return Pos(W["c"][0], W["c"][1], W["z0"]) * w


def light_guide():
    lx, ly = LAY["led"]; gw, gh = v("lguide_wh")
    z0 = BOARD_TOP + v("led_rgb_lwh")[2] + 0.1
    g = Pos(lx, ly, z0 + 0.8) * Box(gh, gw, 30, align=CA)
    g = split(g, bisect_by=wedge_plane(0), keep=Keep.BOTTOM)
    g = g + Pos(lx, ly, z0) * Box(gh + 1.2, gw + 1.2, 0.8, align=CA)
    return g
