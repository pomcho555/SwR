# coding: utf-8 -*-
import json
import config
import convert_hira as ch

class TemplateSimplifier(object):
    def __init__(self, wordlist, usr_level):
        """
        This wordlist doesn't indicate specific type
        It's on a case by case basis
        """
        self.wordlist = wordlist
        self.usr_level =usr_level

    def simplify(self):
        """
        return dict which include a word and the level
        """
        words_level_dict = {}
        print(self.__class__.__name__)
        if(self.__class__.__name__ == NormalSimplifier):
            words_level_dict = config.suggest_words

        word_level = 0
        json.dict = self.read_dictionary()
        for word in self.wordlist:
            try:
                word_level = json.dict[word]
            except KeyError:
                word_level = 7
            print('now is')
            print(word)
            print(word_level)
            words_level_dict = self.set_dict(word, word_level)
        return words_level_dict

    def read_dictionary(self):
        """
        return dict json from goi.json
        It shows such word-level
        """
        f = open('encoded_goi.json', 'r')
        json.dict = json.load(f)
        f.close()
        return json.dict

    def set_dict(self):
        assert False, "called abstruct method set_dict"


class NormalSimplifier(TemplateSimplifier):
    """
    This object takes 1 multiple dict and 1 integer
    This finally return multiple dictinary
    Ex: {'我': {<built-in function id>: 1, 'level': 5}, '迷宮': {<built-in function id>: 3, 'level': 5}}
    """
    def set_dict(self,word, word_level):
        try:
            config.suggest_words[word]['level'] = word_level
        except KeyError:
            config.suggest_word[word]['level'] = None
        words_level_dict = config.suggest_words
        return words_level_dict

class EachWordSimplifier(TemplateSimplifier):
    """
    This object takes 1 array and 1 integer
    This finally return single dictionary
    Ex: {'我': 5, '迷宮': 5}
    """
    #overide
    def __init__(self, wordlist, usr_level, original_word_level):
        self.wordlist = wordlist
        self.usr_level =usr_level
        self.original_word_level = original_word_level
        self.words_level_dict = {}

    def set_dict(self, word, word_level):
        #convert target word to hiragana
        if(self.original_word_level == 1):
            self.words_level_dict[ch.convert_hira(config.target_word)] = 0
            return self.words_level_dict
        if(word_level < self.original_word_level):
            self.words_level_dict[word] = word_level
        return self.words_level_dict




if __name__ == '__main__':
    config.suggest_words = {'我': {id: 1, 'level': 0}, '迷宮': {id: 3, 'level': 0}, '名前': {id: 6, 'level': 0}}
    choosed_token = {'我': {id: 1, 'level': 0}, '迷宮': {id: 3, 'level': 0}, '名前': {id: 6, 'level': 0}}
    usr_level = 1
    normalsimplifier = NormalSimplifier(choosed_token, usr_level)
    output = normalsimplifier.simplify()
    print(output)

    similar_array = ['吾れ', '吾', '主我', '自己', '我れ', '自我', '我', 'エゴ', '吾れ', '主観', '吾', '小生', '主我', '我れ', '自我', '我', 'エゴ']
    eachwordsimplifier = EachWordSimplifier(similar_array, usr_level, 5)
    output2 = eachwordsimplifier.simplify()
    print(output2)
