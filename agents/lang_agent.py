import config
from Templates import message as sm
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour
from spade.template import Template

#------probando spacy--------
import spacy
from spacy.lang.es.stop_words import STOP_WORDS


res = "respuesta del agente 2"
class LangAgent(Agent):
  class RecvBehav(PeriodicBehaviour):
    async def run(self):
      #print("RecvBehav running")
      msg = await self.receive()
      if msg:
        print("Mensage Recibido: {}".format(msg.body))
        await self.send(msg)
        #await sm.SendM(self, res, config.AGENT_MAIN_USER)

     # else:
        #print("Did not received any message")

  async def pln(texto):
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(texto)
    nombre=''

    print("Verbos: ", [token.lemma_ for token in doc if token.pos_ == "VERB"])
 
    for ent in doc.ents:
      nombre = ent.text

    if(nombre != ''):
      return nombre
    else:
      return 'Lo siento, pero no he podido encontrar tu nombre.'

  async def setup(self):
    print("Hola!. Soy el agente encargado del Lenguaje Natural. Mi ID es \"{}\"".format(str(self.jid)))
    b = self.RecvBehav(2)
    template = Template()
    template.set_metadata("test1", "val1")
    self.add_behaviour(b, template)

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
