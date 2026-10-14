# ORGA rev B — assembly guide

Rev B (2026-10-13) replaces the rev A.4 tunnel arm with an HS35-style mechanism: an external horseshoe yoke, a swivel collar at the yoke crown and an S-arm on the slider. Only the arm, yoke, slider and shell features changed; the cup build (frame, PCB, pad ring, keys) is the same as A.4.

Figures: `renders/ORGA-M-CUPL-B_outer.png`, `_front.png`, `_tilt12.png` (rev B mechanism), `ORGA-M-CUPL-B_exploded.png`. The older `ORGA-guide-*.png` figures still show the A.4 arm; the pad (fig. 2) and band detent (fig. 4, rail part) details are unchanged.
Every step below has been simulated in CAD; results are in the "Assembly-motion checks" section of `out/V0_report_B.md`.

## How the cup is built (what each part does)

Read from the ear outward:

| Part | Job | Held by |
|---|---|---|
| Ear pad (bought) | Comfort and seal against the head | Its fabric sleeve is stretched over the PADRING lip |
| **PADRING** | Adapter between whatever pad you buy and the cup | 6 snap bumps click into a groove inside the frame skirt; pull the pad to remove it |
| **CUPx-FRM** (frame) | The structural middle. The **baffle** carries the driver and closes the cup on the ear side; the **16 mm skirt** sets the ear-to-driver distance; the **standoffs** (left only) carry the PCB; the **tabs** fill the USB and wheel notches; the right frame has the **battery tray** | 4 × M2 screws from the ear side into the outer shell |
| Driver | Sound | Glued onto the seat ring on the baffle (foam gasket) |
| PCB (left) | Electronics | 3 × M2 × 4 screws into the frame standoffs |
| **CUPx-OUT** (outer shell) | Cosmetic cover with the cap disc; holds the keys, light guide and mic ports; carries the two **pivot studs** (front and rear, at mid-height) and the **harness grommet hole** near the top of the outer face | Sits on the baffle, located by the frame's lip; the 4 shell screws pull it down |
| **YOKE** | Horseshoe around the upper half of the cup, outside the shell. Tilt pivot on the two studs (±10° free, hard stop at ±12°), swivel pin on the crown | Snaps over the studs by its own spring; no screws |
| **SLIDER** | Rail in the headband (size adjust) that ends in the **S-arm** and the **swivel collar** | Collar set screw rides in the yoke pin's arc groove (±15° yaw) |

The shell and frame meet at a **butt joint on the baffle's rear face**: the shell's bottom edge sits on the baffle, and the frame's 2 mm lip inside the shell keeps them aligned. Every opening that a part sticks out through is a notch **open at the shell's bottom edge** (USB-C, thumbwheel), so the shell can be lowered straight down over the finished PCB. The frame's tabs then close the gaps underneath. Nothing passes through the shell wall for the yoke any more, so there is no tunnel to seal.

## Hardware

| Qty | Item |
|---|---|
| 11 | M2 heat-set insert, L 4 (4 per shell + 3 in the left frame) |
| 8 | M2 × 5 pan or button head (shell screws) |
| 3 | M2 × 4 (PCB) |
| 2 | M2 × 4 self-tapping (collar set screws) |
| 1 | Ø2 × 14 dowel or M2 × 14 screw (steel band pin) |
| 1 | Spring-steel band 171 × 12 × 1 mm (65Mn) |
| 2 | Silicone grommet (or a heat-shrink stop) for the Ø3.4 harness hole, Ø6 counterbore |
| 2 + 1 | Foam: driver gasket Ø44/Ø37 × 1 mm, cell pad 2 mm |
| 2 + 2 | Mic gasket (PORON ring, OD 4 / ID 1.4 / 1.8 thick) and Ø4 acoustic mesh disc |
| ≈ 650 mm | 5-core 28–30 AWG silicone harness (braided sleeve optional for the visible loops) |
| — | Cushion foam ≈ 24 × 100 × 8 mm |

No M3 shoulder screws or nuts any more: the pivots are plastic, so there is no metal near the antenna.

Tools: soldering iron with an M2 insert tip, PH0 or T6 driver (≤ Ø3 shaft), tweezers.

## A. Prepare the printed parts

