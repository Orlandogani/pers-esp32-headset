"""ORGA mechanical parameters - single source of truth for every dimension.

Rules (file 09):
  * every value carries a source tag: "datasheet <file>", "measured <date>", "decision <id>", "doc <file>" or "assumed-VERIFY"
  * nothing tagged assumed-VERIFY may be frozen for a print beyond a fit test
  * build123d part scripts in mech/src import P from here; FreeCAD gets the same values via
    `python orga_params.py --csv` -> out/orga_params.csv (FreeCAD Spreadsheet, alias = name)
Units: mm, degrees, grams.  Frames: head frame H (X fwd, Y left, Z up), board frame B (file 03).
"""
from collections import OrderedDict

P = OrderedDict()
def p(name, value, src, note=""):
    P[name] = dict(value=value, src=src, note=note)

# ---------------------------------------------------------------- decisions (2026-10-09)
p("M1", "A", "decision M1", "PCB component side faces the OUTER shell")
p("concept", "C2", "decision", "cell in the right cup, 5-wire harness")
p("yoke", "HS35-style horseshoe yoke", "decision revB (2026-10-13)", "external horseshoe yoke around the upper half of the cup, plastic snap studs front + rear at y=0, swivel collar at the crown, S-arm on the slider; replaces the rev A.3 tunnel arm")

# ---------------------------------------------------------------- print process (file 05)
p("wall_fdm", 2.0, "doc 05")
p("wall_sla_mjf", 1.6, "doc 05")
p("clr_part_fdm", 0.5, "doc 05", "shell over tallest component")
p("clr_pcb_pocket_fdm", 0.3, "doc 05", "per side")
p("clr_slide_fdm", 0.3, "doc 05", "per side")
p("fillet_in", 0.5, "doc 05")
p("fillet_cosmetic_small", 1.0, "doc 05")
p("fillet_cosmetic_shell", 2.0, "decision revA", "R3 -> R2 so the jack overmold hole clears the edge round")

# ---------------------------------------------------------------- fasteners
p("m2_insert_hole_d", 3.2, "assumed-VERIFY", "use insert vendor's value")
p("m2_insert_hole_depth", 4.0, "assumed-VERIFY")
p("m2_boss_od", 6.4, "doc 05", ">= 2x insert OD")
p("m2_clear_d", 2.4, "doc 03", "FDM board hole / screw clearance")
p("pcb_keepout_d", 7.0, "doc 03", "part-free ring around each mounting hole")

# ---------------------------------------------------------------- ear pad (M7 open)
p("pad_open_h", 75.0, "assumed-VERIFY", "doc 06 target; XM5 model measures 66")
p("pad_open_w", 48.0, "assumed-VERIFY", "doc 06 target; XM5 model measures 44.6")
p("pad_ring_w", 15.0, "assumed-VERIFY")
p("pad_t", 22.0, "assumed-VERIFY", "uncompressed")
p("pad_tc", 12.0, "assumed-VERIFY", "compressed on head")

# ---------------------------------------------------------------- cup (concept C2)
p("cup_n", 2.6, "decision concept", "superellipse exponent of the cup plan shape")
p("cup_tilt_deg", 0.0, "assumed", "XM5-style front tilt, 0 for rev A")
p("baffle_t", 1.6, "doc 02 (1.5-2.0); 1.6 to save mass")
p("front_recess", 16.0, "assumed-VERIFY", "baffle recess behind pad face, I-13")
p("rear_cavity_L", 18.3, "concept report (M1-A, C2)", "baffle rear face -> shell outer; +4 with EC10E wheel")
p("rear_cavity_R", 17.0, "assumed-VERIFY", "driver 8 + cell 6.6 + clearances")
p("antenna_keepout", 15.0, "doc 05 / MR-018, VERIFY Espressif")
p("antenna_below_wall", 6.0, "assumed", "board flat edge below cavity top wall")

# ---------------------------------------------------------------- driver (M5 open)
p("drv_od", 40.0, "assumed-VERIFY", "M5")
p("drv_flange_t", 1.5, "assumed-VERIFY")
p("drv_body_h", 8.0, "assumed-VERIFY", "rear projection behind baffle")
p("drv_mag_d", 20.0, "assumed-VERIFY")
p("drv_rim_h", 3.0, "assumed-VERIFY")
p("drv_vent_gap", 1.0, "assumed")

