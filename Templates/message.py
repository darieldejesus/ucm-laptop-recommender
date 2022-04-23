from spade.message import Message
#-------------- probando spacy ------------------

async def EnviarMensaje(self, msg_body, receptor):
  msg = Message(to=str(receptor))
  msg.set_metadata("test1", "val1")
  msg.body=msg_body

  await self.send(msg)
  print("Message sent to {}".format(receptor))