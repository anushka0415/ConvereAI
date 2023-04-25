
import cv2
import tensorflow as tf
ms_per_frame=1000
def process_img(image):
    dim = (48, 48, 1)
    resized = cv2.resize(image, dim)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    return gray

def partitition_video():
    model = tf.keras.models.load_model('C:/Users/Asus/Documents/fer2013/emotion_analysis')
    
    frames = []
    emotions = []
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
            image = process_img(image)
        
            frames.append(image)
            pred = model.predict(image)
            emotions.append(pred)
    #             print('Read a new frame: ', success)
            count += 1
    #             print(count)

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        print ("Video stop")
    else:
        print("Not Working")
    return emotions
cap = cv2.VideoCapture('video.mp4')
print(partitition_video())