# 📘 PROGRAMME — RATISS Academy

## 1. Point de départ réel (03/11/2026)

- Niveau électro : **débutant**, la loi d'Ohm connue, **aucun montage réalisé**.
- Matériel : fer à souder, étain, tournevis, petit outillage. **Multimètre en cours d'acquisition
  (« cette semaine »)**. Breadboard : à acheter.
- Atelier : réparation d'appareils divers (consoles, téléphones, équipements), maître expérimenté,
  Avenue Kennedy. Disponibilité libre.
- Ordinateur sous **Windows** + connexion fibre à domicile.
- Objectif final : **autonomie technique totale du laboratoire RATISS**, pas seulement la réparation.

## 2. Les niveaux de progression

| Niveau | Compétence attendue | Preuve exigée |
|---|---|---|
| **Apprenant** | Comprendre les leçons, réussir les exercices | Évaluations de leçon |
| **Technicien junior** | Réaliser les manipulations sous supervision | Validation par le maître |
| **Collaborateur technique** | Prendre en charge des réparations confiées | Réparations réussies + rigueur + sécurité |

⚠️ Suivre les cours ne donne **aucun** niveau automatique. Seul le réel valide.

## 3. Le cycle obligatoire de chaque notion

1. **Voir** — représentation visuelle, schéma, animation
2. **Comprendre** — explication intuitive, sans jargon
3. **Simuler** — manipulation virtuelle des paramètres
4. **Calculer** — la formule arrive *après* l'intuition
5. **Construire** — montage réel sur breadboard / à l'établi
6. **Mesurer** — multimètre, comparaison avec la prédiction
7. **Appliquer** — retrouver la notion sur une vraie carte électronique

Une leçon qui saute le 5 ou le 6 ne compte pas.

## 4. Ordre des leçons — pilier ÉLECTRONIQUE

| # | Leçon | Statut | Prérequis |
|---|---|---|---|
| 001 | Tension, courant, résistance | ✅ v1.0 | aucun |
| 002 | Circuit ouvert / fermé + continuité (diagnostic au multimètre) | ⬜ après 1ʳᵉ séance d'atelier | 001 |
| 003 | La résistance : code couleur, valeurs E12, puissance | ⬜ | 001 |
| 004 | Chute de tension & diviseur de tension | ⬜ | 001, 003 |
| 005 | L'électron pour de vrai (et pourquoi l'image de l'eau s'arrête là) | ⬜ | 004 |
| 006 | Le condensateur : le temps entre dans le circuit | ⬜ | 005 |
| 007 | La diode et la LED | ⬜ | 004 |
| 008 | Le transistor comme interrupteur | ⬜ | 007 |
| 009 | Les alimentations : régulateurs, 7805, DC-DC | ⬜ | 006, 008 |
| 010 | Lire une vraie carte : identification de composants | ⬜ | 003 → 009 |
| 011 | Diagnostic méthodique de panne | ⬜ | 010 |
| 012 | Soudure et dessoudage | ⬜ | 011 |

## 5. Pilier ANGLAIS — dépôt séparé

**Décision du 03/11/2026 :** l'anglais est une **vraie formation en anglais** (sons, grammaire,
conversation) et il vit dans son **propre dépôt** : **`RATISS-ENGLISH`**.
Il ne se mélange pas à l'électronique.

- Programme complet : `RATISS-ENGLISH/PROGRAMME.md`
- Première leçon prête : `RATISS-ENGLISH/01-NIVEAU-0/E01-hello-alphabet-sons/index.html`
- Ici, seul le **vocabulaire du travail** est conservé : `GLOSSAIRE-METIER.md` (pas un cours).

## 6. Pilier C puis C++

Démarre quand une notion électro se calcule naturellement (leçon 003, code couleur → petit programme).

| # | Leçon | Lien électro |
|---|---|---|
| C01 | Qu'est-ce que programmer ? Un programme = une suite d'ordres | — |
| C02 | Structure d'un programme C, compilation sous Windows | — |
| C03 | Variables et types (`int`, `float`) | tension, courant = nombres |
| C04 | Opérations et calculs | **U = R × I** en C |
| C05 | Conditions (`if`) | « si U < 2 V alors la LED est éteinte » |
| C06 | Boucles (`for`, `while`) | mesurer 10 fois, moyenner |
| C07 | Fonctions | `float courant(float u, float r)` |
| C08 | Tableaux et structures | série de mesures |
| C09 | Pointeurs (le vrai saut) | registres du microcontrôleur |
| C10 | C++ : classes, objets | un capteur = un objet |

## 7. Pilier KiCad

Installation un soir, étude plus tard.

| # | Étape |
|---|---|
| K01 | Installer KiCad sur Windows, comprendre l'interface |
| K02 | Premier schéma : la résistance et la LED de la leçon 001 |
| K03 | Symboles, empreintes, et pourquoi ce sont deux choses différentes |
| K04 | Du schéma au circuit imprimé (routage simple) |
| K05 | Vérification des règles de conception (DRC) |
| K06 | Fabriquer : fichiers Gerber, options de commande |

⚠️ KiCad conçoit, il ne valide pas. Un PCB non fabriqué et non testé n'est **pas** une preuve.

## 8. Règles pédagogiques verrouillées

- Ne jamais imposer un chronomètre quand le maître répare quelque chose d'intéressant.
- Adapter les exercices aux composants **réellement disponibles** (récupération incluse).
- Toujours distinguer simulation / breadboard / PCB fabriqué.
- Ne jamais confier une réparation au-dessus du niveau validé.
- Archiver **chaque** séance d'atelier dans `journal-de-formation/journal.md`.
- Chaque leçon contient un bloc **« À enseigner à ton ami »** + son critère de validation.
