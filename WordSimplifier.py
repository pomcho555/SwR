# coding: utf-8 -*-
import json
import config

class WordSimplifier:
    def __init__(self, wordlist, usr_level):
        self.wordlist = wordlist
        self.usr_level = usr_level


    def simplify(self, *opt):
        """
        return dict which include a word and the level
        -c: use config.suggest_words
        -n: use words_level_dict
            word_level: It is word_level of original word
        """

        def read_dictionary():
            f = open('encoded_goi.json', 'r')
            json.dict = json.load(f)
            # print(json.dict)
            # print(json.dict["笑う"])
            f.close()
            return json.dict

        words_level_dict = {}
        word_level = 0
        #word_list = self.wordlist
        json.dict = read_dictionary()
        for word in self.wordlist:
            try:
                word_level = json.dict[word]
            except KeyError:
                pass
            # this dict include a word and the level
            if(opt[0] == 'c'):
                #新ロジック
                config.suggest_words[word]['level'] = word_level
                words_level_dict = config.suggest_words
            else:
                print(opt[1])
                if(opt[1] < word_level):
                    #旧ロジック
                    words_level_dict[word] = word_level

        print('word_level~~~~~~~~~~~~~~~~~~~~~')
        print(words_level_dict)

        return words_level_dict




if __name__ == '__main__':
    ws = WordSimplification("a", 5)
    ws.read_dictionary()
