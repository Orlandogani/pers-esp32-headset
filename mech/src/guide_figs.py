"""Assembly-guide figures: labelled exploded views and section details (rev A.4)."""
import math, pathlib, sys
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build123d import Pos, Rot, Cylinder, Box, Plane, mirror, Align  # noqa: E402
from orga_common import v, A_OUT, B_OUT, A_CAV, B_CAV, BOARD_TOP, BOARD_BOT, along, se_face, extrude  # noqa: E402
import render, cups, small_parts as sp, arm as armmod, dummies, yoke_headband as yh  # noqa: E402

REN = HERE.parent / "renders"
CA = (Align.CENTER, Align.CENTER, Align.MIN)
plt = render.plt


def label(ax, M, pts3, text, xy_off, color="k"):
    p = np.array(pts3) @ M.T
    ax.annotate(text, (p[0], p[1]), (p[0] + xy_off[0], p[1] + xy_off[1]), fontsize=9, color=color,
                ha="left" if xy_off[0] >= 0 else "right", va="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=color), bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))


def cup_exploded():
    """Left cup exploded along its axis (cup frame: +Z = outward)."""
    zr = -v("baffle_t") - v("skirt_len")
    E = dummies.left_electronics()
    zp = v("arm_pivot_z")
    parts = [  # (name, solid, dz, colour, label point offset (x, y, z) in local, label text, label screen offset)
        ("pad", dummies.pad(), -70, (0.15, 0.15, 0.15), (0, -B_OUT, zr - 30), "① Ear pad (bought) — sleeve wraps over the pad-ring lip", (-60, -10)),
        ("padring", Pos(0, 0, zr) * cups.padring(), -45, (0.55, 0.55, 0.6), (A_OUT, 0, zr - 1), "② PADRING — snaps into the skirt groove (6 bumps)", (40, -18)),
        ("frame", cups.frame_left(), 0, (0.45, 0.47, 0.52), (A_OUT, -20, -8), "③ CUPL-FRM — baffle + 16 mm skirt; 3 PCB standoffs (M2 inserts)", (45, -10)),
        ("driver", dummies.driver(), 8, (0.75, 0.6, 0.25), (20, 0, 12), "④ Driver — glued to the seat ring, foam gasket", (80, 18)),
        ("pcb", E["PCB"][0], 22, (0.2, 0.6, 0.3), (A_CAV - 3, -25, BOARD_TOP + 22), "⑤ PCB — 3× M2×4 into the standoffs", (60, -22)),
        ("module", E["U2 module"][0], 22, (0.6, 0.75, 0.8), (30, 14, BOARD_TOP + 25), None, None),
        ("arm", armmod.arm(), 40, (0.8, 0.47, 0.15), (-33, 20, 49), "⑥ ARM-L — drops into the shell's tunnel from below", (-70, 5)),
        ("shell", cups.shell_left(), 78, (0.3, 0.32, 0.37), (A_OUT - 4, 30, 100), "⑦ CUPL-OUT — keys, light guide and M3 nut go in first", (70, 20)),
        ("kp", sp.key("PWR"), 78, (0.95, 0.5, 0.1), None, None, None),
        ("km", sp.key("MFB"), 78, (0.95, 0.5, 0.1), None, None, None),
        ("lg", sp.light_guide(), 78, (0.7, 0.9, 1.0), None, None, None),
        ("pivot", along((-A_OUT - 14, 0, zp), (1, 0, 0), Cylinder(2.0, 14.5, align=CA)), 78, (0.7, 0.7, 0.7), (-A_OUT - 14, 0, zp + 78), "⑧ M3 shoulder screw — tilt pivot, from outside (into the nut)", (-60, 25)),
    ]
    items = [(Pos(0, 0, dz) * s, c) for _, s, dz, c, *_ in parts]
    for (x, y) in cups.LAY["screws"]:      # shell screws shown below the baffle, on their way in
        items.append((Pos(x, y, zr - 14) * Cylinder(1.2, 5.0, align=CA), (0.85, 0.2, 0.2)))
    az, el = -55, 22
    ax = render.shade(items, azim=az, elev=el)
    M = render.view_matrix(az, el)
    for name, s, dz, c, lp, txt, off in parts:
        if txt:
            label(ax, M, (lp[0], lp[1], lp[2] if name not in ("padring",) else lp[2] + dz), txt, off)
    x, y = cups.LAY["screws"][2]
    label(ax, M, (x, y, zr - 12), "4× M2×5 shell screws (red) — up through the baffle into the shell; heads hide under the pad ring", (-40, -14))
    ax.set_title("ORGA rev A.4 — left cup, exploded in assembly order (ear side at the bottom)", fontsize=12)
    ax.figure.set_size_inches(14, 13)
    ax.figure.savefig(REN / "ORGA-guide-1_cup_exploded.png", dpi=130, bbox_inches="tight"); plt.close("all")


def pad_detail():
    """Section at the bottom of the left cup (plane X = 6) through the skirt, pad ring, pad and shell."""
    zr = -v("baffle_t") - v("skirt_len")
    sec = [(cups.shell_left(), (0.3, 0.32, 0.37), "CUPL-OUT"), (cups.frame_left(), (0.55, 0.57, 0.63), "CUPL-FRM"),
           (Pos(0, 0, zr) * cups.padring(), (0.85, 0.55, 0.2), "PADRING"), (dummies.pad(), (0.82, 0.82, 0.82), "ear pad (envelope)"),
           (dummies.driver(), (0.75, 0.6, 0.25), "driver")]
    fig, ax = plt.subplots(figsize=(11, 8))
    render.section_yz(sec, x=6.0, ax=ax)
    ax.set_xlim(-48, 24); ax.set_ylim(-56, -30)
    ax.set_xlabel("Z (cup axis) [mm]   ear  ←   → outer shell"); ax.set_ylabel("Y [mm]")
    ax.legend(loc="upper left", fontsize=9)
    notes = [((zr + 4.5, -50.0), "snap bump in the skirt groove", (-6, -53.5)),
             ((zr - 1.0, -53.0), "pad-ring lip: the pad's sleeve stretches over it", (-46, -55)),
             ((-1.6, -47.5), "baffle — shell screws go through it from the ear side", (2, -33)),
             ((0.2, -52.0), "shell bottom edge sits on the baffle; frame lip locates it", (5, -55.0))]
    for xy, t, txy in notes:
        ax.annotate(t, xy, txy, fontsize=9, arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.set_title("Detail A — how the frame, pad ring, pad and shell stack (section through the bottom of the cup)")
    fig.tight_layout(); fig.savefig(REN / "ORGA-guide-2_pad_detail.png", dpi=140); plt.close("all")


def headband_exploded():
    R, CZ = yh.R, yh.CZ
    bt = yh.band_top()
    sl = yh.slider(); slr = mirror(sl, about=Plane.XZ)
    out = 9.0
    loc = lambda d: Pos(0, 0, CZ) * Rot(-d, 0, 0) * Pos(0, 0, -CZ)
    locr = lambda d: Pos(0, 0, CZ) * Rot(d, 0, 0) * Pos(0, 0, -CZ)
    steel = yh.sector(-30.0, v("steel_pin_deg") - 1.5, R + 2.85, R + 3.85, 6.0)
    steel = Pos(0, 0, 25) * steel
    tp = math.radians(v("steel_pin_deg")); rp = R + 3.5
    pin = Pos(-25, rp * math.sin(tp), CZ + rp * math.cos(tp) + 25) * along((0, 0, 0), (1, 0, 0), Cylinder(1.0, 15, align=CA))
    from orga_common import to_head_left, to_head_right, mirror_x
    armL = to_head_left(armmod.arm()); armR = to_head_right(mirror_x(armmod.arm()))
    items = [(bt, (0.25, 0.27, 0.3)), (steel, (0.75, 0.75, 0.8)), (pin, (0.9, 0.2, 0.2)),
             (loc(out) * sl, (0.62, 0.64, 0.68)), (locr(out) * slr, (0.62, 0.64, 0.68)),
             (loc(out) * Pos(0, 0, -14) * armL, (0.8, 0.47, 0.15)), (locr(out) * Pos(0, 0, -14) * armR, (0.8, 0.47, 0.15))]
    az, el = -25, 18
    ax = render.shade(items, azim=az, elev=el)
    M = render.view_matrix(az, el)
    label(ax, M, (0, 0, CZ + R + 6), "⑨ BAND-TOP (cushion foam glues to the inner ribs)", (-60, 45))
    label(ax, M, (0, 30, CZ + R + 30), "[10] spring-steel band — slides in from the +Y end", (90, -10))
    label(ax, M, (-25, rp * math.sin(tp), CZ + rp * math.cos(tp) + 25), "[11] Ø2 cross pin closes the steel slot", (70, 45))
    th = math.radians(48 + out); label(ax, M, (5, R * math.sin(th), CZ + R * math.cos(th)), "[12] SLIDER — rail pushes into the sleeve, clicks every 5 mm, stops at +15.7 mm", (45, -5))
    label(ax, M, (0, yh.SOCKET_Y, 60), "[13] ARM swivel pin into the slider socket; M2 set screw rides in the pin groove", (40, -35))
    ax.set_title("ORGA rev A.4 — headband, exploded (sliders pulled out of their sleeves)", fontsize=12, pad=40)
    ax.figure.set_size_inches(14, 10)
    ax.figure.savefig(REN / "ORGA-guide-3_headband_exploded.png", dpi=130, bbox_inches="tight"); plt.close("all")


def slider_detail():
    R, CZ = yh.R, yh.CZ
    bt, sl = yh.band_top(), yh.slider()
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))
    for ax, d, ttl in ((axs[0], 0.0, "nominal (bump in a detent notch)"), (axs[1], 6.3, "fully extended (bump against the stop wall)")):
        loc = Pos(0, 0, CZ) * Rot(-d, 0, 0) * Pos(0, 0, -CZ)
        render.section_yz([(bt, (0.25, 0.27, 0.3), "BAND-TOP"), (loc * sl, (0.62, 0.64, 0.68), "SLIDER")], x=0.0, ax=ax)
        th = math.radians(yh.BUMP_DEG); r0 = R - 2.0
        cz_, cy_ = CZ + r0 * math.cos(th), r0 * math.sin(th)
        ax.set_xlim(cz_ - 12, cz_ + 12); ax.set_ylim(cy_ - 9, cy_ + 9)
        ax.set_title(ttl); ax.set_xlabel("Z_H [mm]"); ax.set_ylabel("Y_H [mm]")
    axs[0].legend(loc="upper right", fontsize=9)
    fig.suptitle("Detail B — slider detent and pull-out stop (section X = 0 at the left sleeve)")
    fig.tight_layout(); fig.savefig(REN / "ORGA-guide-4_slider_detail.png", dpi=140); plt.close("all")


if __name__ == "__main__":
    cup_exploded(); print("1", flush=True)
    pad_detail(); print("2", flush=True)
    headband_exploded(); print("3", flush=True)
    slider_detail(); print("4", flush=True)
