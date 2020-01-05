import time, cv2, mss, numpy#, ctypes
from directKeys import PressKey, ReleaseKey, W, A, S, D

startTime = time.time()
frames = 0
window = {"top": 0, "left": 0, "width": 960, "height": 540}
title = "Ai_1"
sct = mss.mss()

def ProcessImage(image):
    processedImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    processedImage = cv2.Canny(processedImage, threshold1=300, threshold2=400)
    processedImage = cv2.GaussianBlur(processedImage, (3, 3), 0)
    return processedImage

def DrawCircles(image):
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 5)
    try:
        circles = numpy.uint16(numpy.around(circles))
        for ii in circles[0, :]:
            cv2.circle(image, (ii[0], ii[1]), ii[2], (255, 255, 255), 3)
    except:
        print("no circles")
    return image

for i in list(range(5))[::-1]:
    print(i + 1)
    time.sleep(1)

'''
PressKey(W)
time.sleep(1)
ReleaseKey(W)
PressKey(D)
time.sleep(1)
ReleaseKey(D)
'''
while True:
    screen = numpy.array(sct.grab(window), numpy.uint8) # GRABS AREA
    blackAndWhite = ProcessImage(screen)                # CREATE GRAYSCALE IMAGE
    blackAndWhite = DrawCircles(blackAndWhite)          # DRAW CIRCLES
    #cv2.moveWindow(title, 950, 100)                     # MOVE WINDOW
    #checkPixels(screen)                                 # CHECK PIXELS
    cv2.imshow(title, blackAndWhite)                    # GRAYSCALE WINDOW
    if frames == 100:                                   # FPS
        print("FPS: " + str(frames / (time.time() - startTime)) + " - " + str(time.time() - lastTime))
        frames += 1
    elif frames < 100:
        frames += 1
        lastTime = time.time()
    if cv2.waitKey(25) & 0xFF == ord("q"):              # CLOSE WINDOW
        cv2.destroyAllWindows()
        sct.close()
        break
