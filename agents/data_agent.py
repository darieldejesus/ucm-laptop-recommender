from spade.agent import Agent
from database import load_laptops
from pymongo import MongoClient
import pandas
import csv
import os

class DataAgent(Agent):
  async def setup(self):
    print("Hola!. Soy el agente encargado de la Base de Datos. Mi ID es \"{}\"".format(str(self.jid)))

    # Cargamos DataSet a la DB
    load_laptops()

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
