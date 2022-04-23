#-------------- probando spacy ------------------
from ntpath import join
import spacy
from spacy.lang.es.stop_words import STOP_WORDS

async def procesarTexto(texto):
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(texto)
    dinero = {token.lemma_ for token in doc if token.pos_ == "NUM"}
    verbos = {token.lemma_ for token in doc if token.pos_ == "VERB"}    
    return "Verbos: "+ " ".join(verbos) + "\n Presupuesto: "+" ".join(dinero)