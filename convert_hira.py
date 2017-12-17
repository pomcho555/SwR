# coding: utf-8 -*-
"This module convert hanji-token to hiragana-token by google translater"

import re
import MeCab
def convert_hira(text):
    try:
        mecab = MeCab.Tagger("-Ochasen")#mecabを呼び出し
        o_text=mecab.parse(text)#ふりがなを取得
        o_list = o_text.split( )
        return(o_list[1])
    except IndexError:
        pass

if __name__ == '__main__':
    text = '食べる'
    print(convert_hira(text))
