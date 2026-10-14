"""ORGA - cup concept sketches v0 (sketch level, NOT CAD).

Draws, for each of three cup concepts:
  left  panel: side elevation of the LEFT cup in head frame H (viewed from the wearer's left; FRONT is to the LEFT)
  right panel: section through the cup axis (X_H = 0): depth along Y_H (ear on the left, outer shell on the right)
and prints the depth stack, antenna clearance checks and a mass/balance estimate.

Every number carries a source tag. 'assumed-VERIFY' values must not be frozen.
Run:  python orga_concepts_v0.py   -> out/*.png + table on stdout
"""
import math, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

OUT = pathlib.Path(__file__).with_name("out"); OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------- parameters (value, source)
P = {
    "pad_open_h":   (75.0, "file06 target, assumed-VERIFY until pads bought (M7)"),
    "pad_open_w":   (48.0, "file06 target, assumed-VERIFY (M7)"),
    "pad_ring":     (15.0, "assumed-VERIFY: pad ring width (M7)"),
    "pad_t":        (22.0, "file02/06 18-25 uncompressed, assumed-VERIFY"),
    "pad_tc":       (12.0, "file02 10-15 compressed, assumed-VERIFY"),
    "wall":         (2.0,  "file05 FDM typical"),
    "clear":        (0.5,  "file05 FDM shell-over-part"),
    "baffle":       (2.0,  "file02 1.5-2.0"),
    "front_recess": (16.0, "file02 10-15 (+1); gives 30 mm skin-to-baffle worn, assumed-VERIFY"),
    "drv_r":        (20.0, "40 mm driver, assumed-VERIFY (M5)"),
    "drv_body_h":   (8.0,  "file02 5-10, assumed-VERIFY (M5)"),
    "drv_rim_h":    (3.0,  "rear housing height outside magnet, assumed-VERIFY (M5)"),
    "mag_r":        (10.0, "magnet/pole assembly radius, assumed-VERIFY (M5)"),
    "vent_gap":     (1.0,  "air gap over driver rear vents, assumed"),
    "pcb":          (1.6,  "fab standard 4-layer"),
    "top_over_drv": (1.5,  "orga-v1 csv: tallest part allowed over driver = L1 1.5"),
    "bot_B":        (1.9,  "M1-B: RGB LED moved to bottom side, csv H 1.9 VERIFY"),
    "bot_A":        (0.2,  "M1-A: bottom side over driver = test pads only"),
    "rim_jack":     (5.0,  "SJ2-3593D csv H, VERIFY"),
    "rim_wheel":    (9.0,  "Alps EC10E horizontal mounting height (distributor page), VERIFY drawing"),
    "module":       ((18.0, 25.5, 3.1), "ESP32-S3-WROOM-1 datasheet"),
    "module_pcb":   (0.8,  "module substrate thickness, assumed-VERIFY"),
    "ant_len":      (7.0,  "antenna end length of module, assumed-VERIFY (Espressif drawing)"),
    "keepout":      (15.0, "file05/MR-018, VERIFY with Espressif HW guidelines"),
    "ant_below_wall": (6.0, "board flat edge below cup inner top wall, assumed"),
    "cell_std":     ((6.0, 34.0, 50.0), "603450 class, file04 V"),
    "cell_beside":  ((8.0, 25.0, 50.0), "volume-equivalent cell, NO PART CHOSEN, assumed-VERIFY"),
    "swell":        (0.10, "MR-019 >=10 % thickness"),
    "usb":          ((8.94, 7.35, 3.31), "GCT USB4105 datasheet"),
}
v = lambda k: P[k][0]

# cavity (left cup interior) from the ear-pad: cup outer = pad outer, minus wall
A = (v("pad_open_w") + 2 * v("pad_ring")) / 2 - v("wall")   # half width  (X_H)
B = (v("pad_open_h") + 2 * v("pad_ring")) / 2 - v("wall")   # half height (Z_H)