# ---------------------------------------------------------------- PCB / on-board parts
p("pcb_t", 1.6, "fab standard")
p("pcb_inset", 2.0, "decision I-12", "board outline = cavity - inset")
p("module_lwh", (18.0, 25.5, 3.1), "datasheet ESP32-S3-WROOM-1")
p("antenna_len", 7.0, "assumed-VERIFY", "module antenna end")
p("usb_lwh", (8.94, 7.35, 3.31), "datasheet USB4105-GF-A")
p("usb_mouth", (8.34, 2.56), "datasheet USB4105-GF-A")
p("jack_h", 5.0, "assumed-VERIFY", "SJ2-3593D")
p("jack_overmold_d", 8.0, "assumed-VERIFY", "boom plug, measure")
p("sidekey_travel", 0.2, "assumed-VERIFY", "EVQ-P7A")
p("sidekey_force_N", 1.6, "assumed-VERIFY")
p("led_rgb_lwh", (3.2, 2.8, 1.9), "datasheet Wurth 150141M173100 (H VERIFY)")
p("mic_lwh", (4.0, 3.0, 1.2), "datasheet IM73D122V01")
p("mic_port_pcb_d", 0.8, "datasheet IM73D122V01")
p("mic_port_shell_d", 1.2, "doc 05", "drill to size after FDM")
p("mic_gasket_t", 1.8, "doc 05", "PORON 1.5-2, 25-35 % compression")
p("wheel", "SIQ-02FVS3 (edge-drive dial encoder, push)", "routing chat revA.5", "replaces EVQ-WK; dial built into the encoder, sits on the PCB; 15 detents")
p("wheel_mount_h", 1.5, "assumed-VERIFY", "SIQ-02FVS3 body height under the dial (dial top 4.0 - dial t)")

# ---------------------------------------------------------------- battery (right cup, C2)
p("cell_tlw", (6.0, 34.0, 50.0), "assumed-VERIFY", "603450 class, measure the bought cell")
p("cell_swell", 0.10, "MR-019")
p("cell_clear_side", 0.5, "MR-019")
p("cell_mass", 20.0, "assumed-VERIFY")

# ---------------------------------------------------------------- headband / yoke
p("band_adjust_per_side", 25.0, "doc 06")
p("band_detent_pitch", 5.0, "doc 06")
p("clamp_N", (2.5, 4.5), "MR-005", "at 150 mm cup spacing")
p("steel_band_wt", (1.0, 12.0), "assumed-VERIFY", "spring steel t x w, M6")
p("steel_to_antenna_min", 15.0, "MR-018", "concept gives >= 22")
p("cup_swivel_yaw", 15.0, "doc 06", "+/- deg")
p("cup_swivel_tilt", 10.0, "doc 06", "+/- deg")
p("harness_wires", 5, "decision C2", "HPR_P, HPR_N, BAT+, BAT-, NTC")


