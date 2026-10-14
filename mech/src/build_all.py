"""ORGA rev A: build every part, export STEP / 3MF / STL, render review PNGs, run V0 checks, write the
PCB change package (DXF + table). Usage:  python src/build_all.py   (outputs under out/ and renders/)
"""
import json, math, pathlib, sys, time
import numpy as np
T0 = time.time()
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from build123d import Compound, export_step, export_stl, Mesher, Pos, Plane, Box  # noqa: E402
from orga_common import v, REV, A_CAV, B_CAV, BOARD_TOP, BOARD_BOT, to_head_left, depth_at, WALL  # noqa: E402
import parts, checks, render, cups, dummies  # noqa: E402

OUT = ROOT / "out"; REN = ROOT / "renders"
for d in (OUT / "step", OUT / "print", REN):
    d.mkdir(parents=True, exist_ok=True)
log = lambda *a: print(f"[{time.time() - T0:6.1f}s]", *a, flush=True)
COL = {"CUPL-OUT": (0.30, 0.32, 0.37), "CUPR-OUT": (0.30, 0.32, 0.37), "CUPL-FRM": (0.45, 0.47, 0.52),
       "CUPR-FRM": (0.45, 0.47, 0.52), "PADRING-L": (0.55, 0.55, 0.58), "PADRING-R": (0.55, 0.55, 0.58),
       "KEY-PWR": (0.85, 0.35, 0.15), "KEY-MFB": (0.85, 0.55, 0.15), "WHEEL": (0.85, 0.45, 0.15),
       "LGUIDE": (0.75, 0.9, 1.0), "YOKE-L": (0.88, 0.88, 0.9), "YOKE-R": (0.88, 0.88, 0.9),
       "SLIDER-L": (0.6, 0.62, 0.66), "SLIDER-R": (0.6, 0.62, 0.66), "BAND-TOP": (0.25, 0.27, 0.3)}
ENV_COL = (0.3, 0.6, 0.3)

# ------------------------------------------------------------------ build
log("building parts")
P = parts.build()
log("envelopes")
E = parts.envelopes()

# ------------------------------------------------------------------ export
log("export STEP / 3MF / STL")
asm = []
for n, d in P.items():
    stem = f"ORGA-M-{n}-{REV}"
    export_step(d["local"], str(OUT / "step" / f"{stem}.step"))
    export_stl(d["print"], str(OUT / "print" / f"{stem}.stl"), tolerance=0.02, angular_tolerance=0.15)
    m = Mesher(); m.add_shape(d["print"], linear_deflection=0.02, angular_deflection=0.15); m.write(str(OUT / "print" / f"{stem}.3mf"))
    h = d["H"]; h.label = n; asm.append(h)
export_step(Compound(children=asm, label=f"ORGA-M-ASM-{REV}"), str(OUT / f"ORGA-M-ASM-{REV}.step"))
envs = []
for n, (s, metal, side) in E.items():
    s.label = n; envs.append(s)
export_step(Compound(children=envs, label="purchased envelopes"), str(OUT / f"ORGA-M-ASM-{REV}_envelopes.step"))

# ------------------------------------------------------------------ V0 checks
log("V0: interference")
items = {n: d["H"] for n, d in P.items()}
items.update({n: s for n, (s, metal, side) in E.items()})
hits = checks.interference(items)
log("V0: clearances")
left_env = [n for n, (s, m, side) in E.items() if side == "L" and n not in ("antenna", "pad L")
            and not n.startswith("insert") and not n.startswith("screw")]
