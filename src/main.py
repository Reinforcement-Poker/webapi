from json import JSONDecodeError
from pprint import pprint

import requests
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from src.replaypoker import ReplayPoker
from src.utils.settings import API_URL, TARGET_PSW, TARGET_USR


def make_prediction(state) -> None:
    actions = state.pop("player_actions")
    response = requests.post(API_URL, json=state)
    action_index = response.json()

    print("Bot Action:", action_index)
    if action_index < len(actions):
        actions[action_index].click()
    else:
        actions[-1].click()


def main(driver) -> None:
    replaypoker = ReplayPoker(driver)
    replaypoker.login(TARGET_USR, TARGET_PSW)
    lobbies = replaypoker.get_all_lobbies()
    pprint(lobbies)

    for lobby in lobbies:
        if not lobby.is_full and lobby.maximum_players == 6:
            replaypoker.join_lobby(lobby)
            accept_lobby = input("Accept lobby? (y/N): ")

            if accept_lobby == "y":
                break

    while True:
        try:
            state = replaypoker.scrap_lobby_info()
            make_prediction(state)
        except (NoSuchElementException, StaleElementReferenceException):
            pass
        except JSONDecodeError:
            pass


if __name__ == "__main__":
    driver = webdriver.Remote(
        command_executor="http://localhost:4444",
        desired_capabilities=DesiredCapabilities.FIREFOX,
    )
    driver.implicitly_wait(10)

    try:
        main(driver)
    except Exception as error:
        print(error)
    finally:
        driver.quit()
