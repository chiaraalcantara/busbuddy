import cv2
import face_recognition
from sqlalchemy import create_engine
import base64
import binascii

class VideoCamera(object):
    def __init__(self):
        # Initialize video capture
        self.video = cv2.VideoCapture(0)
        # Load known face encodings
        self.known_face_encodings = self.load_known_faces()

    def __del__(self):
        # Release video capture
        self.video.release()

    def load_known_faces(self):
        # Implement this method to load known faces
        # Return a dictionary or list of known face encodings
        known_encodings = {}
        # Example database URL, replace with your actual database URL
        railway_database_url = "postgresql://postgres:6363c1f1Ad3Cec2DAEeDgF23da42AdAD@viaduct.proxy.rlwy.net:41175/railway"
        engine = create_engine(railway_database_url)
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
                    known_encodings[tuple(image_encoding.flatten())] = row['id']
                except binascii.Error as e:
                    print(e)
        except Exception as e:
            print(f"Error: {e}")
        return known_encodings

    def get_frame(self):
        # Create the engine
        railway_database_url = "postgresql://postgres:6363c1f1Ad3Cec2DAEeDgF23da42AdAD@viaduct.proxy.rlwy.net:41175/railway"
        engine = create_engine(railway_database_url)

        success, frame = self.video.read()
        if not success:
            return None

        # Perform face recognition or other processing
        face_locations = face_recognition.face_locations(frame)
        for top, right, bottom, left in face_locations:
            # Draw rectangles around detected faces
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            # unknown_image = face_recognition.load_image_file(frame)
            unknown_locations = face_recognition.face_locations(frame)

           
            if len(unknown_locations) > 0:
                for face in self.known_face_encodings:
                    unknown_encoding = face_recognition.face_encodings(frame)[0]
                    result = face_recognition.compare_faces([face], unknown_encoding)
                    if result[0]:
                        print("hello")
            # else:
            #     print("get in frame")

        # # The waitkey for space input
        # k = cv2.waitKey(1)
        # if k % 256 == 32:
        #     # If Spacebar
        #     img_name = "opencv_frame_0.png"
        #     cv2.imwrite(img_name, frame)
        #     print("{} written!".format(img_name))

        #     unknown_image = face_recognition.load_image_file(img_name)
        #     unknown_locations = face_recognition.face_locations(unknown_image)

        #     if len(unknown_locations) > 0:
        #         unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        #         for face in self.known_face_encodings:
        #             result = face_recognition.compare_faces([face], unknown_encoding)
        #             if result[0]:
        #                 matched_id = self.known_face_encodings[face]
        #                 # execute a SELECT query to fetch "id" and "encoded_image" (should be BYTEA) from "busdata"
        #                 query = f"SELECT bus_number, stop_number, student_name, on_bus FROM busdata WHERE id = {matched_id}"
        #                 try:
        #                     # Run query and fetch all rows
        #                     result = engine.execute(query)
        #                     rows = result.fetchall()
        #                     db_bus, db_stop, name, on_bus = rows[0]
        #                     prompt = ""
        #                     print("on bus value is" + str(on_bus))

        #                     # # Default value should always be False #TODO We Can leave True and False so the front end
        #                     # # can keep track real time the whereabouts of their child 
        #                     # update_statement = f"UPDATE busdata SET on_bus = 'False' WHERE id = {matched_id}"
        #                     # # Execute the update statement
        #                     # engine.execute(update_statement)

        #                     # Not on bus yet means we check if they are getting on the right bus
        #                     if not on_bus :
        #                         if db_bus != 29:
        #                             print("Wrong Bus " + name + "!")
        #                             text = "Wrong Bus " + name + "!"
        #                             cv2.putText(frame, text, (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        #                             cv2.imshow("test", frame)
        #                             cv2.waitKey(1000)
        #                             break
                                    
        #                         update_statement = f"UPDATE busdata SET on_bus = 'True' WHERE id = {matched_id}"
        #                         # Execute the update statement
        #                         engine.execute(update_statement)

        #                         prompt = "Welcome "
        #                     # On the bus, means we are checking if they are getting off the right stop
        #                     elif on_bus :
        #                         if db_stop != stop :
        #                             print("Wrong Stop " + name + "!")
        #                             text = "Wrong Stop " + name + "!"
        #                             cv2.putText(frame, text, (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        #                             cv2.imshow("test", frame)
        #                             cv2.waitKey(1000)
        #                             break

        #                         update_statement = f"UPDATE busdata SET on_bus = 'False' WHERE id = {matched_id}"
        #                         # Execute the update statement
        #                         engine.execute(update_statement)

        #                         prompt = "Goodbye "
        #                 except Exception as e:
        #                     print(f"Error: {e}")
        #                 # At this point, this means the student is getting on the right bus or getting off at the right stop
        #                 text = prompt + name + "!"
        #                 cv2.putText(frame, text, (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        #                 cv2.imshow("test", frame)
        #                 cv2.waitKey(3000)
        

        # Encode frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