clr_shell = checks.clearances(P["CUPL-OUT"]["H"], {n: E[n][0] for n in left_env}, left_env)
clr_cell = checks.clearances(P["CUPR-OUT"]["H"], {"cell swell": E["cell swell"][0]}, ["cell swell"])
drv_pcb = E["driver L"][0].distance_to(E["PCB"][0])
log("V0: antenna")
metals = {n: s for n, (s, metal, side) in E.items() if metal and n != "U2 module"}
metals["steel band"] = checks.steel_band()
ant = checks.antenna(E["antenna"][0], metals)
log("V0: tilt sweep")
cupL = {n: P[n]["H"] for n in ("CUPL-OUT", "CUPL-FRM", "PADRING-L")}
cupL["pad L"] = E["pad L"][0]
tilt = checks.tilt_sweep(cupL, P["YOKE-L"]["H"], +1)
log("V0: yaw sweep (cup + yoke turning under the slider collar)")
import yoke_headband as _yh0
yaw = checks.yaw_sweep({n: P[n]["H"] for n in ("YOKE-L", "CUPL-OUT", "CUPL-FRM")}, {"SLIDER-L": P["SLIDER-L"]["H"]}, _yh0.SOCKET_Y)
log("V0: mass, bed")
purchased = [("driver L", 12, "L"), ("driver R", 12, "R"), ("PCB assembly", 10, "L"), ("cell 603450", 20, "R"),
             ("ear pad L", 12.5, "L"), ("ear pad R", 12.5, "R"), ("steel band 175x12x1", 16.5, "B"),
             ("screws + inserts", 3, "L"), ("screws + inserts R", 2, "R"), ("harness", 5, "B"), ("cushion foam", 5, "B")]
mrows, mL, mR, mB = checks.masses(P, purchased)
bed = checks.bed_fit(P)

# ------------------------------------------------------------------ assembly-motion checks
log("assembly checks")
from build123d import Cylinder, Pos as _Pos, Align as _Al
from orga_common import along, to_head_left, A_OUT, A_CAV
import yoke_b as _yb, yoke_headband as _yh
_CA = (_Al.CENTER, _Al.CENTER, _Al.MIN)
EH = {n: s for n, (s, m, side) in E.items()}
envL = {n: s for n, (s, m, side) in E.items() if side == "L" and not n.startswith(("insert shell", "screw shell", "pad", "antenna"))}
AS = {}
# 1. close the left outer shell (keys and light guide pre-installed in it) down onto frame + PCB
movL = {n: P[n]["H"] for n in ("CUPL-OUT", "KEY-PWR", "KEY-MFB", "LGUIDE")}
fixL = dict(envL); fixL["CUPL-FRM"] = P["CUPL-FRM"]["H"]
AS["Close left shell onto frame + PCB (travel along the cup axis)"] = checks.sweep(movL, fixL, (0, 1, 0), [22, 16, 11, 7, 4, 2, 1, 0.3])
# 2. close the right outer shell onto frame + driver + cell
movR = {n: P[n]["H"] for n in ("CUPR-OUT",)}
fixR = {n: EH[n] for n in ("driver R", "cell")}; fixR["CUPR-FRM"] = P["CUPR-FRM"]["H"]
AS["Close right shell onto frame + driver + cell"] = checks.sweep(movR, fixR, (0, -1, 0), [22, 16, 11, 7, 4, 2, 1, 0.3])
# 3. yoke onto the closed cup: lowered over the crown from above (studs entered by spreading the ends; the
#    spread itself is a flex step, see the snap calculation in the report), checked along the last 30 mm
from build123d import Box as _Box
_zone = None
for _s in (-1, 1):
    _bx = _Pos(_s * (A_OUT + 2.5), 0, v("yk_pivot_z")) * _Box(6.6, 14.0, 13.0)
    _zone = _bx if _zone is None else _zone + _bx
