from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.database.core import engine, get_db
from api.database.models import Base, Bet, Game, Player, State
from api.models.fuzzy_model import FuzzyModel

app = FastAPI()
fuzzy_model = FuzzyModel()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


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

    action_index = int(score * 4 / 100)

    if state.cost == 0 and action_index == 0:
        action_index = 1

    return action_index


@app.post("/use_database")
async def use_database(db: Session = Depends(get_db)) -> bool:
    player1 = Player(username="John")
    player2 = Player(username="Emma")
    player3 = Player(username="Michael")
    game = Game(n_players=3)
    db.add_all([player1, player2, player3, game])
    db.commit()

    state1 = State(pot=1000, public_cards="AH KH QH", stage="preflop", game_id=game.id)
    state2 = State(pot=500, public_cards="2C 3C 4C", stage="turn", game_id=game.id)
    db.add_all([state1, state2])
    db.commit()

    bet1 = Bet(chips=200, action="fold", player_id=player1.id, state_id=state1.id)
    bet2 = Bet(chips=200, action="fold", player_id=player2.id, state_id=state1.id)
    bet3 = Bet(chips=200, action="fold", player_id=player3.id, state_id=state2.id)
    bet4 = Bet(chips=200, action="fold", player_id=player1.id, state_id=state2.id)

    db.add_all([bet1, bet2, bet3, bet4])
    db.commit()

    return True
