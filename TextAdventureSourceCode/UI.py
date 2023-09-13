import math
import time
import os 
import sys

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"




def loading_animation1():
    animation_chars = ["|", "/", "-", "\\"]
    
    for i in range(20):  # Number of animation frames
        sys.stdout.write("\r" + "Loading " + animation_chars[i % 4])
        sys.stdout.flush()
        time.sleep(0.1)  # Adjust the sleep duration for animation speed
        
    sys.stdout.write("\r" + "Loading Complete!\n")


def loading_animation2():
    bar_length = 20
    for i in range(41):
        time.sleep(0.1)
        sys.stdout.write("\r" + "[" + "=" * i + " " * (bar_length - i) + "]" + " " + str(i * 2.5) + "%")
        sys.stdout.flush()



def status_panel(player_health,pressure,temperature,humidity,high_temperature_threshold,low_temperature_threshold,humidity_threshold,pressure_threshold):
 

    health_threshold = 20
    
    try:
        #while True:
            
                
                #os.system('cls')
                
                
                #Health
                health_flag = "LOW HEALTH!" if player_health < health_threshold else "Normal"
                if health_flag == "LOW HEALTH!":
                    health_up   = "┌" + "─" + f"Health Level:{health_flag}" + "─" + "┐"
                    health_down = "└" + "─" + f"Health: {player_health}%" + "─" *14 + "┘"
                else:
                    health_up   = "┌" + "─" + f"Health Level:{health_flag}" + "─"*6 + "┐"
                    health_down = "└" + "─" + f"Health: {player_health}%" + "─" *13 + "┘"
                health_bar  = "│     " +"[" + "█" * math.ceil(player_health / 10) + " " * (10 - math.ceil(player_health / 10)) + "]"+"         │" 
                
                
                
                # Pressure
                pressure_flag = "HIGH" if pressure > pressure_threshold else "Normal"
                if pressure_flag == "HIGH":
                    pressure_up   = "┌" + "─" + f"Pressure: {pressure_flag}" + "─" * 11 + "┐"
                    pressure_down = "└" + "─" + f"Pressure: {pressure} PSI" + "─" * 9 + "┘"
                else:
                    pressure_up   = "┌" + "─" + f"Pressure: {pressure_flag}" + "─" * 9 + "┐"
                    pressure_down = "└" + "─" + f"Pressure: {pressure} PSI" + "─" * 10 + "┘"
                pressure_bar  = "│     " + "[" + "█" * math.ceil(pressure / 10) + " " * (10 - math.ceil(pressure / 10)) + "]" + "         │"
                

                # Temperature
                temperature_flag = "HIGH" if temperature > high_temperature_threshold else ("LOW" if temperature < low_temperature_threshold else "Normal")
                temperature_up   = "┌" + "─"  + f"Temperature: {temperature_flag}" + "─" * 6 + "┐"
                temp_bar         = "[" + "█" * math.ceil((temperature + 200) / 50) + " " * (10 - math.ceil((temperature + 200) / 50)) + "]"
                temperature_bar  = "│     " + temp_bar + "         │"
                temperature_down = "└" + "─"  + f"Temperature: {temperature}°C" + "─" * 8 + "┘"

                # Humidity
                humidity_flag = "HIGH" if humidity > humidity_threshold else "Normal"
                if humidity_flag == "Normal":
                    humidity_up   = "┌" + "─"  + f"Humidity: {humidity_flag}" + "─" * 9 + "┐"
                    humidity_down = "└" + "─"  + f"Humidity: {humidity}%" + "─" * 12 + "┘"
                else:
                    humidity_up   = "┌" + "─"  + f"Humidity: {humidity_flag}" + "─" * 11 + "┐"
                    humidity_down = "└" + "─"  + f"Humidity: {humidity}%" + "─" * 12 + "┘"
                humidity_bar  = "│     " + "[" + "█" * math.ceil(humidity / 10) + " " * (10 - math.ceil(humidity / 10)) + "]" + "         │"
                # Combine UI elements
                
                ui_elements = "\n".join([
                    health_up,
                    health_bar,
                    health_down,
                    "",
                    pressure_up,
                    pressure_bar,
                    pressure_down,
                    "",
                    temperature_up,
                    temperature_bar,
                    temperature_down,
                    "",
                    humidity_up,
                    humidity_bar,
                    humidity_down
                ])

                # Print the combined UI elements
                
                health_color          = GREEN if health_flag      == "Normal" else RED
                pressure_color        = CYAN  if pressure_flag    == "Normal" else RED
                temperature_color     = CYAN  if temperature_flag == "Normal" else RED
                humidity_color        = CYAN  if humidity_flag    == "Normal" else RED
                    
                print(health_color + health_up   + RESET)
                print(health_color + health_bar  + RESET)
                print(health_color + health_down + RESET)
                
                print(pressure_color + pressure_up   + RESET)
                print(pressure_color + pressure_bar  + RESET)
                print(pressure_color + pressure_down + RESET)
                
                print(temperature_color + temperature_up   + RESET)
                print(temperature_color + temperature_bar  + RESET)
                print(temperature_color + temperature_down + RESET)
                
                print(humidity_color + humidity_up   + RESET)
                print(humidity_color + humidity_bar  + RESET)
                print(humidity_color + humidity_down + RESET)
                
                
                
                time.sleep(1)
    except KeyboardInterrupt:
           print("Keyboard interrupt detected. Exiting...")

