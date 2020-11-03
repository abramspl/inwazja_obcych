import pygame

class Ship:
    """Klasa przeznaczona do zarzadzania statkiem kosmicznym."""

    def __init__(self,ai_game):
        """Inicjalizacja statku kosmicznego i jego polozenie poczatkowe."""

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Wczytanie obrazu statku kosmicznego i pobranie jego prostokata.
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        # Kazdy nowy statek kosmiczny pojawiajacy sie na dole ekranu.
        self.rect.midbottom = self.screen_rect.midbottom

        # Opcje wskazujace na poruszanie sie statku.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Uaktualnienie polozenia statku na podstawie opcji wskazujacej na jego ruch."""
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1

    def blitme(self):
        """Wyswietlanie statku kosmicznego w jego aktualnym polozeniu."""
        self.screen.blit(self.image, self.rect)