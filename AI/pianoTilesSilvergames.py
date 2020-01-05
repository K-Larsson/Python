import time, cv2, mss, numpy, ctypes

xarr, yarr = [], []
startTime = time.time()
frames = 0
window = {"top": 180, "left": 20, "width": 470, "height": 590}
title = "[MSS] Please work...?"
sct = mss.mss()

def processImage (originalImage):
    processedImage = cv2.cvtColor(originalImage, cv2.COLOR_RGB2GRAY)
    processedImage = cv2.Canny(processedImage, threshold1=200, threshold2=300)
    #processedImage = cv2.GaussianBlur(processedImage, (5, 5), 0)
    vertices = numpy.array([[10, 10], [460, 10], [460, 580], [10, 580]])
    processedImage = roi(processedImage, [vertices])
    lines = cv2.HoughLinesP(processedImage, 1, numpy.pi/180, 100, numpy.array([]), 20, 15)
    drawLines(processedImage, lines)
    return processedImage

def drawLines (img, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 255], 2)
    except:
        print("No lines")
        pass

def checkPixels (img):
    # lmbDown = 0x0002
    # lmbUp = 0x0004
    # ctypes.windll.user32.mouse_event(lmbDown)
    # ctypes.windll.user32.mouse_event(lmbUp)
    if numpy.any(img[460, 80] == 0):
        ctypes.windll.user32.SetCursorPos(80, 600)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
    elif numpy.any(img[460, 200] == 0):
        ctypes.windll.user32.SetCursorPos(200, 600)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
    elif numpy.any(img[460, 320] == 0):
        ctypes.windll.user32.SetCursorPos(320, 600)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
    elif numpy.any(img[460, 440] == 0):
        ctypes.windll.user32.SetCursorPos(440, 600)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)

def roi (img, vertices):
    mask = numpy.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

while True:
    screen = numpy.array(sct.grab(window), numpy.uint8) # GRABS AREA
    newScreen = processImage(screen)                    # CREATE GRAYSCALE IMAGE
    cv2.moveWindow(title, 950, 100)                     # MOVE WINDOW
    cv2.imshow(title, screen)                           # COLORED WINDOW
    checkPixels(screen)                                 # CHECK PIXELS
    #cv2.imshow("Grayscale", newScreen)                  # GRAYSCALE WINDOWq
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
