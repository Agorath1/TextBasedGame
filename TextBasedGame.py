# Ver.      Date          Author
# 1.6   Jan 9, 2024    Robert P
#
# This is a text based game that will print out everything
#
# Intro to Python, final project

import time

# Global variables
room_colors = '\033[32m'
item_colors = '\033[34m'
end_colors = '\033[0m'
final_room = 'Cockpit'  # The last room that will be entered based off room name
start_room = 'Corridor'
direction_text = ('forward', 'right', 'back', 'left')  # Rather than hard code certain words, I moved them up here.

# The room_list is a dictionary
rooms_dict = {
    'Cockpit': {
        'connections': ['', '', 'Corridor', ''],
        'description': '',
        'requires_key': True,
        'lock_message': 'Looks like it needs a pass key to enter',
        'key_type': 'Key Codes'
    },
    'Corridor': {
        'connections': ['Cockpit', 'Armory', 'Research Room', 'Supply Room'],
        'description': f'You are in a narrow pathway with 4 doors and wires dangling from a broken terminal by the '
                       f'{final_room} door. Blast marks are scattered along the hardened steel walls.',
        'requires_key': False,
        'lock_message': '',
        'key_type': None
    },
    'Armory': {
        'connections': ['', '', '', 'Corridor'],
        'description': 'You see a vast array of broken armor and blasters scattered across the room.What ever happened'
                       ' to the ship must have triggered an explosion that damaged the armory.',
        'requires_key': True,
        'lock_message': 'Looks like it needs a key code.',
        'key_type': 'Key Codes'
    },
    'Supply Room': {
        'connections': ['', 'Corridor', '', ''],
        'description': 'There are various supplies scattered across the room. There aren\'t many items that are still '
                       'useful.',
        'requires_key': False,
        'lock_message': '',
        'key_type': None
    },
    'Quarters': {
        'connections': ['', 'Research Room', '', ''],
        'description': 'There is a single bunk in the corner of the room. There is not much in the way of decoration, '
                       'just various clothing scattered across the room.',
        'requires_key': True,
        'lock_message': 'The door appears to be unpowered',
        'key_type': 'Energy Cell'
    },
    'Research Room': {
        'connections': ['Corridor', 'Storage Bay', 'Reactor Room', 'Quarters'],
        'description': 'There are various monitors displayed across the room. A majority of them are broken, while '
                       'the rest seem to be displaying large amounts of data continuously.',
        'requires_key': True,
        'lock_message': 'Looks like the reservoir for the door hydraulics is empty.',
        'key_type': 'Can of Hydraulics'
    },
    'Storage Bay': {
        'connections': ['', '', '', 'Research Room'],
        'description': 'There isn\'t much here except a single human sized case. There might be something useful '
                       'inside.',
        'requires_key': False,
        'lock_message': '',
        'key_type': None
    },
    'Reactor Room': {
        'connections': ['Research Room', '', '', ''],
        'description': 'There is what appears to the reactor, however you are no engineer so you pay no further '
                       'attention.',
        'requires_key': True,
        'lock_message': 'The door looks jammed, might need some tools',
        'key_type': 'Multi-Tool'
    }
}

# The items_list is a dictionary with the room name for the key. Each entry has the item name followed by the item
# description
items_list = {
    'Supply Room': (
        'Can of Hydraulics',
        'A can of hydraulic oil used in most machines.'
    ),
    'Armory': (
        'Blaster',
        'It\'s good to have some level of ability to fight.'
    ),
    'player_item': (
        'Data Pad',
        'Useful for when you don\'t have a functioning control panel.'
    ),
    'Research Room': (
        'Multi-Tool',
        'A tool for every purpose.'
    ),
    'Storage Bay': (
        'Space Suit',
        'Might provide some level of protection.'
    ),
    'Reactor Room': (
        'Energy Cell',
        'Could be used to power up some electrical circuitry.'
    ),
    'Quarters': (
        'Key Codes',
        f'These look like the key codes to the {final_room}'
    )
}

# This tuple just contains separate large text for events that happen. The order doesn't matter.
scenes_list: list[str] = [
    'Space Pirate Attack.\n',
    f'Collect all {len(items_list)} items to complete the adventure.\n\n',
    '\"You wake to a throbbing headache and no clue how you got here. You take your first look around the room you '
    'find yourself in. Looking around you appear to be on a space ship. Through a porthole monitor, you can see the '
    'hyperdrive stream. You need to find out how to get out of here.\"',
    '\\-------------------------------------------------------------------------------------------------------------\\',
    f'You enter the {final_room}. Across from you is a man tapping away at a console while alarms are ringing in the '
    f'background. As you approach, the man suddenly turns and fires at you. You attempt to dodge but you are still '
    f'hit. ',
    f'The damage is absorbed by the {item_colors}Space Suit{end_colors}. With a grunt, you reach down to '
    f'your {item_colors}Blaster{end_colors}. ',
    f'Pulling out your blaster, you fire back causing the man to crumble to the ground. You successfully captured you '
    f'first ship! Your life as a space pirate has just begun.',
    f'You crumble to the ground as the blast hits your unprotected body. ',
    f'You find nothing, the man fires again. The {item_colors}Space Suit{end_colors} fails to absorb the damage. '
]


