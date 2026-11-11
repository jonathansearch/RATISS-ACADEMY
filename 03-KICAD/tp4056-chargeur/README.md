# RATISS-CHARGE-01 — Chargeur Li-ion TP4056 1 A

Projet KiCad 9 complet du chargeur étudié dans la **leçon 005**.
C'est une **carte d'exercice** : elle sert à apprendre à dessiner un PCB, pas à
remplacer un module TP4056 du marché (qui coûte ~1 000 F).

```
RATISS-CHARGE-01.kicad_pro   projet KiCad
RATISS-CHARGE-01.kicad_sch   schéma
RATISS-CHARGE-01.kicad_pcb   carte (routée)
RATISS.kicad_sym             symbole TP4056 maison (SOP-8, 8 broches)
sym-lib-table / fp-lib-table bibliothèques du projet
tools/gen_sch.py             script qui génère le schéma
tools/gen_pcb.py             script qui génère la carte
exports/                     PDF, PNG, Gerbers, perçage, BOM, netlist
```

## État vérifié (03/11/2026)

| Contrôle | Résultat |
|---|---|
| ERC (schéma) | **0 erreur** — 12 avertissements `lib_symbol_issues` dus à l'environnement de ligne de commande (bibliothèques globales non déclarées), sans effet électrique |
| DRC (carte) | **0 violation** |
| Netlist | 9 nets, tous conformes à la leçon 005 |
| Gerbers + perçage | générés dans `exports/gerbers/` |
| Rendu | `exports/carte-rendu.png`, `exports/schema-rendu.png`, PDF |

## Les 12 pièces

| Réf | Valeur | Empreinte |
|---|---|---|
| U1 | TP4056 | SOIC-8 3,9 × 4,9 mm, pas 1,27 mm |
| R3 | **0,4 Ω** | 2512 (1 W) — voir ci-dessous |
| R1, R2 | 10 kΩ | 0805 |
| R4 (Rprog) | **1,2 kΩ** | 0805 → I = 1200 / 1,2 = **1 000 mA** |
| C1, C2 | 10 µF | 0805 |
| D1 | LED verte « terminé » | 0805 |
| D2 | LED rouge « en charge » | 0805 |
| J1 | entrée 5 V (VIN, GND) | barrette 2,54 mm, 2 broches |
| J2 | batterie (VBAT, GND) | barrette 2,54 mm, 2 broches |
| J3 | sortie (= batterie) | barrette 2,54 mm, 2 broches |

## Câblage (conforme à la fiche technique Toppower)

| Broche TP4056 | Net | Pourquoi |
|---|---|---|
| 4 VCC | VCC | alimentation, via R3 |
| 8 CE | VCC | **CE actif à l'état haut** : à VCC, la puce travaille |
| 1 TEMP | GND | TEMP à la masse = **surveillance de température désactivée** |
| 3 GND | GND | masse |
| 2 PROG | PROG → R4 → GND | fixe le courant de charge |
| 7 CHRG | → R2 → D2 → VCC | LED rouge quand la charge est en cours |
| 6 STDBY | → R1 → D1 → VCC | LED verte quand c'est terminé |
| 5 BAT | VBAT | batterie + C2 10 µF |

## Décisions de conception

1. **R3 en 2512 et non en 1206.** À 1 A, R3 dissipe `I²·R = 1² × 0,4 = 0,4 W`.
   Un 1206 (0,25 W) chauffe. Le 2512 (1 W) a de la marge. Les modules du marché
   utilisent souvent un 1206 : c'est un de leurs points faibles.
2. **2 faces, et non 1.** Toute la logique est sur la face avant ; **la masse est
   routée sur la face arrière**, rejointe par un via à chaque pastille GND
   (8 pastilles). Une carte simple face était possible mais demandait des straps
   (fils de saut) : moins fiable, plus penible à vérifier.
3. **Pas de protection batterie.** Un vrai module TP4056 embarque en plus un
   DW01A + FS8205A (protection contre surcharge, surdécharge, court-circuit).
   **Cette carte n'en a pas.** La broche J3 « SORTIE » n'est qu'une copie de la
   batterie. Ne jamais laisser un accu Li-ion branché sans surveillance.
4. **Entrée par barrette 2,54 mm** et non par connecteur USB : plus facile à
   récupérer et à souder pour un débutant.

## Limites honnêtes

- La carte **n'a pas été fabriquée**. Elle est validée par ERC + DRC, ce qui
  garantit la cohérence logique et les règles de dessin, **pas** le
  fonctionnement physique.
- Le rendu et les Gerbers ont été produits par KiCad 9.0.2. Aucun contrôle
  humain dans l'éditeur graphique n'a été fait : le projet a été généré par
  script (`tools/gen_pcb.py`).
- Aucun test en simulation électrique (pas de SPICE) : les valeurs viennent de
  la fiche technique, pas d'un calcul de comportement.

## Régénérer

```bash
sudo apt install kicad kicad-symbols kicad-footprints
/usr/bin/python3 tools/gen_sch.py     # schéma
/usr/bin/python3 tools/gen_pcb.py     # carte
kicad-cli sch erc RATISS-CHARGE-01.kicad_sch
kicad-cli pcb drc RATISS-CHARGE-01.kicad_pcb
```

## Sécurité

Li-ion : jamais d'accu gonflé, chaud ou percé. Jamais de court-circuit.
Charge sous surveillance. En cas de doute : demander au maître d'atelier.
