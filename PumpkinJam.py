from __future__ import print_function, division

import random
import aiwolfpy
import aiwolfpy.contentbuilder as cb
import PumpkinVillager as pv
import GameData as gd
import Talk_Text_Parser as ttp
import read_diff_data as rdd

class PumpkinJam(object):
    # !!注意!!これは，クラスの__init__です．ゲームの初期化とは関係ないです．
    def __init__(self, agent_name):
        self.my_name = agent_name
    
    # ゲームサーバーに名前を返します．
    def getName(self):
        return self.my_name
    
    # !!注意!!これは，ゲームの初期化です．__init__とは関係ないです．
    def initialize(self, base_info, diff_data, game_setting):
        self.base_info = base_info
        self.diff_data = diff_data
        self.game_setting = game_setting
        # GameDataのインスタンスを生成
        self.GameData = gd.GameData(self.base_info, self.diff_data, self.game_setting)

        self.CO_dict = {}

        print("-----------------新しいゲーム-------------------")
        print("生存者: %s" % self.GameData.aliveAgent)
        print("自分の陣営：%s陣営" % self.GameData.myCamp)
        print("自分の役職：%s" % self.GameData.myRole)
        print("ゲームの設定：%s人人狼" % self.GameData.playerNum)
        
    def update(self, base_info, diff_data, request):
        self.base_info = base_info
        self.diff_data = diff_data
        self.request = request

        print(self.diff_data)

        data_list = rdd.read_diff_data(self.diff_data)
        for data in data_list:
            index = data[0]
            row = data[1]
            # データがtalk
            if row["type"] == "talk":
                talker = row["agent"]
                day = row["day"]
                turn = row["turn"]
                text = row["text"]

                text_parser = ttp.Talk_Text_Parser(self.GameData, talker, day, turn, text)
            
            if row["type"] == "divine":
                self.GameData.divine_dict[row["agent"]] = row["text"].split(" ")[2]
    
    # その日の最初に呼ばれるメソッド
    def dayStart(self):
        self.GameData.day += 1
        print("-----------%d日目------------" % self.GameData.day)
        # 生存者リストを更新
        self.GameData.update_aliveAgent(self.base_info)

        print("生存者｛%s｝" % self.GameData.aliveAgent)

    def talk(self):
        return "ESTIMATE Agent[02] VILLAGER"

    def whisper(self):
        return cb.over()

    def vote(self):
        state = []
        state.append(self.GameData.day)
        alive_member_without_me = [idx for idx in self.GameData.aliveAgent if idx!=self.GameData.myAgentIdx]
        print("投票先候補: %s" % alive_member_without_me)
        vote_player_idx = random.choice(alive_member_without_me)
        print("エージェント%sに投票" % vote_player_idx)
        return vote_player_idx

    def attack(self):
        return self.base_info["agentIdx"]

    def divine(self):
        return self.base_info["agentIdx"]

    def guard(self):
        return self.base_info["agentIdx"]

    def finish(self):
        print("------------<ゲーム終了>-------------")
        role_reviel = {} # 全プレイヤーの役職をkey:agentidx, value:role
        winner = None
        my_win = False

        # 全プレイヤーの役職を取得
        data = self.diff_data
        for index, row in data.iterrows():
            role_reviel[row["agent"]] = row["text"].split(" ")[2]

        print(role_reviel)
        print(self.GameData.CO_dict)
        print(self.GameData.ESTIMATE_list)
        print(self.GameData.VOTE_list)
        print(self.GameData.divine_dict)

        # 勝利陣営の取得
        for idx, status in self.base_info["statusMap"].items():
            idx = int(idx)
            if status == "ALIVE":
                if role_reviel[idx] == "WEREWOLF":
                    winner = "WEREWOLF"
                    break
        if winner == None:
            winner = "VILLAGER"
        if self.GameData.myCamp == winner:
            my_win = True

        print("勝利: %s陣営" % winner)
        if my_win:
            print("自分：勝利！！")
        else:
            print("自分：敗北！！")
        return None

my_name = "PumpkinJam"
agent = PumpkinJam(my_name)

if __name__ == "__main__":
    aiwolfpy.connect_parse(agent)