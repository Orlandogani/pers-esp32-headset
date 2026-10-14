# 07 — Mechanical Verification Plan

## Stage V0 — digital (every CAD iteration, before printing)

| Check | Method | Pass |
|---|---|---|
| Interference | Boolean intersection: shell ∩ board-STEP envelope, battery, driver, harness | Zero volume |
| Clearances | Minimum distance: shell to tallest parts, battery swell envelope, cable bend zones | Values per file 05 §2 |
| Edge-part alignment | Shell opening centre vs part centre (USB, jack, keys, light pipe, mic ports) | ≤ 0.2 mm offset |
| Antenna zone | No metal bodies (screws, inserts, steel band, magnet, battery) within 15 mm of the antenna end and sides | Pass/fail |
| Mass estimate | Volume × density per material + purchased-part masses | MR-001 / MR-002 |
| Section views | Cut through the cup centre on the X_H = const and Z_H = const planes (both contain the cup axis Y_H), saved as PNG | Review by the owner |

## Stage V1 — print-fit (FDM)

| Check | Method | Pass |
|---|---|---|
| 1:1 paper print of the outline in the cup | Print the DXF at 100 %, cut out | Fits with 0.3 mm/side |
| Tolerance coupon | Print a coupon with holes, pegs, insert bosses and slots at ±0.1 mm steps | Choose clearances for the next prints |
| Dummy board | Print the STL envelope (or the real bare PCB) and fit it into the printed cup | Sits on standoffs; no rocking |
| Connector access | Insert 3 different USB-C cables and the boom-mic plug | Full mating depth and click, no shell interference |
| Keys | Press each key 20× | Click felt; no binding; over-travel stop works |

## Stage V2 — functional prototype (SLA/MJF + real electronics)

| Check | Method | Pass |
|---|---|---|
| PCB retention under USB load | Plug and unplug USB-C 50× and pull the cable sideways | No board movement, no cracked bosses |
| Mic acoustic seal | Record the voice mic with and without tape over the shell port; play a sweep through the driver | Taped port drops the level ≥ 15 dB (seal OK); driver leakage into the voice mic is low |
| Light pipe | View from 0°/45° in room light | LED colours distinguishable; no leak into other openings |
| RF | RSSI/throughput dongle↔headset at 1, 5 and 10 m, worn on a head vs on the bench | Range ≥ 10 m line of sight (design doc §1.3) |
| Clamping force | Spring scale or kitchen scale with cups at 150 mm spacing | 2.5–4.5 N |
| Mass and balance | Kitchen scale per cup | ≤ 300 g total; L/R difference per MR-002 |
| Comfort | 3–5 people, 30–60 min wear | No pain points; pad seal OK |
| Thermal | Charge at 0.5 A for 30 min, touch/IR thermometer on the shell | Shell ≤ 40 °C at skin contact |
| Drop (optional) | 1 m onto a hard floor, 6 orientations | No structural break; electronics still work |

## Records

Keep a test log (date, CAD rev, print process/material, result, photo) for the portfolio write-up.
