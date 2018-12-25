from PIL import Image, ImageDraw
import face_recognition
import numpy

class Face(object):

    def __init__(self):
        self.box = [0] * 4
        self.ary_image = []
        self.pil_image = 0
        self.face_landmarks = {}
class FaceId(object):

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
            # face.pil_image.show()

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
            # face.pil_image.show()


    def _extract_facial_feature(self):

        for face in self.faces_list:

            background_img = Image.new("RGB", self.pil_image.size)

            d_black_img = ImageDraw.Draw(background_img)

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

            background_img.show()


    def run(self):

        self._crop_faces()
        self._get_face_landmarks()
        self._draw_facial_feature_on_img()
        self._extract_facial_feature()


if __name__ == '__main__':

    faceid = FaceId('pic/group.jpg')
    faceid.run()
