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
    position: int,
    chips: int,
    action: str,
) -> Bet:
    new_bet = Bet(
        state_id=state.id,
        position=position,
        player_id=player.id,
        action=action,
        chips=chips,
    )

    db.add(new_bet)

    return new_bet


def get_player(db: Session, player_name: str) -> Player:
    player = db.query(Player).filter(Player.username == player_name).first()

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
    player_status = [True] * len(players)
    board_bets = [0] * len(players)
    previous_stage = 0
    last_action = None
    bets = []

    for state, state_info in zip(states, states_info):
        player_bets = parse_bets(state_info.player_bets, len(players))
        order = 0

        if previous_stage != state_info.stage:
            board_bets = [0] * len(players)
            last_action = None

        for player_index, chips in player_bets:
            action = "call"

            if not player_status[player_index]:
                continue

            if max(*board_bets) < chips:
                action = "raise"

            if max(board_bets) == board_bets[player_index]:
                if last_action == "call":
                    break
                action = "check"

            if chips == 0 and max(board_bets) > 0:
                action = "fold"
                player_status[player_index] = False

            if state_info.stage == 0:
                if chips == 1:
                    action = "small_blind"
                elif chips == 2:
                    action = "big_blind"

            if action != "fold":
                board_bets[player_index] = chips
                last_action = action

            bets.append(
                create_bet(
                    db,
                    state,
                    players[player_index],
                    order,
                    chips,
                    action,
                )
            )

            order += 1

        previous_stage = state_info.stage

    db.add_all(bets)
    db.commit()

    return bets


def parse_bets(
    player_bets: list[tuple[int, int]],
    n_players: int,
) -> list[tuple[int, int]]:
    if len(player_bets) == 0:
        return [(index, 0) for index in range(n_players)]

    for index in range(n_players):
        p_id, _ = player_bets[index]
        next_index = index + 1
        next_p_id = (p_id + 1) % n_players

        if next_index < len(player_bets):
            next_arr_id, _ = player_bets[next_index]

            if next_arr_id != next_p_id:
                player_bets.insert(next_index, (next_p_id, 0))

        elif len(player_bets) < n_players:
            player_bets.append((next_p_id, 0))

    return player_bets
