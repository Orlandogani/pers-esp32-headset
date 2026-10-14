# PCB changes for ORGA rev A (board frame B: origin = driver axis, X rear, Y up)

KiCad mapping: X_kicad = X_B + 100, Y_kicad = -Y_B + 100. Outline, holes and keep-outs are in `ORGA-PCB-outline-A.dxf`.

Direction = in-plane angle of the opening/actuator normal, degrees from +X_B (rear) counter-clockwise; 180 = toward the face.

| Item | X_B | Y_B | Direction [deg] | Height above board top | Note |
|---|---|---|---|---|---|
| J1 USB-C mouth | 0.00 | -50.80 | -90 | 1.60 | board tab to Y = -50.0; mouth 0.3 inside the shell inner wall; plug axis 1.6 above board (VERIFY) |
| J4 jack mouth | -32.20 | -29.25 | -160 | 2.50 | jack face 1.0 mm inside the wall, plug axis 20 deg below horizontal toward the face |
| SW MFB actuator face | 31.86 | -25.84 | -17 | 0.70 | EVQ-P7A, actuator normal to rim |
| SW PWR actuator face | -16.93 | -45.22 | -115 | 0.70 | EVQ-P7A, actuator normal to rim |
| SW3 dial centre (SIQ-02FVS3) | 17.31 | -43.57 | -62 | 1.50 | edge-drive dial Ø14.4 parallel to the board, top 4.0 above it, edge 1.5 mm past the shell; board tab 8 wide to 4.0 past the centre along the normal (dial thickness VERIFY) |
| U2 module ANTENNA END (module rotated 90°) | 33.00 | 14.00 | 0 | 0.00 | module 25.5 along X, 18.0 along Y; antenna end flush with the board flat at X = 33.0; keep-out 15 mm |
| D7 + D3 LEDs (side by side) | 5.00 | -28.00 | 0 | 0.00 | <= 1 mm apart under one 5.8 x 2.8 guide |
| MK1 port (bottom-side mic) | -17.00 | -35.00 | 0 | 0.00 | port hole opens on TOP side; gasket ring Ø4.2 part-free on top |
| MK2 port (bottom-side mic) | 10.00 | 36.00 | 0 | 0.00 | port hole opens on TOP side; gasket ring Ø4.2 part-free on top |
| M2 board hole 1 | 0.00 | -37.00 | — | — | Ø2.4, Ø7 part-free both sides |
| M2 board hole 2 | 22.00 | -12.00 | — | — | Ø2.4, Ø7 part-free both sides |
| M2 board hole 3 | -20.00 | 18.00 | — | — | Ø2.4, Ø7 part-free both sides |
| Shell-screw notch 1 | 20.45 | 43.40 | — | — | notch R3.7 in the outline |
| Shell-screw notch 2 | -7.10 | 48.02 | — | — | notch R3.7 in the outline |
| Shell-screw notch 3 | -24.38 | -40.02 | — | — | notch R3.7 in the outline |
| Shell-screw notch 4 | 26.86 | -36.97 | — | — | notch R3.7 in the outline |
