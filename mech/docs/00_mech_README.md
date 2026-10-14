# ORGA — Mechanical Design Context Package (MDCP) v0.1

| | |
|---|---|
| Product | ORGA (Omni Radiant Gaming Apparatus), over-ear gaming headset |
| Owner | Orlando Gani Sahroni |
| Package date | 2026-10-08 |
| Status | **Input package for the enclosure / 3D design phase.** Nothing mechanical is frozen. |
| Electrical baseline | `claude/custom_headset_hw_design_v0.2.md`, plus the KiCad project `headset-orga` (schematic verified, ERC clean, PCB not yet placed) |

## Purpose

This package gives the 3D-design workstream everything it needs from the electronics side. It also states what the electronics side needs back from mechanics, chiefly the real board outline and edge-part positions. Treat it as the ECAD↔MCAD contract.

## Files

| # | File | What it answers |
|---|---|---|
| 00 | `00_mech_README.md` | Index, source of truth, how to work |
| 01 | `01_mech_requirements.md` | What the mechanics must achieve (IDs MR-xxx), with a verification method for each |
| 02 | `02_system_architecture_mech.md` | What goes in which cup, the stack inside the cup, harness, and the list of purchased mechanical parts |
| 03 | `03_ecad_mcad_interface.md` | Board outline, frames, edge-part positions, keep-outs, heights, mounting. **Read before modelling.** |
| 04 | `04_component_mech_data.md` | Dimensions of every part that touches the enclosure, with source and confidence |
| 05 | `05_enclosure_design_guidelines.md` | DFM for 3D printing, fasteners, acoustics, antenna, ESD, assembly |
| 06 | `06_ergonomics_reference.md` | Head and ear dimensions, clamp force, pad geometry, weight targets |
| 07 | `07_verification_plan.md` | Digital, print-fit and functional checks with pass criteria |
| 08 | `08_open_decisions_and_issues.md` | Decisions to make first (M1…) and issues already found in the baseline placement |
| 09 | `09_cad_workflow_and_conventions.md` | Code-CAD toolchain, coordinate frames, naming, files, ECAD round-trip |
| — | `orga_v1_component_envelope.csv` | All 134 board parts: position, side, body L×W×H, mechanical role (board frame B) |

Binary and script files are delivered as `orga_mech_package_v0.1.zip`; unzip it into `C:\ORLANDO\Lab\kicad\headset-orga\mech\`. Layout as in file 09:

| File | Content |
|---|---|
| `ref/orga_v1_mainboard_envelope.step` | Board (1.6 mm) and a box per component (height-accurate envelope) plus a red antenna keep-out marker. Board frame B. |
| `ref/orga_v1_mainboard_envelope.stl` | The same as a single mesh, for quick print or fit checks |
| `ref/orga_v1_board_outline.dxf` | Outline (layer OUTLINE) and holes ≥ Ø0.5 (layer HOLES: mounting, USB shell slots as circles, jack pegs, mic ports, encoder pins), board frame B, in mm |
| `renders/orga_v1_mech_drawing.png` | Annotated top and bottom view |
| `src/gen_envelope.py`, `src/draw.py` + `src/orga_v1_fps.json`, `src/orga_v1_design_nets.json` | CadQuery scripts and their input data; they regenerate `src/out/` |

## Source-of-truth hierarchy (when two sources disagree)

1. Manufacturer datasheet or drawing of the actual purchased part.
2. KiCad project `headset-orga` (schematic and PCB): electrical truth.
3. This package (MDCP).
4. Design doc v0.2: architecture intent. Its §13 mechanics section is superseded by this package.
5. Generic or reference values marked **VERIFY**. Never freeze a dimension based on these.

## Working rules for the design workstream

- **Decide M1 first** (board orientation in the cup, file 08). Several placement issues depend on it.
- Mechanics owns the board outline, mounting holes and edge-part positions. Electronics owns everything inside the outline. Changes go both ways through files: DXF outline to KiCad, STEP board back to CAD (file 09).
- Every dimension in a CAD parameter file carries a source tag: `datasheet`, `measured`, `assumed-VERIFY`.
- Parametric code-CAD (CadQuery or build123d) is the default, so models stay reviewable and regenerable (file 09).
- Use one coordinate convention throughout: head frame **H** (X forward, Y left, Z up) and board frame **B** (file 03).
