from spade.agent import Agent

class IntelAgent(Agent):
  async def setup(self):
    print("Hola!. Soy el agente encargado de la Inteligencia Artificial. Mi ID es \"{}\"".format(str(self.jid)))

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
