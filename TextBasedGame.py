# Robert Portell IT 140 SNHU
# Intro to Python, final project

rooms_list = [
    ['Cockpit', ',,Corridor,', ''],
    ['Corridor', 'Cockpit,Armory,Research Room,Supply Room',
     'You see a narrow pathway with 4 doors and wires scars along the hardened steel walls.'],
    ['Armory', ',,,Corridor',
     'You enter the armory. You see a vast array of broken armor and blasters scattered across the room.What ever \n'
     'happened to the ship must have triggered an explosion that damaged the armory.'],
    ['Supply Room', ',Corridor,,',
     'You enter the supply room. There are various supplies scattered across the room. You don\'t see much useful '
     'items.'],
    ['Quarters', ',Research Room,,',
     'There is a single bunk in the corner of the room. There is not much in the way of decoration, just various \n'
     'clothing scattered across the room.'],
    ['Research Room', 'Corridor,Storage Bay,Engine Room,Quarters',
     'You enter the research room. There are various monitors displayed across the room. A majority of them are \n'
     'broken, while th rest seem to be displaying larges amount of data continuously.'],
    ['Storage Bay', ',,,Research Room',
     'You enter the storage bay. There isn\'t much here except a single human sized case. There might be something \n'
     'useful inside.'],
    ['Engine Room', 'Research Room,,,', '']
]

items_list = {
    'Supply Room': ('Can of Hydraulics', ''),
    'Armory': ('Blaster', ''),
    'Quarters': ('Data Pad', ''),
    'Research Room': ('Multi-Tool', ''),
    'Storage Bay': ('Space Suit', ''),
    'Engine Room': ('Energy Cell', '')
}

scenes_list = [
    'You wake to a throbbing headache and no clue how you got here. You take your first look around the room you find '
    'yourself in.',
    '----------------------------------------------------------------------------------------------------------------'
]


class Room:
    def __init__(self, name, connected_rooms, description):
        self.name = name  # Room name
        self.connected_rooms = connected_rooms.split(',')  # Stores 4 directions around room with blanks being walls
        self.description = description  # Room description for entering a room
        self.item = None  # All items are empty initially since I need to create item objects first

    def get_name(self):
        return '\033[32m' + self.name + '\033[0m'

    def set_item(self, item):
        self.item = item

    def get_description(self):
        # Since there is only one item, can just have the room describe the one item in the room class
        room_description = '\n*' + self.get_name() + '*\n' + self.description
        if self.item is not None:
            item_check = 'a ' + self.item.get_item_name()
            room_description += '\nThere is ' + item_check + ' here.'
        return room_description


class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description  # Use description for hints, maybe?

    def get_item_name(self):
        return '\033[31m' + self.name + '\033[0m'


class Player:
    def __init__(self, start_room):
        self.current_room = start_room  # Variable start room so that I can change it easily
        self.inventory = []  # Will just randomly store items based off of FIFO
        self.face = 2

    # Will probably rewrite this later
    def move_rooms(self, direction):
        # directions = dict(forward=((0 + self.face) % 4),
        #                   right=((1 + self.face) % 4),
        #                   backward=((2 + self.face) % 4),
        #                   left=((3 + self.face) % 4))

        directions = map_directions(direction)[direction]
        if self.current_room.connected_rooms[directions] == '':
            print('There\'s a wall there, you can\'t go any farther')
            return ''
        else:
            self.face = directions
            return self.current_room.connected_rooms[directions]

    # Maybe add a check for if the item is not there?
    def get_item(self, item_name):
        if self.current_room.item is None:
            print('There\'s nothing to get here.')
            return
        if item_name in self.current_room.item.get_item_name().lower():
            self.inventory.append(self.current_room.item)
            print("You picked up a " + self.current_room.item.get_item_name())
            self.current_room.item = None
        else:
            print(f"There is no \033[31m{item_name}\033[0m to pick up.")


def map_directions(directions):
    all_directions = dict(forward=((0 + player.face) % 4),
                          right=((1 + player.face) % 4),
                          backward=((2 + player.face) % 4),
                          left=((3 + player.face) % 4))
    return all_directions


def describe_directions(all_directions):
    room = player.current_room.connected_rooms

    forward_room = (room[all_directions['forward']] if room[all_directions['forward']] else "bulkhead")
    left_room = (room[all_directions['left']] if room[all_directions['left']] else "bulkhead")
    right_room = (room[all_directions['right']] if room[all_directions['right']] else "bulkhead")
    backward_room = (room[all_directions['backward']] if room[all_directions['backward']] else "bulkhead")

    return ('Ahead of you is a \033[32m{}\033[0m, to your left is a \033[32m{}\033[0m, to your right is a '
            '\033[32m{}\033[0m, and behind you is a \033[32m{}\033[0m.').format(
        forward_room,
        left_room,
        right_room,
        backward_room
    )


def setup_Map():
    # Creates the items and puts them in a dictionary keyed to room names
    items = {i: Item(items_list[i][0], items_list[i][1]) for i in items_list}

    room = []
    room_setup = {}
    for i in rooms_list:
        room = Room(i[0], i[1], i[2])  # Create object for room
        room_setup[i[0]] = room  # Store room in a dictionary for easy access by name
        if i[0] in items:  # Check if there's an item for this room
            room.set_item(items[i[0]])  # Add item to room
    return room_setup


def initialize():
    # print more opening stuff
    print('\n*' + scenes_list[0])


# This will be the first thing displayed after each loop
def print_menu():
    print(player.current_room.get_description())
    print(describe_directions(map_directions(player.face)))
    if player.inventory:
        inventory_names = [item.get_item_name() for item in player.inventory]
        print('Inventory:', ', '.join(inventory_names))
    print('List of commands: get #, forward, backward, left, right, quit.')


initialize()
rooms = setup_Map()
player = Player(rooms['Corridor'])  # Create the player
# Game loop
while True:
    print_menu()
    command = input("Enter Command:> ").lower()
    print(scenes_list[1] + '\n\n')
    command_length = len(command)

    if command in ['forward', 'backward', 'left', 'right']:
        new_room = player.move_rooms(command)
        if new_room != '':
            player.current_room = rooms[new_room]
    elif command.startswith("get") and len(command) > 6:
        player.get_item(command[4:].strip())
    # elif command == "inspect":
    #     print_menu()
    elif command == "quit":
        break
    else:
        print('Invalid command')
