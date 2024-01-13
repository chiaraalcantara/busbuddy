import face_recognition
import cv2
import os
from os import listdir

folder_dir = "./Images"
cam = cv2.VideoCapture(0)
cv2.namedWindow("test")
img_counter = 0

# 1
obama_image = face_recognition.load_image_file("./Images/Barack Obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# 2
donald_image = face_recognition.load_image_file("./Images/Donald Trump.jpg")
donald_face_encoding = face_recognition.face_encodings(donald_image)[0]

# 3
franklin_image = face_recognition.load_image_file("./Images/Franklin Ramirez.jpg")
franklin_face_encoding = face_recognition.face_encodings(franklin_image)[0]

known_face_encodings = [
    obama_face_encoding,
    donald_face_encoding,
    franklin_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Donald Trump",
    "Franklin Ramirez"
]

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
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        # img_counter += 1
        face_encodings = []
        
        for image in os.listdir(folder_dir):
            image_path = os.path.join(folder_dir, image)
            known_image = face_recognition.load_image_file(image_path)
            unknown_image = face_recognition.load_image_file(img_name)


            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

            results = face_recognition.compare_faces([obama_face_encoding], unknown_encoding)
            if(results) 
            results = face_recognition.compare_faces([donald_face_encoding], unknown_encoding)
            results = face_recognition.compare_faces([franklin_face_encoding], unknown_encoding)

            print(results)


cam.release()
cv2.destroyAllWindows()
