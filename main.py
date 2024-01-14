import face_recognition
import cv2
import os
from sqlalchemy import create_engine
import base64
import binascii

# Set Default Filepath
filepath = "./Images"

# Set Default Camera Port 
cam = cv2.VideoCapture(0)

# Set Window Name 
cv2.namedWindow("test")

# Initialize Image Dictionary 
known_face_encodings = {}

# railway url
railway_database_url = "postgresql://postgres:6363c1f1Ad3Cec2DAEeDgF23da42AdAD@viaduct.proxy.rlwy.net:41175/railway"

# create the SQLAlchemy engine
engine = create_engine(railway_database_url)

# execute a SELECT query to fetch "id" and "encoded_image" from "busdata"
query = "SELECT id, encoded_image FROM busdata"

try:
    result = engine.execute(query)
    rows = result.fetchall()

    for row in rows:
        base64_string = row['encoded_image']
        try:
            image = base64.b64decode(base64_string, validate=True)
            file_to_save = f"image_{row['id']}.png"
            with open(file_to_save, "wb") as f:
                f.write(image)
            known_image = face_recognition.load_image_file(file_to_save)
            image_encoding = face_recognition.face_encodings(known_image)[0]
            known_face_encodings[tuple(image_encoding.flatten())] = row['id']
        except binascii.Error as e:
            print(e)

except Exception as e:
    print(f"Error: {e}")

stop = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break

    if stop < 3:
        cv2.putText(frame, "Current Stop: " + str(stop), (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "Next Stop: " + str(stop + 1), (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    elif stop == 3:
        cv2.putText(frame, "Current Stop: " + str(stop), (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    else:
        break

    cv2.imshow("test", frame)

    k = cv2.waitKey(1)

    if k % 256 == 27:
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        img_name = "opencv_frame_0.png"
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))

        unknown_image = face_recognition.load_image_file(img_name)
        unknown_locations = face_recognition.face_locations(unknown_image)

        if len(unknown_locations) > 0:
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            for face in known_face_encodings:
                result = face_recognition.compare_faces([face], unknown_encoding)
                if result[0]:
                    matched_id = known_face_encodings[face]
                    # execute a SELECT query to fetch "id" and "encoded_image" (should be BYTEA) from "busdata"
                    query = f"SELECT bus_number, stop_number, student_name, on_bus FROM busdata WHERE id = {matched_id}"
                    try:
                        # Run query and fetch all rows
                        result = engine.execute(query)
                        rows = result.fetchall()
                        db_bus, db_stop, name, on_bus = rows[0]

                        # Not on bus yet means we check if they are getting on the right bus
                        if not on_bus :
                            print("hi")
                            if db_bus != 29:
                                # TODO Window Text
                                print('wrong bus')
                                break
                            on_bus = True # TODO HELENA CHANGE THE VALUE OF ONBUS
                            prompt = "Welcome "
                        # On the bus, means we are checking if they are getting off the right stop
                        elif on_bus :
                            if db_stop != stop:
                                # TODO Window Text
                                print('wrong stop')
                                break
                            on_bus = False
                            prompt = "Goodbye "
                    
                    except Exception as e:
                        print(f"Error: {e}")
                    # At this point, this means the student is getting on the right bus or getting off at the right stop
                    text = prompt + name + "!"
                    cv2.putText(frame, text, (175, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.imshow("test", frame)
                    cv2.waitKey(3000)
        else:
            text = "Please move into the frame!"
            cv2.putText(frame, text, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow("test", frame)
            cv2.waitKey(500)

    elif k % 256 == 115:
        stop += 1

engine.dispose()
cam.release()
cv2.destroyAllWindows()
