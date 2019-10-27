import GameData as gd
import numpy as np

def create_state(GameData):
    ROLE_DICT = {"VILLAGER":1, "SEER":2, "WEREWOLF":3, "POSSESSED":4, "None":0}
    day = GameData.day
    CO_dict = GameData.CO_dict

    # COした役職のリスト(最後にCOした役職に上書きされる)
    CO_list = [ROLE_DICT["None"] for i in range(GameData.playerNum)]
    for i in range(1, GameData.playerNum+1):
        for key, value in GameData.CO_dict.items():
            for k, v in value.items():
                if str(i)==k:
                    CO_list[i-1] = ROLE_DICT[key]
    print("CO_list: {}".format(CO_list))

    
    state = np.array([])
    
