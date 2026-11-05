# 💻 Pilier PROGRAMMATION — logique, puis C, puis C++

> **Décision du chef (03/11/2026) :** **pas de Python.**
> On apprend **les bases logiques**, puis C et C++ — uniquement ce qui sert à lire,
> écrire, corriger et **vérifier** du code. Pas de parcours encyclopédique.

## Pourquoi ce choix
- Objectif = systèmes embarqués et microcontrôleurs (ESP32, Pico), pas du scripting.
- C / C++ sont les langages du matériel. On va à l'essentiel.
- Toute production est encadrée par **RATISS Framework** (audit exécutable, traçabilité,
  reproductibilité) — le code n'est pas « correct » parce qu'une IA l'affirme.

## Programme
| # | Étape | Lien avec l'électronique |
|---|---|---|
| L0 | **Logique** : 0/1, AND, OR, NOT, XOR, tables de vérité | ✅ fait — leçon électro 003 |
| C01 | Un programme = une suite d'ordres · compiler sous Windows | — |
| C02 | Variables et types (`int`, `float`, `char`) | U, I, R sont des nombres |
| C03 | Opérateurs et calculs | **U = R × I** en C |
| C04 | Conditions `if / else` | « si U < 2 V → LED éteinte » |
| C05 | Boucles `for`, `while` | moyenner 10 mesures |
| C06 | Fonctions | `float courant(float u, float r)` |
| C07 | Tableaux | une série de mesures |
| C08 | Pointeurs et mémoire | registres d'un microcontrôleur |
| C09 | Structures | un capteur = une structure |
| C10 | C++ : classes et objets | un capteur = un objet |

⚠️ On n'apprend pas **tout** le langage. On apprend ce qui permet de **comprendre, écrire,
corriger et vérifier**. Le reste se cherche sur Google quand le besoin arrive.
