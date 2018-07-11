# -*- coding:utf-8 -*-
import face_recognition
from cobra.conf.GlobalSettings import *
from PIL import Image,ImageDraw
import cv2
from cobra.conf.PepleFace import *

class FaceRecognition(object):
    def __init__(self):
        self.aiface = face_recognition
        self.root = ROOT_PATH

    def loadImage(self,path):
        return self.aiface.load_image_file(self.root+'/'+path)

    def touchFaceImage(self,image):
        face_locations = self.aiface.face_locations(img=image, model="cnn")
        return image, face_locations

    def touchFace(self,path):
        image = self.loadImage(path)
        return self.touchFaceImage(image)

    def landmarksImage(self,image,faceLocations):
        return image,self.aiface.face_landmarks(face_image=image,face_locations=faceLocations)

    def landmarks(self,path,faceLocations):
        image = self.loadImage(path)
        return self.landmarksImage(image,faceLocations)

    def compareFaces(self,face,unknownFace):
        image = self.loadImage(path=face)
        # imageArray, faceLocations = self.touchFaceImage(image=image)
        imageEncoding = self.aiface.face_encodings(image,known_face_locations=None,num_jitters=1)[0]

        unknown = self.loadImage(path=unknownFace)
        # unknownImageArray, unknownFaceLocations = self.touchFaceImage(image=unknown)
        unknownEncoding = self.aiface.face_encodings(unknown,known_face_locations=None,num_jitters=1)[0]
        results = self.aiface.compare_faces([imageEncoding], unknownEncoding)
        if results[0] == True:
            print("It's a picture of me!")
        else:
            print("It's not a picture of me!")
        return results[0]

    def showFace(self, image, faceLocations):
        print("I found {} face(s) in this photograph.".format(len(faceLocations)))

        for faceLocation in faceLocations:
            # Print the location of each face in this image
            top, right, bottom, left = faceLocation
            print(
                "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                      right))

            # You can access the actual face itself like this:
            faceImage = image[top:bottom, left:right]
            pilImage = Image.fromarray(faceImage)
            pilImage.show()
    def showFaceLandmarks(self,image,faceLandmarksList):
        print("I found {} face(s) in this photograph.".format(len(faceLandmarksList)))

        for faceLandmarks in faceLandmarksList:

            # Print the location of each facial feature in this image
            facialFeatures = [
                'chin',
                'left_eyebrow',
                'right_eyebrow',
                'nose_bridge',
                'nose_tip',
                'left_eye',
                'right_eye',
                'top_lip',
                'bottom_lip'
            ]

            for facialFeature in facialFeatures:
                print("The {} in this face has the following points: {}".format(facialFeature,
                                                                                 faceLandmarks[facialFeature]))
            # Let's trace out each facial feature in the image with a line!
            pil_image = Image.fromarray(image)
            d = ImageDraw.Draw(pil_image)

            for facialFeature in facialFeatures:
                d.line(faceLandmarks[facialFeature],fill='red', width=3)

            pil_image.show()

    def faceRec(self):
        # This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
        # other example, but it includes some basic performance tweaks to make things run a lot faster:
        #   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
        #   2. Only detect faces in every other frame of video.

        # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
        # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
        # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(0)

        # Create arrays of known face encodings and their names
        known_face_encodings = []
        known_face_names = []

        for face in pf:
            # Load a sample picture and learn how to recognize it.
            rocky_image = self.loadImage("images/" + face["face"])
            rocky_face_encoding = face_recognition.face_encodings(rocky_image,num_jitters=1)[0]
            known_face_encodings.append(rocky_face_encoding)
            known_face_names.append(face["name"])
            # Create arrays of known face encodings and their names



        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations,num_jitters=1)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.6)
                    name = "Unknown"
                    print matches
                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

aiface = FaceRecognition()
# image,faceLocations = aiface.touchFace('images/chuanpu1.jpg')
# limage,landmarks = aiface.landmarksImage(image,faceLocations)
# aiface.showFace(image, faceLocations)
# aiface.showFaceLandmarks(limage,landmarks)
aiface.faceRec()
# print aiface.compareFaces(face='images/chuanpu1.jpg',unknownFace='images/chuanpu2.jpeg')
# print faceLocations,landmarks
