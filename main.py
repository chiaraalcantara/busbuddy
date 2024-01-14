import face_recognition
import cv2
import os
from os import listdir
from sqlalchemy import create_engine
import base64, binascii

# Set Default Filepath
filepath = "./Images"

# Set Default Camera Port 
cam = cv2.VideoCapture(0)

# Set Window Name 
cv2.namedWindow("test")

# Initialize Image Count 
img_counter = 0

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

	# Fetch all rows
	rows = result.fetchall()

	# Print the "id" and "encoded_image" fields for each row
	for row in rows:
		base64_string = row['encoded_image']
		try:
			image = base64.b64decode(base64_string, validate=True)
			file_to_save = f"image_{row['id']}.png"  # Use a unique identifier in the file name
			with open(file_to_save, "wb") as f:
				f.write(image)
			known_image = face_recognition.load_image_file(file_to_save)
			image_encoding = face_recognition.face_encodings(known_image)[0]
			known_face_encodings[tuple(image_encoding.flatten())] = row['id']
		except binascii.Error as e:
			print(e)
		
		print()

except Exception as e:
	print(f"Error: {e}")

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
				# the id we need is called encodedimage     
				# select_imageid 
				# If true, puts text on CV Window Welcome or Goodbye depending on getting on or off the bus
				if result[0] : 
					face
					matched_id = known_face_encodings[face]


				# execute a SELECT query to fetch "id" and "encoded_image" (should be BYTEA) from "busdata"
				query = f"SELECT bus_number, stop_number, student_name, on_bus FROM busdata WHERE id = {matched_id}"

				try:
					result = engine.execute(query)

					# Fetch all rows
					rows = result.fetchall()
					bus_number = 29
					db_bus, db_stop, name, on_bus = rows[0]

					if (on_bus):
						# add logic for checking if on the bus/not etc 
						on_bus = not on_bus
						# TODO Add text to screen 
					elif (db_bus != bus_number):
						print('wrong bus')
						# TODO Add text to screen 
					elif (db_stop != stop):
						print('wrong stop')
						
				
				except Exception as e:
					print(f"Error: {e}")
				
				text = "Welcome/Goodbye!" + name # TODO: add the name
				cv2.putText(frame, text, (175, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
				cv2.imshow("test", frame)
				cv2.waitKey(3000)  # Display the text for 3 seconds
		else: 
			text = "Please move into the frame!"
			cv2.putText(frame, text, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
			cv2.imshow("test", frame)
			cv2.waitKey(500)  # Display the text for .5 seconds
	elif k % 256 == 115: 
		stop+=1

# Close the engine
engine.dispose()
cam.release()
cv2.destroyAllWindows()
