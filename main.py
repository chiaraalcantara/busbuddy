import face_recognition
import cv2
import os
from os import listdir
from sqlalchemy import create_engine
import base64, binascii

#   TODO Import images from database 

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


# Loop throuhg all the encoded image ids, then convert it, then store it in the array

# TODO Helena!
# Loop through images in the Database. Loop through encoded string. Call the function that turns
# it back into an image. 
# Data is called Bus Data c
# In here we store both the encoded string, and the image id associated to the string. 

# For time being will hard code 3
# For time being, we hard code bus 29

# Filter first by bus number, then length of that bus number column
# for i in range(3) : # Grab length of column
#     base64_string = "HELENA STRING" #TODO from the database
#     try:
#         image = base64.b64decode(base64_string, validate=True)
#         file_to_save = "name or path of the file to save, let's say, my_image.png"
#         with open(file_to_save, "wb") as f:
#             f.write(image)
#         known_image = face_recognition.load_image_file(image)
#         image_encoding = face_recognition.face_encodings(image)[0]
#         known_face_encodings[image_encoding] = # Name of Child of the same row
#     except binascii.Error as e:
#         print(e)
# Initialize Image Dictionary 
known_face_encodings = {}

# railway url
railway_database_url = "postgresql://postgres:6363c1f1Ad3Cec2DAEeDgF23da42AdAD@viaduct.proxy.rlwy.net:41175/railway"

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

# finally:
#     # Close the result set
#     if 'result' in locals():
#         result.close()

#     # Close the engine
#     engine.dispose()


		
# for file in os.listdir(filepath):
#     filename = os.fsdecode(file)
#     if filename.endswith(".jpg"):
#        print(file)
#        image_path = os.path.join(filepath, file)
#        # Convert from b64 to image here!
#        image = face_recognition.load_image_file(image_path)
#        image_encoding = face_recognition.face_encodings(image)[0]
#        known_face_encodings.append(image_encoding) # Store it here, two columns. One for id and one for encoded string  
#        # Extract associated image id.
#        print(len(known_face_encodings))
#     else:
#         continue

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
				query = f"SELECT bus_number, stop_number, student_name FROM busdata WHERE id = {matched_id}"

				try:
					result = engine.execute(query)

					# Fetch all rows
					rows = result.fetchall()
					bus_number = 29
					print('these rows', rows)
					db_bus, db_stop, name = rows[0]

					# Print the "id" and "encoded_image" fields for each row
					
					print('bus number', db_bus)
					print('bus nusmss', bus_number)
					if (db_bus != bus_number):
						print('wrong bus')
					print('idiot', db_stop)
					print('yeuck', stop)
					if (db_stop != stop):
						print('wrong stop')
				except Exception as e:
					print(f"Error: {e}")
					# Check if getting on the bus, if it is the right bus
					# Check if getting off the bus, if it is the right stop
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

cam.release()
cv2.destroyAllWindows()
