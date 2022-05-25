#-------------- probando spacy ------------------
from ntpath import join
import spacy
from spacy.lang.es.stop_words import STOP_WORDS

async def procesarNombre(texto):
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(texto)
    res = {"found": False, "name":""}

    for entity in doc.ents:
        print(entity.text, entity.label_)
        if (entity.label_ == "PER"):
            res["found"] = True
            res["name"] = entity.text
    
    return res
        

    

async def procesarTexto(texto):
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(texto)
    verbos = {token.lemma_ for token in doc if token.pos_ == "VERB"}  
    return verbos   

"""
    dinero = {token.lemma_ for token in doc if token.pos_ == "NUM"}
    verbos = {token.lemma_ for token in doc if token.pos_ == "VERB"}    
    return "Verbos: "+ " ".join(verbos) + "\n Presupuesto: "+" ".join(dinero)
"""