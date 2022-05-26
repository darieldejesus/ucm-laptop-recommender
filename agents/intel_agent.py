from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour, TimeoutBehaviour
from spade.message import Message
from spade.template import Template
from constants import actions
from sklearn.cluster import KMeans
import datetime
import config
import json
import numpy

class RequestEntriesBehav(TimeoutBehaviour):
  async def run(self):
    print("Solicitando entradas para la inteligencia")
    msg = Message(to=config.AGENT_DATA_USER)
    msg.set_metadata("action", actions.LOAD_LAPTOPS)
    await self.send(msg)

class RecvDataBehav(PeriodicBehaviour):
  async def run(self):
    msg_received = await self.receive()
    
    if not msg_received:
      return
    
    """
    Obtener listas de computadores portatiles para obtener la listas de "cluster"
    y asigarlo a cada computador en la base de datos
    """
    if msg_received.get_metadata("action") == actions.LOAD_LAPTOPS:
      laptop_list = json.loads(msg_received.body)

      values = []
      for laptop in laptop_list:
        values.append([
          laptop["performance"],
          laptop["price"]
        ])

      measurable_props = numpy.array(values)
      kmeans = KMeans(n_clusters=5).fit(measurable_props)
      center_ids = kmeans.cluster_centers_
      predictions = kmeans.predict(measurable_props)

      center_inserts = []
      for center in center_ids:
        center_inserts.append({
          "performance": center[0],
          "price": center[1],
        })

      for index, laptop in enumerate(laptop_list):
        laptop_list[index]["cluster"] = int(predictions[index])
      
      msg = Message(to=config.AGENT_DATA_USER)
      msg.set_metadata("action", actions.UPDATE_LAPTOPS)
      msg.body = json.dumps(laptop_list)

      await self.send(msg)

class IntelAgent(Agent):
  async def setup(self):
    print("Hola!. Soy el agente encargado de la Inteligencia Artificial. Mi ID es \"{}\"".format(str(self.jid)))

    recv_data_behav = RecvDataBehav(period=0.1) # Recibir mensajes cada 0.1 seg
    template = Template()
    template.to = config.AGENT_INTEL_USER
    template.sender = config.AGENT_DATA_USER
    self.add_behaviour(recv_data_behav, template)

    start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
    solc_data_behav = RequestEntriesBehav(start_at=start_at)
    self.add_behaviour(solc_data_behav)

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
