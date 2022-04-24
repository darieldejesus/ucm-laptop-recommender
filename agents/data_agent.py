from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from spade.template import Template
from database import init_laptops, load_laptops_for_cluster, update_laptops_with_cluster
from pymongo import MongoClient
from bson.json_util import dumps, loads
from constants import actions
import config
import csv
import os

class DataAgent(Agent):
  class RecvIntelBehav(PeriodicBehaviour):
    async def run(self):
      msg_received = await self.receive()
      # print("Mensaje en DataAgente recibido!: {}".format(msg_received))
      if msg_received and msg_received.get_metadata("action") == actions.LOAD_LAPTOPS:
        list_laptops = load_laptops_for_cluster()

        msg_reply = Message(to=config.AGENT_INTEL_USER)
        msg_reply.set_metadata("action", actions.LOAD_LAPTOPS)
        msg_reply.body = dumps(list_laptops)

        await self.send(msg_reply)
      
      if msg_received and msg_received.get_metadata("action") == actions.UPDATE_LAPTOPS:
        print("He recibido la lista de laptops a actualizar")
        list_laptops = loads(msg_received.body)
        update_laptops_with_cluster(list_laptops)

  async def setup(self):
    print("Hola!. Soy el agente encargado de la Base de Datos. Mi ID es \"{}\"".format(str(self.jid)))

    # Cargamos DataSet a la DB
    init_laptops()

    recieveBehavior = self.RecvIntelBehav(period=0.1) # Recibir mensajes cada 0.1 seg
    template = Template()
    template.to = config.AGENT_DATA_USER
    template.sender = config.AGENT_INTEL_USER
    self.add_behaviour(recieveBehavior, template)

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
