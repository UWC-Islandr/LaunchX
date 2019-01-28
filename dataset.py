from fr_api import *
import glob

if __name__ == '__main__':

    file_names = glob.glob(r'./dataset/pic/*.JPG')
    file_names.sort()

    print(file_names)

    for file in file_names:

        save_path = "".join("./dataset/feature/{}.png".format(file[14:18]))
        print(save_path)
        face_image = FacesImage(file)
        face_image.run()
        # face_image.show()
        face_image.save(save_path)
