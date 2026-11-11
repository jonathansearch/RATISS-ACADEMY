#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RATISS Labs — générateur du schéma KiCad du chargeur TP4056.
Projet : RATISS-CHARGE-01
Écrit un fichier .kicad_sch valide pour KiCad 9.

Principe de câblage :
  - deux rails horizontaux : VCC (haut) et GND (bas)
  - les composants suspendus entre les rails sont raccordés par un fil vertical
  - les autres nets utilisent des ETIQUETTES (labels) : même nom = même net
C'est une méthode de schéma normale en électronique (et beaucoup plus lisible
qu'un plat de spaghettis).
"""
import re, uuid, pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "RATISS-CHARGE-01.kicad_sch"
SYMLIB = pathlib.Path("/usr/share/kicad/symbols")

def uid():
    return str(uuid.uuid4())

# ---------------------------------------------------------------- extraction
def top_symbol(libfile, name):
    """Extrait le bloc (symbol "NAME" ...) de premier niveau d'une .kicad_sym."""
    s = (SYMLIB / libfile).read_text()
    m = re.search(r'\n\t\(symbol "%s"\n' % re.escape(name), s)
    if not m:
        raise SystemExit("symbole introuvable: %s dans %s" % (name, libfile))
    i = m.start() + 1
    d = 0
    for j in range(i, len(s)):
        if s[j] == '(':
            d += 1
        elif s[j] == ')':
            d -= 1
            if d == 0:
                return s[i:j + 1]
    raise SystemExit("bloc non ferme: " + name)

def pins_of(block):
    """[(numéro, x, y, angle, type)] des broches d'un symbole."""
    out = []
    for m in re.finditer(r'\(pin\s+(\w+)\s+\w+\s*\n\s*\(at\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\)',
                         block):
        seg = block[m.start():m.start() + 900]
        num = re.search(r'\(number\s+"([^"]+)"', seg)
        out.append((num.group(1) if num else "?",
                    float(m.group(2)), float(m.group(3)), float(m.group(4)), m.group(1)))
    return out

# ------------------------------------------------- symbole maison TP4056 (SOP-8)
TP4056_SYM = '''(symbol "TP4056"
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "U"
\t\t\t(at -12.7 14.605 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t)
\t\t(property "Value" "TP4056"
\t\t\t(at 2.54 14.605 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t)
\t\t(property "Footprint" "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
\t\t\t(at 0 -17.78 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Datasheet" "https://datasheet.lcsc.com/Icsc/1809261820_TOPPOWER-Nanjing-Extension-Microelectronics-TP4056-42-ESOP8_C16581.pdf"
\t\t\t(at 0 -20.32 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Description" "1A linear Li-ion/LiPo single-cell charger, 4.2V, VCC 4.0-8.0V, SOP-8"
\t\t\t(at 0 -22.86 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(symbol "TP4056_0_1"
\t\t\t(rectangle (start -10.16 12.7) (end 10.16 -12.7)
\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t(fill (type background))
\t\t\t)
\t\t)
\t\t(symbol "TP4056_1_1"
%s\t\t)
\t)
'''

def tp_pin(num, name, etype, x, y, ang):
    return ('\t\t\t(pin %s line\n'
            '\t\t\t\t(at %s %s %s)\n'
            '\t\t\t\t(length 2.54)\n'
            '\t\t\t\t(name "%s"\n'
            '\t\t\t\t\t(effects (font (size 1.27 1.27)))\n'
            '\t\t\t\t)\n'
            '\t\t\t\t(number "%s"\n'
            '\t\t\t\t\t(effects (font (size 1.27 1.27)))\n'
            '\t\t\t\t)\n'
            '\t\t\t)\n') % (etype, x, y, ang, name, num)

PIN_LIST = [
    tp_pin("4", "VCC",  "power_in",      0,    15.24, 270),
    tp_pin("3", "GND",  "power_in",      0,   -15.24,  90),
    tp_pin("8", "CE",   "input",       -12.7,   7.62,   0),
    tp_pin("1", "TEMP", "input",       -12.7,   0,      0),
    tp_pin("2", "PROG", "passive",     -12.7,  -7.62,   0),
    tp_pin("7", "CHRG", "open_collector", 12.7,  7.62, 180),
    tp_pin("6", "STDBY","open_collector", 12.7,  0,    180),
    tp_pin("5", "BAT",  "power_out",    12.7,  -7.62, 180),
]
TP4056_SYM = TP4056_SYM % "".join(PIN_LIST)

