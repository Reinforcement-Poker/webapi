from fastapi import FastAPI
from pydantic import BaseModel

from .models.fuzzy_model import FuzzyModel

app = FastAPI()
fuzzy_model = FuzzyModel()


class GameState(BaseModel):
    legal_actions: list[str] = ["fold", "call", "raise_low", "raise_high", "all_in"]
    player_cards: list[str] = ["Td", "Ad"]
    public_cards: list[str] = ["Kd", "Qd", "Jd", "9d", "8d"]
    pot: int = 100
    cost: int = 20
    button: int = 1


@app.post("/fuzzy_model")
def fuzzy_predict(state: GameState) -> int:
    hand_score = fuzzy_model.get_hand_score(
        [f"{card[1]}{card[0]}" for card in state.player_cards],
        [f"{card[1]}{card[0]}" for card in state.public_cards],
    )

    score = fuzzy_model.make_prediction(
        hand_score,
        state.pot,
        state.cost,
    )

    action_index = int(score * len(state.legal_actions) / 100)

    if state.cost == 0 and action_index == 0:
        action_index = 1

    return action_index
