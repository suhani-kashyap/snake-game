import pygame
import cv2
import random


###################################
#         INIT CAMERA             #
###################################
# capture video using default camera
cap = cv2.VideoCapture(0)

# init tracker
tracker = cv2.legacy.TrackerMOSSE_create()

# init stack to store last location of oject
rect_stack = []
directions = {"RIGHT": 0, "LEFT": 0, "UP": 0, "DOWN": 0}

success, img = cap.read()
bounding_box = cv2.selectROI("Tracking",img,False)

rect_stack.append(bounding_box)

tracker.init(img,bounding_box)

def drawBox(img, bounding_box):
    x, y, w, h = int(bounding_box[0]), int(bounding_box[1]), int(bounding_box[2]), int(bounding_box[3])
    cv2.rectangle(img, (x, y), ((x+w), (y+h)), (255, 0, 255), 3, 1)

    bb = rect_stack.pop(-1)
    x_prev, y_prev, w_prev, h_prev = int(bb[0]), int(bb[1]), int(bb[2]), int(bb[3])

    rect_stack.append(bounding_box)

    center_prev_x, center_prev_y = (x_prev + w_prev)/2, (y_prev + h_prev)/2
    center_curr_x, center_curr_y = (x+w)/2, (y+h)/2

    x_diff = int(abs(center_prev_x - center_curr_x))
    y_diff = int(abs(center_prev_y - center_curr_y))

    direction = ""
    if x_diff >= y_diff:
        if center_curr_x >= center_prev_x:
            directions["LEFT"] += 1
        else:
            directions["RIGHT"] += 1
    else:
        if center_curr_y >= center_prev_y:
            directions["DOWN"] += 1
        else:
            directions["UP"] += 1

    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


def find_max_direction(directions):
    max_direction = ""
    directions_list = list(directions.keys())
    max_num = 0

    for direction in directions_list:
        if max_num < directions[direction]:
            max_num = directions[direction]
            max_direction = direction

    directions = {"RIGHT": 0, "LEFT": 0, "UP": 0, "DOWN": 0}

    return (max_direction, directions)


###################################
#          INIT GAME              #
###################################
score = 0

display_width = 400
display_height = 300

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
snake_speed = 1
snake_position = [display_width/2, display_height/2]
snake_body = [[display_width/2, display_height/2]]
fruit_eaten = False

foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

game_over = False
direction = "UP"
changeTo = "UP"

Clock = pygame.time.Clock()

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


while not game_over:
    success, img = cap.read()
    success, bounding_box = tracker.update(img)

    i = 0
    while i < 60:
        success, img = cap.read()
        success, bounding_box = tracker.update(img)
        i += 1

        if success:
            changeTo = drawBox(img, bounding_box)
        else:
            cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    changeTo, directions = find_max_direction(directions)

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
        foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
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
    fps.tick(snake_speed)

    # Show Camera window
    cv2.imshow("Tracking", img)

    Clock.tick(60)

    # check for pressing q
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

pygame.quit()
quit()

