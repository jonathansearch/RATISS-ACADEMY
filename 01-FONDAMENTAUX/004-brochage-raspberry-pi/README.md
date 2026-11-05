# Fiche 004 — Brochage du Raspberry Pi (40 broches)

| Champ | Valeur |
|---|---|
| Fichier | `index.html` (autonome, hors-ligne) |
| Version | 1.0 |
| Date | 03/11/2026 |
| Modèles | B+ · 2 · 3 · 4 · 5 · Zero (connecteur identique) |
| Type | **fiche de référence**, pas une leçon progressive |

## Contenu
- Connecteur 40 broches interactif : **clique sur un pin** → nom BCM, type, fonctions.
- **Code couleur pédagogique** : 5 V (rouge) · 3,3 V (orange) · GND (gris foncé) · GPIO (vert) ·
  I²C (bleu) · SPI (violet) · UART (jaune) · PWM (rose) · ID/EEPROM (gris clair).
- Tableau complet des 40 pins.
- Le piège **numéro physique ≠ BCM** (GPIO17 = pin 11, pas pin 17).
- Les 5 groupes à connaître : 5 V, 3,3 V, GND, I²C, SPI.
- Sécurité électrique : 3,3 V max sur un GPIO, courant très faible.
- Exemple de câblage : LED sur GPIO17 (pin 11) + 330 Ω + GND (pin 9).
- Note Raspberry Pi 5 (RP1, fonctions alternatives déplacées).

## Honnêteté
Les couleurs sont une **convention pédagogique**, pas un standard : c'est le **numéro** et le **nom BCM** qui font foi.
Brochage recoupé sur plusieurs sources publiques.

## À retenir
- Pin 1 = **pad carré**.
- Un GPIO = **3,3 V maximum**, quelques mA seulement.
- I²C (pins 3/5) = le bus de RATISS-GRID (INA219 + OLED SSD1306).
