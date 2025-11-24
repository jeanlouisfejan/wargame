import pygame
import pygame_gui
import json
import os
from pathlib import Path

class WargameMap:
    """Représente une carte de wargame"""
    def __init__(self, name, width, height, terrain_data):
        self.name = name
        self.width = width
        self.height = height
        self.terrain_data = terrain_data
        self.surface = None

    def generate_surface(self, tile_size=50):
        """Génère la surface visuelle de la carte"""
        self.surface = pygame.Surface((self.width * tile_size, self.height * tile_size))

        # Couleurs pour différents types de terrain
        terrain_colors = {
            'grass': (34, 139, 34),
            'water': (0, 119, 190),
            'mountain': (139, 137, 137),
            'forest': (0, 100, 0),
            'desert': (237, 201, 175),
            'plains': (144, 238, 144)
        }

        for y in range(self.height):
            for x in range(self.width):
                terrain_type = self.terrain_data[y][x]
                color = terrain_colors.get(terrain_type, (255, 255, 255))

                pygame.draw.rect(self.surface, color,
                               (x * tile_size, y * tile_size, tile_size, tile_size))
                pygame.draw.rect(self.surface, (0, 0, 0),
                               (x * tile_size, y * tile_size, tile_size, tile_size), 1)

        return self.surface


