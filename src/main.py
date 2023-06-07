from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from replaypoker import ReplayPoker
from utils.settings import TARGET_PSW, TARGET_USR

if __name__ == "__main__":
    driver = webdriver.Remote(
        command_executor="http://localhost:4444",
        desired_capabilities=DesiredCapabilities.FIREFOX,
    )
    driver.implicitly_wait(10)

    try:
        replaypoker = ReplayPoker(driver)

        # Pipeline for playing
        replaypoker.login(TARGET_USR, TARGET_PSW)
        lobbies = replaypoker.get_all_lobbies()
        pprint(lobbies)

        for lobby in lobbies:
            if not lobby.is_full:
                replaypoker.join_lobby(lobby)
                replaypoker.print_board_status()
                break
    except Exception as error:
        print(error)
    finally:
        driver.quit()
