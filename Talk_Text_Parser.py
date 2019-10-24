import re

class Talk_Text_Parser:
    def __init__(self, GameData, talker, day, turn, text):
        self.GameData = GameData
        self.talker = talker
        self.day = day
        self.turn = turn
        self.text = text

        self.text_list = text.split(" ")

        self.subject = "" # talkの主語(基本的に話者が主語)
        self.talktype = ""

        self.parse_talktype()

        if self.talktype == "COMINGOUT":
            self.parse_CO()
        elif self.talktype == "ESTIMATE":
            self.parse_ESTIMATE()

    def get_agentIdx(self, agent):
        idx = re.search(r"[0-9]+", agent)
        return int(idx.group())

    def parse_talktype(self):
        if "Agent" in self.text_list[0] or "ANY" in self.text_list[0] or "UNSPEC" in self.text_list[0]:
            self.subject = self.text_list[0]
        else:
            self.subject = self.talker
            self.talktype = self.text_list[0]
    
    # COMINGOUTの解析
    def parse_CO(self):
        agentIdx = -1
        role = ""
        
        role = self.text_list[2]
        agentIdx = self.get_agentIdx(self.text_list[1])

        self.GameData.CO_dict[role][str(agentIdx)] = (self.day, self.turn)

        print("エージェント%dが，%sCOしました" % (agentIdx, role))

    # ESTIMATEの解析
    def parse_ESTIMATE(self):
        subject = self.subject
        target = self.get_agentIdx(self.text_list[1])
        role = self.text_list[2]
        
        self.GameData.ESTIMATE_list[int(subject)-1][target-1] = role

        print("エージェント[%s]は，エージェント[%d]を[%s]だと推理しています。" % (subject, target, role))