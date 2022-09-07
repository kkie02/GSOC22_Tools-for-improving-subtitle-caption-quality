import re, os, time, signal
import spacy
from spylls.hunspell import *
from spylls.hunspell import readers
from spell.utils import rm_punca, ner_model

class ES_checker():
    def __init__(self, file, dictionary='es_red'):
        cur_dir = os.getcwd()
        self.file = file
        self.main_dictionary = cur_dir + '/spell/dictionary/' + dictionary
        self.en_dictionary = cur_dir + '/spell/dictionary/' + 'en_US'
        
        # Load main dictionary and sub dictionary,
        print(self.main_dictionary)
        es_dictionary = Dictionary.from_files(self.main_dictionary)
        en_dictionary = Dictionary.from_files(self.en_dictionary)


        # Suggest and lookup instantiation
        #en_suggest = en_dictionary.suggester
        self.en_lookup = en_dictionary.lookuper
        self.es_suggest = es_dictionary.suggester
        self.es_lookup = es_dictionary.lookuper
        
        # Set ner model's name
        _ner_model_name = 'es_core_news_md'
        self.ner = ner_model(_ner_model_name)

    def set_timeout(num, callback):
      def wrap(func):
        def handle(signum, frame):
          raise RuntimeError
        def to_do(*args, **kwargs):
          try:
            signal.signal(signal.SIGALRM, handle)
            signal.alarm(num)
            #print('start alarm signal.')
            r = func(*args, **kwargs)
            #print('close alarm signal.')
            signal.alarm(0)
            return r
          except RuntimeError as e:
            callback()
        return to_do
      return wrap
      
    def after_timeout():
      return []
      
    @set_timeout(5, after_timeout)
    def pred_word(self, word):
        predict = [*self.es_suggest(word)]
        return predict

    def check(self):

        # Open file and start loop
        open_file = open(self.file, 'r', encoding='utf-8')
        cur_line = open_file.readline()
        i = 1
        while cur_line:
            line_contents = cur_line.split('|')
            if len(line_contents) < 4 or line_contents[-2] not in ['CC1', 'CCO']:
                cur_line = open_file.readline()
                i += 1
                continue
            words = cur_line.split('|')[-1]

            # Use NER Function here
            doc = self.ner(words)
            for ent in doc.ents:
                if len(ent)!=0:
                    words = re.sub(str(ent), '', words)
            words = rm_punca(words)
            split_words = words.split()
            for word in split_words:

                # If the word can be found in Spanish Dictionary, or it is a pure number, jump to the next one
                if self.es_lookup(word) or word.isdigit():
                    continue
                else:
                    # If the word can be found in Eng Dictionary, jump to the next one
                    if self.en_lookup(word):
                        continue
                    else:
                        # If the word can be found in any dictionaries, it's wrong, use Hunspell to correct it
                        predict = self.pred_word(word)
                        if predict == None:
                            print(f"lines: {i} | wrong word: {word} | can't find correction")
                            continue
                        elif len(predict):
                            print(f"lines: {i} | wrong word: {word} | correction: {predict[0]}")
                            continue
                        else:
                            # Some words, like '22M', is treated as wrong, but Hunspell can't correct it, treat it as right (It can be fixed by adding some rules in .aff file)
                            # print(f"Can't recognise : {predict}, {word}")
                            continue

            cur_line = open_file.readline()
            i += 1
