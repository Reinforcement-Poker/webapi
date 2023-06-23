from pydantic import BaseModel


class GameState(BaseModel):
    legal_actions: list[str] = ["fold", "call", "raise_low", "raise_high", "all_in"]
    player_cards: list[str] = ["Td", "Ad"]
    public_cards: list[str] = ["Kd", "Qd", "Jd", "9d", "8d"]
    pot: int = 100
    cost: int = 20
    button: int = 1


class StateModel(BaseModel):
    public_cards: list[str]
    player_bets: list[tuple[int, int]]
    pot: int
    stage: int


class GameModel(BaseModel):
    players: list[str]
    winner: int
    states: list[StateModel]
    page: str

    @property
    def n_players(self) -> int:
        return len(self.players)
