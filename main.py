import face_recognition
import cv2
import os
from os import listdir
from sqlalchemy import create_engine

# railway url
railway_database_url = "postgresql://postgres:3df35D-fc6ECd4g151d-Agdc25gAC3F6@viaduct.proxy.rlwy.net:53889/railway"

# create the SQLAlchemy engine
engine = create_engine(railway_database_url)

# execute a SELECT query to fetch "id" and "encoded_image" (should be BYTEA) from "busdata"
query = "SELECT id, encoded_image FROM busdata"

try:
    result = engine.execute(query)

    # Fetch all rows
    rows = result.fetchall()

    # Print the "id" and "encoded_image" fields for each row
    for row in rows:
        print(f"ID: {row['id']}")
        print(f"Encoded Image: {row['encoded_image']}")
        print()

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the result set
    if 'result' in locals():
        result.close()

    # Close the engine
    engine.dispose()


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

stop = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    # TODO Check for end of stop and end the program once 
    # Hard Code route length as 3
    if stop < 3: 
        cv2.putText(frame, "Current Stop: " + str(stop), (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "Next Stop: " + str(stop + 1), (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    elif stop == 3:
        cv2.putText(frame, "Current Stop: " + str(stop), (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    else : break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # Space pressed 
        img_name = "opencv_frame_0.png" 
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        face_encodings = []
        
        # Creating the unknown image 
        unknown_image = face_recognition.load_image_file(img_name)
        unknown_locations = face_recognition.face_locations(unknown_image)
        if (len(unknown_locations) > 0):
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            for face in known_face_encodings :  
                result = face_recognition.compare_faces([face], unknown_encoding)
                print(result)
                # If true, puts text on CV Window Welcome or Goodbye depending on getting on or off the bus
                if result[0] : 
                    # Check if getting on the bus, if it is the right bus
                    # Check if getting off the bus, if it is the right stop
                    
                    text = "Welcome/Goodbye!" # TODO add the name
                    cv2.putText(frame, text, (175, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.imshow("test", frame)
                    cv2.waitKey(3000)  # Display the text for 2 seconds
        else: 
            text = "Please move into the frame!"
            cv2.putText(frame, text, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow("test", frame)
            cv2.waitKey(500)  # Display the text for 2 seconds
    elif k % 256 == 115: 
        stop+=1

cam.release()
cv2.destroyAllWindows()
