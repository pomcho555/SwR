# -*- coding: utf-8; -*-
"""
This is config module for Automatic_summarizer
"""
#common settings
usr_level = 7
compression_rate = 1
title = ''
pre_title = ''
original_text = ''
output_txt = ''
#all sentences after summarization
#Ex:{id:{'word':dragon, 'level': 5, 'word_class': '名詞'}}
pre_sentences = {}
#list for temporary saving
pre_word_list = []
#This dict include all token in sentences
pre_token_dict = {}
target_word = ''
word_limit = 0
#{word:{id:level:} => {'eat'{id:1,level:4}}
suggest_words = {}
# Ex:{id:word} => {1:'eat', 34:'bit'}
converted_words = {}
converted_sentences = {}