_shell_wo_studs = P["CUPL-OUT"]["H"] - to_head_left(_zone)
AS["Yoke lowered onto the closed left cup: everything except the stud zones (the ends spread 4.4 mm over the studs, see snap calc)"] = checks.sweep({"YOKE-L": P["YOKE-L"]["H"]}, {"CUPL-OUT (studs excluded)": _shell_wo_studs, "CUPL-FRM": P["CUPL-FRM"]["H"]}, (0, 0, 1), [8, 5, 3, 1.5, 0.5, 0])
# 3b. slider collar over the yoke pin (Z_H travel down onto the crown)
AS["Slider collar down over the yoke's swivel pin"] = checks.sweep({"SLIDER-L": P["SLIDER-L"]["H"]}, {"YOKE-L": P["YOKE-L"]["H"], "CUPL-OUT": P["CUPL-OUT"]["H"]}, (0, 0, 1), [8, 5, 3, 1, 0.3, 0])
# 4. pad ring pushed into the frame skirt from the ear side (bumps snap into the groove)
AS["Pad ring into the skirt (snap: small overlap while the bumps pass is intended)"] = checks.sweep({"PADRING-L": P["PADRING-L"]["H"]}, {"CUPL-FRM": P["CUPL-FRM"]["H"]}, (0, -1, 0), [7, 5, 4.6, 4.2, 3, 2, 1, 0.3, 0])
# 5. slider along the band arc: insertion, nominal, full travel, and the pull-out stop
AS["Slider in BAND-TOP (+ = pulled out; detent and stop contact expected)"] = checks.arc_sweep({"SLIDER-L": P["SLIDER-L"]["H"]}, {"BAND-TOP": P["BAND-TOP"]["H"]}, _yh.CZ, [14, 10, 8.0, 7.0, 6.6, 6.3, 6.1, 5.1, 4.1, 3.0, 2.0, 1.0, 0, -1.0, -2.0, -4.1, -6.1])
# 6. tool access
bt_, sl_ = v("baffle_t"), v("skirt_len")
tools = {}
for i_, (x_, y_) in enumerate(cups.LAY["screws"]):
    tools[f"shell screw {i_+1}: Ø3 bit from the ear side"] = to_head_left(_Pos(x_, y_, -bt_ - 40) * Cylinder(1.5, 40 - 1.3, align=_CA))
obs_ear = {"CUPL-FRM": P["CUPL-FRM"]["H"], "driver L": EH["driver L"]}
TA = checks.tool_access(tools, obs_ear)
tools2 = {f"PCB screw {i_+1}: Ø3 bit from above": to_head_left(_Pos(x_, y_, BOARD_TOP + 1.3) * Cylinder(1.5, 30, align=_CA)) for i_, (x_, y_) in enumerate(v("pcb_holes"))}
TA += checks.tool_access(tools2, {n: s for n, s in envL.items() if n not in ("PCB",) and not n.startswith(("screw pcb", "insert pcb"))})
tools3 = {"collar set screw: Ø3 bit from the -X_H side": along((-40, _yh.SOCKET_Y, _yb.Y_GROOVE), (1, 0, 0), Cylinder(1.5, 40 - _yb.COL_D / 2 - 0.3, align=_CA))}
TA += checks.tool_access(tools3, {"SLIDER-L": P["SLIDER-L"]["H"], "YOKE-L": P["YOKE-L"]["H"], "CUPL-OUT": P["CUPL-OUT"]["H"]})
# snap-on flex estimate: each yoke end must spread by the stud length; half-yoke as a cantilever from the crown
_E = 2000.0; _t = v("yk_t"); _w = v("yk_w"); _I = _w * _t ** 3 / 12; _Lc = 60.0; _d = v("yk_gap_side") + v("yk_t") + 0.3
SNAP = dict(spread=_d, force=3 * _E * _I * _d / _Lc ** 3, stress=3 * _E * _I * _d / _Lc ** 3 * _Lc * (_t / 2) / _I)

# ------------------------------------------------------------------ renders
log("render: iso")
items_iso = [(d["H"], COL[n]) for n, d in P.items()]
items_iso += [(E[n][0], (0.15, 0.15, 0.15)) for n in ("pad L", "pad R")]
ax = render.shade(items_iso, azim=-130, elev=18)
ax.set_title(f"ORGA rev {REV} - assembly (fit-test build, assumed parts marked VERIFY)", fontsize=12)
ax.figure.savefig(REN / f"ORGA-M-ASM-{REV}_iso.png", dpi=150, bbox_inches="tight"); render.plt.close("all")

