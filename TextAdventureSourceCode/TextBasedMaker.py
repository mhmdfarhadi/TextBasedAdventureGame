from time import sleep , perf_counter
from collections import deque
import os
import GameFunctions
from GameFunctions import TimeThread, Item ,Room , RoomObject , Key  , Map , Player
from UI import status_panel



clear = lambda: os.system('cls')
clear()


#2 defining items , rooms, key etc.
flashlight  = Item("flashlight")
screwdriver = Item("screwdriver")


key         = Key('key')


start_room   = Room ("Starting Room")
hall1        = Room ("Short Hall")
hall2        = Room ("Long Hall")
intersection = Room ("Intersection")
hollow_room1 = Room ("Western Hollow Room")
hollow_room2 = Room ("Eastern Hollow Room")
diner_room   = Room ("Diner Room")
kitchen      = Room ("Kitchen")
garage       = Room ("Garage")

garage.make_room(None, None, start_room, None)

start_room.west = garage

hall2.locked = True
hall2.key = key

hollow_room1.item = key
hollow_room2.item = flashlight


closet = RoomObject("closet")
closet.room = intersection
intersection.room_objects.append(closet)
intersection.room_objects_shower.append("closet")
closet.hidable = True
clock = RoomObject("clock")
clock.room = intersection
intersection.room_objects.append(clock)
intersection.room_objects_shower.append("clock")


start_room.give_info("this lobby is really cozy")
hall1.give_info("this hall looks long and scary")
hall2.give_info("this hall even look more scary")
intersection.give_info("wow this place is really confusing")
hollow_room1.give_info("theres nothing to see here")
hollow_room2.give_info("this room is empty too")
diner_room.give_info("wow an old diner room")
kitchen.give_info("this kitchen smells so bad")

#this is how rooms connect:
start_room.south   = hall1
hall1.south        = intersection
hall1.north        = start_room
intersection.north = hall1
intersection.west  = hollow_room1
intersection.east  = hollow_room2
intersection.south = hall2
hollow_room1.east  = intersection
hollow_room2.west  = intersection
hall2.north        = intersection
hall2.south        = diner_room
diner_room.north   = hall2
diner_room.south   = kitchen
kitchen.north      = diner_room



rooms_level_list= [start_room,hall1,hall2,intersection,hollow_room1,hollow_room2,diner_room,kitchen] # a list of rooms , it's easy to work when they are on a list

currentRoom        = rooms_level_list[0] #player's current room: it starts at start room
current_enemy_room = rooms_level_list[-1] #enemy's current romm: it starts at kitchen
player_visibility  = True
player_stunt = False

visited = set()#for search player algorithm 
queue = deque([current_enemy_room])#for search player algorithm

player_visited_rooms = set()
player_visited_rooms.add(currentRoom)

flashlight_button = False #flashlight initiall value: it's turned off at first


inventory = [screwdriver]
inventory_shower = [screwdriver.data]

inventory_storage = 10


look_describtion = {
    "flashlight" : "an old flashlight, looks rusty but it still works",
    "screwdriver": "grandpa used to take this screwdriver eveywhere with himself",
    "key"        : "looks like a regular key"
}

# Create and start the time thread with a time scale factor of 2000
time_thread = TimeThread(time_scale=2000)
time_thread.start()

#create random temp,presuure,humidity for every room
start_room.change_env(time_thread.day_night_cycle)
garage.change_env(time_thread.day_night_cycle)
hall1.change_env(time_thread.day_night_cycle)
hall2.change_env(time_thread.day_night_cycle)
intersection.change_env(time_thread.day_night_cycle)
hollow_room1.change_env(time_thread.day_night_cycle)
hollow_room2.change_env(time_thread.day_night_cycle)
kitchen.change_env(time_thread.day_night_cycle)


rover = Player()

#3 game's main loop
def main(currentRoom,current_enemy_room,player_visibility,player_stunt,flashlight_button,inventory,inventory_shower):   
    while True:
        
        
        
        
        main_input = input(">")
        command , subject = GameFunctions.Control.input_manager(main_input)

        if   command == "go" :   
            currentRoom = GameFunctions.Control.go_command(subject,currentRoom,player_stunt,inventory)
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
                    if subject == "switch" or subject == "lights" or subject == "light":
                        if currentRoom.lights == None:
                            GameFunctions.Control.print_slowly("there are no lights here")
                        else:    
                            GameFunctions.Control.Lightsroom_function(currentRoom)
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
                for i in inventory_shower:
                    GameFunctions.Control.print_slowly(inventory_shower[i])
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
   main(currentRoom,current_enemy_room,player_visibility,player_stunt,flashlight_button,inventory,inventory_shower)