# ---------------------------------------------------------------- rev A layout (proposal, board frame B; origin = driver axis)
# Left-cup local frame == board frame B: X rear, Y up, Z outward from the baffle rear face (M1-A).
p("shell_d0", 20.9, "decision revA", "outer-face depth at x=0 (shallow wedge); set by jack hole (front) and wheel slot (rear)")
p("shell_slope", 0.75 / 35.0, "decision revA", "depth grows 0.75 mm per 35 mm toward the rear")
p("board_bot_z", 9.2, "concept report", "drv_body_h + vent_gap + bottom pads")
p("module_flat_x", 33.0, "decision revA.3", "module rotated 90 deg, antenna end flush with a board flat at the REAR edge")
p("module_cy", 14.0, "decision revA.3", "module centre Y")
p("usb_tab_halfw", 5.5, "decision revA", "board tab under USB-C")
p("usb_pocket", (12.6, 7.0, 1.0), "assumed-VERIFY", "outside overmold pocket w x h x depth")
p("usb_opening", (9.2, 3.6), "assumed-VERIFY", "plug opening in thinned wall")
p("usb_plug_axis_above_board", 1.6, "assumed-VERIFY", "doc 03")
p("jack_s", 30.0, "decision revA.2", "rim arc position [mm from front pivot, via bottom]")
p("jack_dir_deg", 200.0, "decision revA", "plug axis, 180 = straight front, 200 = front and 20 deg down")
p("jack_len", 20.1, "doc envelope csv")
p("jack_axis_above_board", 2.5, "assumed-VERIFY")
p("jack_hole_d", 8.6, "assumed-VERIFY", "= boom overmold 8.0 + 0.6, through the wall so the plug seats fully")
p("jack_mouth_inset", 1.0, "decision revA", "jack face inside the inner wall (curved-wall clearance)")
p("key_mfb_s", 118.0, "decision revA.2", "rear-lower rim")
p("key_pwr_s", 54.0, "decision revA.2", "front-bottom rim, away from MFB")
p("key_axis_above_board", 0.7, "assumed-VERIFY", "EVQ-P7A actuator centre")
p("key_act_from_wall", 2.4, "doc 03", "actuator face 0.4 inside board edge")
p("key_pretravel", 0.1, "doc 05")
p("key_overtravel", 0.05, "doc 05")
p("wheel_s", 92.0, "decision revA.2", "rear-bottom rim, on the flat part")
p("wheel_d", 14.4, "routing chat revA.5 (datasheet 14.5 +/-0.1)", "SIQ-02FVS3 dial")
p("wheel_t", 2.5, "assumed-VERIFY", "SIQ-02FVS3 dial thickness, not given in the datasheet")
p("wheel_protrude", 1.5, "doc 05 (1.5-2.5)")
p("wheel_z0_above_board", 1.5, "routing chat revA.5 (dial top 4.0 above board) - wheel_t", "dial underside above board")
p("enc_body_lw", (11.1, 10.0), "datasheet SIQ-02FVS3 mount area (approx.), VERIFY", "body footprint behind the dial centre (along normal x tangent)")
p("wheel_tab", (8.0, 4.0), "routing chat revA.5", "PCB tab under the dial: width, reach from the dial centre along the wheel normal")
p("wheel_push", True, "datasheet SIQ-02FVS3", "push switch built in; slide force 3-6 N")
p("led_xy", (5.0, -28.0), "decision revA.3", "RGB + charge LED side by side; moved off the new module position")
p("lguide_wh", (5.8, 2.8), "decision revA", "clear light guide section")
p("mk1_xy", (-17.0, -35.0), "decision revA.2", "voice mic, bottom side, front-lower; clear of the lower-front shell screw and the jack")
p("mk2_xy", (10.0, 36.0), "decision revA.3", "reference mic, bottom side, top; >= 15 mm from the antenna (now at the rear)")
p("mic_boss_od", 5.0, "decision revA")
p("mic_channel_d", 2.0, "assumed-VERIFY", "wider channel, 1.2 at the skin")
p("pivot_z", 8.0, "decision revA", "fork pivot height in cup frame")
p("pivot_pin_d", 5.0, "decision revA")
p("pivot_hole_d", 5.2, "doc 05 slide fit")
p("pivot_boss", (10.0, 2.0), "decision revA", "outward boss d x height")
p("harness_bore_d", 3.0, "assumed-VERIFY", "5 x 28 AWG bundle")
p("shell_screw_t_deg", (60.0, 97.0), "decision revA.3", "superellipse angle of the 2 upper shell screws (clear of antenna and arm tunnel)")
p("shell_screw_s_low", (44.0, 105.0), "decision revA.2", "rim arc position of the 2 lower shell screws (gaps between edge parts)")
p("shell_screw_inset", 2.2, "decision revA", "boss centre inside the inner wall; screw head clears the skirt")
p("pcb_holes", ((0.0, -37.0), (22.0, -12.0), (-20.0, 18.0)), "routing chat revA.5 (H1), revA.3", "MR-011: H1 within 10 mm of the USB-C rear; 2 >= 15 mm from antenna; 3 clear of the arm tunnel")
p("pcb_notch_r", 3.7, "decision revA", "board notch around shell screw bosses")
p("skirt_len", 16.0, "= front_recess")
p("padring_t", 2.0, "decision revA")
p("padring_lip", 1.0, "assumed-VERIFY", "pad sleeve hooks over this")
p("lip_h", 2.0, "decision revA", "frame locating lip inside shell")
p("drv_hole_d", 36.0, "assumed-VERIFY", "front opening for the diaphragm")
p("drv_seat_ring", (44.0, 1.5), "decision revA", "locating ring on baffle rear face")
p("cell_center_x_rear", 4.0, "decision revA", "cell shifted toward deep (rear) side")
p("tray_z", 8.5, "concept report", "tray floor bottom, 0.5 over magnet")
p("tray_floor_t", 1.2, "decision revA")
p("tray_rail", (1.5, 4.0), "decision revA", "rail t x h")
p("pad_face_y_h", 75.0, "doc 06/MR-005", "pad faces at 150 mm spacing in the assembly pose")
p("fork_arm", (6.0, 7.0), "decision revA", "arm width (plan) x thickness (Z)")
p("fork_clear", 0.3, "doc 05")
p("fork_bar_y", 58.0, "decision revA.1", "oval fork: inner edge at the crown, cup frame (sides follow the pivot bosses)")
p("fork_pin_y", (72.0, 80.0), "decision revA", "swivel pin span in cup frame Y (= Z_H)")
p("swivel_pin_d", 6.0, "decision revA")
p("band_center_z", 14.5, "derived revA", "band arc centre Z_H (rail through Y_H 125.5, Z_H 82; apex 157)")
p("band_r", 142.5, "derived revA", "band arc radius: 95th-pct vertex 145 + cushion 8 + half section")
p("band_half_deg", 40.0, "decision revA")
p("band_section", (26.0, 9.0), "decision revA", "width (X_H) x radial")
p("rail_section", (10.0, 4.0), "decision revA", "slider rail width x radial")
p("steel_slot", (12.6, 1.4), "decision revA")
p("slider_top_deg", 30.0, "decision revA")
p("density_petg", 1.27, "datasheet typical")
p("fill_factor", 0.9, "assumed", "thin-wall FDM parts print mostly solid")

