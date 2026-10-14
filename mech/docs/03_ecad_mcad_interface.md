# 03 — ECAD ↔ MCAD Interface Control (main PCB, left cup)

> Baseline = the reference placement in `orga-v1` (generated, unrouted). The user's working board `headset-orga` has the same circuit, re-numbered references and some 0603 passives; its parts are not placed yet. **All positions below are a starting proposal.** Mechanics may move any edge part; electronics then re-places the inside of the board to suit.

## 1. Coordinate frames

**Board frame B** (all PCB numbers in this package use it):
- Origin: centre of the outline circle.
- +X_B: right, viewed from the TOP (component) side.
- +Y_B: toward the flat edge (antenna edge).
- +Z_B: out of the top copper.
- Z_B = 0 is the PCB bottom surface; the PCB top surface is Z_B = +1.6 mm.
- KiCad mapping: X_B = X_kicad − 100.0, Y_B = −(Y_kicad − 100.0), in mm (orga-v1 board).

**Head frame H** (whole-product assembly):
- Origin: midpoint between the two ear-canal entrances (interaural axis centre).
- +X_H forward (nose), +Y_H toward the left ear, +Z_H up. Right-handed.
- This matches the usual HRTF/head-tracking convention, so the IMU (U9 / orga-v1 U8) axes map directly to it.

**B → H mapping (left cup)** depends on decision **M1** (file 08):

| M1 option | +Z_B (board top normal) | +Y_B | +X_B | Rotation H←B |
|---|---|---|---|---|
| **A, top faces OUTWARD (recommended)** | +Y_H (out of the left side of the head) | +Z_H (up) | −X_H (rear) | X_H = −X_B, Y_H = Z_B, Z_H = Y_B |
| B, top faces INWARD (toward driver) | −Y_H | +Z_H | +X_H (front) | X_H = X_B, Y_H = −Z_B, Z_H = Y_B |

Under option A, the board's −X edge faces the **front (face/mouth)** and +X faces the **rear**.

## 2. Board

| Item | Value |
|---|---|
| Outline (baseline) | Circle R 31.0 mm centred at the origin, cut by a straight chord at Y_B = +26.0 (flat top for the antenna). Envelope 62.0 × 57.0 mm. |
| Thickness | 1.6 mm, 4-layer FR-4 (JLCPCB standard) |
| Mounting (baseline) | H1 (−21.5, +15.5) and H2 (+14.0, −3.0), M2, Ø2.2 NPTH. Keep **Ø7 mm part-free** on both sides (boss/insert OD 6.4–7.2). For FDM-printed bosses, use Ø2.4–2.5 holes to absorb position error. **Add a third hole within 10 mm of USB-C** (MR-011). H1 is ≈ 13 mm from the antenna region: move it if the shell boss/screw is metal. |
| Fabrication | Outline tolerance ±0.2 mm, hole position ±0.1 mm (typical prototype fab) |
| Panel/edge | No castellations; no parts within 0.3 mm of the edge except edge connectors |

## 3. Edge parts and enclosure interfaces (baseline, board frame B)