1. **Heat-set the inserts.** 4 into each outer shell's screw bosses (from the open side) and 3 into the left frame's PCB standoffs.
2. **Left shell, from the inside:**
   1. Glue the two mesh discs into the outside recesses of the mic ports.
   2. Push the light guide into its boss.
   3. Drop KEY-PWR (dimple) and KEY-MFB (ridges) into their slots so the flanges rest on the inner wall.
3. **Both shells:** push the harness through the grommet hole in the outer face (top, front of the crown) from outside, with about 40 mm outside for the loop. Seat the grommet in the counterbore; it seals the hole acoustically.
4. **Both frames:** glue the driver onto the seat ring with its gasket, diaphragm toward the ear.

## B. Left cup

5. **PCB:** component side up onto the 3 standoffs, then 3 × M2 × 4. Solder the driver wires and fit the harness to the PCB.
6. **Close:** lower the shell (with the keys, light guide and harness) straight onto the frame.
   - The USB-C, jack, keys and wheel line up by themselves.
   - The frame's two tabs fill the notches under the USB-C and the wheel.
   - The lip locates the shell.
7. **Screw:** turn the cup over and put 4 × M2 × 5 up through the baffle from the ear side. They are inside the skirt, about 2 mm from its wall. A Ø3 bit has 0.7 mm clearance.
8. **Yoke:** hold the cup level (no tilt) so the stud lugs point up. Lower YOKE-L over the crown, spread its two ends about 4.5 mm with your thumbs and let them snap over the front and rear studs. The lead-in chamfers guide them; the lug on each stud must enter the arc slot in the yoke end. The cup should now tilt ±10° freely and stop firmly at about ±12°.
9. **Pad:** stretch the pad's sleeve over the PADRING lip (fig. 2). Push the ring into the skirt until all 6 bumps click.

## C. Right cup

10. Glue the driver as in A.4. Put the 2 mm foam pad on the cell, lay the cell in the battery tray, and route its lead out of the tray's front-top corner toward the grommet.
11. Repeat steps 6–9 with YOKE-R. Its harness carries the driver pair and the 3 battery wires, which you join inside the cup.

## D. Headband

12. **Steel band:** slide it into BAND-TOP's slot from the +Y (left) end until it stops. Push the Ø2 pin (or M2 × 14) through the cross hole to close the slot.
13. **Sliders:** push each SLIDER rail, tip first, into its sleeve at the BAND-TOP end.
    - The chamfered tip lifts the detent bump.
    - Once inside, it clicks every 5 mm (±3 positions = ±15 mm).
    - A square stop at +15.7 mm stops it pulling out.
    - To remove a slider, take off the cushion, hook the flexure tab through its slit, and slide the slider out.
14. **Swivel:** push each yoke's crown pin up into the collar at the bottom of the S-arm. Drive the M2 self-tapping screw into the collar's pilot (on the back side, −X_H) until it drops into the pin's arc groove, then back it off ¼ turn. The arc lets the cup swivel ±15° and stops the pin from falling out.
15. **Harness:** lay it in the groove on the front face of the collar and the S-arm, then along the slider's +X groove, through a 30 mm service loop at the BAND-TOP end, along BAND-TOP's side groove, and down the other side the same way. Between the collar and the grommet leave a free loop of about 30 mm: the cup moves up to ±9 mm there when it tilts. Fix the harness with small dabs of hot glue; never across a moving joint.
16. **Cushion:** glue the cushion foam to the inner ribs of BAND-TOP.

## Service

- **Pad:** pull it straight off; it comes away with its PADRING.
- **Cup off the headband:** spread the yoke ends and lift the yoke off the studs. The cup stays closed.
- **Inside a cup:** remove the pad and ring, then the 4 shell screws. The shell lifts off with the harness still in its grommet.

## Still to verify on real parts

- Yoke snap force (calculated ≈ 4.4 N per end, 13 MPa in PETG) and whether the stud lug survives repeated snapping. If the ends feel too stiff, the band thickness `yk_t` is a parameter.
- Stud fit in the yoke end (Ø6.0 in Ø6.4) and how much play the tilt has.
- Pad sleeve style. If the pad you buy has its own clip ring, the PADRING lip changes to match it.
- Steel band clamp force (MR-005, 2.5–4.5 N).
- Whether the detent click is too hard or too soft. The bump height is a parameter.
- That the grommet seals the harness hole acoustically (bass check, file 07).
