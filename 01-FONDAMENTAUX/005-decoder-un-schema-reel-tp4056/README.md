# Leçon 005 — Décoder un vrai schéma : le chargeur TP4056

| Champ | Valeur |
|---|---|
| Fichier | `index.html` (autonome, hors-ligne, images intégrées) |
| Version | 1.0 |
| Date | 03/11/2026 |
| Niveau | après la leçon 001 |
| Durée | 35 min |
| Support | schéma réel du module de charge Li-ion TP4056 |

## Objectifs
1. Lire un schéma réel sans se perdre : repérer masse → entrée → sortie.
2. Identifier les **10 objets** du schéma et leur **effet sur les autres** (pas juste leur fonction).
3. Passer du **dessin** au **graphe** : 6 nœuds, 10 arêtes.
4. Appliquer le contrôle négatif : « et si je l'enlève ? ».
5. Calculer le courant de charge avec Rprog : `I(mA) = 1200 / Rprog(kΩ)`.
6. Repérer les **imperfections d'un schéma trouvé en ligne**.

## Contenu visuel
- Schéma source + version **annotée** (10 repères numérotés)
- **Graphe du circuit** dessiné en SVG (nœuds / arêtes, sans géométrie)
- Tableau composant → rôle → effet
- Tableau « j'enlève X → il se passe Y »
- 3 mesures à faire sur un vrai module

## Points d'honnêteté
- Le schéma source dessine D1/D2 comme des diodes simples (ce sont des LED).
- Il utilise 10 kΩ pour les LED (≈ 0,3 mA) au lieu du 1 kΩ typique.
- Il annonce 4–8 V en entrée, alors que le module réel est prévu pour 5 V USB.

## Sécurité
Batterie Li-ion : jamais de court-circuit, jamais d'accu gonflé/chaud, jamais inversé.
Mesures avec le maître, sur un accu sain, sous surveillance.