# ---------------------------------------------------------------- composants
LIBS = {
    "Device":     "Device.kicad_sym",
    "Connector":  "Connector.kicad_sym",
    "power":      "power.kicad_sym",
}
BLOCKS = {}
for nick, f in LIBS.items():
    for nm in {"Device": ["R", "C", "LED"],
               "Connector": ["Conn_01x02_Pin"],
               "power": ["GND", "+5V", "PWR_FLAG"]}[nick]:
        BLOCKS["%s:%s" % (nick, nm)] = top_symbol(f, nm)

LIB_SYMBOLS = {}
for libid, blk in BLOCKS.items():
    bare = libid.split(":")[1]
    LIB_SYMBOLS[libid] = blk.replace('(symbol "%s"' % bare, '(symbol "%s"' % libid, 1)
LIB_SYMBOLS["RATISS:TP4056"] = TP4056_SYM.replace(
    '(symbol "TP4056"', '(symbol "RATISS:TP4056"', 1)

PINMAP = {libid: pins_of(blk) for libid, blk in BLOCKS.items()}
PINMAP["RATISS:TP4056"] = pins_of(TP4056_SYM)

# ------------------------------------------------------------- placement
# (ref, lib_id, valeur, x, y)  — Y vers le BAS
PARTS = [
    ("U1",  "RATISS:TP4056",        "TP4056",  140, 105),
    ("C1",  "Device:C",             "10µF",     80,  55),
    ("C2",  "Device:C",             "10µF",    218,  75),
    ("R1",  "Device:R",             "10k",     200,  75),
    ("R2",  "Device:R",             "10k",     170,  75),
    ("R3",  "Device:R",             "0,4Ω",     62,  50),
    ("R4",  "Device:R",             "1.2k",    110, 140),
    ("D1",  "Device:LED",           "VERTE",   200,  60),
    ("D2",  "Device:LED",           "ROUGE",   170,  60),
    ("J1",  "Connector:Conn_01x02_Pin", "ENTREE 5V", 50,  30),
    ("J2",  "Connector:Conn_01x02_Pin", "BATTERIE", 230,  60),
    ("J3",  "Connector:Conn_01x02_Pin", "SORTIE",   258,  60),
]

def snap(v):
    """Aligne sur la grille KiCad de 1,27 mm (50 mil) : evite les avertissements ERC."""
    return round(v / 1.27) * 1.27

# toutes les positions sont alignees sur la grille ; les broches le sont alors aussi
PARTS = [(r, l, v, snap(x), snap(y)) for (r, l, v, x, y) in PARTS]

FOOTPRINTS = {
    "J1": "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
    "J2": "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
    "J3": "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
    "R3": "Resistor_SMD:R_2512_6332Metric",
    "R1": "Resistor_SMD:R_0805_2012Metric",
    "R2": "Resistor_SMD:R_0805_2012Metric",
    "R4": "Resistor_SMD:R_0805_2012Metric",
    "C1": "Capacitor_SMD:C_0805_2012Metric",
    "C2": "Capacitor_SMD:C_0805_2012Metric",
    "D1": "LED_SMD:LED_0805_2012Metric",
    "D2": "LED_SMD:LED_0805_2012Metric",
    "U1": "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
}

VCC_Y = snap(40)
GND_Y = snap(165)
RAIL_X0, RAIL_X1 = snap(55), snap(240)

def pin_pos(ref, num):
    part = next(p for p in PARTS if p[0] == ref)
    _, libid, _, sx, sy = part
    for n, px, py, ang, _t in PINMAP[libid]:
        if n == num:
            return (sx + px, sy - py), ang
    raise SystemExit("broche %s introuvable sur %s" % (num, ref))

wires, junctions, labels, texts = [], [], [], []

def wire(x1, y1, x2, y2):
    wires.append(((x1, y1), (x2, y2)))

def label(nom, x, y, ang=0, just="left"):
    labels.append((nom, x, y, ang, just))

def text(t, x, y, size=1.5):
    texts.append((t, x, y, size))

# --- raccordements aux rails : on collecte d'ABORD les points de jonction,
#     parce qu'un fil ne se connecte pas au MILIEU d'un autre fil dans KiCad :
#     le rail doit etre decoupe a chaque point de raccordement.
vcc_taps, gnd_taps = [], []

def pin_xy(ref, num):
    return pin_pos(ref, num)[0]

def to_rail(ref, num, rail):
    (x, y) = pin_xy(ref, num)
    wire(x, y, x, rail)
    (vcc_taps if rail == VCC_Y else gnd_taps).append(x)

to_rail("U1", "4", VCC_Y)     # VCC de la puce
to_rail("U1", "3", GND_Y)     # GND de la puce
to_rail("C1", "1", VCC_Y)
to_rail("C1", "2", GND_Y)
to_rail("C2", "2", GND_Y)
to_rail("R4", "2", GND_Y)
to_rail("R3", "1", VCC_Y)

