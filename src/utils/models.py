from dataclasses import dataclass


@dataclass
class Lobby:
    link: str
    players: str
    stakes: str
    avg_pot: str
    avg_stake: str
    time_played: str

    @property
    def maximum_players(self) -> int:
        return int(self.players[4])

    @property
    def actual_players(self) -> int:
        return int(self.players[0])

    @property
    def is_full(self) -> bool:
        return self.maximum_players == self.actual_players
