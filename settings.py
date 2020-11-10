class Settings:
    """Klasa przeznaczona do przechowywania wszystkich ustawien gry."""

    def __init__(self):
        """Inicjalizacja danych statycznych gry."""

        # Ustawienia ekranu.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ustawienia dotyczace statku.
        self.ship_limit = 3

        # Ustawienia dotyczace pocisku.

        self.bullet_wight = 3
        self.bullet_hight = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        # Ustawiena dotyczace obcego.
        self.fleet_drop_speed = 5

        # Latwa zmiana szybkosci gry.
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicjalizacja ustawien, ktore ulegaja zmianie w trakcie gry."""

        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0


        # Wartosc fleet_direction wynoszaca 1 oznacza prawo, natomiast -1 oznacza lewo.
        self.fleet_direction = 1

    def increase_speed(self):
        """Zmiana ustawien dotyczacych szybkosci."""

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale