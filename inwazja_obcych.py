import sys

import pygame

class InwazjaObcych:
    """Ogolna klasa przeznaczona do zarzadzania zasobami i sposobem dzialania gry"""

    def __init__(self):
        """Inicjalizacja gry i utworzenie jej zasobow"""
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption('Inwazja obcych')

        # Zdefiniowanie koloru tla.
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Rozpoczecie petli glownej gry"""
        while True:
            # Oczekiwanie na nacisniecie klawisza lub przycisku myszy
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Odswiezenie ekranu w trakcie kazdej iteracji petli.
            self.screen.fill(bg_color)

            # Wyswietlenie ostatnio zmodyfikowanego ekranu.
            pygame.display.flip()

if __name__ == '__main__':
    # Utworzenie egzemplarza gry i jej uruchomienie.
    ai = InwazjaObcych()
    ai.run_game()