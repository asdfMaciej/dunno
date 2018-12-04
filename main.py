import uuid


class Game:
	def __init__(self):
		self.reset_map()
		self.players = []
		self.player_ids = []
		self.metadata = {}
		self.inventories = {}

	def add_player(self, player):
		if player.game:
			return False
		if player.get_id() in self.player_ids:
			return False

		self.attach_player(player)
		for id, inventory in self.inventories.items():
			if id == player.get_id():
				player.set_inventory(inventory)
				break

		self.player_ids.append(player.get_id())
		return True

	def remove_player(self, to_remove_player):		
		for pos, player in enumerate(self.players):
			if player == to_remove_player:
				player_id = player.get_id()
				self.deattach_player(player) 
				self.players.pop(pos)
				self.player_ids.remove(player_id)
				return True

	def deattach_player(self, player):
		player.reset_player()

	def attach_player(self, player):
		location = self.map.get_default_location()
		empty_inventory = Inventory()

		player.set_game(self)
		player.set_location(location)
		player.set_inventory(empty_inventory)

	def set_map(self, map):
		if not isinstance(map, type(Map)):
			return False
		self.map = map
		return True
	
	def get_map(self):
		return self.map
	
	def reset_map(self):
		self.map = False

class Player:
	def __init__(self):
		self.reset_player()
		self.id = 0

	def __eq__(self, other):  # equals
		if isinstance(other, type(Player)):
			return other.get_id() == self.id
		return False

	def set_inventory(self, inventory):
		self.inventory = inventory
	def set_location(self, location):
		self.location = location
	def set_game(self, game):
		self.game = game
	
	def reset_inventory(self):
		self.inventory = False
	def reset_location(self):
		self.location = False
	def reset_game(self):
		self.game = False
	
	def reset_player(self):
		self.reset_inventory()
		self.reset_location()
		self.reset_game()

	def get_id(self):
		return self.id

class Inventory:
	def __init__(self):
		self.items = {}
	
	def generate_item_id(self):
		while True:
			rand_id = uuid.uuid4().hex
			if rand_id not in self.items.keys():
				return rand_id

	def add_item(self, item):
		if not isinstance(item, type(Item)):
			return False
		item_id = self.generate_item_id()
		item.set_id(item_id)
		self.items[item_id] = item
		return item_id

	def remove_item(self, item_id):
		if not item_id in self.items.keys():
			return False
		
		item = self.items.pop(item_id)
		item.reset_id()
		return item

	def get_items(self):
		return self.items.values()

class Item:
	def __init__(self):
		self.reset_id()
	
	def __eq__(self, other):
		if self.id == False:
			return False
		if isinstance(other, type(Item)):
			return self.id == other.get_id()
		return False

	def set_id(self, id):
		self.id = id
	def get_id(self):
		return self.id
	def reset_id(self):
		self.id = False

class Map:
	def get_locations(self):
		pass
	def get_default_location(self):
		pass
	pass

class Location:
	def get_map(self):
		pass

	pass


