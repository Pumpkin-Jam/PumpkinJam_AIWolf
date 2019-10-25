import re

"""
※人狼知能プロトコルver3.6　に準拠しています．
"""
class Talk_Text_Parser:
    def __init__(self, GameData, talker, day, turn, text):
        # [verb]: 15種類 
        self.VERB_LIST = ["ESTIMATE", "COMINGOUT",  # 意図表明
                          "DIVINATION", "GUARD", "VOTE", "ATTACK",    # 行動・能力
                          "DIVINED", "IDENTIFIED", "GUARDED", "VOTED", "ATTACKED", # 行動・能力の結果
                          "AGREE", "DISAGREE",  # 同意
                          "OVER", "SKIP"]  # 発話制御
        # operator: 8種類
        self.OPERATOR_LIST = ["REQUEST", "INQUIRE",  # 要請・問いかけ                             
                              "BECAUSE",   # 理由
                              "DAY",   # 時制の指定
                              "NOT", "AND", "OR", "XOR"]  # 論理演算子

        self.GameData = GameData
        self.talker = talker
        self.day = day
        self.turn = turn
        self.text = text

        self.text_list = text.split(" ")

        # text中にあるoperatorの数を数える
        self.operator_num_list = []
        for i, word in enumerate(self.text_list):
            if word in self.OPERATOR_LIST:
                self.operator_num_list.append(i)

        if len(self.operator_num_list)==0: # operatorを一つも含まない場合
            self.parse_sentence(text)
        else:
            pass

    def get_agentIdx(self, agent):
        idx = re.search(r"[0-9]+", agent)
        return int(idx.group())

    def parse_sentence(self, sentence):
        have_subject = True
        subject = ""
        verb = ""
        target = ""
        role = ""
        species = ""
        talk_number = 0

        sentence_words = sentence.split(" ")

        if sentence_words[0] == "UNSPEC":
            subject = "UNSPEC"
        elif sentence_words[0] == "ANY":
            subject = "ANY"
        elif "Agent" in sentence_words[0]:
            subject = str(get_agentIdx(sentnce_words[0]))
        else:
            subject = self.talker
            have_subject = False
        
        if not have_subject:
            verb = sentence_words[0]
        else:
            verb = sentence_words[1]

        if verb in ["ESTIMATE", "COMINGOUT", "DIVINATION", "GUARD", "VOTE", "ATTACK", "DIVINED", "IDENTIFIED", "GUARDED", "VOTED", "ATTACKED"]:
            if not have_subject:
                target = str(self.get_agentIdx(sentence_words[1]))
                if verb in ["ESTIMATE", "COMINGOUT"]:
                    role = sentence_words[2]
                elif verb in ["DIVINED", "IDENTIFIED"]:
                    species = sentence_words[2]
            else:
                target = str(self.get_agentIdx(sentence_words[2]))
                if verb in ["ESTIMATE", "COMINGOUT"]:
                    role = sentence_words[3]
                elif verb in ["DIVINED", "IDENTIFIED"]:
                    species = sentence_words[3]
        elif verb in ["AGREE", "DISAGREE"]:
            if not have_subject:
                talk_number = sentence_words[1]
            else:
                talk_number = sentence_words[2]

        if verb == "ESTIMATE":
            self.parse_ESTIMATE(subject, target, role)
        elif verb == "COMINGOUT":
            self.parse_CO(subject, target, role)
        elif verb == "DIVINATION":
            self.parse_DIVINATION(subject, target)
        elif verb == "GUARD":
            self. parse_GUARD()
        elif verb == "VOTE":
            self.parse_VOTE(subject, target)
        elif verb == "ATTACK":
            self.parse_ATTACK()
        elif verb == "DIVINED":
            self.parse_DIVINED(subject, target, species)
        elif verb == "IDENTIFIED":
            self.parse_IDENTIFIED()
        elif verb == "GUARDED":
            self.parse_GUARDED()
        elif verb == "VOTED":
            self.parse_VOTED()
        elif verb == "ATTACKED":
            self.parse_ATTACKED()
        elif verb == "AGREE":
            self.parse_AGREE()
        elif verb == "DISAGREE":
            self.parse_DISAGREE()
    
    """
    [sentence]を構成する文 (これより小さな単位の文は今のところ生成できません)
    """
    # COMINGOUT文の解析 ([subject] COMINGOUT [target] [role])
    def parse_CO(self, subject, target, role):
        self.GameData.CO_dict[role][str(target)] = (self.day, self.turn)
        print("エージェント[{}]が，[{}]COしました".format(target, role))

    # ESTIMATE文の解析 ([subject] ESTIMATE [target] [role])
    def parse_ESTIMATE(self, subject, target, role):        
        self.GameData.ESTIMATE_list[int(subject)-1][int(target)-1] = role
        print("エージェント[{}]は，エージェント[{}]を[{}]だと推理しています．".format(subject, target, role))

    # VOTE文の解析 ([subject] VOTE [target])
    def parse_VOTE(self, subject, target):
        self.GameData.VOTE_list[int(subject)-1][int(target)-1] = "VOTE"        
        print("エージェント[{}]は，エージェント[{}]に投票しようとしています．".format(subject, target))
    
    # DIVINATION文の解析 ([subject] DIVINATION [target])
    def parse_DIVINATION(self, subject, target):
        pass
    
    # GUARD文の解析 ([subject] GUARD [target])
    def parse_GUARD(self):
        pass

    # ATTACK文の解析 ([subject] ATTACK [target])
    def parse_ATTACK(self):
        pass

    # DIVINED文の解析 ([subject] DIVINED [target] [species])
    def parse_DIVINED(self, subject, target, species):
        self.GameData.DIVINED_list[int(subject)-1][int(target)-1] = species        
        print("エージェント[{}]が，エージェント[{}]を占った結果[{}]でした．".format(subject, target, species))
    
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
    ここから，operator(演算子)の解析 (operator文では，sentenceを埋め込むことで入れ子構造にすることができます．)
    operator文の中にoperator文を入れることができるかの検証は行っていないためまだ不明です．
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