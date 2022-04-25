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
    c.s.status = states.ASK_REQUIREMENTS
    c.s.reply = 'Oh, que bonito nombre! Un gusto servirte, {0}!'.format(c.s.person)
    print(c.s.reply)

  @when_all((s.status == states.ASK_REQUIREMENTS) & (s.reply == ""))
  def ask_requirements(c):
    print(">>>>>>>>> ask_requirements")
    c.s.status = states.REQUIREMENTS_ASKED
    c.s.reply = "¿En que te puedo ayudar?"
    print(c.s.reply)
  
  @when_all((s.status == states.ASK_REQUIREMENTS_AGAIN) & (s.reply == ""))
  def ask_requirements_again(c):
    print(">>>>>>>>> ask_requirements_again")
    c.s.status = states.ASK_REQUIREMENTS
    c.s.reply = 'Dispulta, no he logrado identificar lo que buscas.'
    print(c.s.reply)

  @when_all((s.status == states.REQUIREMENTS_ASKED) & (s.message != "") & (s.action != actions.EXTRACT_REQUIREMENTS))
  def requirements_asked(c):
    print(">>>>>>>>> requirements_asked")
    c.s.action = actions.EXTRACT_REQUIREMENTS

  @when_all((s.status == states.REQUIREMENTS_ASKED) & (s.action == actions.EXTRACT_REQUIREMENTS) & (s.response != ""))
  def requirements_asked_response(c):
    print(">>>>>>>>> requirements_asked_response")
    response = loads(c.s.response)
    print("Parsed response!", response)
    if not response["found"]:
      c.s.status = states.ASK_REQUIREMENTS_AGAIN
      c.s.response = ""
      return

    c.s.status = states.CONFIRM_REQUIREMENTS
    c.s.requirements = response["body"]
    c.s.budget = 0
    c.s.response = ""
  
  @when_all((s.status == states.CONFIRM_REQUIREMENTS) & (s.message == ""))
  def confirm_requirements(c):
    print(">>>>>>>>> confirm_requirements")
    c.s.status = states.WAIT_CONFIRM_REQUIREMENTS
    norm_budget = "de €{} euros".format(c.s.budget)
    c.s.reply = 'A ver si estoy claro... buscas un equipo para "{}" y tienes un presupuesto {}. ¿Estoy correcto?'.format(
      c.s.requirements,
      norm_budget if c.s.budget else "inlimitado"
    )
    print(c.s.reply)
  
  @when_all((s.status == states.WAIT_CONFIRM_REQUIREMENTS) & (s.message != ""))
  def confirm_requirements_response(c):
    print(">>>>>>>>> confirm_requirements_response")
    if c.s.message.lower() == "no":
      c.s.status = states.ASK_REQUIREMENTS_AGAIN
      c.s.response = ""
      c.s.message = ""
      return
    
    if c.s.message.lower() == "si":
      c.s.status = states.LOOK_FOR_REQUIREMENTS
      c.s.response = ""
      c.s.message = ""
      return

    c.s.response = ""
    c.s.message = ""

  @when_all((s.status == states.LOOK_FOR_REQUIREMENTS) & (s.message == "") & (s.action != actions.LOOK_FOR_REQUIREMENT) & (s.action != actions.LOOK_FOR_REQUIREMENT_RESPONSE))
  def look_for_computer(c):
    print(">>>>>>>>> look_for_computer")
    c.s.action = actions.LOOK_FOR_REQUIREMENT
    c.s.reply = "Gracias por confirmar. Un momento por favor, estoy buscando que recomendar..."

  @when_all((s.status == states.LOOK_FOR_REQUIREMENTS) & (s.action == actions.LOOK_FOR_REQUIREMENT_RESPONSE) & (s.response != ""))
  def look_for_requirements_response(c):
    print(">>>>>>>>> look_for_requirements_response")
    response = loads(c.s.response)
    print("Parsed response!", response)
    if not response["found"]:
      c.s.reply = "No conozco esta categoria. Necesito tu ayuda para definirlo. :)"
      c.s.status = states.LOOK_FOR_EDGE_COMPUTERS
      c.s.response = ""
      return

    c.s.status = states.WELCOME
    c.s.requirements = response["body"]
    c.s.budget = 0
    c.s.response = ""
  
  @when_all((s.status == states.LOOK_FOR_EDGE_COMPUTERS) & (s.reply == "") & (s.action != actions.LOOK_FOR_EDGE_COMPUTERS) & (s.action != actions.LOOK_FOR_EDGE_COMPUTERS_RESPONSE))
  def look_for_edge_computers(c):
    print(">>>>>>>>> look_for_edge_computers")
    c.s.action = actions.LOOK_FOR_EDGE_COMPUTERS
    c.s.reply = "Estoy buscando unos equipos para saber cuál de ellos es mas apropiado para \"{}\"...".format(c.s.requirements)

  @when_all((s.status == states.LOOK_FOR_EDGE_COMPUTERS) & (s.action == actions.LOOK_FOR_EDGE_COMPUTERS_RESPONSE) & (s.response != ""))
  def look_for_edge_computers_response(c):
    print(">>>>>>>>> look_for_edge_computers_response")
    response = loads(c.s.response)
    print("Parsed response!", response)
    if not response["found"]:
      # @TODO Asignar estado correspondiente
      c.s.reply = "No he podido encontrar lo que busco... algo esta mal :("
      c.s.response = ""
      return
    c.s.status = states.SHOW_EDGE_COMPUTERS
    c.s.action = ""
  
  @when_all((s.status == states.SHOW_EDGE_COMPUTERS) & (s.response != "") & (s.reply == ""))
  def show_edge_computers(c):
    print(">>>>>>>>> show_edge_computers")
    response = loads(c.s.response)
    laptops = ""
    for index, laptop in enumerate(response["body"]):
      laptops += """Computadora #{}
      Fabricante: {}
      Modelo: {}
      CPU: {}
      GPU: {}
      RAM: {}GB
      Disco: {}\n\n
      """.format(
        index + 1,
        laptop["manufacturer"],
        laptop["model"],
        laptop["cpu"],
        laptop["gpu"],
        laptop["ram_size"],
        laptop["storage"]
      )
    message = "De estas computadoras, ¿Cuál es la más apropiada para \"{}\"? \n\n{}".format(c.s.requirements, laptops)
    c.s.reply = message
    c.s.status = states.ASK_EDGE_COMPUTER
    c.s.action = ""
    c.s.response = ""
