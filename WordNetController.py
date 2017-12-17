# coding: utf-8 -*-
"This module look up a suggest-synonyms from WordNet"

from nltk.corpus import wordnet as wn
import wn_syns
import config
import re

class WordNetController:
    def __init__(self, wordlist):
        self.wordlist = wordlist

    def word_crawl(self):
        '''
        get a synonyms from wordlist
        then call fetch_similar_word each word
        '''
        def fetch_similar_word(word):
            '''
            add that synonyms to suggest_word
            then call lookup_similarity()
            '''
            similaritydict = {}
            selected_sw = ''
            suggest_words = []
            #残念なことにワードネットくんは「みかん」等ひらがな文字列に反応しない
            #そこで、レスポンスが空なら漢字「蜜柑」等に変換して再度入力するぜよ
            if(re.match("[あ-ん|[一-龥]|[a-z]]", word) != None):
                suggest_words = wn_syns.getSynonym(word)
                print('I got synonym')
                print(suggest_words)
            #if(not suggest_words):
            import TemplateSimplifier
            usr_level = 1
            #wordsimplifier = WordSimplifier.WordSimplifier(suggest_words, usr_level)
            #leveled_synonyms = wordsimplifier.simplify('-n', self.wordlist[word])
            eachwordsimplifier = TemplateSimplifier.EachWordSimplifier(suggest_words, usr_level, self.wordlist[word]['level'])
            leveled_synonyms = eachwordsimplifier.simplify()
            print(leveled_synonyms)

            #今はテストのため類似度はオフ
            # for sw in suggest_words:
            #     if(sw != word):
            #         similaritydict[sw] = lookup_similarity(word, sw)
            #         print('===similar===')
            #         print(similaritydict)
            # sorted_similarity = sorted(similaritydict.items(), key=lambda x:x[1])
            # print(sorted_similarity)

            sorted_synonyms = sorted(leveled_synonyms.items(), key=lambda x:x[1])
            try:
                selected_sw = sorted_synonyms[0][0]
            except IndexError:
                selected_sw = word
            #selected_sw = sorted_similarity[0][0]
            print(selected_sw)
            #長さ順にする

            return selected_sw

        def lookup_similarity(target_word, suggest_word):
            output = 0
            try:
                output = wn.synsets(target_word, lang='jpn')[1].path_similarity(wn.synsets(suggest_word, lang='jpn')[0])
            except IndexError:
                pass
            if(output == None):
                output = 0

            return output

        for w in self.wordlist:
            if(len(w) > 0):
                config.target_word = w
                config.converted_words[config.suggest_words[w][id]] = fetch_similar_word(w)
        # for i_id in config.pre_sentences:
        #     for word in config.pre_sentences[i_id]["word"]:
        #         config.suggest_words[i_id] = fetch_similar_word(word)
        #     print(config.suggest_words)



if __name__ == '__main__':
    wordlist = ['リンゴ', '太陽', '蜜柑']
    wnc = WordNetController(wordlist)
    wnc.word_crawl()
    # output = wn.synsets('リンゴ', lang='jpn')[1].path_similarity(wn.synsets('太陽', lang='jpn')[0])
    # print(output)
