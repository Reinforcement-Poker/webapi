from sqlalchemy.orm import Session

from api.database.models import Bet, Game, Player, State
from api.schema import StateModel


def create_player(db: Session, player_name: str) -> Player:
    new_player = Player(username=player_name)
    db.add(new_player)

    return new_player


def create_state(db: Session, state: StateModel, game: Game) -> State:
    new_stage = State(
        game_id=game.id,
        pot=state.pot,
        stage=state.stage,
        public_cards=" ".join(state.public_cards),
    )

    db.add(new_stage)

    return new_stage


def create_bet(
    db: Session,
    state: State,
    player: Player,
    chips: int,
    action: str,
) -> Bet:
    new_bet = Bet(
        state_id=state.id,
        player_id=player.id,
        action=action,
        chips=chips,
    )

    db.add(new_bet)

    return new_bet


def get_player(db: Session, player_name: str) -> Player:
    player = db.query(Player).filter(Player.id == player_name).first()

    if player is None:
        player = create_player(db, player_name)
        db.add(player)
        db.commit()

        return player

    return player


def create_all_states(db: Session, states_info: list[StateModel], game: Game) -> list[State]:
    states = [create_state(db, state_info, game) for state_info in states_info]
    db.add_all(states)
    db.commit()

    return states


def create_all_bets(
    db: Session,
    states: list[State],
    players: list[Player],
    states_info: list[StateModel],
) -> list[Bet]:
    bets = [
        create_bet(db, state, players[player_index], chips, "fold")
        for state, state_info in zip(states, states_info)
        for player_index, chips in state_info.player_bets
    ]

    db.add_all(bets)
    db.commit()

    return bets