log("render: exploded")
zr = -v("baffle_t") - v("skirt_len")
ex = [("CUPL-FRM", 0), ("PADRING-L", -25), ("CUPL-OUT", 45), ("KEY-PWR", 45), ("KEY-MFB", 45),
      ("LGUIDE", 38), ("YOKE-L", 70)]
items_ex = [(Pos(0, 0, dz) * P[n]["local"] if not n.startswith("KEY") else Pos(0, 0, dz) * __import__("small_parts").key(n[4:]),
             COL[n]) for n, dz in ex]
items_ex += [(Pos(0, 0, 14) * dummies.left_electronics()[k][0], ENV_COL) for k in ("PCB", "U2 module", "J1 USB-C", "J4 jack", "SW3 encoder body", "SW3 wheel")]
items_ex += [(Pos(0, 0, 0) * dummies.driver(), (0.6, 0.5, 0.2)), (Pos(0, 0, -50) * dummies.pad(), (0.15, 0.15, 0.15))]
ax = render.shade(items_ex, azim=-35, elev=28)
ax.set_title(f"ORGA rev {REV} - left cup exploded (green = PCB and purchased parts, envelopes)", fontsize=12)
ax.figure.savefig(REN / f"ORGA-M-CUPL-{REV}_exploded.png", dpi=150, bbox_inches="tight"); render.plt.close("all")

log("render: section")
le = dummies.left_electronics()
fig, axs = render.plt.subplots(1, 2, figsize=(18, 10))
for axx, xs, title in ((axs[0], 0.0, "X_B = 0 (USB-C, driver, antenna)"), (axs[1], 19.0, "X_B = 19 (thumbwheel, LED guide)")):
    sec = [(P["CUPL-OUT"]["local"], (0.2, 0.22, 0.26), "outer shell"), (P["CUPL-FRM"]["local"], (0.5, 0.52, 0.58), "frame"),
           (P["PADRING-L"]["local"], (0.6, 0.6, 0.62), "pad ring"), (P["LGUIDE"]["local"], (0.5, 0.75, 1.0), "light guide"),
           (P["YOKE-L"]["local"], (0.85, 0.55, 0.2), "yoke"),
           (dummies.pad(), (0.8, 0.8, 0.8), "ear pad (envelope)"), (dummies.driver(), (0.75, 0.6, 0.25), "driver (envelope)")]
    sec += [(le[k][0], (0.25, 0.65, 0.3), None) for k in ("PCB", "U2 module", "J1 USB-C", "D7+D3 LEDs", "MK2", "SW3 encoder body", "SW3 wheel")]
    sec += [(le["antenna"][0], (0.95, 0.3, 0.6), "antenna")]
    render.section_yz(sec, x=xs, ax=axx)
    axx.set_title(f"Left cup section {title}"); axx.set_xlabel("Z_B depth [mm]  (ear <-   -> outer)"); axx.set_ylabel("Y_B (up) [mm]")
    axx.axvline(0, color="k", lw=0.5, ls=":")
axs[0].legend(loc="lower left", fontsize=8)
fig.tight_layout(); fig.savefig(REN / f"ORGA-M-CUPL-{REV}_section.png", dpi=140); render.plt.close("all")

# ------------------------------------------------------------------ PCB change package (DXF, board frame B)
log("PCB package")
import ezdxf  # noqa: E402
doc = ezdxf.new(setup=True); msp = doc.modelspace()
for ly, col in (("OUTLINE", 7), ("HOLES", 1), ("PORTS_AND_OPENINGS", 3), ("KEEPOUT_TOP", 6), ("KEEPOUT_BOT", 5),
                ("HEIGHT_LIMIT_TOP", 2), ("NOTES", 8)):
    doc.layers.add(ly, color=col)
