import face_recognition
import cv2
import subprocess
import os

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

test1 = face_recognition.load_image_file("aa.jpg")
test1_encoding = face_recognition.face_encodings(test1)[0]
test2 = face_recognition.load_image_file("bb.jpg")
test2_encoding = face_recognition.face_encodings(test2)[0]
test3 = face_recognition.load_image_file("cc.jpg")
test3_encoding = face_recognition.face_encodings(test3)[0]

known_face_encodings = [
    test1_encoding,test2_encoding,test3_encoding
]

known_face_names = [
"aa","bb","cc"
]

test1 = False
test2 = False
test3 = False


face_locations = []
face_encodings = []
face_names = []
process_this_frame  = True
test1

while True:
  
    ret, frame = video_capture.read()


    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    
    rgb_small_frame = small_frame[:, :, ::-1]

    
    if process_this_frame:
  
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
           
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

           
            if True in matches:
               
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                face_names.append(name)
		

	
    process_this_frame = not process_this_frame


   
    for (top, right, bottom, left), name in zip(face_locations, face_names):
       
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        os.system("espeak '%s' " % name)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

   
    cv2.imshow('Video', frame)

  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()
