import re
import spacy

def rm_punca(text):
    #punctuation = f",.¿?!@#$%^&*)(':+<>/÷¡" + f'"-' + f'][}{—'
    #text = re.sub(r"[%s]+" %punctuation,' ',text)
    text = re.sub('[^\w\s]',' ',text)
    return text.strip()

def ner_model(file):
    ner = spacy.load(file, exclude=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
    return ner