sk = cups.board_sketch(with_holes=False)
for e in sk.edges():
    pts = [e @ (i / 40) for i in range(41)]
    msp.add_lwpolyline([(p.X, p.Y) for p in pts], dxfattribs={"layer": "OUTLINE"})
for (x, y) in v("pcb_holes"):
    msp.add_circle((x, y), v("m2_clear_d") / 2, dxfattribs={"layer": "HOLES"})
    msp.add_circle((x, y), v("pcb_keepout_d") / 2, dxfattribs={"layer": "KEEPOUT_TOP"})
    msp.add_circle((x, y), v("pcb_keepout_d") / 2, dxfattribs={"layer": "KEEPOUT_BOT"})
L = cups.LAY
rows = []
def port(name, x, y, dx, dy, z, note):
    msp.add_circle((x, y), 0.6, dxfattribs={"layer": "PORTS_AND_OPENINGS"})
    msp.add_line((x, y), (x + 6 * dx, y + 6 * dy), dxfattribs={"layer": "PORTS_AND_OPENINGS"})
    msp.add_text(name, height=1.2, dxfattribs={"layer": "PORTS_AND_OPENINGS"}).set_placement((x + 6 * dx + 0.5, y + 6 * dy))
    rows.append((name, x, y, math.degrees(math.atan2(dy, dx)), z, note))
U = L["usb"]; port("J1 USB-C mouth", 0.0, U["mouth_y"], 0, -1, U["axis_z"] - BOARD_TOP, f"board tab to Y = {-(B_CAV - 0.5):.1f}; mouth 0.3 inside the shell inner wall; plug axis {v('usb_plug_axis_above_board')} above board (VERIFY)")
J = L["jack"]; port("J4 jack mouth", J["mouth"][0], J["mouth"][1], J["d"][0], J["d"][1], J["axis_z"] - BOARD_TOP, f"jack face {v('jack_mouth_inset')} mm inside the wall, plug axis {v('jack_dir_deg') - 180:.0f} deg below horizontal toward the face")
for k, kk in L["keys"].items():
    a = v("key_act_from_wall"); (xw, yw), (nx, ny) = kk["wall"], kk["n"]
    port(f"SW {k} actuator face", xw - a * nx, yw - a * ny, nx, ny, kk["z"] - BOARD_TOP, "EVQ-P7A, actuator normal to rim")
W = L["wheel"]; port("SW3 dial centre (SIQ-02FVS3)", W["c"][0], W["c"][1], W["n"][0], W["n"][1], W["z0"] - BOARD_TOP, f"edge-drive dial Ø{v('wheel_d')} parallel to the board, top {v('wheel_z0_above_board') + v('wheel_t'):.1f} above it, edge {v('wheel_protrude')} mm past the shell; board tab {v('wheel_tab')[0]:.0f} wide to {v('wheel_tab')[1]:.1f} past the centre along the normal (dial thickness VERIFY)")
port("U2 module ANTENNA END (module rotated 90°)", v("module_flat_x"), v("module_cy"), 1, 0, 0, f"module {v('module_lwh')[1]} along X, {v('module_lwh')[0]} along Y; antenna end flush with the board flat at X = {v('module_flat_x')}; keep-out 15 mm")
lx, ly = L["led"]; port("D7 + D3 LEDs (side by side)", lx, ly, 0, 0, 0, "<= 1 mm apart under one 5.8 x 2.8 guide")
for nm, (x, y) in L["mics"].items():
    port(f"{nm} port (bottom-side mic)", x, y, 0, 0, 0, "port hole opens on TOP side; gasket ring Ø4.2 part-free on top")
    msp.add_circle((x, y), 2.8, dxfattribs={"layer": "KEEPOUT_TOP"})
    msp.add_circle((x, y), 0.4, dxfattribs={"layer": "HOLES"})
