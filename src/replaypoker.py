import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.models import Lobby
from utils.settings import TARGET_URL


class ReplayPoker:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.url = TARGET_URL

    def login(self, username: str, password: str) -> None:
        self.driver.get(self.url + "/login")
        self.driver.find_element(By.ID, "login").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        time.sleep(1)

    def get_all_lobbies(self):
        self.driver.get(self.url + "/lobby")

        lobbies = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "li[class='lobby-game lobby-game-rings']"),
            )
        )

        lobby_list = []
        for element in lobbies:
            try:
                lobby = Lobby(
                    link=element.find_element(By.CSS_SELECTOR, "a").get_attribute("href"),
                    players=element.find_element(By.CSS_SELECTOR, "div:nth-child(4)").text,
                    stakes=element.find_element(By.CSS_SELECTOR, "div:nth-child(5)").text,
                    avg_pot=element.find_element(By.CSS_SELECTOR, "div:nth-child(6)").text,
                    avg_stake=element.find_element(By.CSS_SELECTOR, "div:nth-child(7)").text,
                    time_played=element.find_element(By.CSS_SELECTOR, "div:nth-child(8)").text,
                )

                lobby_list.append(lobby)
            except:
                pass

        return lobby_list

    def join_lobby(self, lobby: Lobby) -> None:
        self.driver.get(lobby.link)

    def print_board_status(self):
        history = self.get_message_history()
        public_cards = self.get_public_cards(history)
        players = self.get_lobby_players()
        button = self.get_button()
        current_bets = self.get_current_bets()
        pot = self.get_pot()
        # actions = self.get_player_actions()
        # actions_text = [action.text.replace("\n", "") for action in actions]

        print(f"Public cards: {public_cards}")
        print(f"Players info: {players}")
        print(f"Button: {button}")
        print(f"Pot: {pot}")
        print(f"Current bets: {current_bets}")
        # print(f"Current actions: {actions_text}")

    def get_current_bets(self) -> list[tuple[int, int]]:
        chip_pool = self.driver.find_element(By.CLASS_NAME, "Chips")
        current_bets = chip_pool.find_elements(By.CLASS_NAME, "Stack--bet")

        bet_list = []
        for i in current_bets:
            position = i.get_attribute("class").split("--")[-1][0]
            bet = i.text
            bet_list.append((position, bet))

        return bet_list

    def get_button(self) -> str:
        button = self.driver.find_element(By.CLASS_NAME, "DealerButton")
        player_index = button.get_attribute("class")[-1]

        return player_index

    def get_message_history(self) -> list[str]:
        message_history = self.driver.find_elements(
            By.CSS_SELECTOR,
            "div[class^='ChatMessage ChatMessage--dealer']",
        )

        return [message.text for message in message_history]

    def get_public_cards(self, history: list[str]) -> list[str]:
        public_cards = []
        for i in reversed(history):
            if "started" in i:
                break

            if "[" in i:
                public_cards += i[i.find("[") + 1 : i.find(" ]")].split(" ")[1:]

        return public_cards

    def get_lobby_players(self) -> list:
        sits_list = self.driver.find_elements(By.CSS_SELECTOR, "div[class^='Seat__nameplate']")

        players = []
        for sit in sits_list:
            username = sit.find_element(By.CLASS_NAME, "Seat__username").text
            if username == "Empty Seat":
                stack = 0
            else:
                stack = sit.find_element(By.CLASS_NAME, "Seat__stack").text

            players.append((username, stack))

        return players

    def get_pot(self) -> int:
        pot = self.driver.find_element(By.CSS_SELECTOR, "div[class='Pot__value']")
        return pot.text

    def get_player_actions(self) -> list:
        children = self.driver.find_element(
            By.CLASS_NAME, "BettingControls__actions"
        ).find_elements(By.XPATH, "./child::*")

        return children
