# coding:utf-8
"""
This codec forked from https://qiita.com/sugulu/items/bc7c70e6658f204f85f9
"""
import numpy as np
import matplotlib.pyplot as plt
import ChooseSummarizer
import get_article_frmWiki as gaf
import evaluate_text as evatxt
import config
import evaluate_text as et


def excute():
    def bins(clip_min, clip_max, num):
        return np.linspace(clip_min, clip_max, num )

    def digitize_state(observation):
            compression_rate, usr_level = observation
            digitized = [
                np.digitize(compression_rate, bins=bins(10,100, 91)),
                np.digitize(usr_level, bins=bins(1,7,7))
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
        print("reward")
        print(reward)
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

    def create_fig(x,y,x_cap,y_cap):
        #reset plot space
        plt.figure()
        plt.plot(x,y,color="red")
        plt.xlabel(x_cap)
        plt.ylabel(y_cap)
        plt.legend()
        filename = "output_"+y_cap+".png"
        plt.savefig(filename)

    x=[]
    y=[]
    y_2=[]
    y_3=[]
    y_4=[]
    #max_number_of_steps = 200
    #num_consecutive_iterations = 100
    num_episodes = 30
    goal_average_reward = 20
    num_dizitized = 91
    num_actions = 4
    q_table = np.random.uniform(
        low=-1, high=1, size=(num_dizitized*7, num_actions))
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
    print(digitize_state(observation))
    action = np.argmax(q_table[state])


    import sys
    argv = sys.argv

    text = ''
    title = "強化学習"
    title = argv[1]
    original_text = gaf.fetch_article(title)
    # word_limit = 200



    config.original_text = original_text
    processed_text = gaf.text_preprocessing(original_text)
    word_limit = len(processed_text)
    config.word_limit = word_limit

    finFlg = False
    #main routin
    for episode in range(num_episodes):
        output1 = ChooseSummarizer.main(title, processed_text, word_limit, compression_rate*0.01)
        print('--------This is %s percent output--------' % (compression_rate))
        print(output1)
        print(episode)

        y_4.append(et.evaluate_text(output1))
        episode_reward = 0
        if(episode==0):
            pass
        else:
            observation = do_action(action, usr_level, compression_rate,abs(temp_reward))
            usr_level = observation[0]
            config.usr_level = usr_level
            compression_rate = observation[1]
            config.compression_rate = compression_rate*0.01
            word_limit = config.word_limit*compression_rate
        print(observation)


        print(q_table)
        reward = int(input('Please input num -10 to 10 that shows number you felt'))
        #Update proccesing
        if(reward==0000):finFlg=True
        episode_reward += reward*abs(reward)
        temp_reward = reward*2
        pre_reward = reward
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

        if(total_reward_vec.mean() >= goal_average_reward or finFlg == True or (reward+pre_reward)/2 >9):
            print('You are satisfied with this sentence:after Ep %d' % episode)

            create_fig(x,y,"Episode","Reward",)
            create_fig(x,y_2,"Episode","User level")
            create_fig(x,y_3,"Episode", "Compression rate")
            create_fig(x,y_4,"Episode","Sentence difficulty")

    create_fig(x,y,"Episode","Reward",)
    create_fig(x,y_2,"Episode","User level")
    create_fig(x,y_3,"Episode", "Compression rate")
    create_fig(x,y_4,"Episode","Sentence difficulty")


if __name__ == '__main__':
    excute()
