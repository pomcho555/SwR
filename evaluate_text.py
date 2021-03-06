#coding : utf-8 -*-
import re
import MeCab

def evaluate_text(text):
    """
    evaluate text difficulty by using frequency-based algorithm
    @argument string
    @return integer
    """
    def loop(result):
        #count word_len
        word_count = 0
        while result:
            #print('''%-10s \t %-s''' % (result.surface, result.feature))
            if(result.feature != '記号'):
                word_count += 1
            result = result.next
        return word_count
    word_count = 0
    han_count = 0

    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse("")
    result = tagger.parseToNode(text)
    try:
        word_count = loop(result)
    except Exception as e:
        word_count = loop(result)

    #count hanji_len
    for word in text:
        if(re.match('[一-龥]', word) != None):
            han_count += 1
    #estimate sentence difficulty
    sentence_difficulty = han_count/word_count
    print('difficulty:', sentence_difficulty)
    return sentence_difficulty

if __name__ == '__main__':
    import sys
    argv = sys.argv
    text = argv[1]
    text_diff = evaluate_text(text)
    print(text_diff)