# rib / guide / key keep-outs (top side)
def rect(cx, cy, w, h, ang, layer):
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = [(cx + c * px - s * py, cy + s * px + c * py) for px, py in ((-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2))]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})
rect(0, U["mouth_y"] + U["len"] + 0.9, 9.6, 2.2, 0, "KEEPOUT_TOP")
d = J["d"]; back = v("jack_len") + 0.9; rect(J["mouth"][0] - back * d[0], J["mouth"][1] - back * d[1], 2.2, 9.6, math.degrees(math.atan2(d[1], d[0])), "KEEPOUT_TOP")
rect(lx, ly, 6.6, 9.4, 0, "KEEPOUT_TOP")
for k, kk in L["keys"].items():
    (xw, yw), (nx, ny) = kk["wall"], kk["n"]
    rect(xw - 1.2 * nx, yw - 1.2 * ny, 2.6, 9.0, math.degrees(math.atan2(ny, nx)), "KEEPOUT_TOP")
# height-limit bands (top side): max part height above board = shell inner face - 0.5 - board top
for x0, x1 in ((-40, -20), (-20, 0), (0, 20), (20, 40)):
    hmax = depth_at(x0) - WALL - v("clr_part_fdm") - BOARD_TOP
    rect((x0 + x1) / 2, 0, x1 - x0, 110, 0, "HEIGHT_LIMIT_TOP")
    msp.add_text(f"<= {hmax:.1f}", height=2, dxfattribs={"layer": "HEIGHT_LIMIT_TOP"}).set_placement(((x0 + x1) / 2 - 4, -54))
doc.saveas(OUT / f"ORGA-PCB-outline-{REV}.dxf")

# ------------------------------------------------------------------ report
log("report")
R = []
R.append(f"# ORGA rev {REV} — V0 check report\n")
R.append("Generated by `src/build_all.py`. Geometry checked with OpenCascade in the build workspace.\n")
R.append("## Interference (all printed parts + purchased envelopes, assembly pose)\n")
if hits:
    R.append("| Part A | Part B | Overlap [mm³] |\n|---|---|---|")
    R += [f"| {a} | {b} | {vol:.2f} |" for a, b, vol in hits]
else:
    R.append("**Zero unintended overlaps.** (Press-fit inserts and the antenna region inside the module are excluded on purpose.)")
R.append("\n## Clearance: left outer shell to each envelope [mm]\n")
R.append("| Envelope | Distance | Rule (≥ 0.5 FDM) |\n|---|---|---|")
for n, dd in clr_shell:
    rule = "OK" if dd >= 0.5 else ("intended back-stop (0.1)" if n in ("J1 USB-C", "J4 jack") else
                                   ("OK (PCB pocket rule ≥ 0.3)" if n == "PCB" and dd >= 0.29 else
                                    ("OK (wheel slot gap ≥ 0.25)" if n == "SW3 wheel" and dd >= 0.25 else "CHECK")))
    R.append(f"| {n} | {dd:.2f} | {rule} |")
