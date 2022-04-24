from durable.lang import *
from constants import states, actions
from bson.json_util import loads

with ruleset('welcome'):
  @when_all(s.status == states.WELCOME)
  def say_hello(c):
    # print(">>>>>>>>> say_hello")
    c.s.status = states.ASK_NAME
    c.s.reply = 'Hola. Benvenido al sistema de recomendación de computadores portátiles :)'
    print(c.s.reply)

  @when_all((s.status == states.ASK_NAME) & (s.person == '') & (s.reply == ""))
  def ask_name(c):
    # print(">>>>>>>>> ask_name")
    c.s.status = states.NAME_ASKED
    c.s.reply = 'Me podrias decir cual es tu nombre?'
    print(c.s.reply)

  @when_all((s.status == states.ASK_NAME_AGAIN))
  def ask_name_again(c):
    # print(">>>>>>>>> ask_name_again")
    c.s.status = states.ASK_NAME
    c.s.reply = 'Dispulta, pero no he logrado identificar tu nombre.'
    print(c.s.reply)

  @when_all((s.status == states.NAME_ASKED) & (s.person == "") & (s.message != "") & (s.action != actions.EXTRACT_NAME))
  def name_asked(c):
    # print(">>>>>>>>> name_asked")
    c.s.action = actions.EXTRACT_NAME

  @when_all((s.status == states.NAME_ASKED) & (s.action == actions.EXTRACT_NAME) & (s.response != ""))
  def name_asked_response(c):
    # print(">>>>>>>>> name_asked_response")
    response = loads(c.s.response)
    print("Parsed response!", response)
    if not response["found"]:
      c.s.status = states.ASK_NAME_AGAIN
      c.s.response = ""
      return

    c.s.status = states.WELCOME_NAME
    c.s.person = response["body"]
    c.s.response = ""

  @when_all((s.status == states.WELCOME_NAME) & (s.person != '') & (s.reply == ""))
  def receive_name(c):
    # print(">>>>>>>>> receive_name")
    c.s.person = c.m.person
    c.s.status = 4
    c.s.reply = 'Oh, que bonito nombre!'
    print(c.s.reply)

  @when_all((s.status == 4) & (s.person != '') & (s.reply == ""))
  def say_goodbye(c):
    # print(">>>>>>>>> say_goodbye")
    c.s.status = 5
    c.s.reply = 'Un gusto conocerte, {0}!'.format(c.s.person)
    print(c.s.reply)

  # @when_all(s.status == 5)
  # def end(c):
  #   print(">>>>>>>>> end")
  #   c.s.status = -1
  #   c.s.reply = '** Terminando **'
  #   print(c.s.reply)
