import sys
import pygame

from settings import Settings
from ship import Ship

class InwazjaObcych:
    """Ogolna klasa przeznaczona do zarzadzania zasobami i sposobem dzialania gry"""

    def __init__(self):
        """Inicjalizacja gry i utworzenie jej zasobow"""

        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Inwazja obcych')

        self.ship = Ship(self)

    def run_game(self):
        """Rozpoczecie petli glownej gry"""

        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        """Relacja na zdarzenia generowane przez klawiature i mysz."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _update_screen(self):
        """Uaktualnienie obrazow na ekranie i przejscie do nowego ekranu."""

        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # Wyswietlenie ostatnio zmodyfikowanego ekranu.
        pygame.display.flip()

if __name__ == '__main__':
    # Utworzenie egzemplarza gry i jej uruchomienie.
    ai = InwazjaObcych()
    ai.run_game()