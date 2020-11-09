class GameStats:
    """Monitorowanie danych statystyczbych w grze 'Inwazja obcych'."""

    def __init__(self,ai_game):
        """Inicjalizacja danych statystycznych"""

        self.settings = ai_game.settings
        self.reset_stats()

        # Uruchomienie gry "Inwazja obcych" w stanie aktywnym.
        self.game_active = False

    def reset_stats(self):
        """Inicjalizacja danych statystycznych, ktore moga zmieniac sie w trakcie gry."""

        self.ships_left = self.settings.ship_limit