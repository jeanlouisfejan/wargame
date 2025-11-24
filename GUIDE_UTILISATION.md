# Guide d'Utilisation - Wargame Map Viewer

## Installation Rapide

Aucune installation nécessaire ! Python est déjà installé sur votre système.

## Lancement

### Option 1: Double-clic (Windows)
Double-cliquez sur `lancer_wargame.bat`

### Option 2: Ligne de commande
```bash
python wargame_tkinter.py
```

## Interface

L'application se compose de 3 parties:

1. **En-tête**: Titre et contrôles
2. **Menu déroulant**: Sélection de la carte
3. **Zone de visualisation**: Affichage de la carte

## Commandes

### Navigation
- **Déplacer la carte**: Cliquez avec le bouton gauche et glissez
- **Zoomer**: Tournez la molette de la souris vers le haut
- **Dézoomer**: Tournez la molette de la souris vers le bas

### Changer de carte
1. Cliquez sur le menu déroulant "Sélectionner une carte"
2. Choisissez une carte dans la liste
3. La carte se charge automatiquement

## Cartes Disponibles

Le programme crée automatiquement 4 cartes d'exemple:

### 1. Plaines et Forêts
- Taille: 20x15
- Terrain mixte alternant plaines vertes et forêts denses
- Idéal pour les batailles de moyenne envergure

### 2. Île Centrale
- Taille: 20x15
- Une île montagneuse au centre, entourée d'eau
- Parfait pour les scénarios de défense insulaire

### 3. Désert et Oasis
- Taille: 20x15
- Vaste désert avec une oasis au centre
- Bon pour les batailles de contrôle de ressources

### 4. Grande Bataille
- Taille: 40x30
- Grande carte avec rivière centrale, montagnes au nord, désert au sud
- Idéal pour les grandes batailles stratégiques

## Types de Terrain

| Terrain | Couleur | Description |
|---------|---------|-------------|
| Plaines (plains) | Vert clair | Terrain ouvert, facile à traverser |
| Herbe (grass) | Vert | Terrain standard |
| Forêt (forest) | Vert foncé | Terrain difficile, couverture |
| Montagne (mountain) | Gris | Terrain élevé, difficile |
| Eau (water) | Bleu | Infranchissable ou lent |
| Désert (desert) | Beige | Terrain ouvert, chaud |

## Créer Vos Propres Cartes

1. Créez un fichier `.json` dans le dossier `maps/`
2. Utilisez ce format:

```json
{
  "name": "Ma Carte Personnalisée",
  "width": 25,
  "height": 20,
  "terrain": [
    ["grass", "forest", "water", ...],
    ["mountain", "desert", "plains", ...],
    ...
  ]
}
```

3. Relancez le programme
4. Votre carte apparaîtra dans le menu déroulant

## Astuces

- **Centrer la vue**: Zoomez/dézoomez pour réinitialiser
- **Explorer une grande carte**: Utilisez le zoom minimum (0.3x) pour voir l'ensemble
- **Détails**: Utilisez le zoom maximum (3.0x) pour voir les détails
- **Navigation rapide**: Déplacez rapidement avec de grands mouvements de souris

## Résolution de Problèmes

### La fenêtre ne s'ouvre pas
- Vérifiez que Python est installé: `python --version`
- Vérifiez que tkinter est disponible: `python -c "import tkinter"`

### La carte ne se charge pas
- Vérifiez que le fichier JSON est valide
- Vérifiez que le dossier `maps/` existe
- Consultez les messages d'erreur dans la console

### Performance lente
- Réduisez la taille de la carte dans le fichier JSON
- Utilisez moins de zoom sur les grandes cartes

## Développement Futur

Fonctionnalités possibles:
- Ajout d'unités militaires
- Déplacement d'unités
- Calcul de portée et de mouvement
- Sauvegarde de positions
- Mode multijoueur

## Contact et Support

Pour signaler un bug ou proposer une amélioration:
1. Notez le message d'erreur exact
2. Décrivez les étapes pour reproduire le problème
3. Indiquez votre version de Python

Bonne stratégie!
