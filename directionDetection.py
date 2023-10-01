import cv2

# capture video using default camera
cap = cv2.VideoCapture(0)

rect_stack = []

tracker = cv2.legacy.TrackerMOSSE_create()
#tracker = cv2.legacy.TrackerCSRT_create()
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

    if x_diff >= y_diff:
        if center_curr_x >= center_prev_x:
            print("Left")
        else:
            print("Right")
    else:
        if center_curr_y >= center_prev_y:
            print("Down")
        else:
            print("Up")


    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

while True:
    timer = cv2.getTickCount()
    success, img = cap.read()

    success, bounding_box = tracker.update(img)

    if success:
        drawBox(img, bounding_box)
    else:
        cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Calculate famres per second
    #fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    fps = 60

    # Show Camera window
    cv2.imshow("Tracking", img)

    # check for pressing q
    if cv2.waitKey(1) & 0xff == ord('q'):
        break