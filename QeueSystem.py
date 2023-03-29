
class Queue:
  def __init__(self, id, maxPlayers):
    self.id = id
    self.maxPlayers = maxPlayers

def create_new_queue( qMessageID, maxPlayers, activeQueues ):
    q = Queue(id = qMessageID, maxPlayers= maxPlayers)
    activeQueues.append(q)


def is_queue_message(id, activeQueues):
    for q in activeQueues:
      if q.id == id:
         return True
    return False

def get_player_rank(player):
    roles = set(player.roles)
    for role in [ "Diamond", "Platinum", "Gold", "Silver", "Bronze" ]:
        if role in roles:
            return role
    return "no rank"

def get_player_region(player):
    roles = set(player.roles)
    for role in [ "USE", "USW", "OCX", "EU" ]:
        if role in roles:
            return role
    return "no region selected"
