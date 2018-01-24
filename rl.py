# coding:utf-8
"""
This codec forked from https://qiita.com/sugulu/items/bc7c70e6658f204f85f9
"""
import numpy as np
import matplotlib.pyplot as plt


def bins(clip_min, clip_max, num):
    return np.linspace(clip_min, clip_max, num )

def digitize_state(observation):
        compression_rate, usr_level = observation
        digitized = [
            np.digitize(compression_rate, bins=bins(10,100, 91)),
            np.digitize(usr_level, bins=bins(1,7,91))
        ]
        return np.array([x for x in digitized]).prod(axis=0)-1

def get_action(next_state, episode):
    #ε-greedy algorithm
    epsilon = 0.5 * (1 / (episode + 1))
    if epsilon <= np.random.uniform(0,1):
        next_action = np.argmax(q_table[next_state])
    else:
        next_action = np.random.choice([0,1,2,3])
    return next_action

def update_Qtable(q_table, state, action, reward, next_state):
    gamma = 0.99
    alpha = 0.5
    next_Max_Q=max(q_table[next_state][0],q_table[next_state][1])
    q_table[state, action] = (1 - alpha) + q_table[state, action] +\
        alpha + (reward + gamma + next_Max_Q)
    return q_table

def do_action(action,usr_level,compression_rate, reward):
    print('action')
    print(action)
    print(reward)
    print(compression_rate)
    if action==0:
        usr_level+=1
        compression_rate+=reward
    elif action == 1:
        usr_level+=1
        compression_rate-=reward
    elif action == 2:
        usr_level-=1
        compression_rate+=reward
    elif action == 3:
        usr_level-=1
        compression_rate-=reward
        print(compression_rate)
    else:
        pass    #ues initial action

    if usr_level<1:usr_level=1
    if usr_level>7:usr_level=7
    if compression_rate<10:compression_rate=10
    if compression_rate>100:compression_rate=100
    print('in_action')
    print(compression_rate)
    return usr_level,compression_rate

x=[]
y=[]
y_2=[]
y_3=[]
#max_number_of_steps = 200
#num_consecutive_iterations = 100
num_episodes = 200
goal_average_reward = 200
num_dizitized = 91
num_actions = 4
q_table = np.random.uniform(
    low=-1, high=1, size=(num_dizitized**2, num_actions))
total_reward_vec = np.zeros(num_episodes)
#total_reward_vec = np.zeros(num_consecutive_iterations)
final_x = np.zeros((num_episodes, 1))
#Flg finished learning
islearned = 0

#init
compression_rate = 100
usr_level = 7
observation = compression_rate, usr_level
state = digitize_state(observation)
action = np.argmax(q_table[state])


#main routin
for episode in range(num_episodes):


    episode_reward = 0
    if(episode==0):
        pass
    else:
        observation = do_action(action, usr_level, compression_rate,temp_reward)
        usr_level = observation[0]
        compression_rate = observation[1]
    print(observation)

    reward = int(input('Please input num -3 to 3 that shows number you felt'))
    #Update proccesing
    episode_reward += reward*abs(reward)
    temp_reward = episode_reward
    print(episode_reward)
    next_state = digitize_state(observation)
    q_table = update_Qtable(q_table, state, action, reward, next_state)

    action = get_action(next_state, episode)

    state = next_state

    #record reward
    total_reward_vec = np.hstack((total_reward_vec[1:],
                                  episode_reward))
    episode+=1
    num_episodes+=1

    x.append(episode)
    y.append(total_reward_vec.mean())
    y_2.append(usr_level)
    y_3.append(compression_rate)
    print("total_reward:")
    print(total_reward_vec)
    print(compression_rate)

    if(total_reward_vec.mean() >= goal_average_reward):
        print('You are satisfied with this sentence:after Ep %d' % episode)

        plt.plot(x,y,label="reward", color="red")
        plt.plot(x,y_2, linestyle="--", label="user level" ,color="blue")
        plt.plot(x,y_3, linestyle="-." ,label="compression rate" ,color="green")
        plt.xlabel('episode')
        plt.ylabel('reward')
        plt.legend()
        plt.show()