# ---------------------------------------------------------------- Sony-style arm (rev A.3)
p("arm_t_e", 120.0, "decision revA.3", "superellipse angle where the arm leaves the cup (top-front rim)")
p("arm_inset0", 0.8, "decision revA.3", "arm outer edge to cavity wall")
p("arm_w", 6.0, "decision revA.3", "arm width in the cup plane (inside the tunnel)")
p("arm_t", 5.0, "decision revA.3", "arm thickness along Z (inside the tunnel)")
p("arm_clr", 0.6, "doc 05 (moving part, FDM)")
p("tunnel_wall", 1.6, "decision revA.3")
p("arm_pivot_z", 9.25, "decision revA.3", "tilt axis height; centred so the tilted arm stays 0.3 under the shell plate and 1 mm over the baffle")
p("arm_tilt_deg", 7.0, "decision revA.3", "+/- tilt; doc 06 asks 10, pad compliance covers the rest (VERIFY on head)")
p("arm_lug_r", 4.0, "decision revA.3")
p("arm_lug_hole_d", 4.3, "decision revA.3", "runs on the M3 shoulder screw's 4 mm shoulder")
p("arm_wall_hole_d", 4.2, "decision revA.3")
p("arm_screw_head", (7.5, 1.2), "assumed-VERIFY", "counterbore d x depth for the shoulder-screw head")
p("arm_insert_boss", (9.0, 3.2), "decision revA.4", "nut-trap boss d x length: nut sits 0.7 behind the boss face so the 4 mm thread of an ISO 7379 4x8 shoulder screw fully engages")
p("m3_insert_hole_d", 4.0, "assumed-VERIFY", "M3 heat-set insert hole")
p("m3_insert_depth", 5.0, "assumed-VERIFY")
p("arm_ext", (7.0, 6.5), "decision revA.3", "external arm width x thickness")
# ---------------------------------------------------------------- assembly features (rev A.4)
p("padring_spigot_len", 6.0, "decision revA.4", "spigot depth into the frame skirt")
p("padring_snap", (0.53, 6.0, 4.5), "decision revA.4", "bump protrusion, bump length along rim, bump centre above skirt end")
p("padring_snap_t_deg", (30.0, 90.0, 150.0, 210.0, 270.0, 330.0), "decision revA.4", "6 snap tabs around the ring")
p("skirt_groove_depth", 0.65, "decision revA.4", "> bump protrusion, leaves 1.35 mm skirt wall")
p("m3_nut", (5.6, 2.5), "datasheet ISO 4032 M3 (5.5 AF x 2.4) + 0.1 FDM", "nut trap AF x thickness")
p("m3_clear_d", 3.4, "doc 05 FDM")
p("harness_groove", (2.4, 1.6), "decision revA.4", "width x depth for the 5-core harness (≈ 2 mm OD, VERIFY)")
p("wheel_plug_gap", 0.55, "decision revA.4", "frame plug top to wheel underside")
p("steel_pin_d", 2.0, "decision revA.4", "cross pin retaining the steel band (M2 screw or 2 mm dowel)")
p("steel_pin_deg", 39.0, "decision revA.4", "pin position on the +Y end of BAND-TOP")
p("yaw_limit_deg", 15.0, "doc 06", "+/- swivel; the slider set screw rides in an arc groove on the pin that stops it")
p("pivot_screw", "ISO 7379 shoulder screw, d 4 x 8, M3 thread", "assumed-VERIFY", "thread length 4 mm assumed")
p("steel_band_len", 171.0, "derived revA.4", "65Mn 12 x 1 mm, arc -30..37.5 deg at r = R + 3.35")

