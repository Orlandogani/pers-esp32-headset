"""ORGA rev A cup parts: outer shells, frames (baffle + skirt), PCB outline and layout.

Local frame = board frame B for the LEFT cup (X rear, Y up, Z outward, origin on driver axis at
baffle rear face). Right-cup parts are built in the same frame and mirrored by the caller.
"""
import math
from orga_common import *  # noqa: F401,F403
from orga_common import v

# ============================================================== layout (shared with dummies + DXF)
def layout():
    L = {}
    # shell screw bosses
    L["screws"] = [rim_point_t(t, v("shell_screw_inset"))[:2] for t in v("shell_screw_t_deg")] + \
                  [rim_point_s(s, v("shell_screw_inset"))[:2] for s in v("shell_screw_s_low")]
    # USB-C, bottom centre
    usb_l, usb_w, usb_h = v("usb_lwh")
    L["usb"] = dict(mouth_y=-(B_CAV + 0.3), len=usb_w, width=usb_l, h=usb_h,
                    axis_z=BOARD_TOP + v("usb_plug_axis_above_board"))
    # jack, front-lower: mouth inside the inner wall along the plug axis
    th = math.radians(v("jack_dir_deg")); d = (math.cos(th), math.sin(th))
    xw, yw, nx, ny = rim_point_s(v("jack_s"))
    mi = v("jack_mouth_inset")
    L["jack"] = dict(wall=(xw, yw), n=(nx, ny), d=d, mouth=(xw - mi * d[0], yw - mi * d[1]),
                     axis_z=BOARD_TOP + v("jack_axis_above_board"))
    # side keys on the lower rim
    L["keys"] = {}
    for name, s in (("MFB", v("key_mfb_s")), ("PWR", v("key_pwr_s"))):
        xw, yw, nx, ny = rim_point_s(s)
        L["keys"][name] = dict(wall=(xw, yw), n=(nx, ny), z=BOARD_TOP + v("key_axis_above_board"))
    # edge-drive dial encoder (SIQ-02FVS3, rev A.5): wheel parallel to the board, edge protrudes past the shell
    xw, yw, nx, ny = rim_point_s(v("wheel_s"))
    r = v("wheel_d") / 2; back = r - v("wheel_protrude") - WALL
    L["wheel"] = dict(wall=(xw, yw), n=(nx, ny), c=(xw - back * nx, yw - back * ny), back=back,
                      z0=BOARD_TOP + v("wheel_z0_above_board"))
    L["led"] = v("led_xy")
    L["mics"] = {"MK1": v("mk1_xy"), "MK2": v("mk2_xy")}
    L["pcb_holes"] = v("pcb_holes")
    return L

LAY = layout()


# ============================================================== PCB outline (board frame B)
def board_sketch(with_holes=True):
    sk = offset(se_face(A_CAV, B_CAV), -v("pcb_inset"))
    fx, cy = v("module_flat_x"), v("module_cy")
    sk = sk - Pos(fx + 50, cy, 0) * Rectangle(100, v("module_lwh")[0] + 4.0)      # antenna flat at the rear edge
    # rev B: no arm tunnel any more -> the strip along the front wall is board area again
    hw = v("usb_tab_halfw")
    sk = sk + Pos(0, (-(B_CAV - 0.5) + -44.0) / 2, 0) * Rectangle(2 * hw, (B_CAV - 0.5) - 44.0)
    sk = sk + wheel_tab_sketch()
    for (x, y) in LAY["screws"]:
        sk = sk - Pos(x, y, 0) * Circle(v("pcb_notch_r"))
    if with_holes:
        for (x, y) in LAY["pcb_holes"]:
            sk = sk - Pos(x, y, 0) * Circle(v("m2_clear_d") / 2)
    return sk


def wheel_tab_sketch(grow=0.0):
    """PCB tab under the SW3 dial (rev A.5, routing chat): width along the tangent, from 6 mm inside the
    board edge out to `reach` past the dial centre along the wheel normal."""
    W = LAY["wheel"]; (cx, cy), (nx, ny) = W["c"], W["n"]
    w, reach = v("wheel_tab")
    r0 = -(v("pcb_inset") + 6.0)                       # start well inside the board outline (overlaps it)
    L = reach - r0 + grow
    mid = (reach + grow + r0) / 2 + 0.0
    ang = math.degrees(math.atan2(ny, nx))
    return Pos(cx + mid * nx, cy + mid * ny, 0) * Rot(0, 0, ang) * Rectangle(L, w + 2 * grow)


