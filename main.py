import face_recognition
import cv2
import os
from os import listdir

#   TODO Import images from database 

# Set Default Filepath
filepath = "./Images"

# Set Default Camera Port 
cam = cv2.VideoCapture(0)

# Set Window Name 
cv2.namedWindow("test")

# Initialize Image Count 
img_counter = 0

# Initialize Image List 
known_face_encodings = []

for file in os.listdir(filepath):
    filename = os.fsdecode(file)
    if filename.endswith(".jpg"):
       print(file)
       image_path = os.path.join(filepath, file)
       image = face_recognition.load_image_file(image_path)
       image_encoding = face_recognition.face_encodings(image)[0]
       known_face_encodings.append(image_encoding)
       print(len(known_face_encodings))
    else:
        continue


while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 97:
        # a pressed - Getting on the Bus
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        face_encodings = []
        
        for image in os.listdir(filepath):
            image_path = os.path.join(filepath, image)
            known_image = face_recognition.load_image_file(image_path)
            unknown_image = face_recognition.load_image_file(img_name)


            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        for face in known_face_encodings :  
            result = face_recognition.compare_faces([face], unknown_encoding)
            print(result)
    elif k % 256 == 100:
        # d pressed - Getting Off the Bus
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        face_encodings = []
        
        for image in os.listdir(filepath):
            image_path = os.path.join(filepath, image)
            known_image = face_recognition.load_image_file(image_path)
            unknown_image = face_recognition.load_image_file(img_name)


            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        for face in known_face_encodings :  
            result = face_recognition.compare_faces([face], unknown_encoding)
            print(result)



cam.release()
cv2.destroyAllWindows()
