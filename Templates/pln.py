#-------------- probando spacy ------------------
from ntpath import join
import spacy
from spacy.lang.es.stop_words import STOP_WORDS
from spacy.matcher import Matcher

VERB_NOUN_PATTERN = [{"POS": "VERB"}, {"POS": "NOUN"}]
NUM_PATTERN = [{"POS": "NUM"}]
NAME_PATTERN = [{"POS": "PROPN"}, {"POS": "PROPN"}]

def get_spacy():
    # return spacy.load('es_core_news_sm')
    return spacy.load('es_core_news_lg')

def extract_name(texto):
    nlp = get_spacy()
    doc = nlp(texto)
    res = {"found": False, "name":""}

    matcher = Matcher(nlp.vocab)
    matcher.add("NAME", [NAME_PATTERN])

    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        if string_id == "NAME":
            res = {
                "found": True,
                "name": span.text
            }

    return res

def extract_requirements(text):
    nlp = get_spacy()
    doc = nlp(text)

    matcher = Matcher(nlp.vocab)
    matcher.add("VERB_NOUN", [VERB_NOUN_PATTERN])
    matcher.add("NUMBER", [NUM_PATTERN])

    categories = []
    budget = -1

    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        if string_id == "VERB_NOUN":
            categories.append(span.text)
        if string_id == "NUMBER" and span.text.isdigit():
            budget = int(span.text)

    return {
        "categories": categories,
        "budget": budget
    }