CONCEPTS = {
    "C1": dict(name="C1 STACK - cell behind the left driver", n=2.6, cell="stack"),
    "C2": dict(name="C2 SPLIT - cell in the right cup (5-wire harness)", n=2.6, cell="right"),
    "C3": dict(name="C3 BESIDE - cell below the left driver, squarer cup", n=4.0, cell="beside"),
}

def superellipse(a, b, n, m=400):
    t = np.linspace(0, 2 * np.pi, m)
    c, s = np.cos(t), np.sin(t)
    return a * np.sign(c) * np.abs(c) ** (2 / n), b * np.sign(s) * np.abs(s) ** (2 / n)

def inside(u, w, a, b, n):
    return (abs(u) / a) ** n + (abs(w) / b) ** n <= 1.0

def cell_box(kind):
    """cell footprint in elevation (u0,u1,v0,v1) and depth band (w0,w1) - None if not in left cup"""
    if kind == "stack":
        t, h, L = v("cell_std"); t *= 1 + v("swell")
        w0 = v("drv_body_h") + v("clear")
        return (-L / 2, L / 2, -29.0, -29.0 + h), (w0, w0 + t)
    if kind == "beside":
        t, h, L = v("cell_beside"); t *= 1 + v("swell")
        v1 = -(v("drv_r") + 1.5)
        return (-L / 2, L / 2, v1 - h, v1), (v("clear"), v("clear") + t)
    return None

def stack(kind, m1, wheel=False):
    """w = depth outward from baffle rear face (Y_H). Returns dict of planes."""
    cb = cell_box(kind)
    cell_top = cb[1][1] if cb else 0.0
    rim = max(v("rim_jack"), v("rim_wheel") if wheel else 0)
    if m1 == "B":   # component side faces the driver
        top = max(v("drv_body_h") + v("vent_gap") + v("top_over_drv"),
                  cell_top + v("clear") + v("top_over_drv"),
                  rim + v("clear"))
        inner = top + v("pcb") + v("bot_B") + v("clear")
        ant_w = top - v("module_pcb")            # antenna trace faces the driver
    else:           # component side faces the outer shell
        bot = max(v("drv_body_h") + v("vent_gap") + v("bot_A"), cell_top + v("clear") + v("bot_A"))
        top = bot + v("pcb")
        inner = top + max(rim, v("module")[0][2] if False else v("module")[2]) + v("clear")
        ant_w = top + v("module_pcb")
    return dict(board_comp_side=top, inner=inner, depth=inner + v("wall"), ant_w=ant_w)

def box_dist(b1, b2):
    d = [max(0, lo2 - hi1, lo1 - hi2) for (lo1, hi1), (lo2, hi2) in zip(b1, b2)]
    return math.sqrt(sum(x * x for x in d))

def antenna_checks(kind, m1, v_flat):
    s = stack(kind, m1)
    ant = ((-9, 9), (v_flat - v("ant_len"), v_flat), (s["ant_w"], s["ant_w"]))
    # magnet = cylinder r=mag_r, w 0..drv_body_h
    rad = max(0.0, (v_flat - v("ant_len")) - v("mag_r"))
    dw = max(0.0, s["ant_w"] - v("drv_body_h"))
    res = {"magnet": math.hypot(rad, dw)}
    cb = cell_box(kind)
    if cb:
        res["cell"] = box_dist(ant, ((cb[0][0], cb[0][1]), (cb[0][2], cb[0][3]), cb[1]))
    piv = A + v("wall") + 4
    res["fork pivot"] = box_dist(ant, ((piv, piv), (0, 0), (s["depth"] / 2,) * 2))
    res["steel band end"] = box_dist(ant, ((0, 0), (B + v("wall") + 22,) * 2, (s["depth"] / 2,) * 2))
    res["top-hinge yoke (alt)"] = box_dist(ant, ((0, 0), (B + v("wall") + 3,) * 2, (s["depth"] / 2,) * 2))
    return res

