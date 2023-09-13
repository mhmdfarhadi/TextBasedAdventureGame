import operator
import time 
from time import sleep , perf_counter
import random
from collections import deque
import os
import sys
import random
import threading
import math


CONVERSION_FACTOR = 60  # 1 minute in real-time is 60 seconds in game-time
class Player:
    def __init__(self):
        self.health = 100
        self.high_temperature_threshold = 450
        self.low_temperature_threshold = -70
        self.humidity_threshold = 40
        self.pressure_threshold = 70

class TimeThread(threading.Thread):
    def __init__(self, time_scale):
        super().__init__()
        self.game_time = 0
        self.day_night_cycle = "Night"
        self.time_scale = time_scale  # Time scale factor for speeding up game-time
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            time.sleep(1 / self.time_scale)  # Adjusted sleep duration
            
            self.game_time += 1
            self.toggle_day_night_cycle()

    def toggle_day_night_cycle(self):
        current_hour = (self.game_time // (CONVERSION_FACTOR * 60)) % 24
        if 6 <= current_hour < 18:
            self.day_night_cycle = "Day"
        else:
            self.day_night_cycle = "Night"
            
class Map:
    def mini_map_func(currentRoom):
        mini_map = [['   ' for _ in range(3)] for _ in range(3)]
        mini_map[1][1] = " ☻ "
        # Check and update mini-map based on adjacent rooms
        if currentRoom.north is not None:
            mini_map[0][1] = " * " if currentRoom.north.item is not None else " ○ "
        if currentRoom.south is not None:
            mini_map[2][1] = " * " if currentRoom.south.item is not None else " ○ "
        if currentRoom.west is not None:
            mini_map[1][0] = "*  " if currentRoom.west.item  is not None else "○  "
        if currentRoom.east is not None:
            mini_map[1][2] = "  *" if currentRoom.east.item  is not None else "  ○"
        
        # Check and update mini-map based on diagonal rooms
        if currentRoom.north is not None:
            if currentRoom.north.west is not None:
                mini_map[0][0] = "*  " if currentRoom.north.west.item is not None else "○  "
            if currentRoom.north.east is not None:
                mini_map[0][2] = "  *" if currentRoom.north.east.item is not None else "  ○"
        if currentRoom.south is not None:
            if currentRoom.south.west is not None:
                mini_map[2][0] = "*  " if currentRoom.south.west.item is not None else "○  "
            if currentRoom.south.east is not None:
                mini_map[2][2] = "  *" if currentRoom.south.east.item is not None else "  ○"
        
        # Update the current room's marker
        mini_map[1][1] = " ◙ " if currentRoom.item is not None else " ☻ "
        
        for row in mini_map:
            ''.join(row)
        return mini_map

    def display_mini_map(mini_map):
        box_width = len(mini_map[0]) * 3 + 2
        box_height = len(mini_map) + 2
        
        print("┌" + "─"*math.floor(box_width/2) +"N" + "─"*math.floor(box_width/2)+ "┐")
        
        for i, row in enumerate(mini_map):
            row_text = " ".join(row)
            if i == math.floor(box_height/2) - 1:
                print("W" + row_text + "E")
            else:
                print("│" + row_text + "│")
        
        print("└" + "─"*math.floor(box_width/2) +"S" + "─"*math.floor(box_width/2) + "┘")
    
class Room:
    def __init__(self,data):
        self.data         = data
        self.north        = None
        self.west         = None
        self.east         = None
        self.south        = None
        self.locked       = False
        self.key          = None
        self.item         = None
        self.room_objects = []
        self.room_objects_shower = []
        self.lights       = True
        self.temperature  = 50
        self.pressure     = 8
        self.humidity     = 10
        self.lever        = None
        self.terminal     = None
        
    def change_env(self,time_factor):
        if time_factor == 'Day':
            self.temperature  = math.floor(random.gauss(60,20))
            self.pressure     = math.floor(random.gauss(16,5))
            self.humidity     = math.floor(random.gauss(10,5))
        if time_factor == 'Night':
            self.temperature  = math.floor(random.gauss(-40,50))
            self.pressure     = math.floor(random.gauss(10,5))
            self.humidity     = math.floor(random.gauss(15,4))

    def make_room(self,north,west,east,south):
        self.north     = north
        self.west      = west
        self.east      = east
        self.south     = south

    def give_info(self,info):
        self.info      = info

    def make_key(self,key):
        self.key       = key
    
    def create_grid(rows, cols):
        grid = [[None for _ in range(cols)] for _ in range(rows)]
        for row in range(rows):
            for col in range(cols):
                room_name = f"Room ({row}, {col})"
                grid[row][col] = Room(room_name)
        return grid
    
    def connect_rooms(grid):
        rows = len(grid)
        cols = len(grid[0])
        
        for row in range(rows):
            for col in range(cols):
                if row > 0:
                    grid[row][col].north = grid[row - 1][col]
                if row < rows - 1:
                    grid[row][col].south = grid[row + 1][col]
                if col > 0:
                    grid[row][col].west = grid[row][col - 1]
                if col < cols - 1:
                    grid[row][col].east = grid[row][col + 1]

class RoomObject:
     def __init__(self,name):
          self.data        = name
          self.hidable     = False
          self.key         = None
          self.room        = None
          self.hidden_door = False
          self.usable      = False

class Key:
    def __init__(self,name):
        self.data   = name
        self.room   = None #key belongs to which room(which room is an object to Room class)
        
class Item:
    def __init__(self,data):
         self.data = data
         self.usable = False

class Lever:
    def __init__(self):
        self.room      = None
        self.open_room = None
        self.locked    = True    
        

class Terminal:
    def __init__(self,name):
        self.name        = name
        self.room        = None
        self.password    = None
        self.locked_room = None
        

class Control:
    def print_slowly(text, delay=0.03):
        try:
            for char in text:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)
            print()
        except KeyboardInterrupt:
            print(text)

    def print_slowly_advanced(text, char_delay=0.02, punct_delay=0.1, keyword=None):
        for line in text.split('\n'):
            for char in line:
                print(char, end='', flush=True)
                delay = char_delay + random.uniform(-0.01, 0.01)  # Add a small variation
                time.sleep(delay)
                
                if keyword and char.lower() in keyword.lower():
                    time.sleep(0.05)  # Pause slightly on keyword characters
            
            if char in '.?!':
                delay = punct_delay + random.uniform(-0.05, 0.05)  # Add variation
                time.sleep(delay)
            
            print()  # Move to the next line

    def input_manager(main_input):    
        try:
                if operator.contains(main_input,' '):#if input is two word
                    input1,input2 = main_input.split(' ')
                    command = input1.lower()
                    subject = input2.lower()
                    return command , subject
                else: #if input is one word
                    command = main_input.lower()
                    subject = None
                    return command , subject
        except ValueError: #for some erroe handling returns something that has no meaning
                Control.print_slowly("too many input, input should be one or two part seperated by space")
                command = "gibberish" #this is literal giberish!
                subject = "gibberish" #this is literal giberish!
                return command, subject
                
    """def search_for_player(player_room,player_visibility):
        while queue:
            time.sleep(4)
            room = None

            
            if queue:
                room = queue.popleft()

            if room is not None:
                Control.print_slowly(f"ghost is in {room.data}")

            
                if room == player_room and player_visibility:
                    Control.print_slowly(f"ghost found you in {room.data}!")
                    break

                visited.add(room)

                for next_room in [room.north, room.south, room.east, room.west]:
                    if next_room and next_room not in visited:
                        queue.append(next_room)
                        Control.print_slowly(f"ghost is searching for you...")
        else:
            Control.print_slowly("ghost didn't find you")"""
        
    def go_command(subject, currentRoom, player_stunt,inventory,flashlight,flashlight_button):
            if player_stunt == False :  
                #verifyng which direction player gave  
                if subject == "south": 
                    currentRoom = Control.move(currentRoom, 's',inventory,flashlight,flashlight_button)
                elif subject == "north":
                    currentRoom = Control.move(currentRoom, 'n',inventory,flashlight,flashlight_button)
                elif subject == "east":
                    currentRoom = Control.move(currentRoom, 'e',inventory,flashlight,flashlight_button)
                elif subject == "west":
                    currentRoom = Control.move(currentRoom, 'w',inventory,flashlight,flashlight_button)
                else:
                        Control.print_slowly("invalid direction, directions should be north, west, east or south")
            else:
                Control.print_slowly("you can't move right now")    
            return currentRoom

    def take_command(subject, currentRoom,inventory,inventory_storage,inventory_shower, player_stunt):
        if player_stunt == False:
            try:
                    if subject == currentRoom.item.data :#if asked item is available in current room
                        if Control.inventory_stats(inventory,inventory_storage) == 0:#check if inventory has space
                            Control.print_slowly("your inventory is full")
                        else:
                            inventory.append(currentRoom.item)#put item in inventory
                            inventory_shower.append(currentRoom.item.data)
                            Control.print_slowly(f"{currentRoom.item.data} is added to your inventory")
                            currentRoom.item = None
                    else:
                        Control.print_slowly(f"there is no item as {subject} in this room")
                    
            except :   
                    Control.print_slowly(f"there is no item as {subject} in this room")
        else:
            Control.print_slowly("you are stunt, you can't take right now")

    def look_command(subject,inventory_shower,currentRoom,player_stunt,look_describtion,flashlight_button):
        if player_stunt == False:
            if flashlight_button == False and currentRoom.lights == False:#check if there is light in room
                Control.print_slowly("you can't see shit")
            else:    
                try:
                    if operator.contains(inventory_shower, subject):#if asked item is in inventory
                        Control.print_slowly(look_describtion[subject])
                    elif subject == currentRoom.item.data :#if asked item is in current room
                        Control.print_slowly(look_describtion[subject])
                    elif operator.contains(currentRoom.room_objects , subject) :
                        Control.print_slowly(look_describtion[subject])
                except:          
                        Control.print_slowly(f"there is no such thing as {subject} right now")
        else:
            Control.print_slowly("you ca't look right now, you are stunt")

    def drop_command(subject,inventory,inventory_shower,currentRoom,player_stunt):    
        if player_stunt == False:
            if currentRoom.lights != True or None:
                Control.print_slowly("you can't drop items in the dark")
            elif currentRoom.item == None:
                if  subject in inventory_shower:                                                           
                    get_index_inv = operator.indexOf(inventory_shower,subject)
                    dropped_item = inventory.pop(get_index_inv)
                    inventory_shower.pop(get_index_inv)
                    currentRoom.item = dropped_item
                    Control.print_slowly(f"you droped {dropped_item.data}")
                else:
                    Control.print_slowly(f"there is no such thing as {subject} to drop")
            else:
                Control.print_slowly("you can't drop an item in a room which already has an item") 
        else:
            Control.print_slowly("you can't drop right now, you are stunt")

    def hide_command(subject,currentRoom,player_visibility,player_stunt):
        search_for_obj_res = False
        if player_visibility == True and player_stunt == False:
            for object in currentRoom.room_objects_shower:#searches for asked room object
                if subject == object:
                    get_index_current_room_object = operator.indexOf(currentRoom.room_objects_shower,subject)
                    temp = currentRoom.room_objects[get_index_current_room_object]
                    if temp.hidable == True:#if object is hidable, hide in it
                        player_visibility = False
                        player_stunt = True
                        search_for_obj_res = True
                        Control.print_slowly(f"you are hidden at {subject}")
                        return player_visibility,player_stunt
                    else:
                        Control.print_slowly(f"you can't hide in {subject}")
                        search_for_obj_res = True
            if search_for_obj_res == False:
                    Control.print_slowly(f"there is no such thing as {subject} to hide")
        elif player_stunt == True:
            Control.print_slowly("you can' move right now")
        elif player_visibility == False:
            Control.print_slowly("you are already hidden")
        return player_visibility,player_stunt

    def quit_command():
        quit_input = input(">are you sure you want to quit?(y/n)").lower()
        if quit_input == "y" or quit_input == "yes":
            quit()
        elif quit_input == "n" or quit_input == "no":
            Control.print_slowly("Okay")
        else:
            Control.print_slowly("I don't understand")           

    def Lightsroom_function(currentRoom):
        #turns room's lights on and off
        currentRoom.lights = Control.light_function(currentRoom.lights)
        if currentRoom.lights == True:
            Control.print_slowly(f"{currentRoom.data} light are on")
        elif currentRoom.lights == False:
            Control.print_slowly(f"{currentRoom.data} light are off")

    def flashlight_function(flashlight_button):
        #turns flashlight on and off
        flashlight_button = Control.light_function(flashlight_button)
        if flashlight_button == True:
            Control.print_slowly("flashlight is on")
        elif flashlight_button == False:
            Control.print_slowly("flashlight is off")
        return flashlight_button

    def light_function(light_button):
        #used for both flashlight and room's lights
        if light_button == False:
            
            return True
        else:
            
            return False    

    def turn_visibility(player_visibility):
        #turn player visible or invisible
        if player_visibility == False:
            return True
        else:
            return False

    def inventory_stats(inventory , inventory_storage): 
        #show if inventory has storage    
        count_int_item = len(inventory)
        empty_strage_space = inventory_storage - count_int_item 
        return empty_strage_space
            
    def check_lock(current_pos_key,inventory):
        #checks if you have keys for a locked door
        if current_pos_key in inventory:                           
            return True
        else :
            return False
        
    def move(currentRoom, pos, inventory,flashlight,flashlight_button):
        #verifing what is the next room player asked for
        if pos == 's':
            nextRoom = currentRoom.south
        elif pos == 'n':
            nextRoom = currentRoom.north
        elif pos == 'w':
            nextRoom = currentRoom.west
        elif pos == 'e':
            nextRoom = currentRoom.east
            
            
        if nextRoom != None:
            if nextRoom.lights == False and not operator.contains(inventory,flashlight):
                Control.print_slowly("this room is dark i need some light source before I enter it")
                return currentRoom
            elif nextRoom.lights == False and operator.contains(inventory,flashlight) and flashlight_button == False:
                Control.print_slowly("turn on your flashlight before entering this new room")
                return currentRoom
            
            elif nextRoom.locked == True and not Control.check_lock(nextRoom.key,inventory):#if door is locked and you don't have keys
                    Control.print_slowly('this door is locked')
                    return currentRoom
            elif nextRoom.locked == True and Control.check_lock(nextRoom.key,inventory) :#if door is locked but you have keys
                    nextRoom.locked = False
                    Control.print_slowly(f"{nextRoom.data} was locked but you opened {nextRoom.data} with {nextRoom.key.data}")
                    Control.print_slowly(nextRoom.data)
                    currentRoom = nextRoom
                    return currentRoom
            elif nextRoom.locked == False:#if it's a regular door with no lock
                    Control.print_slowly(nextRoom.data)
                    currentRoom = nextRoom
                    return currentRoom
        elif nextRoom == None:#if player hit wall
                Control.print_slowly(f"you reached end of {currentRoom.data}")
                return currentRoom
        
    def show_time(time_thread):
        in_game_seconds = time_thread.game_time % CONVERSION_FACTOR
        in_game_minutes = (time_thread.game_time // CONVERSION_FACTOR) % 60
        in_game_hours   = (time_thread.game_time // (CONVERSION_FACTOR * 60)) % 24
        day_night_cycle = time_thread.day_night_cycle
        Control.print_slowly(f"In-game time: {in_game_hours:02d}:{in_game_minutes:02d}:{in_game_seconds:02d}, Day/Night: {day_night_cycle}")   
        
    def open_door_lever(lever):
        if lever.locked == True:
            print(f"{lever.open_room.data} is open")
            return lever.open_room.locked == False , lever.locked == False
            
        else:
            print(f"{lever.open_room.data} is closed")
            return lever.open_room.locked == True , lever.locked == True
            