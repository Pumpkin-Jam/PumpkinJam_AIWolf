import PumpkinJam

# 1ゲームのデータを保存するクラス
class GameData(object):
    def __init__(self, base_info, diff_data, game_setting):
        # 1ゲーム中変更されないデータ
        self.playerNum = game_setting["playerNum"] # ゲームに参加する人数
        self.myAgentIdx = base_info["agentIdx"] # 自分のエージェントのidx
        self.myRole = base_info["myRole"] # 自分の役職
        self.myCamp = "WEREWOLF" if self.myRole == "WEREWOLF" or self.myRole == "POSSESSED" else "VILLAGER"
        self.roleMap = base_info["roleMap"] # 役職一覧(自分以外に知っているエージェントの役職(他の人狼))


        self.aliveAgent = [i+1 for i in range(self.playerNum)] # 生存者のAgentIdxリスト
        self.day = -1

        
        self.CO_dict = {"VILLAGER":{}, "SEER":{}, "POSSESSED":{}, "WEREWOLF":{}} # key: AgentIdx, value: (day, turn, order)
        self.ESTIMATE_list = [[None for i in range(self.playerNum)] for j in range(self.playerNum)]
        self.VOTE_list = [[None for i in range(self.playerNum)] for j in range(self.playerNum)]
        self.vote_dict = {}

        self.divine_dict = {} # key: AgentIdx, value: result
        
        self.executedAgentList = []
        self.attackedAgentList = []

    # 生存者リストの更新
    def update_aliveAgent(self, base_info):
        statusMap = base_info["statusMap"]
        for i in range(self.playerNum):
            idx = i+1 # 生死判定をするAgentIdx
            status = statusMap[str(idx)]
            if status=="DEAD":
                self.aliveAgent.remove(idx)