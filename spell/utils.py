import re
import spacy

def rm_punca(text):
    punctuation = f",.¿?!@#$%^&*)(':+<>/÷" + '"-'
    text = re.sub(r"[%s]+" %punctuation,' ',text)
    return text.strip()

def ner_model(file):
    ner = spacy.load(file, exclude=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
    return ner
