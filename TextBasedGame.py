# Ver.      Date          Author
# 1.3   Jan 8, 2024    Robert Portell
#
# This is a text based game that will print out everything
#
# Intro to Python, final project

import textwrap  # Imported so that I can wrap large texts so that  it doesn't disappear to the right.

room_colors = '\033[32m'
item_colors = '\033[34m'
end_colors = '\033[0m'
final_room = 'Cockpit'  # The last room that will be entered based off room name
direction_text = ('forward', 'right', 'back', 'left')  # Rather than hard code certain words, I moved them up here.

# The lists below contain the data for rooms contained in the following order:
# Room name, Connected Rooms, Room Description, Bool for the room's lock, the lock description, and the
# item needed to unlock the door.
# The room_lisr is a tuple containing lists for each room
rooms_list = (['Cockpit', ',,Corridor,', '', False, '', ''],
              ['Corridor', 'Cockpit,Armory,Research Room,Supply Room',
               f'You are in a narrow pathway with 4 doors and wires dangling from a broken terminal by the '
               f'{final_room} door. Blast marks are scattered along the hardened steel walls.',
               False, '', None],
              ['Armory', ',,,Corridor',
               'You see a vast array of broken armor and blasters scattered across the room.\n'
               'What ever happened to the ship must have triggered an explosion that damaged the armory.',
               True, 'Looks like it needs a key code.', 'Key Codes'],
              ['Supply Room', ',Corridor,,',
               'There are various supplies scattered across the room. You don\'t see much '
               'useful items.',
               False, '', None],
              ['Quarters', ',Research Room,,',
               'There is a single bunk in the corner of the room. There is not much in the way of decoration, just \n'
               'various clothing scattered across the room.',
               True, 'The door appears to be unpowered', 'Energy Cell'],
              ['Research Room', 'Corridor,Storage Bay,Engine Room,Quarters',
               'There are various monitors displayed across the room. A majority of them\n'
               ' are broken, while th rest seem to be displaying large amounts of data continuously.',
               True, 'Looks like the reservoir for the door hydraulics is empty.', 'Can of Hydraulics'],
              ['Storage Bay', ',,,Research Room',
               'There isn\'t much here except a single human sized case. There might be '
               'something \nuseful inside.',
               False, '', None],
              ['Engine Room', 'Research Room,,,', '',
               True, 'The door looks jammed, might need some tools', 'Multi-Tool'])

# The items_list is a dictionary with the room name for the key. Each entry has the item name followed by the item
# description
items_list = {
    'Supply Room': ('Can of Hydraulics', f'A can of hydraulic oil used in most machines.'),
    'Armory': ('Blaster', 'It\'s good to have some level of ability to fight.'),
    'player_item': ('Data Pad', 'Useful for when you don\'t have a functioning control panel.'),
    'Research Room': ('Multi-Tool', 'A tool for every purpose.'),
    'Storage Bay': ('Space Suit', 'Might provide some level of protection.'),
    'Engine Room': ('Energy Cell', 'Could be used to power up some electrical circuitry.'),
    'Quarters': ('Key Codes', f'These look like the key codes to the {final_room}')
}

# This tuple just contains separate large text for events that happen. The order doesn't matter.
scenes_list = (
    'You wake to a throbbing headache and no clue how you got here. You take your first look around the room you find '
    'yourself in. Looking around you appear to be on a space ship. Through a porthole monitor, you can see the '
    'hyperdrive stream. You need to find out how to get out of here.',
    '----------------------------------------------------------------------------------------------------------------',
    f'You approach the door to the {final_room}, pulling out your {item_colors}Multi-Tool{end_colors}, you open the '
    f'side panel of the door and refill the reserves from the {item_colors}Can of Hydraulics{end_colors}. Pulling out '
    f'your {item_colors}Data Pad{end_colors}, you initiate the door overrides with the {item_colors}Key Codes'
    f'{end_colors}. You find yourself in the {final_room}, ahead of you there is a man that turns to face you. He pulls'
    f' a blaster out and fires. The energy blast from the blaster is absorbed by your {item_colors}Space Suit'
    f'{end_colors}. You pull out your own {item_colors}Blaster{end_colors} and fire back. The man crumbles to the '
    f'ground. Approaching the console, you pull out your {item_colors}Multi-Tool{end_colors} to open the console. You '
    f'insert the {item_colors}Energy Cell{end_colors} into the console, restoring temporary power. With power restored'
    f', you have captured your first vessel. You journey as a pirate has just begun...'
)


class Room:
    def __init__(self, name, connected_rooms, description, lock, lock_description, lock_items):
        self.name = name  # Room name
        self.connected_rooms = connected_rooms.split(',')  # Stores 4 directions around room with blanks being walls
        self.description = description  # Room description for entering a room
        self.item = None  # All items are empty initially since I need to create item objects first
        self.lock = lock
        self.lock_description = lock_description
        self.lock_items = lock_items

    def get_color_room_name(self):
        return room_colors + self.name + end_colors

    def set_item(self, item):
        self.item = item

    def get_description(self):
        # Since there is only one item, can just have the room describe the one item in the room class
        room_description = '\n*' + self.get_color_room_name() + '*\n' + self.description
        return room_description

    def check_item(self):
        if self.item is not None:
            item_check = 'a ' + self.item.get_color_item_name() + ': ' + self.item.description
        else:
            item_check = 'no item.'
        return '\nThere is ' + item_check


class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description  # Use description for hints, maybe?

    def get_color_item_name(self):
        return item_colors + self.name + end_colors