# ---------------------------------------------------------------- drawing
def draw(key, c, m1="B"):
    n = c["n"]
    v_flat = B - v("ant_below_wall")
    s = stack(c["cell"], m1)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(15, 8.2), gridspec_kw=dict(width_ratios=[1.05, 1]))
    fig.suptitle(f"ORGA {c['name']}   (sketch, M1-{m1}, all dims assumed-VERIFY unless datasheet)", fontsize=12, weight="bold")

    # ---- elevation
    x, y = superellipse(A + v("wall"), B + v("wall"), n); ax.fill(x, y, color="#e9e6df", zorder=0)
    x, y = superellipse(A, B, n); ax.plot(x, y, color="k", lw=1.2, label="cavity (inner wall)")
    x, y = superellipse(v("pad_open_w") / 2, v("pad_open_h") / 2, 2.0)
    ax.plot(x, y, ls=":", color="#7a5", lw=1.5, label="ear-pad opening 75x48 (other side)")
    bx_, by_ = superellipse(A - 2, B - 2, n); by_ = np.minimum(by_, v_flat)
    ax.fill(bx_, by_, color="#9bc49b", alpha=.55, zorder=1)
    ax.plot(bx_, by_, color="#2b6b2b", lw=1, zorder=1)
    ax.text(A - 4, 10, "main PCB\n(new outline =\ncavity - 2 mm)", fontsize=8, color="#2b6b2b", ha="left")
    ax.add_patch(Circle((0, 0), v("drv_r"), fill=False, ec="#444", lw=1.3, ls="--", zorder=3))
    ax.add_patch(Circle((0, 0), v("mag_r"), color="#888", alpha=.6, zorder=3))
    ax.text(0, 0, "magnet", ha="center", va="center", fontsize=7, zorder=4)
    ax.text(14, -16, "driver Ø40", fontsize=7, color="#444")
    mw, ml, _ = v("module")
    ax.add_patch(Rectangle((-mw / 2, v_flat - ml), mw, ml, fc="#cdd", ec="#356", zorder=3))
    ax.add_patch(Rectangle((-mw / 2, v_flat - v("ant_len")), mw, v("ant_len"), fc="#f6c", ec="#a26", hatch="///", zorder=4))
    ax.text(0, v_flat - 14, "ESP32-S3\nmodule", ha="center", fontsize=7, zorder=5)
    ko = v("keepout")
    ax.add_patch(Rectangle((-mw / 2 - ko, v_flat - v("ant_len") - ko), mw + 2 * ko, v("ant_len") + 2 * ko,
                           fill=False, ec="red", ls="--", lw=1.2, zorder=5))
    ax.text(mw / 2 + ko - 1, v_flat + ko - 3, "15 mm antenna\nkeep-out", color="red", fontsize=7, ha="right", va="top")
    cb = cell_box(c["cell"])
    if cb:
        (u0, u1, v0, v1), _ = cb
        ax.add_patch(Rectangle((u0, v0), u1 - u0, v1 - v0, fc="#fc8", ec="#b60", alpha=.7, zorder=2,
                               ls="--" if c["cell"] == "stack" else "-"))
        ax.text((u0 + u1) / 2, (v0 + v1) / 2,
                "Li-Po " + ("6x34x50\n(stacked behind PCB)" if c["cell"] == "stack" else "8x25x50 (VERIFY)\nbeside driver"),
                ha="center", va="center", fontsize=7, zorder=6)
    else:
        ax.text(0, -33, "no cell in left cup\n(603450 in right cup)", ha="center", fontsize=8, color="#b60")
    # edge parts (proposal)
    # x-axis is inverted: front (+X) on screen-left, rear (-X) on screen-right
    def mark(u, w, label):
        ax.plot(u, w, "s", color="#036", ms=6, zorder=6)
        if u >= 0:   ax.text(u + 3, w, label, fontsize=7, ha="right", va="center", zorder=6)
        else:        ax.text(u - 3, w, label, fontsize=7, ha="left", va="center", zorder=6)
    mark(-2, -B + 3, "USB-C (down)")
    mark(A * 0.80, -B * 0.62, "3.5 jack (front-low)")
    mark(A * 0.45, -B * 0.85, "MK1 voice")
    mark(-A + 1, 18, "thumbwheel"); mark(-A + 0.5, -2, "MFB"); mark(-A + 4, -26, "POWER")
    mark(-A + 9, 33, "MK2 ref (top-rear)"); mark(-A + 2, 8, "LED window")
    # fork yoke
    piv = A + v("wall") + 4; topb = B + v("wall") + 14
    for sgn in (-1, 1):
        ax.plot([sgn * piv, sgn * piv, sgn * 18], [0, topb - 8, topb], color="#666", lw=4, solid_capstyle="round", zorder=1)
        ax.plot(sgn * piv, 0, "o", color="k", ms=6)
    ax.plot([-18, 18], [topb, topb], color="#666", lw=4)
    ax.plot([0, 0], [topb, topb + 14], color="#333", lw=3, ls="--")
    ax.text(3, topb + 8, "steel band ends in slider\n(>= 22 mm above cavity)", fontsize=7)
    ax.text(piv + 3, 6, "fork pivot\n(plastic fork,\nharness exits\nREAR arm)", fontsize=7, ha="left")
    ax.set_xlim(A + 30, -A - 30)  # front on the left
    ax.set_ylim(-B - 10, B + 40); ax.set_aspect("equal"); ax.grid(alpha=.25)
    ax.set_xlabel("X_H [mm]   FRONT (face) <-   ->  REAR"); ax.set_ylabel("Z_H [mm]  (up)")
    ax.set_title("Left cup, side elevation (seen from the wearer's left)", fontsize=10)
    ax.legend(loc="lower right", fontsize=7)

    # ---- section through the cup axis (Y_H depth horizontal, Z_H vertical)
    f = -v("baffle"); pad_in = f - v("front_recess"); pad_out = pad_in - v("pad_t")
    skin = pad_in - v("pad_tc")
    ro, ri = v("pad_open_h") / 2 + v("pad_ring"), v("pad_open_h") / 2
    for sgn in (-1, 1):
        bx.add_patch(Rectangle((pad_out, sgn * ri if sgn > 0 else -ro), v("pad_t"), ro - ri, fc="#bbb", ec="#777", alpha=.5))
    bx.text(pad_out + 1, ro + 2, "ear pad 22 (12 worn)", fontsize=7)
    # shell outline
    W0, W1 = pad_in, s["depth"]; R = B + v("wall")
    bx.plot([W0, W1 - 6, W1, W1, W1 - 6, W0], [R, R, R - 10, -R + 10, -R, -R], color="k", lw=1.6)
    bx.plot([W1 - v("wall")] * 2, [-R + 10, R - 10], color="k", lw=.8, ls=":")
    bx.add_patch(Rectangle((f, -B), v("baffle"), 2 * B, fc="#666", alpha=.8))
    bx.text(f - 1, B - 4, "baffle", fontsize=7, ha="right")
    # driver
    bx.add_patch(Rectangle((f - 1, -v("drv_r")), 1 + v("baffle"), 2 * v("drv_r"), fc="#444"))
    bx.add_patch(Rectangle((0, -v("drv_r")), v("drv_rim_h"), 2 * v("drv_r"), fc="#777"))
    bx.add_patch(Rectangle((0, -v("mag_r")), v("drv_body_h"), 2 * v("mag_r"), fc="#999", ec="k"))
    bx.text(v("drv_body_h") / 2, 0, "driver\nbody", ha="center", va="center", fontsize=6.5)
    # cell
    if cb:
        (_, _, v0, v1), (w0, w1) = cb
        bx.add_patch(Rectangle((w0, v0), w1 - w0, v1 - v0, fc="#fc8", ec="#b60"))
        bx.text((w0 + w1) / 2, (v0 + v1) / 2, "cell\n+10%", ha="center", va="center", fontsize=6.5, rotation=90)
    # board + module + usb
    top = s["board_comp_side"]; pb = B - 2
    if m1 == "B":
        bx.add_patch(Rectangle((top, -pb), v("pcb"), pb + v_flat, fc="#2b6b2b"))
        bx.add_patch(Rectangle((top - mw * 0 - v("module")[2], v_flat - ml), v("module")[2], ml, fc="#cdd", ec="#356"))
        bx.add_patch(Rectangle((top - v("module")[2], v_flat - v("ant_len")), v("module")[2], v("ant_len"), fc="#f6c", hatch="///", ec="#a26"))
        ul, uw, uh = v("usb"); bx.add_patch(Rectangle((top - uh, -pb), uh, uw, fc="#356"))
        bx.text(top - uh - 1, -pb + 2, "USB-C", fontsize=6.5, ha="right")
        bx.text(top + 2.5, -8, "PCB (components face driver)\nbottom side + debug pads\nface the removable cover", fontsize=7, color="#2b6b2b")
    bx.add_patch(Rectangle((s["ant_w"] - v("keepout"), v_flat - v("ant_len") - v("keepout")), 2 * v("keepout"),
                           v("ant_len") + 2 * v("keepout"), fill=False, ec="red", ls="--"))
    # head + pinna
    bx.axvline(skin, color="#c77", lw=2); bx.text(skin - 1, -B + 2, "head skin (worn)", rotation=90, fontsize=7, ha="right", color="#c77")
    bx.add_patch(Rectangle((skin, -32), 25, 64, fill=False, ec="#c77", ls=":", lw=1.2))
    drv_front = f - 1
    bx.text(skin + 1, -38, f"pinna 20 (median): {drv_front - (skin + 20):.0f} mm clear\npinna 25 (95th): {drv_front - (skin + 25):.0f} mm clear (need 5)", fontsize=7, color="#c77")
    bx.annotate("", (0, -R - 5), (s["depth"], -R - 5), arrowprops=dict(arrowstyle="<->"))
    bx.text(s["depth"] / 2, -R - 9, f"rear cavity {s['depth']:.1f}", ha="center", fontsize=8, weight="bold")
    bx.annotate("", (pad_out, R + 9), (s["depth"], R + 9), arrowprops=dict(arrowstyle="<->"))
    bx.text((pad_out + s["depth"]) / 2, R + 11, f"cup off-head {s['depth'] - pad_out:.0f} / worn {s['depth'] - skin:.0f}", ha="center", fontsize=8)
    bx.set_xlim(pad_out - 6, s["depth"] + 8); bx.set_ylim(-R - 14, R + 16); bx.set_aspect("equal"); bx.grid(alpha=.25)
    bx.set_xlabel("Y_H depth [mm]   EAR <-   ->  OUTER SHELL (0 = baffle rear face)"); bx.set_ylabel("Z_H [mm]")
    bx.set_title("Section X_H = 0 (through cup axis)", fontsize=10)
    fig.tight_layout(); fig.savefig(OUT / f"ORGA-concept-{key}.png", dpi=130); plt.close(fig)

