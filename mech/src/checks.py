"""V0 digital checks (file 07): interference, clearances, antenna zone, tilt sweep, mass, bed fit."""
import itertools, math
from build123d import Rot, Pos, Location, Axis
from orga_common import v, Y_ZC0
import yoke_headband as yh

ALLOWED = [("insert", "CUP"), ("antenna", "U2 module"), ("cell swell", "cell"), ("pad", "PADRING"), ("SW3 wheel", "SW3 encoder body"), ("magnet", "driver")]
BED = 256.0


def _allowed(a, b):
    for x, y in ALLOWED:
        if (x in a and y in b) or (x in b and y in a):
            return True
    return False


def _bbox_overlap(s1, s2, tol=0.05):
    a, b = s1.bounding_box(), s2.bounding_box()
    return not (a.max.X < b.min.X - tol or b.max.X < a.min.X - tol or a.max.Y < b.min.Y - tol or
                b.max.Y < a.min.Y - tol or a.max.Z < b.min.Z - tol or b.max.Z < a.min.Z - tol)


def interference(items):
    """items: dict name -> shape (all in H). Returns list of (a, b, volume)."""
    hits = []
    names = list(items)
    for a, b in itertools.combinations(names, 2):
        if _allowed(a, b) or not _bbox_overlap(items[a], items[b]):
            continue
        try:
            vol = (items[a] & items[b]).volume
        except Exception:
            vol = float("nan")
        if not (vol < 0.01):
            hits.append((a, b, vol))
    return hits


def clearances(shell, envs, names):
    out = []
    for n in names:
        try:
            out.append((n, shell.distance_to(envs[n])))
        except Exception:
            out.append((n, float("nan")))
    return sorted(out, key=lambda t: t[1])


def antenna(ant, metals):
    return sorted(((n, ant.distance_to(s)) for n, s in metals.items()), key=lambda t: t[1])


def tilt_sweep(cup_parts, fork, side=+1, angles=(-14.0, -12.5, -11.5, -10.0, -5.0, 5.0, 10.0, 11.5, 12.5, 14.0)):
    """Rotate the cup about the yoke stud axis (parallel to X_H through Y = +/-(Y_ZC0+zp), Z = 0) and test vs the yoke."""
    y0 = side * (Y_ZC0 + v("yk_pivot_z"))
    res = []
    for ang in angles:
        loc = Pos(0, y0, 0) * Rot(ang, 0, 0) * Pos(0, -y0, 0)
        worst = 0.0
        for n, s in cup_parts.items():
            if not _bbox_overlap(loc * s, fork):
                continue
            vol = ((loc * s) & fork).volume
            worst = max(worst, vol)
        res.append((ang, worst))
    return res


def masses(P, purchased):
    rho, ff = v("density_petg"), v("fill_factor")
    left = right = band = 0.0
    rows = []
    for n, d in P.items():
        g = d["local"].volume / 1000 * rho * ff
        rows.append((n, round(g, 1)))
        if n.endswith("-L") or n.startswith("CUPL") or n.startswith("KEY") or n == "LGUIDE":
            left += g
        elif n.endswith("-R") or n.startswith("CUPR"):
            right += g
        else:
            band += g
    for n, g, side in purchased:
        rows.append((n + " (bought)", g))
        if side == "L": left += g
        elif side == "R": right += g
        else: band += g
    return rows, left, right, band


def bed_fit(P):
    out = []
    for n, d in P.items():
        bb = d["print"].bounding_box()
        dims = (bb.size.X, bb.size.Y, bb.size.Z)
        out.append((n, dims, max(dims) <= BED))
    return out


def steel_band():
    sw, st = v("steel_slot")
    return yh.sector(-30.0, v("band_half_deg"), yh.R + 2.85, yh.R + 2.85 + 1.0, 6.0)


# ======================================================================= assembly-motion checks (rev A.4)
def _overlaps(moving, fixed):
    """moving/fixed: dict name -> shape. Returns (worst volume, pair)."""
    worst, pair = 0.0, None
    for a, sa in moving.items():
        for b, sb in fixed.items():
            if _allowed(a, b) or not _bbox_overlap(sa, sb):
                continue
            vol = (sa & sb).volume
            if vol > worst:
                worst, pair = vol, (a, b)
    return worst, pair


def sweep(moving, fixed, direction, steps):
    """Translate `moving` by direction*d for each d in steps (assembly path, d = distance still to travel)."""
    from build123d import Vector
    out = []
    for d in steps:
        loc = Pos(*(Vector(*direction) * d))
        w, p = _overlaps({n: loc * s for n, s in moving.items()}, fixed)
        out.append((d, w, p))
    return out


def arc_sweep(moving, fixed, cz, deltas):
    """Slide along the headband arc: rotate about X through (0, 0, cz); +delta = slider pulled outward."""
    out = []
    for dl in deltas:
        loc = Pos(0, 0, cz) * Rot(-dl, 0, 0) * Pos(0, 0, -cz)
        w, p = _overlaps({n: loc * s for n, s in moving.items()}, fixed)
        out.append((dl, w, p))
    return out


def tool_access(tools, obstacles):
    """tools: dict name -> tool envelope (screwdriver bit / tweezers). Returns name, overlap, min distance."""
    out = []
    for n, t in tools.items():
        w, p = _overlaps({n: t}, obstacles)
        try:
            dmin = min(t.distance_to(o) for o in obstacles.values())
        except Exception:
            dmin = float("nan")
        out.append((n, w, p, dmin))
    return out


def yaw_sweep(moving, fixed, axis_y, axis_x=0.0, angles=(-15.0, -7.5, 7.5, 15.0)):
    """Rotate `moving` (cup + yoke) about the vertical swivel axis (Z_H through X_H = axis_x, Y_H = axis_y)."""
    out = []
    for a in angles:
        loc = Pos(axis_x, axis_y, 0) * Rot(0, 0, a) * Pos(-axis_x, -axis_y, 0)
        w, p = _overlaps({n: loc * s for n, s in moving.items()}, fixed)
        out.append((a, w, p))
    return out
