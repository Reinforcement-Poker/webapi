from typing import Callable

import numpy as np
from skfuzzy.control import (
    Antecedent,
    Consequent,
    ControlSystem,
    ControlSystemSimulation,
    Rule,
)
from treys import Card, Evaluator


class FuzzyModel:
    def __init__(self) -> None:
        self.use_raw = False

        # Fuzzy variables
        hand_rank = Antecedent(np.arange(0, 1, 0.001), "hand_rank")
        pot = Antecedent(np.arange(0, 150, 1), "pot")
        cost = Antecedent(np.arange(0, 1, 0.001), "cost")
        action = Consequent(np.arange(0, 101, 1), "action")

        hand_rank.automf(5)
        pot.automf(3, names=["low", "medium", "high"])
        cost.automf(3, names=["low", "medium", "high"])
        action.automf(5, names=["fold", "call", "raise_low", "raise_high", "all_in"])

        all_pot = pot["low"] | pot["medium"] | pot["high"]
        all_cost = cost["low"] | cost["medium"] | cost["high"]
        no_high_pot = pot["medium"] | pot["low"]

        # Rules
        r1 = Rule(hand_rank["poor"] & all_pot & all_cost, action["fold"])
        r2 = Rule(hand_rank["mediocre"] & all_pot & all_cost, action["fold"])
        r3 = Rule(hand_rank["average"] & pot["high"] & cost["high"], action["fold"])
        r4 = Rule(hand_rank["average"] & pot["high"] & cost["medium"], action["fold"])
        r5 = Rule(hand_rank["average"] & pot["high"] & cost["low"], action["call"])
        r6 = Rule(hand_rank["average"] & no_high_pot & all_cost, action["call"])
        r7 = Rule(hand_rank["decent"] & pot["high"] & all_cost, action["fold"])
        r8 = Rule(hand_rank["decent"] & no_high_pot & all_cost, action["raise_high"])
        r9 = Rule(hand_rank["good"] & pot["high"] & all_cost, action["all_in"])
        rA = Rule(hand_rank["good"] & no_high_pot & all_cost, action["raise_low"])

        rule_list = [r1, r2, r3, r4, r5, r6, r7, r8, r9, rA]
        action_ctrl = ControlSystem(rule_list)
        self.action_sim = ControlSystemSimulation(action_ctrl)

    def get_hand_score(self, hand: list[str], board: list[str]) -> float:
        if len(board) > 0:
            N_HAND_RANKS = 7462
            evaluator = Evaluator()
            to_card = lambda card: Card.new(f"{card[1]}{card[0].lower()}")
            eval_hand = list(map(to_card, hand))
            eval_board = list(map(to_card, board))
            return (1 - evaluator.evaluate(eval_board, eval_hand) / N_HAND_RANKS) * 1.3

        card_number = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

        max_score = 318
        card_number = sum(card_number.index(card[1]) ** 2.5 for card in hand)
        is_suited = hand[0][0] == hand[1][0]
        is_pair = hand[0][1] == hand[1][1]

        if is_pair or is_suited:
            return 1 - card_number / max_score

        return 1 - card_number * 1.2 / max_score

    def make_prediction(self, hand_rank: float, pot: float, cost: float) -> float:
        self.action_sim.input["hand_rank"] = hand_rank
        self.action_sim.input["pot"] = pot
        self.action_sim.input["cost"] = cost
        self.action_sim.compute()

        return self.action_sim.output["action"]
