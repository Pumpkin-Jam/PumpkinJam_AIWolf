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
        elif self.talktype == "VOTE":
            self.parse_VOTE()

    def get_agentIdx(self, agent):
        idx = re.search(r"[0-9]+", agent)
        return int(idx.group())

    def parse_talktype(self):
        if "Agent" in self.text_list[0] or "ANY" in self.text_list[0] or "UNSPEC" in self.text_list[0]:
            self.subject = self.text_list[0]
        else:
            self.subject = self.talker
            self.talktype = self.text_list[0]
    
    # COMINGOUT文の解析 ([subject] COMINGOUT [target] [role])
    def parse_CO(self):
        agentIdx = -1
        role = ""
        
        role = self.text_list[2]
        agentIdx = self.get_agentIdx(self.text_list[1])

        self.GameData.CO_dict[role][str(agentIdx)] = (self.day, self.turn)

        print("エージェント%dが，%sCOしました" % (agentIdx, role))

    # ESTIMATE文の解析 ([subject] ESTIMATE [target] [role])
    def parse_ESTIMATE(self):
        subject = self.subject
        target = self.get_agentIdx(self.text_list[1])
        role = self.text_list[2]
        
        self.GameData.ESTIMATE_list[int(subject)-1][target-1] = role

        print("エージェント[%s]は，エージェント[%d]を[%s]だと推理しています．" % (subject, target, role))

    # VOTE文の解析 ([subject] VOTE [target])
    def parse_VOTE(self):
        subject = self.subject
        target = self.get_agentIdx(self.text_list[1])
        self.GameData.VOTE_list[int(subject)-1][target-1] = "VOTE"
        
        print("エージェント[%s]は，エージェント[%d]に投票しようとしています．" % (subject, target))
    
    # DIVINATION文の解析 ([subject] DIVINATION [target])
    def parse_DIVINATION(self):
        pass
    
    # GUARD文の解析 ([subject] GUARD [target])
    def parse_GUARD(self):
        pass

    # ATTACK文の解析 ([subject] ATTACK [target])
    def parse_ATTACK(self):
        pass

    # DIVINED文の解析 ([subject] DIVINED [target] [species])
    def parse_DIVINED(self):
        pass
    
    # IDENTIFIED文の解析 ([subject] IDENTIFIED [target] [species])
    def parse_IDENTIFIED(self):
        pass

    # GUARDED文の解析 ([subject] GUARDED [target])
    def parse_GUARDED(self):
        pass
    
    # VOTED文の解析 ([subject] VOTED [target])
    def parse_VOTED(self):
        pass

    # ATTACKED文の解析 ([subject] ATTACKED [target])
    def parse_ATTACKED(self):
        pass
    
    # AGREE文の解析 ([subject] AGREE [talk number])
    def parse_AGREE(self):
        pass

    # DISAGREE文の解析 ([subject] DISAGREE [talk number])
    def parse_DISAGREE(self):
        pass

    """
    ここから，operator(演算子)の解析
    """
    # REQUEST文の解析 ([subject] REQUEST [target] ([sentence]))
    def parse_REQUEST(self):
        pass
    
    # INQUIRE文の解析 ([subject] INQUIRE [target] ([sentence]))
    def parse_INQUIRE(self):
        pass

    # BECAUSE文の解析 ([subject] BECAUSE ([sentence1]) ([sentence2]))
    def parse_BECAUSE(self):
        pass

    # DAY文の解析 ([subject] DAY [day_number] ([sentence]))
    def parse_DAY(self):
        pass
    
    # NOT文の解析 ([subject] NOT ([sentence]))
    def parse_NOT(self):
        pass

    # AND文の解析 ([subject] AND ([sentence1]) ([sentence2]) ...)
    def parse_AND(self):
        pass
    
    # OR文の解析 ([subject] OR ([sentence1]) ([sentence2]) ...)
    def parse_OR(self):
        pass
    
    # XOR文の解析 ([subject] XOR ([sentence1]) ([sentence2]))
    def parse_XOR(self):
        pass