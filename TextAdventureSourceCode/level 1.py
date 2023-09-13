from time import sleep , perf_counter
from collections import deque
import os
import GameFunctions
from GameFunctions import TimeThread, Item ,Room , RoomObject , Key  , Map , Player , Lever , Terminal
from UI import status_panel
import operator

def open_finall_room(inventory):
    if operator.contains(inventory,blue_ring) and operator.contains(inventory,red_ring):
        congrats_room.locked = False
    else:
        pass
    
    
    
    
#2 defining items , rooms, key etc.
flashlight  = Item("flashlight")
screwdriver = Item("screwdriver")
blue_ring   = Item("ring")
red_ring    = Item("ring")


key  = Key("key")
non_exist_key = Key("BRUH")

intersection = Room("intersection")
room1  = Room("room1")
room2  = Room("room2")
room3  = Room("room3")
room4  = Room("room4")
room5  = Room("room5")
room6  = Room("room6")
room7  = Room("room7")
room8  = Room("room8")
room9  = Room("room9")
room10 = Room("room10")
room11 = Room("room11")
room12 = Room("room12")
room13 = Room("room13")
room14 = Room("room14")
room15 = Room("room15")
room16 = Room("room16")
room17 = Room("room17")
room18 = Room("room18")
room19 = Room("room19")
room20 = Room("room20")
room21 = Room("room21")
room22 = Room("room22")
room23 = Room("room23")
room24 = Room("room24")
room25 = Room("room25")
room26 = Room("room26")
congrats_room = Room("congrats room")
extra_room = Room("extra room")



painting = RoomObject("painting")
painting.room = room25
room25.room_objects.append(painting)
room25.room_objects_shower.append("painting")

book_shelf = RoomObject("library")
book_shelf.room = room25
room25.room_objects.append(book_shelf)
room25.room_objects_shower.append("library")


clock = RoomObject("clock")
clock.room = intersection
intersection.room_objects.append(clock)
intersection.room_objects_shower.append("clock")

room18.item = flashlight
room11.item = blue_ring
room26.item = red_ring

room6.locked = True
room6.key    = key
key.room     = room5
room5.item   = key

room18.item = flashlight

congrats_room.locked = True
congrats_room.key    = non_exist_key

room20.locked          = True
rusted_lever           = Lever()
rusted_lever.room      = extra_room
rusted_lever.open_room = room20
extra_room.lever       = rusted_lever




#this is how rooms connect:
intersection.make_room(congrats_room,room21,room1,room20)
room1.make_room(None,intersection,room2,None)
room2.make_room(None,room1,room3,None)
room3.make_room(None,room2,None,room4)
room4.make_room(room3,None,room5,room6)
room5.make_room(None,room4,None,None)
room6.make_room(room4,None,None,room7)
room7.make_room(room6,None,None,room8)
room8.make_room(room7,None,None,room9)
room9.make_room(room8,None,None,room10)
room10.make_room(room9,None,None,room11)
room11.make_room(room10,room12,None,None)
room12.make_room(None,room13,room11,None)
room13.make_room(None,room14,room12,None)
room14.make_room(room15,None,room13,None)
room15.make_room(room16,None,None,room14)
room16.make_room(room17,None,None,room15)
room17.make_room(room18,None,None,room16)
room18.make_room(room19,None,None,room17)
room19.make_room(room20,extra_room,None,room18)
extra_room.make_room(None,None,room19,None)
room20.make_room(intersection,None,None,room19)
room21.make_room(None,room22,intersection,None)
room22.make_room(None,room23,room21,None)
room23.make_room(None,room24,room22,None)
room24.make_room(room25,None,room23,room26)
room25.make_room(None,None,None,room24)
room26.make_room(room24,None,None,None)
congrats_room.make_room(None,None,None,intersection)

room21.lights = False


terminal = Terminal("terminal")
terminal.password = "1111"
terminal.room     = room24
room24.terminal   = terminal
room26.locked     = True
terminal.locked_room = room26


#rooms_level_list= [start_room,hall1,hall2,intersection,hollow_room1,hollow_room2,diner_room,kitchen] # a list of rooms , it's easy to work when they are on a list

currentRoom        = intersection #rooms_level_list[0] #player's current room: it starts at start room
#current_enemy_room = rooms_level_list[-1] #enemy's current romm: it starts at kitchen
player_visibility  = True
player_stunt = False

visited = set()#for search player algorithm 
#queue = deque([current_enemy_room])#for search player algorithm

player_visited_rooms = set()
player_visited_rooms.add(currentRoom)

flashlight_button = False #flashlight initiall value: it's turned off at first


inventory = [screwdriver]
inventory_shower = [screwdriver.data]

inventory_storage = 10


look_describtion = {
    "flashlight" : "an old flashlight, looks rusty but it still works",
    "screwdriver": "grandpa used to take this screwdriver eveywhere with himself",
    "key"        : "looks like a regular key",
    "painting"   : "a painting with France flag",
    "library"    : "a library with colorful books"
}

# Create and start the time thread with a time scale factor of 2000
time_thread = TimeThread(time_scale=2000)
time_thread.start()

