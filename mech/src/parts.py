"""ORGA rev A part registry: builds every printed part, its placement in head frame H and its print pose."""
from orga_common import *  # noqa: F401,F403
from orga_common import v, REV
import cups, small_parts as sp, yoke_headband as yh, dummies


def print_pose(solid, down):
    """Rotate so local vector `down` points to -Z, then sit on Z=0 centred in XY."""
    d = Vector(*down).normalized()
    z_new = -d
    x_try = Vector(1, 0, 0) if abs(z_new.X) < 0.9 else Vector(0, 1, 0)
    x_new = (x_try - z_new * x_try.dot(z_new)).normalized()
    # inverse of the frame (x_new, y_new, z_new): express the solid in that frame
    pl = Plane(origin=(0, 0, 0), x_dir=x_new, z_dir=z_new)
    s = pl.to_local_coords(solid)
    bb = s.bounding_box()
    return Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -bb.min.Z) * s


def build():
    P = {}
    zr = -v("baffle_t") - v("skirt_len")
    wn = Vector(-v("shell_slope"), 0, 1)

    def add(name, local, place, down, mat="PETG", qty=1, note=""):
        P[name] = dict(local=local, H=place(local), down=down, mat=mat, qty=qty, note=note)

    L, Rr = to_head_left, (lambda s: to_head_right(mirror_x(s)))
    print("  cups...", flush=True)
    add("CUPL-OUT", cups.shell_left(), L, (wn.X, wn.Y, wn.Z), note="outer face down, tree support under the R3 edge")
    add("CUPL-FRM", cups.frame_left(), L, (0, 0, -1), note="skirt end down, support inside skirt for the baffle")
    add("CUPR-OUT", cups.shell_right_local(), Rr, (wn.X, wn.Y, wn.Z), note="mirror of the base shell")
    add("CUPR-FRM", cups.frame_right_local(), Rr, (0, 0, -1), note="battery tray integrated")
    ring = Pos(0, 0, zr) * cups.padring()
    add("PADRING-L", ring, L, (0, 0, -1), note="adapter for the bought ear pad (M7)")
    add("PADRING-R", ring, Rr, (0, 0, -1))
    print("  small parts...", flush=True)
    for k in ("PWR", "MFB"):
        P[f"KEY-{k}"] = dict(local=sp.key_local(k), H=L(sp.key(k)), down=(0, 0, 1), mat="PETG", qty=1,
                             note="cap face down")
    add("LGUIDE", sp.light_guide(), L, (0, 0, -1), mat="clear PETG / clear resin")
    print("  yoke + headband...", flush=True)
    import yoke_b as _yb
    yk = _yb.yoke()
    add("YOKE-L", yk, L, (0, 0, -1), note="flat on the bed (band plane), no supports; snaps over the shell studs")
    add("YOKE-R", yk, Rr, (0, 0, -1))
    sl = yh.slider()
    P["SLIDER-L"] = dict(local=sl, H=sl, down=(-1, 0, 0), mat="PETG", qty=1, note="on its side")
    slr = mirror(sl, about=Plane.XZ)
    P["SLIDER-R"] = dict(local=slr, H=slr, down=(-1, 0, 0), mat="PETG", qty=1, note="on its side")
    bt = yh.band_top()
    P["BAND-TOP"] = dict(local=bt, H=bt, down=(-1, 0, 0), mat="PETG", qty=1,
                         note="on its side; steel band slides in from the +Y end")
    for n, d in P.items():
        d["print"] = print_pose(d["local"], d["down"])
    return P


def envelopes():
    """Purchased / electronic envelopes in H (not printed)."""
    E = {}
    for n, (s, metal) in dummies.left_electronics().items():
        E[n] = (to_head_left(s), metal, "L")
    E["pad L"] = (to_head_left(dummies.pad()), False, "L")
    for n, (s, metal) in dummies.right_contents_local().items():
        E[n] = (to_head_right(mirror_x(s)), metal, "R")
    E["pad R"] = (to_head_right(mirror_x(dummies.pad())), False, "R")
    return E