| Ref headset-orga (orga-v1) | Function | Position X, Y [mm] | Faces / actuates | Height above PCB top [mm] | Notes |
|---|---|---|---|---|---|
| J1 (J1) | USB-C receptacle, USB4105-GF-A | body centre (0, −27.9); mouth at Y ≈ −31.6 | −Y_B (bottom of cup) | 3.31 | Body 8.94 × 7.35 mm. The mouth protrudes ≈ 0.6 mm past the round edge at X = 0 and ≈ 0.9 mm at the body corners → give the outline a local flat at the USB. Plug-opening centreline ≈ PCB top + 1.6 mm (VERIFY drawing). |
| J4 (J3) | Boom-mic 3.5 mm jack SJ2-3593D-SMT | courtyard X 8.1…28.7, Y −17.6…−6.4 (centre 18.4, −12.0); plug axis Y = −12 | +X_B (**rear** under M1-A ✗) | ≈ 5.0 (VERIFY) | Locating pegs Ø1.7 at (15.23, −12) and (22.23, −12). The courtyard corner overhangs the round edge by 2.7 mm. **Must move to the front-lower edge** (issue I-1). |
| SW1 (SW1) | POWER, EVQ-P7A side-push | (−28.8, 0.0), rot 90° | −X_B (front under A) | 1.35 | Actuator ≈ 0.4 mm inside the edge. The shell key needs ≈ 0.2 mm travel (VERIFY). |
| SW4 (SW4) | MFB, EVQ-P7A side-push | (+28.68, −1.0), rot −90° | +X_B (rear under A) | 1.35 | As SW1 |
| SW3 (SW3) | Thumbwheel encoder, **PLACEHOLDER PEC09** | footprint origin (+21.8, +8.0); courtyard X 19.3…26.8, Y 5.5…15.5 (centre 23.1, 10.5) | Rim, rear (under A) | 7.5 (placeholder) | Replace with a real low-profile roller encoder (M4); position and height will change |
| SW2 (SW2) | BOOT, B3U-1000P top-push | (−12.85, +10.7) | +Z_B | 1.6 | Internal/service access only |
| D7 (D6) | RGB LED, top-view PLCC4 | (−26.2, +9.0) | +Z_B (emits up from the board) | 1.9 | Light pipe to the shell window. Under M1-A it shines outward ✓. |
| D3 (D2) | Charge LED 0603 red | (−24.05, −14.35) | +Z_B | 0.8 | **Move next to D7** so both share one light pipe (issue I-4) |
| MK1 (MK1) | Voice mic, bottom-port | body (−16.0, −22.0); **port hole Ø0.8 at (−16.0, −21.32)** (top-side, rot 0°) | port opens on the side opposite the mic body | 1.2 | Under M1-A it must move to the BOTTOM side (issue I-2). Flipping mirrors the port offset: the hole moves to (−16.0, −22.68) unless the part is also rotated 180°. |
| MK2 (MK2) | Reference mic, bottom-port | body (15.5, 16.5); **port Ø0.8 at (15.5, 17.18)** | as above | 1.2 | As MK1 (after a flip: (15.5, 15.82) unless rotated 180°) |
| MK3 (MK3) | Inner mic (DNP), bottom-port, BOTTOM side | body (−1.25, −4.1); port Ø0.8 at (−1.25, −4.78) | opens to the top side | 1.2 (below board) | See issue I-6 |
| U2 (U6) | ESP32-S3-WROOM-1 module | body X −9.0…+9.0, Y +0.5…+26.0 (antenna end flush with the flat edge) | — | 3.1 | **Antenna keep-out:** no copper on any PCB layer under or beside the antenna (KiCad courtyard spans X ±24 mm, 15 mm beyond the flat edge). No metal, battery, screws, steel headband/yoke, driver magnet or metallic paint within 15 mm of the antenna end and sides (Espressif guidance, VERIFY in the hardware design guidelines). The shell over it must be plastic. See issue I-11. |
| J3 (J2) | Battery JST SH 3p horizontal | (−25.0, −8.5), rot −90° | plug inserts parallel to the board (direction: check footprint) | 2.95 + plug | Cable to the battery pocket |
| J5 (J4) | Left driver JST SH 2p | (−17.5, −8.5), rot 0° | parallel to the board (check footprint) | 2.95 + plug | Pigtail to the left driver |
| J6 (J5) | Right-cup harness JST SH 2p | (+10.3, −23.0), rot −25° | parallel to the board (check footprint) | 2.95 + plug | Route to the headband entry with strain relief |
| U9 (U8) | IMU LSM6DSV16X | (+13.0, +11.2), rot 0° | — | 0.86 | Record the chip's X/Y/Z axis directions vs frame H in the assembly drawing |

Full list (all 134 parts, both sides, L×W×H): `orga_v1_component_envelope.csv`.

## 4. Height map (baseline)

| Zone | Max height above PCB top (Z_B max) | Driven by |
|---|---|---|
| Jack J4 area (right-lower) | 5.0 (Z_B 6.6) | 3.5 mm jack |
| Thumbwheel area | 7.5 (Z_B 9.1), placeholder | PEC09 placeholder; expect lower with the real part |
| USB-C area | 3.31 (Z_B 4.91) | Receptacle |
| Module area | 3.1 (Z_B 4.7) | ESP32 shield can |
| JST connectors | 2.95 + mated plug, plus cable bend radius ~3 mm | Cable exits need space |
| Rest of top side | ≤ 1.9 | ICs, LED, passives |
| Bottom side | 1.2 below the board (MK3), test pads flat | Keep ≥ 1.0 mm clearance for pogo-pin testing access if possible |

Rule: shell inner surface ≥ 0.5 mm above the tallest part in each zone (FDM), ≥ 0.3 mm (SLA/MJF).

## 5. What mechanics must hand back (MR-050…053)

1. **Outline DXF** in frame B: layer `OUTLINE` (closed), layer `HOLES` (mounting).
2. **Ports/openings DXF** in frame B: layer `PORTS_AND_OPENINGS` with the required centre and direction of every edge part (table §3).
3. **Keep-out/height map:** polygons with max height for the top and bottom sides, gasket rings around mic ports (≥ Ø4 mm part-free on the gasket side), light-pipe footprint, key-cap contact zones, screw-head and insert-boss clearances (Ø7 mm part-free around each hole).
4. Electronics then re-places the parts, updates KiCad (Edge.Cuts from the DXF, `User.1` = shell inner wall, `User.2` = keep-outs), and returns a new board **STEP** for the next CAD iteration.