def rail(y, taps):
    xs = [RAIL_X0] + sorted(set(taps)) + [RAIL_X1]
    for a, b in zip(xs, xs[1:]):
        wire(a, y, b, y)
    for t in sorted(set(taps)):
        junctions.append((t, y))

rail(VCC_Y, vcc_taps)
rail(GND_Y, gnd_taps)

# PWR_FLAG : indique a l'ERC que VCC et GND sont bien alimentes.
# Sans eux, ERC signale "Input Power pin not driven by any Output Power pins".
FLAG = 240.03 + 10.16
wire(RAIL_X1, VCC_Y, FLAG, VCC_Y)
wire(RAIL_X0, GND_Y, RAIL_X0 - 10.16, GND_Y)
label("VCC", RAIL_X0, VCC_Y, 0, "right")
label("GND", RAIL_X1, GND_Y, 0, "left")

# --- etiquettes : dx/dy = direction VERS L'EXTERIEUR de la broche
def lab_at(ref, num, nom, dx=0.0, dy=0.0, just="left"):
    (x, y) = pin_xy(ref, num)
    wire(x, y, x + dx, y + dy)
    label(nom, x + dx, y + dy, 0, just)

L = 3.81
lab_at("U1", "8", "VCC",  -L, 0, "right")   # CE -> VCC (CE actif a l'etat haut)
lab_at("U1", "1", "GND",  -L, 0, "right")   # TEMP -> GND : sonde desactivee
lab_at("U1", "2", "PROG", -L, 0, "right")
lab_at("U1", "7", "CHRG",  L, 0, "left")
lab_at("U1", "6", "STDBY", L, 0, "left")
lab_at("U1", "5", "VBAT",  L, 0, "left")

lab_at("R3", "2", "VIN",  0,  L, "left")    # broche basse de R3
lab_at("R4", "1", "PROG", -L, 0, "right")
lab_at("C2", "1", "VBAT", L, 0, "left")

lab_at("D2", "2", "VCC",  L, 0, "left")     # anode
lab_at("D2", "1", "nD2", -L, 0, "right")    # cathode
lab_at("R2", "1", "nD2", -L, 0, "right")
lab_at("R2", "2", "CHRG", 0, L, "left")

lab_at("D1", "2", "VCC",  L, 0, "left")
lab_at("D1", "1", "nD1", -L, 0, "right")
lab_at("R1", "1", "nD1", -L, 0, "right")
lab_at("R1", "2", "STDBY", 0, L, "left")

lab_at("J1", "1", "VIN",  L, 0, "left")
lab_at("J1", "2", "GND",  L, 0, "left")
lab_at("J2", "1", "VBAT", L, 0, "left")
lab_at("J2", "2", "GND",  L, 0, "left")
lab_at("J3", "1", "VBAT", L, 0, "left")
lab_at("J3", "2", "GND",  L, 0, "left")

# --- annotations de lecture (zone libre sous la puce)
text("RATISS-CHARGE-01 — chargeur Li-ion 1 A (TP4056)", 140, 18, 2.5)
LEG = [
    "TEMP -> GND : sonde de temperature desactivee",
    "CE -> VCC : puce active",
    "R4 = Rprog : I(mA) = 1200 / R(kohm) -> 1,2k = 1 A",
    "D2 rouge = en charge  |  D1 verte = termine",
    "R3 0,4 ohm : limite le courant d'entree",
]
for k, t in enumerate(LEG):
    text(t, 152, 136 + 6 * k, 1.27)

# ------------------------------------------------------------ serialisation
def wire_s(w):
    (x1, y1), (x2, y2) = w
    return ('\t(wire\n\t\t(pts\n\t\t\t(xy %g %g) (xy %g %g)\n\t\t)\n'
            '\t\t(stroke (width 0) (type default))\n\t\t(uuid "%s")\n\t)\n'
            % (x1, y1, x2, y2, uid()))

def junc_s(p):
    return ('\t(junction\n\t\t(at %g %g)\n\t\t(diameter 0)\n\t\t(color 0 0 0 0)\n'
            '\t\t(uuid "%s")\n\t)\n' % (p[0], p[1], uid()))

def label_s(l):
    nom, x, y, ang, just = l
    return ('\t(label "%s"\n\t\t(at %g %g %g)\n\t\t(effects (font (size 1.27 1.27)) '
            '(justify %s bottom))\n\t\t(uuid "%s")\n\t)\n' % (nom, x, y, ang, just, uid()))

