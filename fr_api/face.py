from PIL import Image, ImageDraw
import face_recognition
import numpy
import hashlib

class Face(object):

    def __init__(self):

        self.box = [0] * 4
        self.ary_image = []
        self.pil_image = 0
        self.face_landmarks = {}
        self.blackbg_img = 0
        self.identity = []
        self.__hash_identity = -1

    #TODO add face identification process, save the identity in self.indentity
    def face_identification(self):

        try:

            self.identity = face_recognition.face_encodings(self.ary_image)[0]
            md5 = hashlib.md5()
            md5.update(str(self.identity).encode('utf-8'))
            self.__hash_identity = md5.hexdigest()
            print(self.__hash_identity)
        
        except IndexError:

            print("face_identification: No face detected")

class FacesImage(object):

    def __init__ (self, img_location):

        self.ary_image = face_recognition.load_image_file(img_location)
        self.pil_image = Image.fromarray(self.ary_image)
        self.faces_list = []

    def _locate_faces(self):

        face_locations = face_recognition.face_locations(self.ary_image)

        return face_locations

    def _padding(self, box, pixel):

        box[0] -= pixel
        box[1] -= pixel
        box[2] += pixel
        box[3] += pixel

    def _regularize_locations(self, face_locations):

        for face_location in face_locations:
            tmpbox = [0] * 4
            for i in range(4):
                tmpbox[i] = face_location[i]

            tmpface = Face()

            tmpface.box[0] = tmpbox[3]
            tmpface.box[1] = tmpbox[0]
            tmpface.box[2] = tmpbox[1]
            tmpface.box[3] = tmpbox[2]

            self._padding(tmpface.box, 15)

            self.faces_list.append(tmpface)

    def _crop_faces(self):

        face_locations = self._locate_faces()
        self._regularize_locations(face_locations)

        tmp_pil_image = Image.fromarray(self.ary_image)

        for face in self.faces_list:
            face.pil_image = tmp_pil_image.crop(face.box)
            face.ary_image = numpy.array(face.pil_image)
            print(str(face.box))
            face.pil_image.show()
          

    def _get_face_landmarks(self):

        for face in self.faces_list:

            try:
                face.face_landmarks = face_recognition.face_landmarks(face.ary_image)[0]
            except IndexError:
                print("No feature detected")
                self.faces_list.remove(face)
                continue

            for facial_feature in face.face_landmarks.keys():
                print("The {} in this face has the following points: {}".format(facial_feature, face.face_landmarks[facial_feature]))

    def _draw_facial_feature_on_img(self):

        for face in self.faces_list:

            d_image = ImageDraw.Draw(face.pil_image)

            for facial_feature in face.face_landmarks.keys():

                d_image.line(face.face_landmarks[facial_feature], width = 3)

            # Show the picture
            face.pil_image.show()
        


    def _draw_feature_map(self):

        for face in self.faces_list:

            blackbg_img = Image.new("RGB", self.pil_image.size)

            d_black_img = ImageDraw.Draw(blackbg_img)

            for facial_feature in face.face_landmarks.keys():

                origin_landmarks = []
                
                for landmark in face.face_landmarks[facial_feature]:

                    tmpmark = [0] * 2
                    tmpmark[0] = face.box[0] + landmark[0]
                    tmpmark[1] = face.box[1] + landmark[1]

                    tmpmark = tuple(tmpmark)

                    origin_landmarks.append(tmpmark)


                d_black_img.line(origin_landmarks, width = 3)

            # Show the picture

            blackbg_img.show()
            face.blackbg_img = blackbg_img

    def _faces_identification(self):

        for face in self.faces_list:

            face.face_identification()

            # print(face.identity)

    def run(self):

        # crop faces in the image, store them in both array form and pil form
        self._crop_faces()

        # extract and draw facial feature on faces, generate feature maps
        self._get_face_landmarks()
        self._draw_facial_feature_on_img()
        self._draw_feature_map()

        # identify faces, store hash value of face identity
        self._faces_identification()


if __name__ == '__main__':

    face_image = FacesImage('pic/index.jpg')
    face_image.run()
