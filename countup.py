# coding: utf-8 -*-
def countup(sentences):
    #counter = sentences.values()
    counter = sum([len(sentences[x]) for x in sentences])
    print(counter)
