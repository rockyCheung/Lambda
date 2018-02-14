# -*- coding:utf-8 -*-
import face_recognition
from cobra.conf.GlobalSettings import *
from PIL import Image,ImageDraw

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

aiface = FaceRecognition()
# image,faceLocations = aiface.touchFace('images/chuanpu1.jpg')
# limage,landmarks = aiface.landmarksImage(image,faceLocations)
# aiface.showFace(image, faceLocations)
# aiface.showFaceLandmarks(limage,landmarks)
print aiface.compareFaces(face='images/chuanpu1.jpg',unknownFace='images/chuanpu2.jpeg')
# print faceLocations,landmarks