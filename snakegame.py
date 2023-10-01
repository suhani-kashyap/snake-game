import pygame
import cv2
import numpy as np
import random
import mediapipe as mp

score = 0

def show_score(display):
    score_font = pygame.font.SysFont("Arial", 15)
    score_surface = score_font.render('Score : ' + str(score), True, "White")

    # create a rectangular object for the
    # text surface object
    score_rect = score_surface.get_rect()

    # displaying text
    display.blit(score_surface, score_rect)

def show_dir():
    dir_list = ["UP", "DOWN", "RIGHT", "LEFT"]
    return random.choice(dir_list)

display_width = 400
display_height = 300

# Create a VideoCapture object
cap = cv2.VideoCapture(0)  # 0 for the default camera, you can change this number for other cameras

pygame.init()
display = pygame.display.set_mode((display_width, display_height))

# FPS (frames per second) controller
fps = pygame.time.Clock()
pygame.display.update()
pygame.display.set_caption('Snake game by Suhani and Nidhi')

blue=(0,0,255)
red=(255,0,0)
black=(0,0,0)

snake_block = 10
snake_speed = 15
snake_position = [display_width, display_height]
snake_body = [[display_width, display_height]]
fruit_eaten = False

foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
foody = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0

firstTime = True
game_over = False
while not game_over:
    for event in pygame.event.get():
        #If we close the game then set game_over to be true
        if event.type == pygame.QUIT:
            game_over = True

    changeTo = show_dir()
    if firstTime:
        direction = changeTo
    else:
        if changeTo == "UP" and direction != "DOWN":
            direction = "UP"
        if changeTo == "DOWN" and direction != "UP":
            direction = "DOWN"
        if changeTo == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        if changeTo == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"

    if direction == "UP":
        snake_position[1] -= 10
    if direction == "DOWN":
        snake_position[1] += 10
    if direction == "LEFT":
        snake_position[0] -= 10
    if direction == "RIGHT":
        snake_position[0] += 10

    snake_body.insert(0, list(snake_position))

    if snake_position[0] == foodx and snake_position[1] == foody:
        score+=10
        fruit_eaten = True
    else:
        snake_body.pop()

    if fruit_eaten:
        foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
        fruit_eaten = False

    display.fill(black)


    # Draws the snake
    for part in snake_body:
        pygame.draw.rect(display, blue, pygame.Rect(
            part[0], part[1], 10, 10))

    #Draws the food
    pygame.draw.rect(display, red, [foodx, foody, snake_block, snake_block])

    if snake_position[0] < 0 or snake_position[0] > display_width - 10:
        game_over = True
    if snake_position[1] < 0 or snake_position[1] > display_height - 10:
        game_over = True

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over = True

    show_score(display)
    pygame.display.update()

    # Loop to continuously capture frames from the camera
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was successfully captured
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the frame
        cv2.imshow('Camera Feed', frame)

        # Break the loop on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

pygame.quit()
quit()

