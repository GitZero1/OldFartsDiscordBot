
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
    rank = "no rank"
    if search_for_rank(player, "Bronze"):
        rank = "Bronze"
    
    if search_for_rank(player, "Silver"):
        rank = "Silver"
    
    if search_for_rank(player, "Gold"):
        rank = "Gold"
    
    if search_for_rank(player, "Platinum"):
        rank = "Platinum"
    
    if search_for_rank(player, "Diamond"):
        rank = "Diamond"
    
    return rank

def get_player_region(player):
    reg = "No reg selected"

    if search_for_Region(player, "USE"):
        reg = "USE"
    if search_for_Region(player, "USW"):
        reg = "USW"
    if search_for_Region(player, "OCX"):
        reg = "OCX"
    if search_for_Region(player, "EU"):
        reg = "EU"
    return reg

def search_for_rank(player, rank):
    for r in player.roles:
        if r.name == rank:
            return True
    return False

def search_for_Region(player, reg):
    for r in player.roles:
        if r.name == reg:
            return True
    return False
