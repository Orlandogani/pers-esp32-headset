# ORGA mech — how the pieces work together

## Where things live

| What | Where | Owner |
|---|---|---|
| Spec docs (MDCP 00–09, design doc) | claude.ai project "Embedded Headset" + copy in `docs/` | Claude updates both when a decision changes them |
| Every dimension | `params/orga_params.py` (source-tagged) | Single source of truth |
| Part geometry | `src/*.py` (build123d), one script per part | Regenerated, never edited by hand in FreeCAD |
| Generated parts | `out/` — STEP (CAD), 3MF (print, already oriented), STL | Never edit by hand |
| Visual review, sections, measurements, interference | FreeCAD via the FreeCAD MCP (`out/*.step` opened as an assembly) | Checks only; findings go back into params/scripts |
| Your own quick edits in FreeCAD | Save as `scratch/*.FCStd`, then tell Claude the change | Claude moves it into params/scripts |
| Iteration history | `log.md` | One line per iteration |

## One iteration

1. Change a value in `params/orga_params.py` (or a script in `src/`).
2. Build: `python src/build_all.py` → `out/` (STEP + 3MF + STL per part, plus `ORGA-M-ASM-<rev>.step`).
   Claude can run this in its own workspace and write the results into this folder, or you run it locally.
3. Check: Claude opens `out/ORGA-M-ASM-<rev>.step` in your running FreeCAD through the MCP, runs interference, clearance and section checks (V0 table, file 07) and takes the 3 review renders.
4. Log the result in `log.md`. Print from `out/*.3mf`.

FreeCAD can also read the parameters: `python params/orga_params.py --csv` → `out/orga_params.csv`, importable into a FreeCAD Spreadsheet (column `name` = alias).

## Requirements for the FreeCAD link

- FreeCAD running with the AICopilot workbench (it listens on localhost:23456).
- The FreeCAD MCP registered in the **Claude desktop app** and the desktop app open while we work.
