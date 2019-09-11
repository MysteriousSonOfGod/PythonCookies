import sys

import cv2

image_name = sys.argv[1]
casc_xml = sys.argv[2]

face_cascade = cv2.CascadeClassifier(casc_xml)

img = cv2.imread(image_name)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.2,
    minNeighbors=5,
    minSize=(20, 20),
)
print("Found {0} faces!".format(len(faces)))
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow('Face Found', img)
cv2.waitKey(0)
