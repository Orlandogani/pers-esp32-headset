"""Envelopes of purchased / electronic parts for interference and antenna checks (NOT printed).

All in the left frame B unless noted. Sizes from params (most are assumed-VERIFY).
Each entry: name -> (solid, is_metal)
"""
import math
from orga_common import *  # noqa: F401,F403
from orga_common import v
from cups import LAY, board_sketch, cell_box


def driver():
    od = v("drv_od")
    d = Cylinder(od / 2, v("drv_flange_t"), align=CA)
    d = d + Cylinder(od / 2 - 0.5, v("drv_rim_h"), align=CA)
    d = d + Cylinder(v("drv_mag_d") / 2, v("drv_body_h"), align=CA)
    d = d + Pos(0, 0, -v("baffle_t")) * Cylinder(v("drv_hole_d") / 2 - 0.3, v("baffle_t"), align=CA)
    return d


def left_electronics():
    D = {}
    D["PCB"] = (Pos(0, 0, BOARD_BOT) * extrude(board_sketch(), v("pcb_t")), False)
    mw, ml, mh = v("module_lwh")
    fx, cy = v("module_flat_x"), v("module_cy")
    D["U2 module"] = (Pos(fx - ml / 2, cy, BOARD_TOP) * Box(ml, mw, mh, align=CA), True)
    D["antenna"] = (Pos(fx - v("antenna_len") / 2, cy, BOARD_TOP) * Box(v("antenna_len"), mw, 0.8, align=CA), False)
    U = LAY["usb"]
    D["J1 USB-C"] = (Pos(0, U["mouth_y"] + U["len"] / 2, BOARD_TOP) * Box(U["width"], U["len"], U["h"], align=CA), True)
    J = LAY["jack"]; d = J["d"]; mx, my = J["mouth"]; L = v("jack_len")
    c = (mx - L / 2 * d[0], my - L / 2 * d[1])
    D["J4 jack"] = (Plane(origin=(c[0], c[1], BOARD_TOP), x_dir=(d[0], d[1], 0), z_dir=(0, 0, 1)) *
                    Box(L, 10.7, v("jack_h"), align=CA), True)
    for name, k in LAY["keys"].items():
        (xw, yw), (nx, ny) = k["wall"], k["n"]
        act = v("key_act_from_wall")
        D[f"SW {name}"] = (radial_box(xw, yw, -nx, -ny, BOARD_TOP + 0.675, 2.9, 3.5, 1.35,
                                      start=act), True)
    W = LAY["wheel"]
    (cx, cy), (nx, ny) = W["c"], W["n"]
    bl, bw = v("enc_body_lw")
    body = radial_box(cx, cy, -nx, -ny, BOARD_TOP + v("wheel_mount_h") / 2, bl, bw, v("wheel_mount_h"), start=-1.0)
    D["SW3 encoder body"] = (body, True)
    D["SW3 wheel"] = (Pos(cx, cy, W["z0"]) * Cylinder(v("wheel_d") / 2, v("wheel_t"), align=CA), False)
    lx, ly = LAY["led"]
    D["D7+D3 LEDs"] = (Pos(lx, ly, BOARD_TOP) * Box(2.8, 5.6, v("led_rgb_lwh")[2], align=CA), False)
    for name, (x, y) in LAY["mics"].items():
        D[name] = (Pos(x, y, BOARD_BOT - v("mic_lwh")[2]) * Box(4.0, 3.0, v("mic_lwh")[2], align=CA), True)
    D["driver L"] = (driver(), False)                      # frame assumed plastic (VERIFY driver construction)
    D["driver L magnet"] = (Cylinder(v("drv_mag_d") / 2, v("drv_body_h"), align=CA), True)
    # brass inserts + screws (metal, for the antenna check)
    for i, (x, y) in enumerate(LAY["screws"]):
        D[f"insert shell {i+1}"] = (Pos(x, y, 0) * Cylinder(1.8, v("m2_insert_hole_depth"), align=CA), True)
        D[f"screw shell {i+1}"] = (Pos(x, y, -v("baffle_t") - 1.3) * Cylinder(1.9, 1.3, align=CA), True)
    for i, (x, y) in enumerate(LAY["pcb_holes"]):
        D[f"insert pcb {i+1}"] = (Pos(x, y, BOARD_BOT - v("m2_insert_hole_depth")) * Cylinder(1.8, v("m2_insert_hole_depth"), align=CA), True)
        D[f"screw pcb {i+1}"] = (Pos(x, y, BOARD_TOP) * Cylinder(1.9, 1.3, align=CA), True)
    return D


def pad():
    """Ear pad envelope (left frame): from padring flange face toward the head."""
    z0 = -v("baffle_t") - v("skirt_len") - v("padring_t")
    ring = extrude(se_face(A_OUT, B_OUT), v("pad_t")) - extrude(se_face(v("pad_open_w") / 2, v("pad_open_h") / 2, 2.2), v("pad_t"))
    return Pos(0, 0, z0 - v("pad_t")) * ring


def right_contents_local():
    D = {"driver R": (driver(), False), "driver R magnet": (Cylinder(v("drv_mag_d") / 2, v("drv_body_h"), align=CA), True)}
    x0, x1, y0, y1, z0, z1 = cell_box()
    t = v("cell_tlw")[0]
    D["cell"] = (Pos((x0 + x1) / 2, 0, z0) * Box(x1 - x0, y1 - y0, t, align=CA), True)
    D["cell swell"] = (Pos((x0 + x1) / 2, 0, z0) * Box(x1 - x0, y1 - y0, z1 - z0, align=CA), False)
    return D
