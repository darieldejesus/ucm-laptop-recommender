from spade.message import Message

async def SendM(self, msg_body, receptor):
  msg = Message(to=receptor)
  msg.set_metadata("test1", "val1")
  msg.body=msg_body

  await self.send(msg)
  print("Message sent to {}".format(receptor))
 