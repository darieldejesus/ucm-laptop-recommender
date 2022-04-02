from durable.lang import *

with ruleset('welcome'):
  @when_all(s.status == 1)
  def say_hello(c):
    c.s.status = 2
    c.s.message = 'Hola. Benvenido al sistema de recomendación de computadores portátiles :)'
    print(c.s.message)

  @when_all((s.status == 2) & (s.person == ''))
  def ask_name(c):
    c.s.status = 3
    c.s.message = 'Me podrias decir cual es tu nombre?'
    print(c.s.message)

  @when_all((s.status == 3) & (s.person != ''))
  def receive_name(c):
    c.s.person = c.m.person
    c.s.status = 4
    c.s.message = 'Oh, que bonito nombre!'
    print(c.s.message)

  @when_all((s.status == 4) & (s.person != ''))
  def say_goodbye(c):
    c.s.status = 5
    c.s.message = 'Un gusto conocerte, {0}!'.format(c.s.person)
    print(c.s.message)

  @when_all(s.status == 5)
  def end(c):
    c.s.status = -1
    c.s.message = '** Terminando **'
    print(c.s.message)
