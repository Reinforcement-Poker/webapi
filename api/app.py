from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import api.database.queries as query
from api.database.core import engine, get_db
from api.database.models import Base, Bet, Game, Player, State
from api.models.fuzzy_model import FuzzyModel
from api.schema import GameModel, GameState

app = FastAPI()
fuzzy_model = FuzzyModel()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


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


@app.post("/add_game")
async def add_game(game_info: GameModel, db: Session = Depends(get_db)) -> str:
    players_name = game_info.players
    states_info = game_info.states

    new_game = Game(
        n_players=game_info.n_players,
        winner=game_info.winner,
    )
    db.add(new_game)
    db.commit()

    players = [query.get_player(db, name) for name in players_name]
    states = query.create_all_states(db, states_info, new_game)
    query.create_all_bets(db, states, players, states_info)

    return "Game added"
