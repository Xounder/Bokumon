import os
import json
from settings.settings import SAVE_PATH
from game_types import PlayerData


def save_data(data: PlayerData) -> None:
    try:
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

        with open(SAVE_PATH, "w") as file:
            json.dump(data, file, indent=4)

    except OSError as e:
        print(f"Erro ao salvar o jogo: {e}")


def load_data() -> PlayerData:
    with open(SAVE_PATH, "r") as file:
        return json.loads(file.read())


def has_saved_game() -> bool:
    return os.path.exists(SAVE_PATH)
