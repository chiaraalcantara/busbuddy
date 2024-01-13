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

img_counter = 0

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

stop = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    # cv2.imshow("test", frame)
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    font_scale = 1
    color = (0, 255, 0)  # Green color
    thickness = 2
    cv2.putText(frame, str(stop), org, font, font_scale, color, thickness, cv2.LINE_AA)
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # Space pressed 
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        face_encodings = []
        
         
        unknown_image = face_recognition.load_image_file(img_name)
        unknown_locations = face_recognition.face_locations(unknown_image)
        if (len(unknown_locations) > 0):
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            for face in known_face_encodings :  
                result = face_recognition.compare_faces([face], unknown_encoding)
                print(result)
                if(result == "True") :
                    text = "Face jjjjjjj"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    org = (50, 50)
                    font_scale = 1
                    color = (0, 255, 0)  # Green color
                    thickness = 2

                    cv2.putText(frame, text, org, font, font_scale, color, thickness, cv2.LINE_AA)
                    cv2.imshow("test", frame)
                    cv2.waitKey(2000)  # Display the text for 2 seconds
        else: 
            # TODO: Change to Text on Screen 
            print("Please move into the frame")
    elif k % 256 == 115: 
        stop+=1
        # TODO: Change to Text on Screen 
        print("Going to stop number:", stop)



cam.release()
cv2.destroyAllWindows()
