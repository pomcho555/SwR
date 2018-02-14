#coding : utf-8 -*-
import MeCab
import config

class WordChooser:
    def __init__(self, text, word_limit):
        self.text = text
        self.word_limit = word_limit

    def convert(self):
        def serialize_sentences(sentences):
            completed_text = ""
            for i in sentences:
                try:
                    completed_text += sentences[i]
                except:
                    pass
            return completed_text

        def countup(sentences):
            counter = sum([len(sentences[x]) for x in sentences])
            print(counter)
            return counter

        for p_id in config.pre_sentences:
            config.converted_sentences[p_id] = config.pre_sentences[p_id]['word']
            print('sentences_length')
            print(config.converted_sentences)
            if(countup(config.converted_sentences) < self.word_limit):
                for c_id in config.converted_words:
                    if(c_id == p_id):
                        config.converted_sentences[c_id] = config.converted_words[c_id]

        print(config.converted_sentences)
        serialize_sentences = serialize_sentences(config.converted_sentences)
        return serialize_sentences



    def choose_appropriate_word(self):
        leveled_word_list = []
        import set_token_to_dict as stt
        token_dict = stt.set_token_to_dict(self.text)
        #a list of a converted target token
        choosed_token_list = stt.classify_token_dict(token_dict)
        import TemplateSimplifier
        self.usr_level = config.usr_level
        wordsimplifier = TemplateSimplifier.NormalSimplifier(choosed_token_list, self.usr_level)
        words_level_dict = wordsimplifier.simplify()
        import WordNetController
        wordnetcontroller = WordNetController.WordNetController(words_level_dict)
        wordnetcontroller.word_crawl()
        output = WordChooser.convert(self)
        return output


if __name__ == '__main__':
    text = '我は猫だ。名前はまだない。君たちと仲良くしたいと思っている。これからもよろしく頼む。'
    text = 'フーリエ変換は、実変数の複素または実数値函数を別の仲間の函数に撮る変換である。変える後ろの函数はもとの函数に含まれる周波数を歴史し、しばしばもとの函数の周波数領域表現と呼ばれる。これは、弾く中のオンガクを聴いてソレをコードに書き出すというようなことと同じな思想である。素晴らしいの場合として、材料の函数とその周波世界意味が連続かつ非有界である時を見る事が可能'
    wordchooser = WordChooser(text, 100)
    wordchooser.choose_appropriate_word()
