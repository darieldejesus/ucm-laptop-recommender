from durable.lang import *
from constants import states, actions
from bson.json_util import loads

with ruleset('welcome'):
  @when_all(s.status == states.RESET) # @TODO: Procesar mensaje y detectar "salida"
  def reset(c):
    # print(">>>>>>>>> reset")
    c.s.status = ""
    c.s.action = actions.RESET

  @when_all(s.message == "salir") # @TODO: Procesar mensaje y detectar "salida"
  def salir_message(c):
    # print(">>>>>>>>> salir_message")
    c.s.prev_status = c.s.status
    c.s.status = states.CONFIRM_FINISH
    c.s.message = ""

  @when_all((s.status == states.CONFIRM_FINISH) & (s.message == ""))
  def confirm_finish(c):
    # print(">>>>>>>>> confirm_finish")
    c.s.reply = "Vamos. Veo que quieres terminar. ¿Es correcto?"
    c.s.status = states.CONFIRM_FINISH_ANSWER
  
  @when_all((s.status == states.CONFIRM_FINISH_ANSWER) & (s.message == "si")) # @TODO: Procesar mensaje y detectar "si"
  def confirm_finish_answer_yes(c):
    # print(">>>>>>>>> confirm_finish_answer_yes")
    c.s.reply = "Bueno. Fue un placer servirte.\n\n\n\n\n\n"
    c.s.status = ""
    c.s.action = actions.RESET

  @when_all((s.status == states.CONFIRM_FINISH_ANSWER) & (s.message == "no")) # @TODO: Procesar mensaje y detectar "si"
  def confirm_finish_answer_no(c):
    # print(">>>>>>>>> confirm_finish_answer_yes")
    c.s.reply = "Bueno. Pues continuamos.\n\n"
    c.s.status = c.s.prev_status
    c.s.prev_status = ""

  @when_all((s.status == states.CONFIRM_FINISH_ANSWER) & (s.message != "") & (s.message != "si") & (s.message != "no")) # @TODO: Procesar mensaje y detectar "no"
  def confirm_finish_unknown_reply(c):
    # print(">>>>>>>>> confirm_finish_unknown_reply")
    c.s.reply = 'No conozco esta respuesta. Por favor responder con un "si" o un "no".'
    c.s.message = ""

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
    c.s.reply = 'Disculpa, pero no he logrado identificar tu nombre.'
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
    c.s.reply = 'Disculpa, no he logrado identificar lo que buscas.'
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
    c.s.reply = 'A ver si estoy claro. Buscas un equipo para "{}" y tienes un presupuesto {}. ¿Estoy en lo correcto?'.format(
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
    c.s.reply = 'No conozco esta respuesta. Por favor responder con un "si" o un "no".'

  @when_all((s.status == states.LOOK_FOR_REQUIREMENTS) & (s.message == "") & (s.action != actions.LOOK_FOR_REQUIREMENT) & (s.action != actions.LOOK_FOR_REQUIREMENT_RESPONSE))
  def look_for_computer(c):
    print(">>>>>>>>> look_for_computer")
    c.s.response = ""
    c.s.reply = "Gracias por confirmar. Un momento por favor, estoy buscando que recomendar..."
    c.s.action = actions.LOOK_FOR_REQUIREMENT

  @when_all((s.status == states.LOOK_FOR_REQUIREMENTS) & (s.action == actions.LOOK_FOR_REQUIREMENT_RESPONSE) & (s.response != ""))
  def look_for_requirements_response(c):
    print(">>>>>>>>> look_for_requirements_response")
    response = loads(c.s.response)
    print("Parsed response!", response)
    if not response["found"]:
      c.s.reply = "No conozco esta categoria. Necesito tu ayuda para definirlo. :)"
      c.s.response = ""
      c.s.status = states.LOOK_FOR_EDGE_COMPUTERS
      return

    c.s.response = ""
    c.s.message = ""
    c.s.reply = ":) Tengo algunos equipos para lo que buscas"
    c.s.action = actions.LOOK_FOR_COMPUTERS_RECOMMEND
    c.s.status = states.RECOMMEND_COMPUTER
  
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
      option_message = (
        "Computadora #{}\n"
        "\tFabricante: {}\n"
        "\tModelo: {}\n"
        "\tCPU: {}\n"
        "\tGPU: {}\n"
        "\tRAM: {}GB\n"
        "\tDisco: {}\n"
        "\tPrecio: €{}\n\n"
      )
      laptops += option_message.format(
        index + 1,
        laptop["manufacturer"],
        laptop["model"],
        laptop["cpu"],
        laptop["gpu"],
        laptop["ram_size"],
        laptop["storage"],
        laptop["price"]
      )

    message = 'De estas computadoras, ¿Cuál es la más apropiada para "{}"? \n\n{}\n\nPor favor de responder con "1", "2", "3", "4" o "5".'.format(c.s.requirements, laptops)
    c.s.reply = message
    c.s.status = states.ASK_EDGE_COMPUTER
    c.s.action = ""

  @when_all((s.status == states.ASK_EDGE_COMPUTER) & (s.response != "") & (s.reply == "") & (s.message != "") & (s.action != actions.INSERT_REQUIREMENTS) & (s.action != actions.INSERT_REQUIREMENTS_RESPONSE))
  def show_edge_computers_response(c):
    print(">>>>>>>>> show_edge_computers_response")
    response = loads(c.s.response)
    answer = str(c.s.message)
    if not answer.isdigit() or not (int(answer) >= 1 and int(answer) <= 5):
      c.s.reply = 'No he logrado capturar tu respuesta. Por favor con responder con "1", "2", "3", "4" o "5".'
      c.s.message = ""
      return

    answer_index = int(answer) - 1
    # print("$$$$$$$$$$$$$$$$$ A seleccionar cluster", response["body"])
    # print("Tiene?", response["body"][answer_index])

    c.s.selected_cluster = response["body"][answer_index]["cluster"]
    c.s.response = ""
    c.s.action = actions.INSERT_REQUIREMENTS

  @when_all((s.status == states.ASK_EDGE_COMPUTER) & (s.reply == "") & (s.response != "") & (s.action == actions.INSERT_REQUIREMENTS_RESPONSE))
  def show_edge_computers_update(c):
    print(">>>>>>>>> show_edge_computers_update")
    response = loads(c.s.response)
    print("Parsed response!", response)
    if not response["success"]:
      # @TODO Asignar estado correspondiente
      c.s.reply = "No he completar el proceso que corresponde... algo esta mal :("
      c.s.response = ""
      c.s.message = ""
      return

    c.s.response = ""
    c.s.message = ""
    c.s.reply = "Gracias!. Acabo de aprender algo nuevo gracias a ti <3 :)\nAhora ya puedo recomendarte algunas computadoras para \"{}\"".format(c.s.requirements)
    c.s.status = states.RECOMMEND_COMPUTER
    c.s.action = actions.LOOK_FOR_COMPUTERS_RECOMMEND

  @when_all((s.status == states.RECOMMEND_COMPUTER) & (s.response != "") & (s.action == actions.LOOK_FOR_COMPUTERS_RECOMMEND_RESPONSE))
  def recommend_computer(c):
    print(">>>>>>>>> recommend_computer")
    response = loads(c.s.response)
    if not response["found"]:
      # @TODO Asignar estado correspondiente
      c.s.reply = "No he completar el proceso que corresponde... algo esta mal :("
      c.s.response = ""
      c.s.message = ""
      return
    
    laptops = ""
    for index, laptop in enumerate(response["body"]):
      option_message = (
        "Computadora #{}\n"
        "\tFabricante: {}\n"
        "\tModelo: {}\n"
        "\tCPU: {}\n"
        "\tGPU: {}\n"
        "\tRAM: {}GB\n"
        "\tDisco: {}\n"
        "\tPrecio: €{}\n\n"
      )
      laptops += option_message.format(
        index + 1,
        laptop["manufacturer"],
        laptop["model"],
        laptop["cpu"],
        laptop["gpu"],
        laptop["ram_size"],
        laptop["storage"],
        laptop["price"]
      )

    message = "Estas son algunas computadoras para \"{}\"\n\n{}. \n\n¡Espero haber ayudado. ¡Un placer!.\n\n\n\n".format(c.s.requirements, laptops)
    c.s.reply = message
    c.s.message = ""
    c.s.response = ""
    c.s.status = states.ASK_FOR_FEEDBACK

  @when_all((s.status == states.ASK_FOR_FEEDBACK) & (s.reply == ""))
  def ask_for_feedback(c):
    # print(">>>>>>>>> ask_for_feedback")
    c.s.reply = "Me gustaría conocer tu nivel de sastifacción. ¿Tienes un momento para responder?"
    c.s.status = states.ASK_FOR_FEEDBACK_WAIT_REPLY
    c.s.message = ""

  @when_all((s.status == states.ASK_FOR_FEEDBACK_WAIT_REPLY) & (s.message == "si"))
  def ask_for_feedback_reply_yes(c):
    # print(">>>>>>>>> ask_for_feedback_reply_yes")
    c.s.reply = "¡Excelente!\nDel 1 al 10, siendo 1 no satisfecho y 10 totalmente satisfecho.\n¿Qué tan satisfecho estas con el servicio que te he brindado?"
    c.s.status = states.FEEDBACK_SATISFACTION_WAIT
    c.s.message = ""

  @when_all((s.status == states.ASK_FOR_FEEDBACK_WAIT_REPLY) & (s.message == "no"))
  def ask_for_feedback_reply_no(c):
    # print(">>>>>>>>> ask_for_feedback_reply_no")
    c.s.reply = "Terminando sesión.\n\n\n"
    c.s.status = states.RESET

  @when_all((s.status == states.ASK_FOR_FEEDBACK_WAIT_REPLY) & (s.message != "") & (s.message != "si") & (s.message != "no"))
  def ask_for_feedback_reply_unknown(c):
    # print(">>>>>>>>> ask_for_feedback_reply_unknown")
    c.s.reply = 'No conozco esta respuesta. Por favor responder con un "si" o un "no".'
    c.s.status = states.ASK_FOR_FEEDBACK_WAIT_REPLY
    c.s.message = ""

  @when_all((s.status == states.FEEDBACK_SATISFACTION_WAIT) & (s.message != ""))
  def feedback_satisfaction_reply(c):
    # print(">>>>>>>>> feedback_satisfaction_reply")
    if str(c.s.message).isdigit() and int(c.s.message) >= 1 and int(c.s.message) <= 10:
      c.s.reply = 'Gracias por responder.\n'
      c.s.satisfaction = c.s.message
      c.s.status = ""
      c.s.action = actions.INSERT_SATISFACTION
    else:
      c.s.reply = 'No conozco esta respuesta. Por favor responder con un numero entre "1" y "10"'
      c.s.status = states.FEEDBACK_SATISFACTION_WAIT

    c.s.message = ""
  
  @when_all((s.action == actions.INSERT_SATISFACTION) & (s.response != ""))
  def feedback_satisfaction_reply_response(c):
    # print(">>>>>>>>> feedback_satisfaction_reply_response")
    response = loads(c.s.response)
    if response["count"] > 0:
      avg = round(response["avg"], 1)
      c.s.reply = "Seguiremos mejorando el servicio del asistente.\n\nCon {} usuarios que han valorado nuestro asistente, tenemos un promedio de satisfacción de {}.\n\n\n\n".format(response["count"], avg)
      c.s.response = ""
      c.s.action = actions.RESET
    else:
      c.s.response = ""
      c.s.action = actions.RESET