# ============================================================== outer shell
def _outer_inner_solids():
    outer = split(extrude(se_face(A_OUT, B_OUT), 40), bisect_by=wedge_plane(0), keep=Keep.BOTTOM)
    outer = fillet(outer.edges().filter_by_position(Axis.Z, 12, 40), v("fillet_cosmetic_shell"))
    inner = Pos(0, 0, -1) * extrude(se_face(A_CAV, B_CAV), 41)
    inner = split(inner, bisect_by=wedge_plane(WALL), keep=Keep.BOTTOM)
    inner = fillet(inner.edges().filter_by_position(Axis.Z, 12, 40), 1.0)
    return outer, inner


def shell_base():
    """Outer shell common to both cups: wedge shell, 4 screw bosses, yoke studs, harness grommet, cap-disc groove."""
    outer, inner = _outer_inner_solids()
    shell = outer - inner
    od = v("m2_boss_od")
    for (x, y) in LAY["screws"]:
        boss = (Pos(x, y, 0) * Cylinder(od / 2, 40, align=CA)) & inner
        shell = shell + boss
        shell = shell - Pos(x, y, 0) * Cylinder(v("m2_insert_hole_d") / 2, v("m2_insert_hole_depth"), align=CA)
    import yoke_b as _yb                       # rev B: snap studs for the external yoke, harness grommet, cap disc
    shell = shell + _yb.shell_add(inner)
    shell = shell - _yb.shell_cut()
    return shell, inner


def shell_left():
    shell, inner = shell_base()
    adds, cuts = [], []
    # ---- USB-C: outside overmold pocket (thins the wall to 1 mm) + plug opening + back-stop rib
    U = LAY["usb"]; pw, ph, pdp = v("usb_pocket"); ow, oh = v("usb_opening")
    yo = -B_OUT
    cuts.append(Pos(0, yo + pdp / 2 - 2.0, U["axis_z"]) * Box(pw, pdp + 4.0, ph))
    # plug opening OPEN AT THE BOTTOM EDGE: the receptacle corners sit in the wall line, so the shell must
    # slide down past them; the frame's USB plug tab fills the notch below the receptacle
    ztop = U["axis_z"] + oh / 2
    cuts.append(Pos(0, yo + 2.0, (ztop - 1.0) / 2) * Box(ow, 6.0, ztop + 1.0))
    rib_y0 = U["mouth_y"] + U["len"] + 0.1
    adds.append((Pos(0, rib_y0 + 0.8, BOARD_TOP + 0.3) * Box(9.0, 1.6, 30, align=CA)) & inner)
    # ---- 3.5 mm jack: hole along the plug axis, overmold counterbore, back-stop rib
    J = LAY["jack"]; d = J["d"]; mx, my = J["mouth"]
    cuts.append(along((mx, my, J["axis_z"]), (d[0], d[1], 0), Cylinder(v("jack_hole_d") / 2, 10, align=CA)))
    back = v("jack_len") + 0.1
    rib_c = (mx - (back + 0.8) * d[0], my - (back + 0.8) * d[1])
    rib = Plane(origin=(rib_c[0], rib_c[1], BOARD_TOP + 0.3), x_dir=(-d[1], d[0], 0), z_dir=(0, 0, 1)) * \
        Box(9.0, 1.6, 30, align=CA)
    adds.append(rib & inner)
    # ---- side keys: slot through the wall
    for k in LAY["keys"].values():
        (xw, yw), (nx, ny) = k["wall"], k["n"]
        cuts.append(radial_box(xw, yw, nx, ny, k["z"], 4.0, 6.8, 3.0, start=-1.0))
    # ---- thumbwheel slot
    W = LAY["wheel"]; (xw, yw), (nx, ny) = W["wall"], W["n"]
    r = v("wheel_d") / 2 + 0.3; back = W["back"]
    chord = 2 * math.sqrt(max(r * r - (back - 1.0) ** 2, 1.0)) + 0.6     # slot = wheel chord at the inner wall + 0.3/side
    # open at the bottom edge so the shell can be lowered over the wheel; the frame's plug fills the gap below it
    ztop = W["z0"] + v("wheel_t") + 0.3
    cuts.append(radial_box(xw, yw, nx, ny, (ztop - 1.0) / 2, 6.0, chord, ztop + 1.0, start=-3.0))
    # ---- LED light-guide boss + window
    lx, ly = LAY["led"]; gw, gh = v("lguide_wh")
    led_top = BOARD_TOP + v("led_rgb_lwh")[2]
    boss_z0 = led_top + 0.1 + 0.8
    adds.append((Pos(lx, ly, boss_z0) * Box(gh + 2.6, gw + 2.4, 30, align=CA)) & inner)
    cuts.append(Pos(lx, ly, boss_z0 - 1) * Box(gh + 0.2, gw + 0.2, 40, align=CA))
    # ---- mic ports: boss with gasket recess, wide channel, 1.2 skin hole, mesh recess
    for (x, y) in LAY["mics"].values():
        gap = v("mic_gasket_t") * 0.7
        z_floor = BOARD_TOP + gap
        adds.append((Pos(x, y, z_floor - 0.3) * Cylinder(v("mic_boss_od") / 2, 30, align=CA)) & inner)
        zo = depth_at(x)
        cuts.append(Pos(x, y, z_floor - 0.31) * Cylinder(4.2 / 2, 0.31, align=CA))           # gasket recess
        cuts.append(Pos(x, y, z_floor - 0.1) * Cylinder(v("mic_channel_d") / 2, zo - 1.0 - z_floor + 0.1, align=CA))
        cuts.append(Pos(x, y, zo - 1.5) * Cylinder(v("mic_port_shell_d") / 2, 3, align=CA))
        cuts.append(Pos(x, y, zo - 0.3) * Cylinder(2.0, 2, align=CA))                         # mesh recess
    import os, time
    dbg = os.environ.get("ORGA_DEBUG"); t0 = time.time()
    for i, a in enumerate(adds):
        shell = shell + a
        if dbg: print("add", i, round(time.time() - t0, 1), flush=True)
    for i, c in enumerate(cuts):
        shell = shell - c
        if dbg: print("cut", i, round(time.time() - t0, 1), flush=True)
    return shell