def text_s(t):
    s, x, y, size = t
    return ('\t(text "%s"\n\t\t(exclude_from_sim no)\n\t\t(at %g %g 0)\n'
            '\t\t(effects (font (size %g %g)))\n\t\t(uuid "%s")\n\t)\n'
            % (s.replace('"', '\\"'), x, y, size, size, uid()))

def sym_s(p, root):
    ref, libid, val, x, y = p[:5]
    flag = len(p) > 5 and p[5] == "power"
    # placement des champs selon le type (evite les chevauchements)
    if libid == "RATISS:TP4056":
        rx, vx, fy, jr, jv = -13.97, 13.97, -17.78, "right", "left"
    elif libid.startswith("Device:LED"):
        rx, vx, fy, jr, jv = -7.62, 7.62, -5.08, "right", "left"
    elif libid.startswith("Connector"):
        rx, vx, fy, jr, jv = -6.35, 6.35, -5.08, "right", "left"
    elif libid.startswith("power:"):
        rx, vx, fy, jr, jv = 0.0, 0.0, -3.81, "center", "center"
    else:
        rx, vx, fy, jr, jv = -5.08, 5.08, -7.62, "right", "left"
    props = [
        ("Reference", ref, x + rx, y + fy, jr, False),
        ("Value",     val, x + vx, y + fy, jv, libid.startswith("power:")),
        ("Footprint", FOOTPRINTS.get(ref, ""), x, y - fy, "center", True),
        ("Datasheet", "",  x, y - fy - 2.54, "center", True),
    ]
    body = ['\t(symbol\n\t\t(lib_id "%s")\n\t\t(at %g %g 0)\n\t\t(unit 1)\n'
            '\t\t(exclude_from_sim no)\n\t\t(in_bom %s)\n\t\t(on_board %s)\n'
            '\t\t(dnp no)\n' % (libid, x, y,
                                 "no" if flag else "yes", "no" if flag else "yes")]
    for i, (k, v, px, py, just, hide) in enumerate(props):
        body.append('\t\t(property "%s" "%s"\n\t\t\t(at %g %g 0)\n'
                    '\t\t\t(effects (font (size 1.27 1.27))%s%s)\n\t\t)\n'
                    % (k, v, px, py,
                       '' if just == "center" else ' (justify %s)' % just,
                       ' (hide yes)' if hide else ''))
    for n, _px, _py, _a, _t in PINMAP[libid]:
        body.append('\t\t(pin "%s"\n\t\t\t(uuid "%s")\n\t\t)\n' % (n, uid()))
    body.append('\t\t(instances\n\t\t\t(project "RATISS-CHARGE-01"\n'
                '\t\t\t\t(path "/%s"\n\t\t\t\t\t(reference "%s")\n\t\t\t\t\t(unit 1)\n'
                '\t\t\t\t)\n\t\t\t)\n\t\t)\n' % (root, ref))
    body.append('\t)\n')
    return "".join(body)

root = uid()
parts = ['(kicad_sch\n\t(version 20250114)\n\t(generator "eeschema")\n'
         '\t(generator_version "9.0")\n\t(uuid "%s")\n\t(paper "A4")\n' % root]
parts.append('\t(title_block\n\t\t(title "RATISS-CHARGE-01 — Chargeur Li-ion TP4056 1 A")\n'
             '\t\t(date "2026-11-03")\n\t\t(rev "1.0")\n'
             '\t\t(company "RATISS Labs — Yaoundé")\n'
             '\t\t(comment 1 "Carte d\'exercice — simple face, sans via")\n'
             '\t\t(comment 2 "Sans protection batterie : ne pas laisser sans surveillance")\n\t)\n')
parts.append('\t(lib_symbols\n')
for libid in sorted(LIB_SYMBOLS):
    blk = LIB_SYMBOLS[libid]
    parts.append("\n".join("\t" + ln for ln in blk.split("\n")) + "\n")
parts.append('\t)\n')
parts += [junc_s(p) for p in junctions]
parts += [wire_s(w) for w in wires]
parts += [text_s(t) for t in texts]
parts += [label_s(l) for l in labels]
parts += [sym_s(p, root) for p in PARTS]
parts.append(sym_s(("#FLG1", "power:PWR_FLAG", "PWR_FLAG", FLAG, VCC_Y, "power"), root))
parts.append(sym_s(("#FLG2", "power:PWR_FLAG", "PWR_FLAG", RAIL_X0 - 10.16, GND_Y, "power"), root))
parts.append('\t(sheet_instances\n\t\t(path "/"\n\t\t\t(page "1")\n\t\t)\n\t)\n')
parts.append('\t(embedded_fonts no)\n)\n')

OUT.write_text("".join(parts))
print("ecrit:", OUT, "|", len("".join(parts)) // 1024, "Ko |", len(PARTS), "composants")
