from PIL import Image, ImageDraw
import face_recognition

# Load the jpg file into a numpy array
image = face_recognition.load_image_file("pic/sky.jpg")

face_locations = face_recognition.face_locations(image)

box = [337, 229, 411, 304]

def padding(box, pixel):
    box[0] -= pixel
    box[1] -= pixel
    box[2] += pixel
    box[3] += pixel

padding(box, 10)

print(str(face_locations)+'\n')

# Find all facial features in all the faces in the image
face_landmarks_list = face_recognition.face_landmarks(image)

print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

# Create a PIL imagedraw object so we can draw on the picture
pil_image = Image.fromarray(image)

print(str(pil_image.size) + '\n')

d = ImageDraw.Draw(pil_image)

print(str(pil_image.size) + '\n')

# Print the region where contains face in the picture
region = pil_image.crop(box)
region.show()

for face_landmarks in face_landmarks_list:

    # Print the location of each facial feature in this image
    for facial_feature in face_landmarks.keys():
        print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))

    # Let's trace out each facial feature in the image with a line!
    for facial_feature in face_landmarks.keys():
        d.line(face_landmarks[facial_feature], width=5)

# Show the picture
pil_image.show()
