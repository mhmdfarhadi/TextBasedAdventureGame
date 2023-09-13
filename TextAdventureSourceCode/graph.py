import pygame
import sys

pygame.init()

# Create a Pygame window
window_size = (400, 300)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Text Input Example")

font = pygame.font.Font(None, 32)
input_text = ""
all_input_text = []  # List to store all entered text

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("Input:", input_text)
                all_input_text.append(input_text)  # Store the entered text
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    screen.fill((255, 255, 255))

    # Render the input text
