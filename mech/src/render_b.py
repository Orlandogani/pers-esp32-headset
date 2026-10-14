"""Rev B close-up review renders: left cup + yoke + slider, outer view, front view, and the 12 deg tilt stop."""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
from build123d import Pos, Rot
import parts, render
from orga_common import v, Y_ZC0, REV
REN = HERE.parent / "renders"
P = parts.build(); E = parts.envelopes()
C = {"CUPL-OUT": (0.93, 0.93, 0.95), "CUPL-FRM": (0.80, 0.81, 0.84), "PADRING-L": (0.7, 0.7, 0.72),
     "YOKE-L": (0.98, 0.98, 1.0), "SLIDER-L": (0.86, 0.87, 0.9), "KEY-PWR": (0.75, 0.75, 0.78), "KEY-MFB": (0.75, 0.75, 0.78), "LGUIDE": (0.75, 0.9, 1.0)}
def grp(tilt=0.0):
    y0 = Y_ZC0 + v("yk_pivot_z")
    loc = Pos(0, y0, 0) * Rot(tilt, 0, 0) * Pos(0, -y0, 0)
    out = []
    for n, c in C.items():
        s = P[n]["H"]
        out.append(((loc * s) if n not in ("YOKE-L", "SLIDER-L") else s, c))
    out.append(((loc * E["pad L"][0]), (0.55, 0.55, 0.57)))
    return out
for name, az, el, tilt, title in (("outer", 60, 12, 0, "outer side: cap disc, horseshoe yoke, swivel collar, S-arm"),
                                   ("front", 0, 5, 0, "front view (looking back): S-arm drops into the collar at the yoke crown"),
                                   ("tilt12", 0, 5, 12, "front view, cup at the +12 deg tilt stop")):
    ax = render.shade(grp(tilt), azim=az, elev=el)
    ax.set_title(f"ORGA rev {REV} left cup - {title}", fontsize=11)
    ax.figure.savefig(REN / f"ORGA-M-CUPL-{REV}_{name}.png", dpi=150, bbox_inches="tight"); render.plt.close("all")
print("ok")
