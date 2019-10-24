import tensorflow as tf
import numpy as np
from collections import deque

MEMORY_SIZE = 100000

class select_vote:
    def __init__(self):
        self.eps = 0.1
        self.main_qn = inference(state_size, action_size)
        self.target_qn = inference(state_size, action_size)
        self.memory = Memory(MEMORY_SIZE)

    def inference(self, state_size, actioin_size):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(100, activation="relu", input_shape=(state_size,)),
            tf.keras.layers.Dropout(0.15),
            tf.keras.layers.Dense(100, activation="relu"),
            tf.keras.layers.Dropout(0.15),
            tf.keras.layers.Dense(action_size, activation="linear")
        ])

        model.compile(loss = tf.losses.huber_loss, optimizer=tf.keras.optimizers.Adam(0.001))
        
        return model

    # 投票先の決定
    def select_vote(self, alive_member_without_me):
        eps = 0.01
        if np.random.rand() < eps:
            vote_player_idx = random.choice(alive_member_without_me)
        else:
            vote_player_idx = np.argmax(main_qn.predict(state)[0]) + 1
        
        return vote_player_idx

    # ターゲットネットワークの更新
    def update_target_qn(self):
        self.target_qn.set_weights(main_qn.get_weights())
    

# 経験再生用メモリ   
class Memory:
    # 初期化
    def __init__(self, memory_size):
        self.buffer  = deque(maxlen=memory_size)

    # 経験の追加
    def add(self, experience):
        self.buffer.append(experience)
    
    # バッチサイズ分の経験をランダムに取得
    def sample(self, batch_size):
        idx = np.random.choice(np.arange(len(self.buffer)), size = batch_size, replace = False)
        return [self.buffer[i] for i in idx]

    # 経験メモリのサイズ
    def __len__(self):
        return len(self.buffer)