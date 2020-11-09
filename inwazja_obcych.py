import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
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

        # Utworzenie egzemplarza przechowujacego dane statystyczne dotyczace gry.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Utworzenie przycisku Gra.
        self.play_button = Button(self, 'Gra')

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

            if self.stats.game_active:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Rozpoczecie nowej gry po kliknieciu przycisku Gra przez uzytkownika."""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Wyzerowanie danych statycznych gry.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Usuniecie zawartosci list aliens i bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Utworzenie nowej floty i wysrodkowanie statku.
            self._create_fleet()
            self.ship.center_ship()

            # Ukrycie kursora myszy.
            pygame.mouse.set_visible(False)

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

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Reakcja na kolizje miedzy pociskiem i obcym."""

        # Usuniecie wszystkich pociskow i obcych, miedzy ktorymi doszlo do kolizji.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Pozbycie sie istniejacych pociskow i utworzenie nowej floty.
            self.bullets.empty()
            self._create_fleet()

    def _check_aliens_bottom(self):
        """Sprawdzanie, czy ktorykolwiek obcy dotarl do dolnej krawedzi ekranu."""

        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Tak samo jak w przypadku zderzenia statku z obcym
                self._ship_hit()
                break

    def _update_aliens(self):
        """Sprawdzanie, czy flota obcych znajduje sie przy krawedzi,
        a nastepnie uaktualnienie polozenia wszystkich obcych we flocie.
        """

        self._check_fleet_edges()
        self.aliens.update()

        # Wykrywanie kolizji miedzy obcym i statkiem.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Wyszukiwanie obcych docierajacych do dolnej krawedzi ekranu.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Reakcja na uderzenie obcego w statek."""

        if self.stats.ships_left > 0:
            # Zmniejszenie wartosci przechowywanej w ships_left.
            self.stats.ships_left -= 1

            # Usuniecie zawartosci list aliens i bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Utworzenie nowej floty i wysrodkowanie statku.
            self._create_fleet()
            self.ship.center_ship()

            # Pauza.
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Uaktualnienie obrazow na ekranie i przejscie do nowego ekranu."""

        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Wyswietlenie orzycisku tylko wtedy, gdy gra jest nieaktywna.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Wyswietlenie ostatnio zmodyfikowanego ekranu.
        pygame.display.flip()

if __name__ == '__main__':
    # Utworzenie egzemplarza gry i jej uruchomienie.
    ai = InwazjaObcych()
    ai.run_game()