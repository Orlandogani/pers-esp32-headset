# 12 — Rev B status (2026-10-13)

Supersedes the yoke/arm parts of file 10 (rev A.5). Everything else in file 10 still holds. Iteration history: `mech/log.md`. Assembly: file 11.

## Decision: HS35-style mechanism (own geometry)
Reference: a Corsair HS35 the user showed. We copy the mechanism principle only, not its parts or styling details.

| Item | Rev A.5 | Rev B |
|---|---|---|
| Cup to headband | Single arm in a tunnel along the front wall, M3 shoulder-screw pivot inside the cup | **Horseshoe yoke** outside the shell, around the upper half of the cup |
| Tilt pivot | Front only, metal screw + nut | **Two plastic studs** moulded on the shell side wall (front and rear, y = 0, z = 9.25); the yoke snaps over them |
| Tilt range | ±7° | **±10° free, hard stop at ±12°** (wedge lug on each stud in an arc slot in the yoke end). Without the stop the cup would flop off the head: its CoM is ~9 mm ear-side of the axis. |
| Yaw swivel | Pin in the slider socket, ±15° | **Collar at the yoke crown** (the visible swivel ring), ±15° via set screw in an arc groove |
| Slider end | Straight rail into a socket | Rail turns into an **S-arm** that bows out and drops into the collar |
| Harness | Down the tunnel, through a bore into the cavity | **Free loop** from the collar to a grommet hole in the outer face near the top. The hole is radially inside the yoke, so the yoke can never pinch the cable in tilt. |
| Outer face | Plain wedge | **Cap disc** Ø56 at (0, 5): 1.6 mm ring groove, 0.8 deep. No mass added. |
| Board outline | Minus the tunnel strip and the nut boss | **+487 mm²** along the front-upper wall (X_B −35…−11, Y_B −11…47; KiCad X 65…89, Y 53…111). Nothing removed. |

**Why the outline and proportions stay as they are:** the cup is already a tall oval (78 × 105 outer), close to the HS35's proportion. The edge parts (lower rim), the ear pad size and the ESP32 antenna flat (2 mm from the rear-upper wall) pin the outline.

**Why the yoke stands proud instead of flush:** a flush HS35 yoke would need a 4.1 mm step in the upper side wall. At the rear-upper wall that step would cut into the U2 module (antenna end at X_B 33, wall at 35). The yoke therefore stands 4.1 mm proud at the pivots and 6.1 mm at the crown. To make it flush, U2 would have to move about 4 mm toward the front and the upper board edge shrink by about 4 mm. That is open as an option (not done).

## Key dimensions (params/orga_params.py, "rev B" block)
- **Yoke band:** 3.5 radial × 10 along the cup axis. Radial gap 0.6 at the pivots, 2.6 at the crown (the crown region swings outward ~1.7 mm at 10°).
- **Side panels:** recessed 6.5 × 1.5 for looks and mass.
- **Studs:** Ø6 with a 1 mm lead-in. Yoke holes Ø6.4. Inner reinforcing boss Ø10 × 1.2, which leaves 0.8 mm to the board edge.
- **Stop lug:** ±10° wedge, 1.2 high. Slot half-angle 22°.
- **Collar:** Ø12 × 7. Pin Ø6. 0.5 mm axial gap to the crown boss.
- **S-arm:** 12 × 4 section. Starts at band angle 56° and passes through (Y_H 127.2, Z_H 79).
- **Snap-on:** each end spreads 4.4 mm, about 4.4 N, peak 13 MPa (PETG yield ≈ 50).

## V0 result (rev B, OpenCascade)
- **Interference:** zero unintended overlaps; all clearances unchanged from A.5.
- **Tilt sweep:** 0 overlap to ±11.5°, contact at ±12.5° (lug stop).
- **Yaw sweep:** ±15° clear.
- **Assembly paths:**
  - Both shells close with 0 overlap.
  - The yoke lowers onto the closed cup with 0 overlap outside the stud zones (it crosses the studs by spreading, as intended).
  - The collar slides over the pin with 0 overlap.
  - The slider detent and stop behave as in A.5.
- **Tool access:** shell screws 0.7 mm, PCB screws ≥ 4.95 mm, collar set screw 0.3 mm.
- **Antenna:** the nearest metal is the driver magnet at 16.7 mm (the rev A.5 pivot screw is gone).
- **Mass:** 294 g (MR-001 ≤ 300 OK).
  - Yoke 6.6 g each, against 4.2 g for the old arm.
  - Slider 4.6 g, against 3.7 g.
  - Shells about 3.5 g lighter each (no tunnel).

## Electronics side
- The edge-part table in `out/PCB_changes_B.md` is identical to A.5. The KiCad board is valid as it is.
- `out/ORGA-PCB-outline-B.dxf` is optional: import it only if you want the extra 487 mm² along the front wall.

## Still to verify
- Snap force and lug durability, the stud play, and the grommet seal (bass check), all on the first print.
- Tilt on a real head (now ±10° as doc 06 asks).
- Everything already open in file 10 (driver, pads, cell, boom plug, clamp force).