def shell_right_local():
    """Right shell built in the left frame (mirror applied by the caller)."""
    shell, inner = shell_base()
    return shell


# ============================================================== frame (baffle + skirt + lip)
def frame_base():
    bt, sl = v("baffle_t"), v("skirt_len")
    baffle = Pos(0, 0, -bt) * extrude(se_face(A_OUT, B_OUT), bt)
    skirt = Pos(0, 0, -bt - sl) * (extrude(se_face(A_OUT, B_OUT), sl) - extrude(se_face(A_CAV, B_CAV), sl))
    lip = extrude(se_face(A_CAV - 0.3, B_CAV - 0.3), v("lip_h")) - extrude(se_face(A_CAV - 1.3, B_CAV - 1.3), v("lip_h"))
    for (x, y) in LAY["screws"]:
        lip = lip - Pos(x, y, 0) * Cylinder(v("m2_boss_od") / 2 + 0.3, 5, align=CA)
    # groove inside the skirt for the pad ring's snap bumps
    zr = -bt - sl
    zc = zr + v("padring_snap")[2]
    gd = v("skirt_groove_depth")
    groove = Pos(0, 0, zc - 0.8) * (extrude(se_face(A_CAV + gd, B_CAV + gd), 1.6) - extrude(se_face(A_CAV - 0.3, B_CAV - 0.3), 1.6))
    so, sh = v("drv_seat_ring")
    ring = Cylinder(so / 2, sh, align=CA) - Cylinder((v("drv_od") + 0.4) / 2, sh, align=CA)
    frame = baffle + skirt + lip + ring - groove
    frame = frame - Pos(0, 0, -5) * Cylinder(v("drv_hole_d") / 2, 10, align=CA)
    for (x, y) in LAY["screws"]:
        frame = frame - Pos(x, y, -5) * Cylinder(v("m2_clear_d") / 2, 10, align=CA)
    return frame


def wheel_plug():
    """Frame tab that fills the wheel notch below the wheel (the notch is open at the shell's bottom edge)."""
    W = LAY["wheel"]; (xw, yw), (nx, ny) = W["wall"], W["n"]
    r = v("wheel_d") / 2 + 0.3; back = W["back"]
    chord = 2 * math.sqrt(max(r * r - (back - 1.0) ** 2, 1.0)) + 0.6 - 0.4
    h = W["z0"] - v("wheel_plug_gap")
    plug = radial_box(xw, yw, nx, ny, h / 2, WALL + 3.5, chord, h, start=-0.5)
    plug = plug & extrude(se_face(A_OUT, B_OUT), 20)
    # pocket for the PCB's dial tab (+0.3 all round), open upward so the board drops onto the standoffs
    z0 = BOARD_BOT - 0.3
    plug = plug - Pos(0, 0, z0) * extrude(wheel_tab_sketch(0.3), 20)
    return plug


def usb_plug():
    """Frame tab filling the USB notch below the receptacle (outer face follows the overmold pocket)."""
    U = LAY["usb"]; ow, oh = v("usb_opening"); pw, ph, pdp = v("usb_pocket")
    h = U["axis_z"] - oh / 2 - 0.2
    tab = Pos(0, -B_OUT + 1.0, 0) * Box(ow - 0.4, WALL + 2.0, h, align=(Align.CENTER, Align.CENTER, Align.MIN))
    tab = tab & extrude(se_face(A_OUT, B_OUT), 20)
    tab = tab - extrude(se_face(A_CAV - 0.3, B_CAV - 0.3), 20)
    tab = tab - Pos(0, -B_OUT + pdp / 2 - 2.0, U["axis_z"]) * Box(pw, pdp + 4.0, ph)     # keep the overmold pocket
    return tab


