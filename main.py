import uuid


class Game:
	def __init__(self):
		self.metadata = {}
		self.reset_game()

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
		if not isinstance(map, Map):
			return False
		self.map = map
		return self
	
	def get_map(self):
		return self.map
	
	def reset_map(self):
		self.map = False
	
	def reset_game(self):
		self.reset_map()
		self.player_ids = []
		self.players = []
		self.inventories = {}

class Player:
	def __init__(self):
		self.reset_player()
		self.id = 0

	def __eq__(self, other):  # equals
		if isinstance(other, Player):
			return other.get_id() == self.get_id()
		return False

	def set_inventory(self, inventory):
		self.inventory = inventory
		return self

	def set_location(self, location):
		self.location = location
		return self

	def set_game(self, game):
		self.game = game
		return self
	
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

	def get_move_choices(self):
		map = self.game.get_map()
		choices = map.get_connected_locations(self.location)
		choices.append(self.location)  # current location
		return choices

class Inventory:
	def __init__(self):
		self.items = {}
	
	def generate_item_id(self):
		while True:
			rand_id = uuid.uuid4().hex
			if rand_id not in self.items.keys():
				return rand_id

	def add_item(self, item):
		if not isinstance(item, Item):
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
		if isinstance(other, Item):
			return self.get_id() == other.get_id()
		return False

	def set_id(self, id):
		self.id = id
		return self

	def get_id(self):
		return self.id
	def reset_id(self):
		self.id = False

class Map:
	def __init__(self):
		self.allowed_locations = {}  # id: [id1, id2, id3], id2 ...
		self.locations = {}  # id: Location objects
		self.default_location = False
		self.name = ""

	def __str__(self):
		string = "Map {}, locations: {}"
		string = string.format(self.name, len(self.locations))
		return string

	def is_location(self, location):
		if not isinstance(location, Location):
			return False
		if not location.is_valid():
			return False

		return True

	def is_added_location(self, location):
		if not self.is_location(location):
			return False

		location_id = location.get_id()
		if location_id not in self.locations.keys():
			return False

		return location_id
			
	def add_location(self, location):
		if not self.is_location(location) or self.is_added_location(location):
			return False

		location_id = location.get_id()

		self.locations[location_id] = location
		self.allowed_locations[location_id] = []
		return self

	def connect_location(self, source, destinations, mirror=False):
		source_id = self.is_added_location(source)
		if not source_id:
			return False

		for dest in destinations:
			dest_id = self.is_added_location(dest)
			if not dest_id:
				return False

			if mirror and source_id not in self.allowed_locations[dest_id]:
				# destination -> source path, only on mirror == True
				self.allowed_locations[dest_id].append(source_id)

			if dest_id not in self.allowed_locations[source_id]:
				# source -> destination path
				self.allowed_locations[source_id].append(dest_id)
		return self

	def is_connected(self, source, destination):
		if not self.is_location(source):
			return False
		
		source_id = self.is_added_location(source)
		destination_id = self.is_added_location(destination)

		if not source_id or not destination_id:
			return False

		return destination_id in self.allowed_locations[source_id]

	def remove_location(self, location):
		removed_id = self.is_added_location(location)
		if not removed_id:
			return False

		self.locations.pop(removed_id)
		self.allowed_locations.pop(removed_id)
		for key, locations in self.allowed_locations.items():
			for index, l_id in enumerate(locations):
				if l_id == removed_id:
					self.allowed_locations[key].pop(index)
					continue  	
		location.reset_location()
		return self

	def get_locations(self):
		return self.locations.items()

	def get_connected_locations(self, source):
		source_id = self.is_added_location(source)
		if not source_id:
			return False

		destinations = []

		for dest_id in self.allowed_locations[source_id]:
			destinations.append(self.locations[dest_id])
		
		return destinations

	def set_default_location(self, location):
		location_id = self.is_added_location(location)
		if not location_id:
			return False

		self.default_location = location
		return self

	def get_default_location(self):
		return self.default_location

	def set_name(self, name):
		if not isinstance(name, str):
			return False
		self.name = name
		return self

	def get_name(self):
		return self.name

class Location:
	def __init__(self):
		"""
		name = name of location, map = pointer to parent Map
		"""
		self.reset_location()
		self.id = self.generate_id()

	def __eq__(self, other):
		if not isinstance(other, Location):
			return False
		return other.get_name() == self.get_name()
	
	def __str__(self):
		string = "Empty location"
		if self.name:
			string = "Location {}".format(self.name)
		return string
	
	def generate_id(self):
		rand_id = uuid.uuid4().hex
		return rand_id
	
	def get_id(self):
		return self.id

	def get_map(self):
		return self.map
	
	def set_map(self, map):
		if not isinstance(map, Map):
			return False
		self.map = map
		return self

	def reset_map(self):
		self.map = False
	
	def get_name(self):
		return self.name

	def set_name(self, name):
		if not isinstance(name, str):
			return False
		self.name = name
		return self
	
	def reset_name(self):
		self.name = ""

	def reset_location(self):
		self.reset_name()
		self.reset_map()	

	def is_valid(self):
		return self.name != ""

	def get_connected_locations(self):
		return self.map.get_connected_locations(self)

mapa = Map()
lokacja = Location().set_name("Lokacja")
szkola = Location().set_name("Szkola")
dom = Location().set_name("Dom")

#create_location_path
#is_path
mapa.set_name("Mapka")
mapa.add_location(lokacja).add_location(szkola).add_location(dom)
print(mapa.connect_location(szkola, [dom], True))
print(mapa.connect_location(lokacja, [szkola, dom]))
"""print(mapa)
print(mapa.is_connected(szkola, dom))  # True
print(mapa.is_connected(dom, szkola))  # True - mirrored
print(mapa.is_connected(szkola, lokacja)) # False
print(mapa.is_connected(lokacja, szkola)) # True
print(mapa.allowed_locations)
print(mapa.locations)
print(mapa.remove_location(dom))
print(mapa.locations)
print(mapa.allowed_locations)
print(mapa.remove_location(dom))  # false
print(mapa.add_location("Dupa"))"""
print(mapa.set_default_location(dom))
gra = Game()
gra.set_map(mapa)

gracz = Player()
gra.add_player(gracz)
gracz.get_move_choices()
