import sys
import cv2
sys.path.append(r'\Users\Asus\Documents\fer2013\eye tracking')
from Track import GazeTracking
def track_gaze(frame, blinking):
    gaze = GazeTracking()
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

#     print('Horizontal Ratio: ', gaze.horizontal_ratio())
#     print('Vertical Ratio: ', gaze.vertical_ratio())
    
    # can I add a look up and look down? 
    if gaze.is_blinking() and blinking is True:
        text = "blinking"
    elif gaze.is_blinking() and blinking is False: 
        text = "center"
    elif gaze.is_right():
        # Right
        text = "right"
    elif gaze.is_left():
        # Left
        text = "left"
    elif gaze.is_center() and gaze.is_below():
        # Down
        text = "down"
    elif gaze.is_center() and gaze.is_above():
        # Up
        text = "up"
    elif gaze.is_center():
        # Center
        text = "center"
    else: 
        text = "other"
    
    return text
def track_eyes(cap, ms_per_frame=1000, blinking=True):
    images_eyes = {} # timestamp (sec, int) : eyes position classification (str)
    frames = []
    if cap.isOpened():
        print ("File Can be Opened")

        success, image = cap.read()
        count = 0
        while success:
    #         cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file 
            cap.set(cv2.CAP_PROP_POS_MSEC,(count*ms_per_frame))    # added this line 
            success, image = cap.read()
            
            if image is None: 
                break
            frames.append(image)
            gaze = track_gaze(image, blinking)
            images_eyes[count] = gaze
#             print('Read a new frame: ', success)
            count += 1
#             print(count)
        
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        print ("Video stop")
    else:
        print("Not Working")
    
    return frames, images_eyes
cap = cv2.VideoCapture('video.mp4')
frames, images_eyes = track_eyes(cap)
print(images_eyes)