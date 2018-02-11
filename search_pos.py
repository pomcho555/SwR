from janome.tokenizer import Tokenizer
def search_pos(word):
    t = Tokenizer()
    tokens = t.tokenize(word)
    for token in tokens:
        partOfSpeech = token.part_of_speech.split(',')[0]

    return partOfSpeech

def extract_word(words, target_word):

    convertable_words = []
    target_pos = search_pos(target_word)

    for word in words:
        pos = search_pos(word)
        if(pos==target_pos):
            convertable_words.append(word)

    return convertable_words
