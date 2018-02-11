# coding: utf-8 -*-
"The langage processing tools"

import MeCab
import config
def set_token_to_dict(text):
    """
    set token-info to dictionary
    @arg string
    @return dictionary
    """

    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse("") #mecab-python3のunicodeエラー対策
    node = tagger.parseToNode(text)
    token_dict = {}
    feature_array = []
    word_count = 0
    config.pre_sentences = {}
    print("docter")
    while node:
        try:
            feature_array = node.feature.split(",")
            if(word_count > 0):
                token_dict[node.surface] = feature_array[0]
                config.pre_sentences[word_count] = {"word": node.surface, "level": 0, "word_class":feature_array[0]}
        except UnicodeDecodeError:
            pass
        word_count += 1
        node = node.next
    print(config.pre_sentences)


    return token_dict


def classify_token_dict(target_dict):
    """
    classify tokens under a part of speech
    """
    #extract noun, verb, adjective from dict
    picked_word_list = []
    try:
        print('==target_dict==')
        print(config.pre_sentences)
        if(len(config.pre_sentences) != 0):
            for i_id in config.pre_sentences:
                word = config.pre_sentences[i_id]['word']
                if(config.pre_sentences[i_id]["word_class"] == "名詞"  or config.pre_sentences[i_id]["word_class"] == "形容詞" or config.pre_sentences[i_id]["word_class"] == "動詞" ):
                    config.suggest_words[word] = {id:i_id, 'level': 0}

        else:
            for word in target_dict:
                if(target_dict[word][0] == "名詞" or target_dict[word][0] == "形容詞" or target_dict[word][0] == "動詞"):
                    picked_word_list.append(word)
    except UnicodeDecodeError:
        return 1
    except TypeError:
        return 1
    # print('The word picked up is')
    # print(config.suggest_words)
    # print(picked_word_list)
    # print(config.usr_level)
    if(len(config.suggest_words) != 0):
        picked_word_list = config.suggest_words
    return picked_word_list


def main():
    text = '我々は宇宙人だ。名前はまだない。君たちと仲良くしたいと思っている。これからもよろしく頼む。'
    result = set_token_to_dict(text)
    classify_token_dict(result)
    #set_token_to_dict(result)

if __name__ == '__main__':
    main()
