# 08 — Open Mechanical Decisions and Known Issues

## A. Decisions (resolve roughly in this order)

| ID | Decision | Options | Recommendation | Blocks |
|---|---|---|---|---|
| **M1** | **PCB orientation in the left cup** | A: component (top) side faces OUTWARD toward the outer shell. B: top side faces INWARD toward the driver. | **A.** The module and antenna sit away from the head (design doc §11). The top-view LED shines outward. The tall jack and USB use the outer shell's depth. Trade-off: the test pads face the baffle, so the PCB must be unscrewed to reach them (or add pogo-access holes in the baffle). | Everything below |
| M2 | Boom-mic connector | 3.5 mm 3-pole jack (current SJ2-3593D) vs keyed/2.5 mm | Keep 3.5 mm for V1 (cheap off-the-shelf booms). Check the boom plug pinout. | Jack position |
| M3 | Battery location (V1) | Behind the PCB (stacked) vs beside the PCB in the left cup vs right cup (V2) | Behind or beside the PCB in the left cup for V1 (simplest harness). Right cup in V2. | Cup depth, balance |
| M4 | Thumbwheel encoder part | Low-profile side-actuated roller encoder (part TBD) vs volume buttons | Choose a real part with a drawing before shell design of the rear rim | Rear-rim geometry, PCB edge |
| M5 | Driver part | 40 mm 32 Ω ≥ 100 dB/mW, with a drawing | Pick it now; the cup and baffle depend on it | Cup/baffle |
| M6 | Headband construction | Spring-steel band + printed sliders vs fully printed band | Steel band (consistent clamp force, durable) | Clamp force, mass |
| M7 | Ear pads | Off-the-shelf replacement size vs custom | Off-the-shelf (inner opening target ≈ 75 × 48, minimum 65 × 45; file 06) | Cup outer ring geometry |
| M8 | Cup shape / ID language | Round vs oval vs D-shaped cup; style | Oval/rounded-rectangle cup gives room for the pinna and the electronics. Final ID by the owner. | Board outline |
| M9 | Print process for V2 shells | MJF PA12 + SLA vs SLA only | MJF + SLA (file 05) | Tolerances |
| M10 | Swivel / fold | Fixed yoke, swivel only, or folding | Swivel (yaw + tilt) only for V1 | Harness routing |

## B. Issues found in the baseline placement (orga-v1)

| ID | Issue | Fix (under M1 = A) |
|---|---|---|
| **I-1** | The boom-mic jack mouth faces +X_B. Under M1-A that is the **rear** of the cup, but the boom must exit at the **front-lower** edge toward the mouth. The README text ("right edge, mouth out") assumed the opposite orientation. | Move the jack to the front-lower rim (−X_B, −Y_B quadrant). Electronics re-places J4 and its ESD/RF parts. |
| **I-2** | MEMS mics are **bottom-port**. With MK1/MK2 on the top side, their PCB hole opens to the board's bottom side. Under M1-A that is the driver side, so they would listen to the cup interior. | Move MK1 and MK2 to the **bottom side** (port opens through the PCB to the top/outer side) and seal it to the shell with a gasket. Flipping mirrors the port offset, so re-derive the port coordinates (file 03 §3). Or keep them on top and choose M1-B (not recommended). |
| I-3 | The jack courtyard overhangs the round outline by about 2.7 mm at one corner; the USB-C mouth protrudes ≈ 0.6 mm (centre) to 0.9 mm (body corners). | Give the outline local flats at the USB and jack positions in the MCAD outline. |
| I-4 | The charge LED (D3/orga-v1 D2) sits about 23 mm away from the RGB LED, so two light windows would be needed. | Move D3 right next to D7 (≤ 1 mm gap) under one slot light guide (file 05 §4). |
| I-5 | POWER key at the front edge (−X_B) under M1-A, while design doc §13.3 wants power/MFB at the lower rear. | Owner decision. Recommended: thumbwheel and MFB on the rear rim, POWER on the lower rear or bottom, so it is not pressed by accident when adjusting the cup. |
| I-6 | MK3 (inner-cup mic, DNP) on the main PCB only hears the cavity **behind** the driver, not the ear-side front volume. | For measurement/auto-EQ research, add a small mic flex/board in front of the driver later, or an acoustic tube through the baffle. Leave MK3 as is (DNP). |
| I-7 | Only 2 mounting holes, none near USB-C | Add a third hole within 10 mm of J1 (MR-011) |
| I-8 | The thumbwheel is a placeholder (PEC09 is a 9 mm panel encoder, not a thumbwheel) | Decision M4 |
| I-9 | The user's board `headset-orga` uses 0603 passives where orga-v1 uses 0402, so the inner placement will be slightly denser | Electronics side; no mechanical impact beyond the height map (≤ 1 mm) |
| I-10 | Ø2.2 mounting holes leave little margin for FDM boss position error | Ø2.4–2.5 for FDM prototypes, or SLA/MJF bosses |
| **I-11** | The antenna keep-out (15 mm around the module's antenna end and sides) conflicts with the usual design: the headband yoke/steel band attaches at the **top** of the cup, right over the antenna. H1 is ≈ 13 mm away, the placeholder encoder body ≈ 11 mm, and the right-cup harness must leave toward the top. | Decide the yoke attachment early. Options: a plastic yoke/top section with the steel band ending ≥ 15 mm away; or rotate the board so the antenna points up-rear, away from the yoke; or switch to WROOM-1U + an FPC antenna placed away from metal. Route the harness outside the zone. Verify with an RSSI test (file 07). |

## C. Process

1. The design chat resolves M1 and proposes M3–M8 with the owner.
2. Mechanics produces the cup concept and the outline/ports DXF (file 03 §5).
3. Electronics updates the KiCad placement (I-1, I-2, I-4, I-7) and exports a board STEP.
4. Run V0 checks, then the V1 print-fit (file 07).
