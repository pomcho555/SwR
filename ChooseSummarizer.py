#Desktop/Automatic_summarizer
# coding: utf-8 -*-

import config
import evaluate_text as evatxt
#take Strategy-pattern in the code
class ChooseSummarizer(object):
    def __init__(self, title, text, word_limit, summarizer, compression_rate):
        self.title = title
        self.text = text
        self.word_limit = word_limit
        self.summarizer = summarizer
        self.compression_rate = compression_rate

    def summarize(self):
        return self.summarizer.summarize(self.title, self.text, self.word_limit, self.compression_rate)

#Argumentation of superclass
class Summarizer(object):
    def summarize(self, title, text, word_limit, compression_rate):
        assert False
        return text

class WordPositionBasedSummarizer(Summarizer):

    def summarize(self, title, text, word_limit, compression_rate):
        """
        text: target text
        limit: summary length limit
        option:
        -m: summarization mode
            0: basic summarization model
            1: using word position feature
        -f: feature function
            0: direct proportion (DP)
            1: inverse proportion (IP)
            2: Geometric sequence (GS)
            3: Binary function (BF)
            4: Inverse entropy
        """
        import MeCab
        import numpy as np

        m = MeCab.Tagger("-Ochasen")
        m.parse("") #mecab-python3のunicodeエラー対策
        word_limit = 0
        word_limit = config.word_limit * compression_rate

        def sent_tokenize(text):
            #for python2.x
            unicode = 'utf-8'
            if type(text) is unicode:
                text = text.encode("utf8")
            node = m.parseToNode(text)
            sentences = []
            sentence = []
            while node:
                if type(node.surface) is unicode:
                    text = text.encode("utf8")

                #surface:表層形, feature:形態素情報
                sentence.append(node.surface)
                if node.surface == "。":
                    sentences.append(sentence)
                    sentence = []

                #call "next" method in iterator
                node = node.next
            return sentences

        def get_freqdict(sentences):
            #calculate frequency
            freqdict = {}
            N = 0
            """
            ここでsentencesはsentenceの集合
            sentenceはwordの集合
            集合＝辞書
            """
            for sentence in sentences:
                for word in sentence:
                    freqdict.setdefault(word, 0.)
                    #wordのvalueに1をたす＊語数カウント
                    freqdict[word] += 1
                    N += 1
            return freqdict

        def score(sentence, freqdict):
            return np.sum([np.log(freqdict[word]) for word in sentence]) / len(sentence)

        def direct_proportion(i, n):
            return float(n-i+1)/n

        def inverse_proportion(i, n):
            return 1.0 / i

        def geometric_sequence(i, n):
            return 0.5 ** (i-1)

        def inverse_entropy(p):
            if p == 1.0 or 0.0:
                return 1.0
            return 1-(-p*np.log(p) - (1-p)*np.log(1-p))

        def binary_function(i, n):
            p = 0
            if i == 1:
                p = 1
            else:
                p = 0.001
            return p

        def inverse_entropy_proportion(i, n):
            p = i / n
            return inverse_entropy(p)

        #fixed variable options to '0' for test
        options = {"m":1, "f":3}
        try:
            sentences = sent_tokenize(text)
        except Exception:
            sentences = sent_tokenize(text)
        freqdict = get_freqdict(sentences)
        if options["m"] == 0:
            scores = [score(sentence, freqdict) for sentence in sentences]
        if options["m"] == 1:
            if options["f"] == 0:
                word_features = direct_proportion
            elif options["f"] == 1:
                word_features = inverse_proportion
            elif options["f"] == 2:
                word_features = geometric_sequence
            elif options["f"] == 3:
                word_features = binary_function
            elif options["f"] == 4:
                word_features = inverse_entropy_proportion

            scores = []
            feature_dict = {}
            for sentence in sentences:
                sent_score = 0.0
                for word in sentence:
                    feature_dict.setdefault(word, 0.0)
                    feature_dict[word] += 1
                    sent_score += np.log(freqdict[word]) * word_features(feature_dict[word], freqdict[word])
                sent_score /= len(sentence)
                scores.append(sent_score)

        topics = []
        length = 0
        word_counter = 0
        for index in sorted(range(len(scores)), key=lambda k: scores[k], reverse=True):
            word_counter += sum([len(x) for x in sentences[index]])
            length += len(sentences[index])
            print('word_counter:%s' % word_counter)
            print('sentences %s' % sentences)
            print(word_limit)
            if(word_counter > word_limit):
                print('break')
                break
            topics.append(index)
        topics = sorted(topics)
        text = "".join(["".join(sentences[topic]) for topic in topics])
        print("summtext:%s" %text)
        return text

def main(title, processed_text, word_limit, compression_rate):
        config.pre_sentences = {}
        config.pre_word_list = []
        config.pre_token_dict = {}
        config.suggest_words = {}
        config.converted_words = {}
        config.converted_sentences = {}
        choosesummarizer = ChooseSummarizer(title, processed_text, word_limit, WordPositionBasedSummarizer(), compression_rate)
        output_text = choosesummarizer.summarize()
        evatxt.evaluate_text(output_text)
        import WordChooser
        wordchooser = WordChooser.WordChooser(output_text, word_limit)
        output = wordchooser.choose_appropriate_word()
        config.output_txt = output_text
        return output

def excute(usr_level, compression_rate):
    import config
    import get_article_frmWiki as gaf
    import evaluate_text as evatxt
    text = ''
    title = config.title
    config.original_text = original_text
    config.usr_level = usr_level
    word_limit = len(original_text)
    processed_text = gaf.text_preprocessing(original_text)
    output1 = main(title, processed_text, word_limit, compression_rate)

if __name__ == '__main__':
    import sys
    import get_article_frmWiki as gaf
    import evaluate_text as evatxt
    argv = sys.argv
    text = ''
    title = argv[1]
    # word_limit = 200
    compression_rate = 0.3

    original_text = gaf.fetch_article(title)
    processed_text = gaf.text_preprocessing(original_text)
    config.original_text = processed_text
    word_limit = len(processed_text)

    output1 = main(title, processed_text, word_limit, compression_rate)


    print('--------Original article-----------')
    print(original_text)
    print('')
    print('--------Summarized article---------')
    print(config.output_txt)
    print('')
    print('--------This is %s percent output--------' % (compression_rate *100))
    print(output1)