class WargameViewer:
    """Visualiseur de carte de wargame avec pan et zoom"""
    def __init__(self):
        pygame.init()

        # Configuration de la fenêtre
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Wargame Map Viewer")

        # Gestionnaire d'interface
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height))

        # Variables de pan (déplacement)
        self.pan_x = 0
        self.pan_y = 0
        self.is_panning = False
        self.last_mouse_pos = (0, 0)

        # Variables de zoom
        self.zoom_level = 1.0
        self.min_zoom = 0.3
        self.max_zoom = 3.0

        # Carte actuelle
        self.current_map = None
        self.map_surface = None
        self.scaled_surface = None

        # Liste des maps disponibles
        self.available_maps = self.load_available_maps()

        # Créer le menu déroulant
        self.create_ui()

        # Clock pour le framerate
        self.clock = pygame.time.Clock()
        self.running = True

    def load_available_maps(self):
        """Charge la liste des maps disponibles"""
        maps_dir = Path("maps")
        maps_dir.mkdir(exist_ok=True)

        available_maps = []
        for map_file in maps_dir.glob("*.json"):
            available_maps.append(map_file.stem)

        # Si aucune map n'existe, créer des maps par défaut
        if not available_maps:
            self.create_default_maps()
            for map_file in maps_dir.glob("*.json"):
                available_maps.append(map_file.stem)

        return available_maps if available_maps else ["Aucune map disponible"]

    def create_default_maps(self):
        """Crée des maps par défaut pour l'exemple"""
        maps_dir = Path("maps")
        maps_dir.mkdir(exist_ok=True)

        # Map 1: Plaines et forêts
        map1 = {
            "name": "Plaines et Forêts",
            "width": 20,
            "height": 15,
            "terrain": [
                ["grass" if (x + y) % 3 != 0 else "forest"
                 for x in range(20)] for y in range(15)
            ]
        }

        with open(maps_dir / "plaines_forets.json", "w") as f:
            json.dump(map1, f, indent=2)

        # Map 2: Île
        map2_terrain = []
        for y in range(15):
            row = []
            for x in range(20):
                # Créer une île au centre
                dist_from_center = ((x - 10) ** 2 + (y - 7.5) ** 2) ** 0.5
                if dist_from_center < 4:
                    row.append("mountain")
                elif dist_from_center < 7:
                    row.append("grass")
                else:
                    row.append("water")
            map2_terrain.append(row)

        map2 = {
            "name": "Île Centrale",
            "width": 20,
            "height": 15,
            "terrain": map2_terrain
        }

        with open(maps_dir / "ile_centrale.json", "w") as f:
            json.dump(map2, f, indent=2)

        # Map 3: Désert et oasis
        map3_terrain = []
        for y in range(15):
            row = []
            for x in range(20):
                if 8 <= x <= 12 and 6 <= y <= 9:
                    row.append("water")
                elif 7 <= x <= 13 and 5 <= y <= 10:
                    row.append("grass")
                else:
                    row.append("desert")
            map3_terrain.append(row)

        map3 = {
            "name": "Désert et Oasis",
            "width": 20,
            "height": 15,
            "terrain": map3_terrain
        }

        with open(maps_dir / "desert_oasis.json", "w") as f:
            json.dump(map3, f, indent=2)

    def create_ui(self):
        """Crée l'interface utilisateur"""
        # Menu déroulant pour sélectionner la map
        self.map_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self.available_maps,
            starting_option=self.available_maps[0] if self.available_maps else "Aucune map",
            relative_rect=pygame.Rect((10, 10), (250, 40)),
            manager=self.manager
        )

        # Texte d'instructions
        instructions_text = (
            "Clic gauche + glisser: Déplacer la carte | "
            "Molette: Zoom/Dézoom | "
            f"Zoom: {self.zoom_level:.2f}x"
        )

        self.instructions_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 60), (800, 30)),
            text=instructions_text,
            manager=self.manager
        )

    def load_map(self, map_name):
        """Charge une map depuis un fichier JSON"""
        map_path = Path("maps") / f"{map_name}.json"

        if not map_path.exists():
            print(f"La map {map_name} n'existe pas")
            return

        try:
            with open(map_path, "r") as f:
                map_data = json.load(f)

            self.current_map = WargameMap(
                name=map_data["name"],
                width=map_data["width"],
                height=map_data["height"],
                terrain_data=map_data["terrain"]
            )

            # Générer la surface de la carte
            self.map_surface = self.current_map.generate_surface()
            self.update_scaled_surface()

            # Centrer la carte
            self.pan_x = (self.screen_width - self.map_surface.get_width() * self.zoom_level) // 2
            self.pan_y = (self.screen_height - self.map_surface.get_height() * self.zoom_level) // 2

            print(f"Map '{map_data['name']}' chargée avec succès!")

        except Exception as e:
            print(f"Erreur lors du chargement de la map: {e}")

    def update_scaled_surface(self):
        """Met à jour la surface zoomée de la carte"""
        if self.map_surface:
            new_width = int(self.map_surface.get_width() * self.zoom_level)
            new_height = int(self.map_surface.get_height() * self.zoom_level)
            self.scaled_surface = pygame.transform.scale(
                self.map_surface,
                (new_width, new_height)
            )

    def handle_events(self):
        """Gère les événements"""
        time_delta = self.clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Gestion du menu déroulant
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.map_dropdown:
                    selected_map = event.text
                    self.load_map(selected_map)

            # Gestion du pan (déplacement avec la souris)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    self.is_panning = True
                    self.last_mouse_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.is_panning = False

            if event.type == pygame.MOUSEMOTION:
                if self.is_panning:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.pan_x += dx
                    self.pan_y += dy
                    self.last_mouse_pos = event.pos

            # Gestion du zoom avec la molette
            if event.type == pygame.MOUSEWHEEL:
                # Position de la souris
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Calculer la position relative à la carte avant le zoom
                if self.map_surface:
                    old_zoom = self.zoom_level

                    # Ajuster le zoom
                    if event.y > 0:  # Molette vers le haut = zoom in
                        self.zoom_level = min(self.zoom_level * 1.1, self.max_zoom)
                    else:  # Molette vers le bas = zoom out
                        self.zoom_level = max(self.zoom_level / 1.1, self.min_zoom)

                    # Mettre à jour la surface
                    self.update_scaled_surface()

                    # Ajuster le pan pour zoomer vers la position de la souris
                    zoom_ratio = self.zoom_level / old_zoom
                    self.pan_x = mouse_x - (mouse_x - self.pan_x) * zoom_ratio
                    self.pan_y = mouse_y - (mouse_y - self.pan_y) * zoom_ratio

                    # Mettre à jour le label d'instructions
                    instructions_text = (
                        "Clic gauche + glisser: Déplacer la carte | "
                        "Molette: Zoom/Dézoom | "
                        f"Zoom: {self.zoom_level:.2f}x"
                    )
                    self.instructions_label.set_text(instructions_text)

            self.manager.process_events(event)

        self.manager.update(time_delta)

    def draw(self):
        """Dessine l'écran"""
        # Fond
        self.screen.fill((50, 50, 50))

        # Dessiner la carte si elle existe
        if self.scaled_surface:
            self.screen.blit(self.scaled_surface, (self.pan_x, self.pan_y))
        else:
            # Texte si aucune carte n'est chargée
            font = pygame.font.Font(None, 36)
            text = font.render("Sélectionnez une carte dans le menu", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(text, text_rect)

        # Dessiner l'interface
        self.manager.draw_ui(self.screen)

        pygame.display.flip()

    def run(self):
        """Boucle principale"""
        while self.running:
            self.handle_events()
            self.draw()

        pygame.quit()


def main():
    viewer = WargameViewer()
    viewer.run()


if __name__ == "__main__":
    main()
