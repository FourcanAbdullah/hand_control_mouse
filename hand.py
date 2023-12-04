import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time
import pyautogui
import argparse
import random
import time

from pythonosc import udp_client
vid = cv2.VideoCapture(0)
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


# Create a hand landmarker instance with the live stream mode:
def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):

    try:
        global handData
        handData = result.hand_landmarks

    except:
        handData = []



    #21 landmarks for each joint. 
def handVid(client):
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
        running_mode=VisionRunningMode.LIVE_STREAM,
        num_hands = 2,
        result_callback=print_result)
    grabflag = False
    screenWidth, screenHeight = pyautogui.size()
    screenWidth, screenHeight = screenWidth, screenHeight 
 

    with HandLandmarker.create_from_options(options) as landmarker:
        while(True):
                    temp, still = vid.read()
                    still = cv2.flip(still, 1)
                    newimg = cv2.cvtColor(still, cv2.COLOR_BGR2RGB)
                    millisec = int(time.time() * 1000)
                    image= mp.Image(image_format=mp.ImageFormat.SRGB, data=newimg)
                    landmarker.detect_async(image, millisec )
                    height, width, color_channels = still.shape

                    try:
                        if(handData):
                            for hand in handData:
                                try:
                                    x, y = int(hand[0].x*width), int(hand[0].y*height) 
                                    
                                    cv2.circle(still,(x,y), 7, (0, 255, 0), cv2.FILLED)
                                    #right side of the screen
                                    if(hand[0].x > .5):
                                        client.send_message("/juce/rotaryknob", [x, y])
                                        print(hand[0].x, hand[0].y)
                                        cv2.putText(still, f"palm base: {hand[0].x}", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                                        #if gesture is closed fist then mouse drag
                                        if((hand[8].y >hand[5].y) and (hand[12].y >=hand[9].y) and (hand[16].y >hand[13].y) and (hand[20].y >hand[17].y)and (hand[4].x >=hand[2].x)):
                                            x = int(hand[0].x*width)
                                            y = int(hand[0].y*height)
                                            cv2.circle(img=still, center=(x,y), radius=30, color=(0, 255, 255))
                                            mousePositionX = (screenWidth/width*x)
                                            mousePositionY = (screenHeight/height*y)
                                            if grabflag == False: 
                                                grabflag = True
                                                pyautogui.mouseDown(button = "left")
                                            pyautogui.moveTo(mousePositionX, mousePositionY, duration = 0.1)
                                        #if gesture is open palm then move mouse
                                        if((hand[8].y <hand[5].y) and (hand[12].y <hand[9].y) and (hand[16].y <hand[13].y) and (hand[20].y <hand[17].y)and (hand[4].x <=hand[2].x)):
                                            if grabflag == True:
                                                grabflag = False
                                                pyautogui.mouseUp(button="left")
                                            x = int(hand[0].x*width)
                                            y = int(hand[0].y*height)
                                            cv2.circle(img=still, center=(x,y), radius=30, color=(0, 255, 255))
                                            mousePositionX = screenWidth/width*x
                                            mousePositionY = screenHeight/height*y
                                            pyautogui.moveTo(mousePositionX, mousePositionY)
                                    #left side of the screen
                                    if(hand[0].x <= .5):
                                        #for each gesture
                                        if((hand[8].y <hand[5].y) and (hand[12].y >=hand[9].y) and (hand[16].y >hand[13].y) and (hand[20].y >hand[17].y)and (hand[4].x <=hand[2].x)):
                                            cv2.putText(still, "Point up", (70,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                                            print("1 finger")
                                        if((hand[8].y <hand[5].y) and (hand[12].y <hand[9].y) and (hand[16].y >hand[13].y) and (hand[20].y >hand[17].y)and (hand[4].x <=hand[2].x)):
                                            cv2.putText(still, "Point up 2", (70,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                                            print("2 finger")
                                        if((hand[8].y <hand[5].y) and (hand[12].y <hand[9].y) and (hand[16].y <hand[13].y) and (hand[20].y >hand[17].y)and (hand[4].x <=hand[2].x)):
                                            cv2.putText(still, "Point up 3", (70,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                                            print("3 finger")
                                        if((hand[8].y <hand[5].y) and (hand[12].y <hand[9].y) and (hand[16].y <hand[13].y) and (hand[20].y <hand[17].y)and (hand[4].x <=hand[2].x)):
                                            cv2.putText(still, "Point up 4", (70,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                                            print("4 finger")
                                        if((hand[8].y <hand[5].y) and (hand[12].y <hand[9].y) and (hand[16].y <hand[13].y) and (hand[20].y <hand[17].y)and (hand[4].x >hand[2].x)):
                                            cv2.putText(still, "palm", (70,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                                            print("palm")
                                        if((hand[8].y >hand[5].y) and (hand[12].y >hand[9].y) and (hand[16].y >hand[13].y) and (hand[20].y >hand[17].y)and (hand[4].x <hand[2].x)):
                                            cv2.putText(still, "fist", (70,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                                            print("fist")
                                        
                                    
                                except:
                                    pass
                    except:
                        pass
                        
                    cv2.imshow("frame", still)
                    if cv2.waitKey(1) == ord('q'):
                            break

    vid.release()

    cv2.destroyAllWindows()





if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=9001,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)
handVid(client)
#   for x in range(500):
#     num1, num2 = random.random(), random.random()
#     client.send_message("/juce/rotaryknob", [num1, num2])
#     print(num1, num2)
#     time.sleep(.01)