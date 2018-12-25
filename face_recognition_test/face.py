from PIL import Image, ImageDraw
import face_recognition
import numpy

class FaceId (object):

    def __init__ (self, img_location):

        self.ary_image = face_recognition.load_image_file(img_location)
        self.pil_image = 0
        self.box = [0] * 4
        self.face_landmarks_list = []

    def _locate_faces(self):

        face_locations = face_recognition.face_locations(self.ary_image)

        return face_locations[0]

    def _regularize_locations(self, face_location):

        tmpbox = [0] * 4
        for i in range(4):
            tmpbox[i] = face_location[i]

        self.box[0] = tmpbox[3]
        self.box[1] = tmpbox[0]
        self.box[2] = tmpbox[1]
        self.box[3] = tmpbox[2]

    def _padding(self, pixel):

        self.box[0] -= pixel
        self.box[1] -= pixel
        self.box[2] += pixel
        self.box[3] += pixel

    def _crop_face(self):

        face_location = self._locate_faces()
        self._regularize_locations(face_location)
        self._padding(15)

        tmp_pil_image = Image.fromarray(self.ary_image)
        self.pil_image = tmp_pil_image.crop(self.box)
        self.ary_image = numpy.array(self.pil_image)

        print(str(self.box))
        self.pil_image.show()

    def _get_face_landmarks(self):

        self.face_landmarks_list = face_recognition.face_landmarks(self.ary_image)

        print("I found {} face(s) in this photograph.".format(len(self.face_landmarks_list)))

        for face_landmarks in self.face_landmarks_list:

            # Print the location of each facial feature in this image
            for facial_feature in face_landmarks.keys():
                print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))

    def _draw_facial_feature(self):

        d_image = ImageDraw.Draw(self.pil_image)

        for face_landmarks in self.face_landmarks_list:

            for facial_feature in face_landmarks.keys():

                d_image.line(face_landmarks[facial_feature], width = 3)

        # Show the picture
        self.pil_image.show()

    def run(self):

        self._crop_face()
        self._get_face_landmarks()
        self._draw_facial_feature()


if __name__ == '__main__':

    face = FaceId('pic/index.jpg')
    face.run()