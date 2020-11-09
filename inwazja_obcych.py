import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class InwazjaObcych:
    """Ogolna klasa przeznaczona do zarzadzania zasobami i sposobem dzialania gry"""

    def __init__(self):
        """Inicjalizacja gry i utworzenie jej zasobow"""

        pygame.init()
        self.settings = Settings()

        # Tryb gry onkienkowy
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Inwazja obcych')

        # Tryb gry pelnoekranowy
        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        # pygame.display.set_caption('Inwazja obcych')

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def _create_fleet(self):
        """Utworzenie pelnej floty obcych."""

        # Utworzenie obcego i ustalenie liczby obcych, ktorzy zmieszcza sie w rzedzie.
        # Odleglosc miedzy poszczegolnymi obcymi jest rowna szerokosci obcego.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        iavailable_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = iavailable_space_x // (2 * alien_width)

        # Ustalenie ile rzedow obcych zmiesci sie na ekranie.
        ship_height = self.ship.rect.height
        iavailable_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = iavailable_space_y // (2 * alien_height)

        # Utworzenie pelnej floty obcych.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        """Utworzenie obcego i umieszczenie go w rzedzie."""

        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def run_game(self):
        """Rozpoczecie petli glownej gry"""

        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Relacja na zdarzenia generowane przez klawiature i mysz."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        """Reakacja na nacisniecie klawisza."""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """Reakcja na zwolnienie klawisza."""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_fleet_edges(self):
        """Odpowiednia reakacja, gdy obcy dotrze do krawedzi ekranu."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Przesuniecie calej floty w dol i zmiana kierunku, w ktorym sie ona porusza."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _fire_bullet(self):
        """Utworzenie nowego pocisku i dodanie go do grupy pociskow."""

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Uaktualnienie polozenia pociskow i usuniecie tych niewidocznych na ekranie."""

        # Uaktualnienie polozenia pociskow.
        self.bullets.update()

        # Usuwanie pociskow, ktore znajda sie poza ekranem.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_aliens(self):
        """Sprawdzanie, czy flota obcych znajduje sie przy krawedzi,
        a nastepnie uaktualnienie polozenia wszystkich obcych we flocie.
        """

        self._check_fleet_edges()
        self.aliens.update()


    def _update_screen(self):
        """Uaktualnienie obrazow na ekranie i przejscie do nowego ekranu."""

        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Wyswietlenie ostatnio zmodyfikowanego ekranu.
        pygame.display.flip()

if __name__ == '__main__':
    # Utworzenie egzemplarza gry i jej uruchomienie.
    ai = InwazjaObcych()
    ai.run_game()