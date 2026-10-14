# 01 — Mechanical Requirements (PRD-M)

Priority: **M** = must, **S** = should, **C** = could.
Verification method: **I** = inspection, **A** = analysis/CAD, **T** = test, **D** = demonstration (see `07_verification_plan.md`).

## Product-level (MR-001 from design doc v0.2 §1.3; the rest are new mechanical targets)

| ID | Requirement | Target | Pri | Ver |
|---|---|---|---|---|
| MR-001 | Total mass, headset without boom mic | ≤ 300 g | M | T |
| MR-002 | Left/right cup mass difference | ≤ 40 g (V1: battery and PCB in the left cup) | S | T |
| MR-003 | Form factor | Over-ear (circumaural), closed-back, two cups on an adjustable headband | M | I |
| MR-004 | Head-size coverage | Fits about 5th-percentile female to 95th-percentile male (file 06) | M | A/T |
| MR-005 | Clamping force | 2.5–4.5 N at 150 mm cup-to-cup spacing (file 06) | S | T |
| MR-006 | Comfort | 1 h continuous wear with no hot spots or pinna contact with the driver grille | S | D |

## Electronics integration

| ID | Requirement | Target | Pri | Ver |
|---|---|---|---|---|
| MR-010 | The main PCB fits in the left cup with all edge parts reachable through the shell | Outline from MCAD → KiCad (file 03) | M | A |
| MR-011 | PCB retention | ≥ 3 fixing points (M2 screws or heat-set inserts). One must sit within 10 mm of the USB-C receptacle. | M | A/I |
| MR-012 | USB-C plug insertion and extraction loads go into the shell, not the solder joints | Shell back-stop rib behind J1; the plug reaches full mating depth | M | T |
| MR-013 | Boom-mic 3.5 mm plug | Full insertion, retained by the jack, positioned toward the mouth (front-lower, left cup) | M | T |
| MR-014 | POWER, MFB and thumbwheel operable with a thumb while wearing the headset, without looking | Actuators on the cup rim. Travel and force per file 05. | M | D |
| MR-015 | BOOT button reachable for service only | Pin-hole or internal access with the cover off | S | I |
| MR-016 | Status LED and charge LED visible from the side | One light pipe/window on the outer shell | S | D |
| MR-017 | Voice mic (MK1) acoustic port toward the mouth; reference mic (MK2) port on the outer shell, top/rear | Sealed acoustic path: shell hole + gasket + mesh | M | T |
| MR-018 | Antenna region (ESP32-S3 module end) | Plastic only, no metal, metallic paint or battery within 15 mm; antenna faces up and away from the head | M | A/T |
| MR-019 | Battery: 1S Li-Po (≈1000 mAh, 603450 class) held without pressure on the cell; swell allowance | ≥ 0.5 mm per side and ≥ 10 % thickness allowance; no sharp edges | M | A/I |
| MR-020 | Right-cup harness (2 wires, V1) through the headband | Strain relief at both cup entries; service loop for full slider extension; no pinching at hinges | M | T |
| MR-021 | Driver mounting | 40 mm driver sealed to the front volume (ear side); rear volume and vent per driver vendor; electronics cavity separated from the front volume | M | A/T |
| MR-022 | No metal parts in contact with the driver wires or HP± pads | The speaker outputs are floating differential and must never touch GND | M | I |

## Use, durability, manufacturing

| ID | Requirement | Target | Pri | Ver |
|---|---|---|---|---|
| MR-030 | Prototype manufacturing | 3D-printable (FDM, SLA or MJF). No undercuts that need tooling. | M | A |
| MR-031 | Serviceability | Main PCB and battery replaceable with screws only (no glue) | M | D |
| MR-032 | Ear pads | Replaceable. Prefer an off-the-shelf pad size the cup interface is designed around. | S | I |
| MR-033 | Operating environment | 0–40 °C, indoor | M | A |
| MR-034 | Drop | 1 m onto a hard floor without structural failure (V1 target, not a gate) | C | T |
| MR-035 | Cycles | Headband adjustment ≥ 1000; hinge/swivel ≥ 1000 (prototype level) | C | T |
| MR-036 | Skin contact | Pad and headband cushion materials safe for skin contact; no exposed print layers on contact areas | S | I |
| MR-037 | Appearance | Portfolio-quality look: clean surfaces, consistent radii, visible "ORGA" branding area | S | I |

## Interfaces owed back to electronics (MCAD → ECAD)

| ID | Deliverable | Format |
|---|---|---|
| MR-050 | Final PCB outline + mounting-hole positions | DXF in board frame B (file 09) |
| MR-051 | Required edge-part positions/directions (USB-C, jack, keys, thumbwheel, LED, mic ports) | Table like file 03, plus DXF layer `PORTS_AND_OPENINGS` |
| MR-052 | Height-limit map over the board (top and bottom) | Polygons with max Z in DXF or a table |
| MR-053 | Gasket / light-pipe / key-cap contact areas on the PCB that must stay free of parts | DXF keep-out polygons |
