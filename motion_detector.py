# import numpy
import cv2
import pandas
from datetime import *

background = None
statusList = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])

camera = cv2.VideoCapture(0)

while True:
    _, frame = camera.read()
    status = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0, )

    if background is None:
        background = gray
        continue

    deltaFrame = cv2.absdiff(background, gray)
    thresholdFrame = cv2.threshold(deltaFrame, 30, 255, cv2.THRESH_BINARY)[1]
    thresholdFrame = cv2.dilate(thresholdFrame, None, iterations=2)

    contours, hierarchy = cv2.findContours(thresholdFrame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    statusList.append(status)

    if statusList[-1] == 1 and statusList[-2] == 0:
        times.append(datetime.now())
    if statusList[-1] == 0 and statusList[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("Background", background)
    cv2.imshow("grayFrame", gray)
    cv2.imshow("deltaFrame", deltaFrame)
    cv2.imshow("thresholdFrame", thresholdFrame)
    cv2.imshow("colorImage", frame)

    if cv2.waitKey(1) == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

# print(statusList)
# print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index=True)

df.to_csv("Times.csv")

camera.release()
cv2.destroyAllWindows()