# ---------------------------------------------------------------- HS35-style yoke (rev B, 2026-10-13; own geometry)
p("yk_t", 3.5, "decision revB", "yoke band radial thickness")
p("yk_w", 10.0, "decision revB", "yoke band width along Z (cup axis)")
p("yk_gap_side", 0.6, "doc 05 (moving part, FDM)", "radial gap to the shell at the pivots")
p("yk_gap_top", 2.6, "decision revB (tilt sweep)", "radial gap at the crown: the crown region swings ~1.7 mm outward at 10 deg tilt")
p("yk_pivot_z", 9.25, "decision revB", "tilt axis height on the shell side wall (same as rev A.3)")
p("yk_tilt_free", 10.0, "doc 06", "+/- tilt without contact")
p("yk_tilt_stop", 12.0, "decision revB", "+/- hard stop: wedge lug on the stud in an arc slot in the yoke end (off the head the cup would otherwise flop, its CoM is ~9 mm ear-side of the axis)")
p("yk_lug", (10.0, 1.2, 0.3), "decision revB", "stop lug half-angle [deg], radial height, radial clearance in the slot")
p("yk_stud_d", 6.0, "decision revB", "plastic pivot stud moulded on the shell side wall (no metal near the antenna)")
p("yk_hole_d", 6.4, "doc 05 slide fit (+0.4 FDM)", "yoke end hole")
p("yk_end_d", 12.0, "decision revB", "round boss at each yoke end")
p("yk_stud_chamfer", 1.0, "decision revB", "lead-in on the stud tip for the snap-on")
p("yk_inner_boss", (10.0, 1.2), "decision revB", "boss inside the wall behind each stud: d x height (0.8 mm to the board edge)")
p("yk_pocket", (6.5, 1.5, 8.0), "decision revB", "cosmetic panel recess on the yoke sides: width x depth, starts this far above the pivot")
p("swivel_collar", (12.0, 7.0), "decision revB", "slider collar at the yoke crown: d x length (the visible swivel ring)")
p("swivel_axial_gap", 0.5, "doc 05", "collar to yoke crown boss")
p("sarm_section", (12.0, 4.0), "decision revB", "S-arm (slider lower end) width X_H x thickness")
p("sarm_start_deg", 56.0, "decision revB", "band-arc angle where the rail turns into the S-arm (outside the BAND-TOP sleeve over the full +/-15 mm travel)")
p("sarm_mid", (127.2, 79.0), "decision revB", "S-arm waypoint Y_H, Z_H: bows outward, then drops vertically into the collar")
p("harness_entry", (-12.0, 44.0, 3.4, 6.0), "decision revB", "harness hole in the outer face, cup frame x, y, hole d, grommet counterbore d (outside of the yoke: never pinched in tilt)")
p("cap_disc", (56.0, 5.0, 1.6, 0.8), "decision revB", "cap disc on the outer face: d, centre y, ring-groove width, groove depth")


def v(name):
    return P[name]["value"]


def unverified():
    return [k for k, d in P.items() if "VERIFY" in d["src"]]


if __name__ == "__main__":
    import sys, csv, pathlib
    if "--csv" in sys.argv:
        out = pathlib.Path(__file__).resolve().parents[1] / "out" / "orga_params.csv"
        out.parent.mkdir(exist_ok=True)
        with open(out, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["name", "value", "src", "note"])
            for k, d in P.items():
                val = d["value"]
                if isinstance(val, tuple):
                    for i, x in enumerate(val):
                        w.writerow([f"{k}_{i}", x, d["src"], d["note"]])
                else:
                    w.writerow([k, val, d["src"], d["note"]])
        print("wrote", out)
    else:
        print(f"{len(P)} parameters, {len(unverified())} still assumed-VERIFY:")
        for k in unverified():
            print("  ", k, P[k]["value"])
