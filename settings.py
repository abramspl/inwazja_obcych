class Settings:
    """Klasa przeznaczona do przechowywania wszystkich ustawien gry."""

    def __init__(self):
        """Inicjalizacja ustawien gry."""

        # Ustawienia ekranu.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ustawienia dotyczace statku.
        self.ship_speed = 1.5

        # Ustawienia dotyczace pocisku.
        self.bullet_speed = 1.0
        self.bullet_wight = 3
        self.bullet_hight = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3