class Room:
    def __init__(self, name, connected_rooms, description, lock, lock_description, lock_items):
        self.name = name  # Room name
        self.connected_rooms = connected_rooms  # Stores 4 directions around room with blanks being walls
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
    def __init__(self, start_room_class):
        self.current_room = start_room_class  # Variable start room so that I can change it easily
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
            print_slower('There\'s a wall there, you can\'t go any farther')
            return ''

        # Checks if the room is locked
        elif class_room_list[new_room_movement].lock:
            for item in self.inventory:  # Loops through players items

                # Checks items name against lock requirements
                if class_room_list[new_room_movement].lock_items == item.name:
                    class_room_list[new_room_movement].lock = False  # Unlocks door for the future.
                    print_slower(f'{new_room_movement} unlocked')
                    break
            if class_room_list[new_room_movement].lock:  # Checks if it is still locked
                print_slower(f'The {new_room_movement} is locked.')
                print_slower(class_room_list[new_room_movement].lock_description)
                self.face = directions
                return ''

        # Upon successfully entering room, faces the room from the direction entering
        print_slower(f'You go {direction} and enter {class_room_list[new_room_movement].get_color_room_name()}.')
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
            print(f"There is no {item_name[:30]} to pick up.")


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
    print(scenes_list[3])  # Prints a line break
    print_slower(scenes_list[0])
    print_slower(scenes_list[1])
    print_slower(scenes_list[2] + '\n')  # Prints the opening scene
    help_menu()
    # Creates the items and puts them in a dictionary keyed to room names
    items = {i: Item(items_list[i][0], items_list[i][1]) for i in items_list}

    room_setup = {}
    for room_name, room_data in rooms_dict.items():
        room = Room(room_name, room_data['connections'], room_data['description'],
                    room_data['requires_key'], room_data['lock_message'], room_data['key_type'])

        room_setup[room_name] = room  # Store room in a dictionary for easy access by name
        if room_name in items:  # Check if there's an item for this room
            room.set_item(items[room_name])  # Add item to room
    return room_setup


# Based on map setup, you have to get all items but the blaster and space suit. So I just lock it with the last item
def good_ending():
    print_slower(scenes_list[4] + scenes_list[5] + scenes_list[6])
    print('\n You win! Thanks for playing my game developed for SNHU Introduction to Scripting. Hope you enjoyed it.')


def bad_ending(space_suit_value):  # Assumes that either blaster or space suit is false, so I only need one of those.
    if space_suit_value is False:
        print_slower(scenes_list[4] + scenes_list[7])
    else:
        print_slower(scenes_list[4] + scenes_list[5] + scenes_list[8])
    print('\nGAME OVER. Try to collect all items next time.')


def help_menu():
    print(f'List of commands: \nget #, {', '.join(direction_text)}, look around , inventory ,help, quit.\n')


def print_slower(text_output):
    letter_counter = 0
    letter_number = 0
    while letter_number < len(text_output):
        if (letter_counter >= 120 and text_output[letter_number] == " ") or text_output[letter_number] == '\n':
            print('')
            letter_counter = 0
            letter_number += 1
        elif text_output[letter_number] == '\033':
            # Handle ANSI escape code
            start = letter_number
            letter_number += 1
            while letter_number < len(text_output) and text_output[letter_number] not in ('m', 'H', 'J', 'K'):
                letter_number += 1
            # Print the entire escape code without delay
            print(text_output[start:letter_number + 1], end='', flush=True)
            letter_number += 1  # Skip the last character of the escape code
        else:
            print(text_output[letter_number], end="", flush=True)
            letter_number += 1
            letter_counter += 1
            time.sleep(0.00)
    print()


def main_loop():
    while True:
        print_slower(player.current_room.get_description())
        player_command = input("\nEnter Command:> ").lower().strip()
        print(scenes_list[3] + '\n')  # Prints a bunch of dashes to split dialogues

        if len(player_command) < 3:
            continue

        if player_command in direction_text:  # Player movement
            new_room = player.move_rooms(player_command)
            if new_room != '':
                player.current_room = class_room_list[new_room]
        elif player_command == 'get #':
            print('Please replace the # with the item name you wish to pick up.')
        elif player_command.startswith("get") and len(player_command) > 6:  # Item check and retrieval
            player.get_item(player_command[4:].strip())
        elif player_command in 'look around':
            print_slower(describe_directions(map_directions()))  # Call the 4 directions
            print_slower(player.current_room.check_item())
        elif player_command in 'inventory':
            if player.inventory:
                inventory_names = [item.get_color_item_name() for item in player.inventory]
                print('Current Inventory:', ', '.join(inventory_names))  # Lists items in inventory
            else:
                print('You are not carrying anything')
        elif player_command == 'help':
            help_menu()
        elif player_command == 'quit':  # Straight forward just ends the program
            print('The End')
            break
        else:
            print('Invalid command')  # Only displayed if other commands don't find anything.

        # Final Boss encounter
        if final_room == player.current_room.name or player_command == 'skip':
            space_suit = False
            blaster = False
            for item in player.inventory:
                if item.name == 'Space Suit' or item.name == 'Blaster':
                    space_suit = True
                if item.name == 'Blaster':
                    blaster = True
            if space_suit and blaster:
                good_ending()
            else:
                bad_ending(space_suit)
            break


if __name__ == '__main__':
    class_room_list = setup_map()  # Set up rooms and items
    player = Player(class_room_list[start_room])  # Create the player
    main_loop()
    # Main Game loop
