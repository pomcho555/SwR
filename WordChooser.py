#coding : utf-8 -*-
import MeCab
import config

class WordChooser:
    def __init__(self, text, word_limit):
        self.text = text
        self.word_limit = word_limit
    # def fetch_target_word(self, text, usr_level):
    #     unicode = 'utf-8'
    #     if type(text) is unicode:
    #         text = text.encode("utf8")
    #     tagger = MeCab.Tagger('-Ochasen')
    #     result = tagger.parseToNode(text)
    #     while result:
    #         print('''%-10s \t %-s''' % (result.surface, result.feature))
    #         if(result.feature != '記号'):
    #             word_count += 1
    #         result = result.next

    def convert():
        def serialize_sentences(sentences):
            completed_text = ""
            for i in sentences:
                try:
                    completed_text += sentences[i]
                except:
                    pass
            return completed_text


        for p_id in config.pre_sentences:
            config.converted_sentences[p_id] = config.pre_sentences[p_id]['word']
            for c_id in config.converted_words:
                if(c_id == p_id):
                    config.converted_sentences[c_id] = config.converted_words[c_id]

        print(config.converted_sentences)
        serialize_sentences = serialize_sentences(config.converted_sentences)
        print('This is final output')
        print(serialize_sentences)
        return serialize_sentences



    def choose_appropriate_word(self):
        leveled_word_list = []
        import set_token_to_dict as stt
        token_dict = stt.set_token_to_dict(self.text)
        #a list of a converted target token
        choosed_token_list = stt.classify_token_dict(token_dict)
        import TemplateSimplifier
        #fixed level 1 at test
        config.usr_level = 1
        self.usr_level = config.usr_level
        wordsimplifier = TemplateSimplifier.NormalSimplifier(choosed_token_list, self.usr_level)
        words_level_dict = wordsimplifier.simplify()
        print(words_level_dict)
        import WordNetController
        wordnetcontroller = WordNetController.WordNetController(words_level_dict)
        wordnetcontroller.word_crawl()
        WordChooser.convert()

if __name__ == '__main__':
    text = '我は猫だ。名前はまだない。君たちと仲良くしたいと思っている。これからもよろしく頼む。'
    text = '食玩は食品玩具の略。「おまけ」として玩具を添付した食品の商品様態の総称である。業界用語では玩菓とも言われる。玩具業界では食玩は「食べられる玩具」という意味で使われていたこともあり、玩具菓子の方が使われる。'
    wordchooser = WordChooser(text, 100)
    wordchooser.choose_appropriate_word()