class Player:
    def __init__(self, start_room):
        self.current_room = start_room  # Variable start room so that I can change it easily
        self.inventory = []  # Will just randomly store items based off of FIFO
        self.face = 2  # Face 'South', opposite of the final room.
        if 'player_item' in items_list:  # Checks if the player starts with an item and then adds it
            self.inventory.append(Item(items_list['player_item'][0], items_list['player_item'][1]))

    # Rotates the list of connections based off of the direction the player is facing.
    # Checks if there is anything there before moving.
    # If it is the final room, has a special function for that. Final room var is farther up.
    def move_rooms(self, direction):
        directions = map_directions()[direction_text.index(direction)]  # Store direction
        new_room_movement = self.current_room.connected_rooms[directions]  # Store new room location

        # Checks if there is no room connected in the direction
        if new_room_movement == '':
            print('There\'s a wall there, you can\'t go any farther')
            return ''

        # Checks if the room is locked
        elif rooms[new_room_movement].lock:
            for item in self.inventory:  # Loops through players items
                if rooms[new_room_movement].lock_items == item.name:  # Checks items name against lock requirements
                    rooms[new_room_movement].lock = False  # Unlocks door for the future.
                    print(f'{new_room_movement} unlocked')
                    break
            if rooms[new_room_movement].lock:  # Checks if it is still locked
                print(f'The {new_room_movement} is locked.')
                print(rooms[new_room_movement].lock_description)
                self.face = directions
                return ''

        # Checks if the room being entered is the final room
        elif self.current_room.connected_rooms[directions] == final_room:
            if len(self.inventory) == len(items_list):  # Checks if you have all items
                print('Final Boss')
            else:
                # Turns you to face the final room if you can't enter
                print(f'You can\'t enter there yet. You\'ll need all {len(items_list)} items.')
                self.face = directions
                return ''

        # Upon successfully entering room, faces the room from the direction entering
        print(f'You go {direction} and enter {rooms[new_room_movement].get_color_room_name()}.')
        self.face = directions
        return self.current_room.connected_rooms[directions]  # Stores new room as current room.

    # Gets item if it matches 3 char. If there is nothing, it will display that there is nothing to get
    # if there is an item it will match it to the item that was input into the command.
    def get_item(self, item_name):
        if self.current_room.item is None:
            print('There\'s nothing to get here.')
            return
        if item_name.lower() in self.current_room.item.name.lower():
            self.inventory.append(self.current_room.item)
            print("You picked up a " + self.current_room.item.get_color_item_name())
            self.current_room.item = None
        else:
            print(f"There is no {item_name} to pick up.")


# Rotates the numbers based on the direction the player is facing.
def map_directions():
    all_directions = [(0 + player.face) % 4,
                      (1 + player.face) % 4,
                      (2 + player.face) % 4,
                      (3 + player.face) % 4]
    return all_directions


def describe_directions(new_direction_numbers):
    # I spent too much time on this section. However, I wanted the remove the direction text from here and make
    # them into a global variable that I could change at will.
    connected_room_list = player.current_room.connected_rooms
    dead_end = 'bulkhead'
    new_direction_words = [dead_end, dead_end, dead_end, dead_end]

    for counter, new_direction_counter in enumerate(new_direction_numbers):
        if connected_room_list[new_direction_counter]:
            new_direction_words[counter] = room_colors + connected_room_list[new_direction_counter] + end_colors

    return ('Ahead of you is a {}, to your right is a {}, behind you is a {}, and to your left is a {}.'
            .format(*new_direction_words))


def setup_map():
    print(scenes_list[1])
    print('\n*' + textwrap.fill(scenes_list[0], 120))
    # Creates the items and puts them in a dictionary keyed to room names
    items = {i: Item(items_list[i][0], items_list[i][1]) for i in items_list}

    # room = []
    room_setup = {}
    for i in rooms_list:
        room = Room(*i)  # Create object for room
        room_setup[i[0]] = room  # Store room in a dictionary for easy access by name
        if i[0] in items:  # Check if there's an item for this room
            room.set_item(items[i[0]])  # Add item to room
    return room_setup


# This will be the first thing displayed after each loop
def print_menu():
    print(player.current_room.get_description())  # Call room description

    # Gets list of items and prints them
    print(f'List of commands: get #, {', '.join(direction_text)}, look around , inventory ,quit.\n')  # Command list


if __name__ == '__main__':

    rooms = setup_map()  # Set up rooms and items
    player = Player(rooms['Corridor'])  # Create the player

    # Main Game loop
    while True:
        print_menu()  # Print UI
        command = input("Enter Command:> ").lower().strip()
        print(scenes_list[1] + '\n')  # Prints a bunch of dashes to split dialogues
        command_length = len(command)

        if len(command) < 3:
            continue

        if command in direction_text:  # Player movement
            new_room = player.move_rooms(command)
            if new_room != '':
                player.current_room = rooms[new_room]
        elif command.startswith("get") and len(command) > 6:  # Item check and retrieval
            player.get_item(command[4:].strip())
        elif command in 'look around':
            print(describe_directions(map_directions()))  # Call the 4 directions
            print(player.current_room.check_item())
        elif command in 'inventory':
            if player.inventory:
                inventory_names = [item.get_color_item_name() for item in player.inventory]
                print('Current Inventory:', ', '.join(inventory_names))  # Lists items in inventory
            else:
                print('You are not carrying anything')
        elif command == "quit":  # Straight forward just ends the program
            print('The End')
            break
        else:
            print('Invalid command')  # Only displayed if other commands don't find anything.

        # Final Boss encounter
        if final_room == player.current_room.name or command == 'skip':
            print(textwrap.fill(scenes_list[2], 120))
            break
