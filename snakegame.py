import pygame
import cv2
import numpy as np

pygame.init()
dis = pygame.display.set_mode((400, 300))
pygame.display.update()
pygame.display.set_caption('Snake game by Suhani and Nidhi')

blue=(0,0,255)
red=(255,0,0)

# Create a VideoCapture object
cap = cv2.VideoCapture(0)  # 0 for the default camera, you can change this number for other cameras

# Check if the camera is opened correctly
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Loop to continuously capture frames from the camera
while True:
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

game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    pygame.draw.rect(dis,blue,[200,150,10,10])
    pygame.display.update()

pygame.quit()
quit()