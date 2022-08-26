import re
import spacy
from spylls.hunspell import *
from spylls.hunspell import readers
from utils import rm_punca, ner_model

class ES_checker():
    def __init__(self, file, dictionary='./dictionary/es_red'):
        self.file = file
        self.main_dictionary = dictionary

    def check(self):
        # Set ner model's name
        _ner_model_name = 'es_core_news_md'
        _USENER = True
        ner = ner_model(_ner_model_name)

        # Load main dictionary and sub dictionary,
        es_dictionary = Dictionary.from_files(self.main_dictionary)
        en_dictionary = Dictionary.from_files('./dictionary/en_US')


        # Suggest and lookup instantiation
        #en_suggest = en_dictionary.suggester
        en_lookup = en_dictionary.lookuper
        es_suggest = es_dictionary.suggester
        es_lookup = es_dictionary.lookuper

        # Open file and start loop
        open_file = open(self.file, 'r', encoding='utf-8')
        cur_line = open_file.readline()
        i = 1
        while cur_line:
            if cur_line.split('|')[-2] not in ['CC1', 'CCO']:
                cur_line = open_file.readline()
                i += 1
                continue
            words = cur_line.split('|')[-1]

            # Use NER Function here
            doc = ner(words)
            for ent in doc.ents:
                words = re.sub(str(ent), '', words)
            words = rm_punca(words)
            split_words = words.split()
            for word in split_words:
                #word = rm_punca(word)
                # If the word can be found in Spanish Dictionary, or it is a pure number, jump to the next one
                if es_lookup(word) or word.isdigit():
                    continue
                else:
                    # If the word can be found in Eng Dictionary, jump to the next one
                    if en_lookup(word):
                        continue
                    else:
                        # If the word can be found in any dictionaries, it's wrong, use Hunspell to correct it
                        predict = [*es_suggest(word)]
                        if len(predict):
                            # print(f"correction: {predict[0]}, {word}")
                            print(f"lines: {i} | wrong word: {word} | correction: {predict[0]}")
                            continue
                        else:
                            # Some words, like '22M', is treated as wrong, but Hunspell can't correct it, treat it as right (It can be fixed by adding some rules in .aff file)
                            # print(f"Can't recognise : {predict}, {word}")
                            continue

            cur_line = open_file.readline()
            i += 1