def frame_left():
    frame = frame_base() + wheel_plug() + usb_plug()
    for (x, y) in LAY["pcb_holes"]:
        so = Pos(x, y, 0) * Cylinder(v("m2_boss_od") / 2, BOARD_BOT, align=CA)
        so = so - Pos(x, y, BOARD_BOT - v("m2_insert_hole_depth")) * Cylinder(v("m2_insert_hole_d") / 2, 5, align=CA)
        frame = frame + so
    return frame


def cell_box():
    """Cell envelope in the RIGHT cup, expressed in the left frame (mirror later): x>0 is rear here."""
    t, h, L = v("cell_tlw")
    tz = v("tray_z") + v("tray_floor_t")
    cx = v("cell_center_x_rear")
    return (cx - L / 2, cx + L / 2, -h / 2, h / 2, tz, tz + t * (1 + v("cell_swell")))


def frame_right_local():
    """Right frame (built in left frame, rear = +x): battery tray on 4 posts over the driver."""
    frame = frame_base()
    x0, x1, y0, y1, z0, z1 = cell_box()
    c = v("cell_clear_side"); rt, rh = v("tray_rail"); ft = v("tray_floor_t")
    fx0, fx1, fy0, fy1 = x0 - c - rt, x1 + c + rt, y0 - c - rt, y1 + c + rt
    tz = v("tray_z")
    floor = Pos((fx0 + fx1) / 2, (fy0 + fy1) / 2, tz) * Box(fx1 - fx0, fy1 - fy0, ft, align=CA)
    floor = floor - Pos((x0 + x1) / 2, 0, tz - 1) * Box((x1 - x0) - 10, (y1 - y0) - 10, 5, align=CA)
    rails = Pos((fx0 + fx1) / 2, (fy0 + fy1) / 2, tz) * Box(fx1 - fx0, fy1 - fy0, ft + rh, align=CA)
    rails = rails - Pos((x0 + x1) / 2, 0, tz) * Box(x1 - x0 + 2 * c, y1 - y0 + 2 * c, 20, align=CA)
    rails = rails - Pos(fx0 + 2, fy1 - 6, tz + ft) * Box(10, 8, 10, align=CA)   # cable exit, front-top corner (toward the harness grommet)
    tray = floor + rails
    for px in (fx0 + 3, fx1 - 3):
        for py in (fy0 + 3, fy1 - 3):
            tray = tray + Pos(px, py, 0) * Cylinder(3.0, tz, align=CA)
    return frame + tray


# ============================================================== pad adapter ring
def padring():
    """Local frame: z=0 at the skirt end face (Zc = -bt - skirt), flange toward -z, spigot into skirt (+z).
    The bought pad's sleeve wraps over the flange lip; the ring snaps into the skirt groove with 6 bumps on
    slit (flexible) tabs. Pull the pad straight off to remove; the pry notch at the bottom helps."""
    t, lip = v("padring_t"), v("padring_lip")
    sl = v("padring_spigot_len")
    flange = Pos(0, 0, -t) * (extrude(se_face(A_OUT + lip, B_OUT + lip), t) - extrude(se_face(A_CAV - 1.6, B_CAV - 1.6), t))
    spigot = extrude(se_face(A_CAV - 0.15, B_CAV - 0.15), sl) - extrude(se_face(A_CAV - 1.6, B_CAV - 1.6), sl)
    ring = flange + spigot
    pr, plen, pz = v("padring_snap")
    for td in v("padring_snap_t_deg"):
        x, y, nx, ny = rim_point_t(td, 0.15)
        tx, ty = -ny, nx
        pl = Plane(origin=(x, y, pz), x_dir=(tx, ty, 0), z_dir=(nx, ny, 0))
        a = pr * math.sqrt(2)
        ring = ring + pl * Rot(45, 0, 0) * Box(plen, a, a)
        for s in (-1, 1):                         # slits either side make the bump a flexible tab
            ox, oy = x + s * (plen / 2 + 0.6) * tx, y + s * (plen / 2 + 0.6) * ty
            ring = ring - radial_box(ox, oy, nx, ny, (1.5 + sl + 1) / 2, 3.0, 0.8, sl + 1 - 1.5, start=-2.2)
    x, y, nx, ny = rim_point_t(270.0)
    ring = ring - radial_box(x, y, nx, ny, -t / 2, 3.0, 8.0, t + 0.2, start=WALL + lip - 1.2)     # pry notch
    return ring
