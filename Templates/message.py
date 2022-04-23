from spade.message import Message
#-------------- probando spacy ------------------
import spacy
from spacy.lang.es.stop_words import STOP_WORDS


diccionario = {
  "saludar": "Hola, soy tu asistente virtual\n Te ayudaré a elegir la computadora con las características que necesitas.\n Dime tu nombre",
  "pregunta1":"¿Cuáles son las características de la computadora que buscas?",
  "capacidade de memoria":"¿Te refieres a la capacidade de almacenamiento o de la memoria física?",
  "juego": "se mostrarán las computadoras para juego",
  "programacion": "se mostrarán las computadoras para juego",
  "programar": "se mostrarán las computadoras para juego",
  "navegar": "se mostrarán las computadoras para juego",
  "trabajar": "Cual es tu trabajo?",


}


async def SendM(self, msg_body, receptor):
  msg = Message(to=str(receptor))
  msg.set_metadata("test1", "val1")
  msg.body=msg_body

  await self.send(msg)
  print("Message sent to {}".format(receptor))

async def pln(clave, state):
  res = diccionario.get(clave)
  if(state == 0):
    return diccionario['saludar']
  if(state == 1):
    return await plnSpacy(clave)
  if(res != None):
    return diccionario[clave]
  else:    
    #await plnSpacy(clave)
    return "¿podrías ser más específico por favor?"

async def plnSpacy(clave):
 nlp = spacy.load('es_core_news_sm')
 doc = nlp(clave)
 nombre=''

 print("Verbos: ", [token.lemma_ for token in doc if token.pos_ == "VERB"])
 
 for ent in doc.ents:
  nombre = ent.text

 if(nombre != ''):
  return nombre
 else:
  return 'Lo siento, pero no he podido encontrar tu nombre.'
