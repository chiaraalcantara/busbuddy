from flask import Flask, Response
import cv2
import face_recognition
import base64
import binascii
# from sqlalchemy import create_engine


# from flask import Flask, render_template, Response
# from camera import VideoCamera

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.js')
    
# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
               
# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(VideoCamera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)
    
import face_recognition
import cv2
import os
from sqlalchemy import create_engine
import base64
import binascii

# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy

    
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
                        prompt = ""
                        print("on bus value is" + str(on_bus))

                        # # Default value should always be False #TODO We Can leave True and False so the front end
                        # # can keep track real time the whereabouts of their child 
                        # update_statement = f"UPDATE busdata SET on_bus = 'False' WHERE id = {matched_id}"
                        # # Execute the update statement
                        # engine.execute(update_statement)

                        # Not on bus yet means we check if they are getting on the right bus
                        if not on_bus :
                            if db_bus != 29:
                                print("Wrong Bus " + name + "!")
                                text = "Wrong Bus " + name + "!"
                                cv2.putText(frame, text, (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                                cv2.imshow("test", frame)
                                cv2.waitKey(1000)
                                break
                                
                            update_statement = f"UPDATE busdata SET on_bus = 'True' WHERE id = {matched_id}"
                            # Execute the update statement
                            engine.execute(update_statement)

                            prompt = "Welcome "
                        # On the bus, means we are checking if they are getting off the right stop
                        elif on_bus :
                            if db_stop != stop :
                                print("Wrong Stop " + name + "!")
                                text = "Wrong Stop " + name + "!"
                                cv2.putText(frame, text, (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                                cv2.imshow("test", frame)
                                cv2.waitKey(1000)
                                break

                            update_statement = f"UPDATE busdata SET on_bus = 'False' WHERE id = {matched_id}"
                            # Execute the update statement
                            engine.execute(update_statement)

                            prompt = "Goodbye "
                    except Exception as e:
                        print(f"Error: {e}")
                    # At this point, this means the student is getting on the right bus or getting off at the right stop
                    text = prompt + name + "!"
                    cv2.putText(frame, text, (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
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

