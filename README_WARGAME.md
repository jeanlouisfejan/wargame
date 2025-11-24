# Wargame Map Viewer

Un visualiseur de cartes de wargame interactif avec système de navigation et zoom.

## Fonctionnalités

- **Menu déroulant**: Sélectionnez et chargez différentes cartes
- **Déplacement**: Cliquez et glissez avec le bouton gauche de la souris pour déplacer la carte
- **Zoom**: Utilisez la molette de la souris pour zoomer/dézoomer
- **Maps personnalisables**: Créez vos propres maps au format JSON

## Installation

1. Installer les dépendances:
```bash
pip install -r requirements.txt
```

## Utilisation

Lancez le programme:
```bash
python wargame.py
```

### Contrôles

- **Clic gauche + glisser**: Déplacer la carte
- **Molette souris haut**: Zoomer
- **Molette souris bas**: Dézoomer
- **Menu déroulant**: Charger une carte différente

## Format des cartes

Les cartes sont stockées dans le dossier `maps/` au format JSON:

```json
{
  "name": "Nom de la carte",
  "width": 20,
  "height": 15,
  "terrain": [
    ["grass", "forest", "water", ...],
    ["mountain", "desert", "plains", ...],
    ...
  ]
}
```

### Types de terrain disponibles

- `grass`: Herbe (vert)
- `water`: Eau (bleu)
- `mountain`: Montagne (gris)
- `forest`: Forêt (vert foncé)
- `desert`: Désert (beige)
- `plains`: Plaines (vert clair)

## Maps par défaut

Le programme crée automatiquement 3 cartes d'exemple:
1. **Plaines et Forêts**: Terrain mixte de plaines et forêts
2. **Île Centrale**: Une île montagneuse entourée d'eau
3. **Désert et Oasis**: Désert avec une oasis au centre

## Créer vos propres cartes

Créez un fichier JSON dans le dossier `maps/` en suivant le format ci-dessus. Le fichier sera automatiquement détecté au lancement du programme.