R.append(f"\nCell swell envelope to right outer shell: **{clr_cell[0][1]:.2f} mm** · driver to PCB: **{drv_pcb:.2f} mm** (vent gap ≥ 1.0)\n")
R.append("## Antenna keep-out (≥ 15 mm to metal)\n")
R.append("| Metal item | Distance [mm] | Result |\n|---|---|---|")
R += [f"| {n} | {dd:.1f} | {'OK' if dd >= 15 else 'FAIL'} |" for n, dd in ant[:8]]
R.append(f"\n## Cup tilt vs yoke (rotation about the stud axis)\n\nDoc 06 asks ±10° free. Contact past ±{v('yk_tilt_stop'):.0f}° is the intended hard stop (stud lug in the yoke-end arc slot).\n")
R.append("| Tilt [deg] | Worst overlap [mm³] |\n|---|---|")
R += [f"| {a:+.1f} | {w:.2f} |" for a, w in tilt]
R.append("\n## Swivel (yaw) vs slider collar and S-arm\n")
R.append("| Yaw [deg] | Worst overlap [mm³] | Between |\n|---|---|---|")
R += [f"| {a:+.1f} | {w:.2f} | {' / '.join(p) if p else '—'} |" for a, w, p in yaw]
R.append(f"\n## Yoke snap-on (hand calculation, PETG E ≈ 2 GPa)\n\nEach end spreads **{SNAP['spread']:.1f} mm** to pass its stud: ≈ **{SNAP['force']:.1f} N** per end, peak bending stress ≈ **{SNAP['stress']:.0f} MPa** (PETG yield ≈ 50 MPa). VERIFY on the first print.\n")
R.append("\n## Assembly-motion checks (rev B)\n")
R.append("Each part is moved along its real assembly path; the table gives the worst overlap with anything it meets (0 = free path).\n")
for title, rows_ in AS.items():
    R.append(f"**{title}**\n\n| Distance to go / offset | Worst overlap [mm³] | Between |\n|---|---|---|")
    R += [f"| {d:g} | {w:.2f} | {' / '.join(p) if p else '—'} |" for d, w, p in rows_]
    R.append("")
R.append("**Tool access**\n\n| Tool path | Overlap [mm³] | Min clearance [mm] |\n|---|---|---|")
R += [f"| {n} | {w:.2f} | {dmin:.2f} |" for n, w, p, dmin in TA]
R.append("\n## Mass (PETG 1.27 g/cm³ × 0.9 fill; bought parts assumed)\n")
R.append("| Item | g |\n|---|---|")
R += [f"| {n} | {g} |" for n, g in mrows]
R.append(f"\n**Left cup {mL:.0f} g · right cup {mR:.0f} g · headband {mB:.0f} g · total {mL + mR + mB:.0f} g** "
         f"(MR-001 ≤ 300: {'OK' if mL + mR + mB <= 300 else 'FAIL'}; MR-002 L/R Δ {abs(mL - mR):.0f} g ≤ 40: {'OK' if abs(mL - mR) <= 40 else 'FAIL'})\n")
R.append("## Print bed fit (256 × 256 × 256)\n")
R.append("| Part | Print bbox [mm] | Fits |\n|---|---|---|")
R += [f"| {n} | {a:.0f} × {b:.0f} × {c:.0f} | {'yes' if ok else 'NO'} |" for n, (a, b, c), ok in bed]
R.append("\n## Edge-part alignment\n")
R.append("Shell openings are generated from the same layout table as the PCB change list, so offsets are 0.0 mm by construction. "
         "The real check runs when the updated KiCad board STEP comes back (file 09 round-trip).\n")
(OUT / f"V0_report_{REV}.md").write_text("\n".join(R), encoding="utf-8")
pcb = ["# PCB changes for ORGA rev B (board frame B: origin = driver axis, X rear, Y up)\n",
       "Rev B vs A.5: only the outline changes. The rev A.3 arm-tunnel strip along the front-upper wall is board area again (no tunnel, no pivot nut). Every edge part, hole, keep-out and the antenna flat is unchanged.\n",
       "KiCad mapping: X_kicad = X_B + 100, Y_kicad = -Y_B + 100. Outline, holes and keep-outs are in `ORGA-PCB-outline-B.dxf`.\n",
       "Direction = in-plane angle of the opening/actuator normal, degrees from +X_B (rear) counter-clockwise; 180 = toward the face.\n",
       "| Item | X_B | Y_B | Direction [deg] | Height above board top | Note |", "|---|---|---|---|---|---|"]
