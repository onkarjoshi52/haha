import cv2
cam = cv2.VideoCapture(0)
ret,image = cam.read()
if ret :
    #cv2.imshow('a',image)
    cv2.waitKey(0)
    cv2.destroyWindow('a')
    cv2.imwrite('abc.jpg',image)

cam.release()
