import sys

sys.path.append(r'\Users\Asus\Documents\fer2013')
from Track import GazeTracking

import cv2
from typing import Dict, Tuple, List

class EyeTracker:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.gaze = None

    def track_gaze(self, frame, blinking):
        if self.gaze is None:
            self.gaze = GazeTracking()
        self.gaze.refresh(frame)

        frame = self.gaze.annotated_frame()
        text = ""

        #     print('Horizontal Ratio: ', gaze.horizontal_ratio())
        #     print('Vertical Ratio: ', gaze.vertical_ratio())

        # can I add a look up and look down?
        if self.gaze.is_blinking() and blinking is True:
            text = "blinking"
        elif self.gaze.is_blinking() and blinking is False:
            text = "center"
        elif self.gaze.is_right():
            # Right
            text = "right"
        elif self.gaze.is_left():
            # Left
            text = "left"
        elif self.gaze.is_center() and self.gaze.is_below():
            # Down
            text = "down"
        elif self.gaze.is_center() and self.gaze.is_above():
            # Up
            text = "up"
        elif self.gaze.is_center():
            # Center
            text = "center"
        else:
            text = "other"

        return text

    def track_eyes(self, ms_per_frame=1000, blinking=True) -> Tuple[List, Dict[int, str]]:
        images_eyes = {}  # timestamp (sec, int) : eyes position classification (str)
        frames = []
        cap = cv2.VideoCapture(self.video_path)
        if cap.isOpened():
            print("File Can be Opened")

            success, image = cap.read()
            count = 0
            while success:
                #         cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
                cap.set(cv2.CAP_PROP_POS_MSEC, (count * ms_per_frame))  # added this line
                success, image = cap.read()

                if image is None:
                    break
                frames.append(image)
                gaze = self.track_gaze(image, blinking)
                images_eyes[count] = gaze
                #             print('Read a new frame: ', success)
                count += 1
                #             print(count)

            # When everything done, release the capture
            cap.release()
            cv2.destroyAllWindows()
            print("Video stop")
        else:
            print("Not Working")

        return frames, images_eyes