# ---------------------------------------------------------------- report
if __name__ == "__main__":
    print(f"cavity {2*A:.0f} x {2*B:.0f} mm (W x H)")
    # baseline check: 62 mm round board centred on driver axis, flat at Y_B = +26
    for m1 in "AB":
        r = antenna_checks("right", m1, 26.0)
        print(f"BASELINE Ø62 board centred, M1-{m1}: antenna-to-magnet {r['magnet']:.1f} mm (need >= 15)")
    for k, c in CONCEPTS.items():
        n = c["n"]; cb = cell_box(c["cell"])
        fit = "-"
        if cb and c["cell"] == "beside":
            (u0, u1, v0, v1), _ = cb
            fit = all(inside(u, w, A - v("clear"), B - v("clear"), n) for u in (u0, u1) for w in (v0, v1))
        print(f"\n{c['name']}   cell fits in-plane: {fit}")
        for m1 in "AB":
            s, sw = stack(c["cell"], m1), stack(c["cell"], m1, wheel=True)
            print(f"  M1-{m1}: rear cavity {s['depth']:.1f} mm (with 9 mm EC10E wheel at rim: {sw['depth']:.1f})")
            for name, d in antenna_checks(c["cell"], m1, B - v("ant_below_wall")).items():
                print(f"      antenna to {name:<22} {d:5.1f} mm  {'OK' if d >= 15 else 'FAIL'}")
        draw(k, c)
    print("\nPNGs in", OUT)
