# -*- coding: utf-8; -*-
import sys
from SPARQLWrapper import SPARQLWrapper
import re

def fetch_article(query):
    text = ''
    sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
    sparql.setQuery(r'''select distinct ?abstract where  { <http://ja.dbpedia.org/resource/%s> <http://dbpedia.org/ontology/abstract> ?abstract .}
    ''' % query)
    sparql.setReturnFormat('json')
    response = sparql.query().convert()
    print(response)
    for result in response['results']['bindings']:
        text = result['abstract']['value']
    return text

def text_preprocessing(text):
    text = re.sub(r'（.[^\（]*）', '', text)
    text = re.sub(r'\(.[^\(]*\)', '', text)
    return text

def main():
    title = sys.argv[1]
    original_text = fetch_article(sys.argv[1])
    processed_text = text_preprocessing(original_text)
    print('Search_Result below!')
    print(title)
    print("====================================================================================================")
    print(processed_text)

if __name__ == '__main__':
    main()