pcb += [f"| {n} | {x:.2f} | {y:.2f} | {a:.0f} | {z:.2f} | {note} |" for n, x, y, a, z, note in rows]
pcb += [f"| M2 board hole {i+1} | {x:.2f} | {y:.2f} | — | — | Ø2.4, Ø7 part-free both sides |" for i, (x, y) in enumerate(v("pcb_holes"))]
pcb += [f"| Shell-screw notch {i+1} | {x:.2f} | {y:.2f} | — | — | notch R3.7 in the outline |" for i, (x, y) in enumerate(cups.LAY["screws"])]
(OUT / f"PCB_changes_{REV}.md").write_text("\n".join(pcb) + "\n", encoding="utf-8")
# ------------------------------------------------------------------ parts list
BL = [f"# ORGA rev {REV} — parts list\n", "## Printed (files in out/print, already oriented for the bed)\n",
      "| Part | Qty | Material | Print note |", "|---|---|---|---|"]
BL += [f"| ORGA-M-{n}-{REV} | {d['qty']} | {d['mat']} | {d['note']} |" for n, d in P.items()]
BL += ["\n## Hardware and bought parts\n", "| Item | Qty | Spec | Status |", "|---|---|---|---|",
       "| M2 heat-set insert | 11 | brass, OD ≈3.6, L 4 (hole Ø3.2 × 4): 4 per shell + 3 in the left frame | standard |",
       "| M2 × 5 screw | 8 | pan/button head, shell to frame (from the ear side, under the pad) | standard |",
       "| M2 × 4 screw | 3 | PCB to standoffs | standard |",
       "| M2 × 4 self-tapping | 2 | collar set screw: rides in the arc groove of the yoke's swivel pin (retention + ±15° yaw stop) | standard |",

       "| Ø2 × 14 pin | 1 | dowel or M2 × 14 screw, closes the steel-band slot | standard |",
       "| Harness grommet | 2 | silicone grommet or heat-shrink stop for the Ø3.4 hole in the outer face (Ø6 counterbore) | buy |",
       "| Driver gasket | 2 | closed-cell foam ring, Ø44 / Ø37 × 1 mm | buy |",
       "| Spring-steel band | 1 | 171 × 12 × 1 mm (65Mn), slides into BAND-TOP from the +Y end | VERIFY M6 |",
       "| Headband cushion foam | 1 | ≈24 × 100 × 8 mm, glued to the BAND-TOP inner ribs | buy |",
       "| Mic gasket | 2 | PORON ring OD 4.0 / ID 1.4 / 1.8 thick | buy / die-cut |",
       "| Acoustic mesh | 2 | Ø4 disc, glued into the 0.3 mm recess at each mic port | buy |",
       "| Cell foam pad | 1 | 2 mm soft foam on the right-shell inner face over the cell | buy |",
       "| Harness | 1 | 5-core 28-30 AWG silicone (HPR+, HPR-, BAT+, BAT-, NTC), ≈ 650 mm | buy |",
       "| Thumbwheel encoder | 1 | SIQ-02FVS3 edge-drive dial encoder, Ø14.5 dial built in, 15 detents, push switch | from routing chat rev A.5 |",
       "| Driver | 2 | 40 mm, 32 Ω (M5) | TBD — dimensions assumed |",
       "| Ear pad | 2 | oval, opening ≥ 65 × 45 (M7) | TBD — PADRING adapts it |",
       "| Li-Po 603450 | 1 | 1S ≈1000 mAh, PCM + 10 k NTC | TBD — measure |",
       "| Boom mic | 1 | 3.5 mm, overmold ≤ Ø8.0 | TBD — measure |"]
(OUT / f"ORGA-M-parts-list-{REV}.md").write_text("\n".join(BL) + "\n", encoding="utf-8")
json.dump({"hits": hits, "clr_shell": clr_shell, "ant": ant[:8], "tilt": tilt, "yaw": [(a, w) for a, w, p in yaw], "snap": SNAP, "mass": [mL, mR, mB],
           "bed": [(n, list(d), ok) for n, d, ok in bed], "cell_clr": clr_cell[0][1], "drv_pcb": drv_pcb},
          open(OUT / f"V0_{REV}.json", "w"), indent=1, default=float)
log("done")