#create random temp,presuure,humidity for every room
"""start_room.change_env(time_thread.day_night_cycle)
garage.change_env(time_thread.day_night_cycle)
hall1.change_env(time_thread.day_night_cycle)
hall2.change_env(time_thread.day_night_cycle)
intersection.change_env(time_thread.day_night_cycle)
hollow_room1.change_env(time_thread.day_night_cycle)
hollow_room2.change_env(time_thread.day_night_cycle)
kitchen.change_env(time_thread.day_night_cycle)
"""

rover = Player()




#3 game's main loop
def main(currentRoom,player_visibility,player_stunt,flashlight_button,inventory,inventory_shower):   
    while True:
        
        if currentRoom.terminal != None:
            GameFunctions.Control.print_slowly("there is a Terminal in this room")
        if currentRoom.lever != None:
            GameFunctions.Control.print_slowly("there is a Lever in this room")
        open_finall_room(inventory)
        Map.display_mini_map(Map.mini_map_func(currentRoom))
        main_input = input(">")
        command , subject = GameFunctions.Control.input_manager(main_input)

        if   command == "go" :   
            currentRoom = GameFunctions.Control.go_command(subject,currentRoom,player_stunt,inventory,flashlight,flashlight_button)
            if currentRoom.item != None:    
                GameFunctions.Control.print_slowly(f"{currentRoom.item.data} is in room")
            if currentRoom.room_objects_shower != []:
                GameFunctions.Control.print_slowly(currentRoom.room_objects_shower)
        elif command == "take":
            GameFunctions.Control.take_command(subject, currentRoom,inventory,inventory_storage,inventory_shower,player_stunt)
        elif command == "look":
            GameFunctions.Control.look_command(subject,inventory_shower,currentRoom,player_stunt,look_describtion,flashlight_button)
        elif command == "drop":
            GameFunctions.Control.drop_command(subject,inventory,inventory_shower,currentRoom,player_stunt)
        elif command == "use":
            if player_stunt == False:
                try:
                    if subject == "lever" and currentRoom.lever != None:
                        currentRoom.lever.open_room.locked  , currentRoom.lever.locked = GameFunctions.Control.open_door_lever(currentRoom.lever)
                        
                    elif subject == "terminal" and currentRoom.terminal != None:
                        for iterations in range(0,4):
                            player_pass = input("Please Enter the Password:\n(for hint type hint)")
                            player_pass = player_pass.lower()
                            if player_pass == currentRoom.terminal.password:
                                if currentRoom.terminal.locked_room.locked == True:
                                    currentRoom.terminal.locked_room.locked = False
                                    GameFunctions.Control.print_slowly(f"{currentRoom.terminal.locked_room.data} is Now Open")
                                    break
                                else:
                                    GameFunctions.Control.print_slowly(f"{currentRoom.terminal.locked_room.data} is Already Open")
                            elif player_pass == "hint":
                                GameFunctions.Control.print_slowly("the Password is a 4 Digit code, to find it you must search nearby areas for hints")
                            else:
                                GameFunctions.Control.print_slowly("Your Password is Wrong!")
                        else:
                            GameFunctions.Control.print_slowly("You Tried Too Many Times, Try again Later!")
                            
                            
                    elif subject in inventory_shower or subject == currentRoom.item.data:
                        if subject == "flashlight":
                            flashlight_button = GameFunctions.Control.flashlight_function(flashlight_button)
                        else:
                            GameFunctions.Control.print_slowly(f"{subject} has no use")            
                except AttributeError:
                    GameFunctions.Control.print_slowly(f"there is no such thing as {subject}")
            else:
                GameFunctions.Control.print_slowly("you can't use here because you are stunned")
        elif command == "hide":
            if player_visibility == True and player_stunt == False:
                player_visibility,player_stunt = GameFunctions.Control.hide_command(subject,currentRoom,player_visibility,player_stunt)
            else:
                GameFunctions.Control.print_slowly("you are already hidden")    
        elif command == "get":
            if subject == "out":
                if player_visibility == False and player_stunt == True:
                    player_stunt = False
                    player_visibility = True
                    GameFunctions.Control.print_slowly("you are out/visible now")
                else:
                    GameFunctions.Control.print_slowly("you are alrady out")
            else:
                GameFunctions.Control.print_slowly("invalid input")                  
        elif subject == None:
            if command == "quit":
                GameFunctions.Control.quit_command()             
            elif command == "where":
                GameFunctions.Control.print_slowly(f"you are at {currentRoom.data}")
            elif command == "info":
                GameFunctions.Control.print_slowly(currentRoom.info)
            elif command == "inventory":
                GameFunctions.Control.print_slowly(inventory_shower)
                GameFunctions.Control.print_slowly(f"you have {GameFunctions.Control.inventory_stats(inventory,inventory_storage)} empty space in your inventory")
            elif command == "map":
                Map.display_mini_map(Map.mini_map_func(currentRoom))
            elif command == "time":
                GameFunctions.Control.show_time(time_thread)
            elif command == "status":
                status_panel(rover.health,currentRoom.pressure,currentRoom.temperature,currentRoom.humidity,rover.high_temperature_threshold,rover.low_temperature_threshold,rover.humidity_threshold,rover.pressure_threshold)
            else:
                GameFunctions.Control.print_slowly("invalid input")
        else :
            GameFunctions.Control.print_slowly("invalid input")
    
          

        

            

if __name__ == "__main__":
   main(currentRoom,player_visibility,player_stunt,flashlight_button,inventory,inventory_shower)
