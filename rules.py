from durable.lang import *
from enum import Enum
import rules.welcome

class Status(Enum):
  HELLO = 1
  PRESENT = 2
  GOODBYE = 3
  END = 4

INITIAL_CONTEXT = {
  'status': 1,
  'person': '',
  'message': '',
}

update_state('welcome', INITIAL_CONTEXT)
state = get_state('welcome')

state['person'] = 'Dariel de Jesus'
post('welcome', state)

state = get_state('welcome')
#update_state('welcome', state)
print(state)
#post('welcome', { 'person': 'Dariel de Jesus' })
#post('welcome', { 'person': 'Juan Perez' })
