#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RATISS Labs - RATISS-CHARGE-01 : generateur de carte (PCB) KiCad.
A executer avec /usr/bin/python3 (module pcbnew fourni par KiCad).

Principe :
  - 2 faces. Toute la logique sur la face AVANT (F.Cu).
  - La masse GND n'est PAS routee : elle est donnee par un plan de masse
    sur la face ARRIERE (B.Cu), relie par un via a chaque pastille GND.
    C'est la methode normale en electronique : moins de bruit, moins de pistes.

Usage :  /usr/bin/python3 tools/gen_pcb.py [--dump]
"""
import sys, math
import pcbnew

HERE = pcbnew.Path = None
import pathlib
PRJ = pathlib.Path(__file__).resolve().parent.parent
BOARD_FILE = PRJ / "RATISS-CHARGE-01.kicad_pcb"
FP_DIR = "/usr/share/kicad/footprints"

MM = pcbnew.FromMM
def V(x, y):
    return pcbnew.VECTOR2I(MM(x), MM(y))

# ---------------------------------------------------------------- placement
# (ref, valeur, bibliotheque empreinte, nom empreinte, x, y, rotation)
#  x,y en mm depuis le coin haut-gauche de la carte
PARTS = [
    ("J1",  "IN 5V",    "Connector_PinHeader_2.54mm", "PinHeader_1x02_P2.54mm_Vertical",  4.0, 12.0,  90),
    ("R3",  "0R4",      "Resistor_SMD", "R_2512_6332Metric",                              12.0,  7.0,  90),
    ("C1",  "10uF",     "Capacitor_SMD", "C_0805_2012Metric",                             14.5, 16.0,  90),
    ("U1",  "TP4056",   "Package_SO", "SOIC-8_3.9x4.9mm_P1.27mm",                         20.0, 13.0,   0),
    ("R4",  "1.2k",     "Resistor_SMD", "R_0805_2012Metric",                              10.5, 20.0,  90),
    ("D2",  "ROUGE",    "LED_SMD", "LED_0805_2012Metric",                                 29.0,  6.5,  90),
    ("R2",  "10k",      "Resistor_SMD", "R_0805_2012Metric",                              29.0, 10.5,   0),
    ("D1",  "VERTE",    "LED_SMD", "LED_0805_2012Metric",                                 34.0,  6.5,  90),
    ("R1",  "10k",      "Resistor_SMD", "R_0805_2012Metric",                              34.0, 10.5,   0),
    ("C2",  "10uF",     "Capacitor_SMD", "C_0805_2012Metric",                             36.0, 17.0, 270),
    ("J3",  "SORTIE",   "Connector_PinHeader_2.54mm", "PinHeader_1x02_P2.54mm_Vertical",  33.0, 22.0,  90),
    ("J2",  "BATTERIE", "Connector_PinHeader_2.54mm", "PinHeader_1x02_P2.54mm_Vertical",  41.0, 22.0,  90),
]

BOARD_W, BOARD_H = 46.0, 26.0

# ------------------------------------------------------------------- reseau
# net -> [(ref, pad), ...]
NETS = {
    "VIN":   [("J1", "1"), ("R3", "1")],
    "VCC":   [("R3", "2"), ("C1", "1"), ("U1", "4"), ("U1", "8"), ("D2", "2"), ("D1", "2")],
    "GND":   [("J1", "2"), ("C1", "2"), ("U1", "1"), ("U1", "3"), ("R4", "2"),
              ("C2", "2"), ("J2", "2"), ("J3", "2")],
    "VBAT":  [("U1", "5"), ("C2", "1"), ("J2", "1"), ("J3", "1")],
    "PROG":  [("U1", "2"), ("R4", "1")],
    "CHRG":  [("U1", "7"), ("R2", "2")],
    "STDBY": [("U1", "6"), ("R1", "2")],
    "nD1":   [("D1", "1"), ("R1", "1")],
    "nD2":   [("D2", "1"), ("R2", "1")],
}

# routage : net -> [[(x1,y1),(x2,y2),...], ...]  (polylignes, face avant)
ROUTES = {
    "VIN":   [[(4.0, 12.0), (4.0, 9.96), (12.0, 9.96)]],
    "VCC":   [[(12.0, 4.04), (12.0, 2.0)],
              [(2.0, 2.0), (34.0, 2.0)],
              [(29.0, 5.56), (29.0, 2.0)],
              [(34.0, 5.56), (34.0, 2.0)],
              [(22.475, 11.095), (24.0, 11.095)],
              [(24.0, 11.095), (24.0, 2.0)],
              [(14.5, 16.94), (14.5, 22.0)],
              [(17.525, 14.905), (17.525, 22.0)],
              [(17.525, 22.0), (2.0, 22.0), (2.0, 2.0)]],
    "PROG":  [[(17.525, 12.365), (12.5, 12.365), (12.5, 20.913), (10.5, 20.913)]],
    "VBAT":  [[(22.475, 14.905), (36.0, 14.905)],
              [(36.0, 14.905), (36.0, 16.06)],
              [(36.0, 14.905), (39.0, 14.905), (39.0, 20.5)],
              [(39.0, 20.5), (41.0, 20.5), (41.0, 22.0)],
              [(39.0, 20.5), (33.0, 20.5), (33.0, 22.0)]],
    "CHRG":  [[(22.475, 12.365), (31.0, 12.365), (31.0, 10.5), (29.94, 10.5)]],
    "nD2":   [[(29.0, 7.438), (29.0, 8.0), (27.5, 8.0), (27.5, 10.5), (28.06, 10.5)]],
    "STDBY": [[(22.475, 13.635), (35.8, 13.635), (35.8, 10.5), (34.94, 10.5)]],
    "nD1":   [[(34.0, 7.438), (34.0, 8.0), (32.5, 8.0), (32.5, 10.5), (33.06, 10.5)]],
}

# masse : chaque pastille GND -> un via ; le reseau se termine sur la face ARRIERE
B_ROUTES = [
    [(6.54, 14.5), (6.54, 17.2), (10.5, 17.2)],
    [(10.5, 17.2), (13.5, 17.2), (13.5, 13.635)],
    [(13.5, 13.635), (13.5, 9.0), (17.525, 9.0)],
    [(17.525, 9.0), (17.525, 5.0), (38.5, 5.0), (38.5, 17.94), (37.6, 17.94)],
    [(37.6, 17.94), (37.6, 24.2), (43.54, 24.2), (43.54, 23.4)],
    [(37.6, 24.2), (35.54, 24.2), (35.54, 23.4)],
]
GND_LINKS = [
    ((6.54, 12.0),     (6.54, 14.5)),    # J1.2
    ((14.5, 15.06),    (14.5, 13.635), False),  # C1.2 : rejoint la piste GND de U1.3 (pas de via)
    ((17.525, 11.095), (17.525, 9.0)),   # U1.1 TEMP
    ((17.525, 13.635), (13.5, 13.635)),  # U1.3 GND
    ((10.5, 19.09),    (10.5, 17.2)),    # R4.2
    ((36.0, 17.94),    (37.6, 17.94)),   # C2.2
    ((35.54, 22.0),    (35.54, 23.4)),   # J3.2
    ((43.54, 22.0),    (43.54, 23.4)),   # J2.2
]

# --------------------------------------------------------------- construction
NOZONE = '--nozone' in sys.argv

def build(dump=False):
    board = pcbnew.BOARD()
    board.SetCopperLayerCount(2)

    # --- contour de la carte (Edge.Cuts)
    corners = [(0, 0), (BOARD_W, 0), (BOARD_W, BOARD_H), (0, BOARD_H)]
    for i in range(4):
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(V(*corners[i]))
        seg.SetEnd(V(*corners[(i + 1) % 4]))
        seg.SetLayer(pcbnew.Edge_Cuts)
        seg.SetWidth(MM(0.1))
        board.Add(seg)

    # --- nets
    netcode = {}
    for n in NETS:
        ni = pcbnew.NETINFO_ITEM(board, n)
        board.Add(ni)
        netcode[n] = ni.GetNetCode()

    # --- empreintes
    fps = {}
    for ref, val, lib, name, x, y, rot in PARTS:
        fp = pcbnew.FootprintLoad(f"{FP_DIR}/{lib}.pretty", name)
        if fp is None:
            raise SystemExit("empreinte introuvable: %s/%s" % (lib, name))
        fp.SetReference(ref)
        fp.SetValue(val)
        fp.SetPosition(V(x, y))
        if rot:
            fp.SetOrientationDegrees(rot)
        board.Add(fp)
        fps[ref] = fp

    # --- champs Reference deplacees (evite le chevauchement avec la serie de D1/D2)
    for ref, x, y in (("R2", 29.6, 12.4), ("R1", 34.6, 12.4)):
        fps[ref].Reference().SetPosition(V(x, y))

    # --- affectation des nets sur les pastilles
    for net, pads in NETS.items():
        for ref, num in pads:
            pad = fps[ref].FindPadByNumber(num)
            if pad is None:
                raise SystemExit("pastille %s.%s introuvable" % (ref, num))
            pad.SetNetCode(netcode[net])

    # --- pistes
    for net, polys in ROUTES.items():
        for poly in polys:
            for a, b in zip(poly, poly[1:]):
                t = pcbnew.PCB_TRACK(board)
                t.SetStart(V(*a))
                t.SetEnd(V(*b))
                t.SetWidth(MM(0.4))
                t.SetLayer(pcbnew.F_Cu)
                t.SetNetCode(netcode[net])
                board.Add(t)

    # --- vias de masse + liaison pastille -> via
    for link in GND_LINKS:
        a, b = link[0], link[1]
        need_via = link[2] if len(link) > 2 else True
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(V(*a)); t.SetEnd(V(*b))
        t.SetWidth(MM(0.4)); t.SetLayer(pcbnew.F_Cu)
        t.SetNetCode(netcode["GND"]); board.Add(t)
        if not need_via:
            continue
        v = pcbnew.PCB_VIA(board)
        v.SetPosition(V(*b))
        v.SetDrill(MM(0.4))
        v.SetWidth(pcbnew.F_Cu, MM(0.8)); v.SetWidth(pcbnew.B_Cu, MM(0.8))
        v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        v.SetNetCode(netcode["GND"]); board.Add(v)


    # --- masse : pistes sur la face arriere (B.Cu)
    for poly in B_ROUTES:
        for a, b in zip(poly, poly[1:]):
            t = pcbnew.PCB_TRACK(board)
            t.SetStart(V(*a)); t.SetEnd(V(*b))
            t.SetWidth(MM(0.6)); t.SetLayer(pcbnew.B_Cu)
            t.SetNetCode(netcode["GND"]); board.Add(t)

    board.BuildConnectivity()

    if dump:
        for ref, *_ in PARTS:
            fp = fps[ref]
            print(f"--- {ref} {fp.GetValue()}")
            for pad in fp.Pads():
                p = pad.GetPosition()
                print("   pad %-2s  x=%6.3f  y=%6.3f  net=%s" %
                      (pad.GetNumber(), pcbnew.ToMM(p.x), pcbnew.ToMM(p.y),
                       pad.GetNetname() or "-"))
        print("\n=== PADS PAR NET ===")
        for net, pads in NETS.items():
            lst = []
            for ref, num in pads:
                p = fps[ref].FindPadByNumber(num).GetPosition()
                lst.append("%s.%s(%.2f,%.2f)" % (ref, num, pcbnew.ToMM(p.x), pcbnew.ToMM(p.y)))
            print(f"{net:6s} " + "  ".join(lst))
        return board

    pcbnew.SaveBoard(str(BOARD_FILE), board)
    print("ecrit:", BOARD_FILE)
    return board


if __name__ == "__main__":
    build(dump="--dump" in sys.argv)
