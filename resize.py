from PIL import Image
import glob

FINALSIZE = (1104, 736)

class ResizeImage(object):

    def __init__(self, path, final_size):

        self.origin_img = Image.open(path)
        self.origin_size = self.origin_img.size
        self.final_img = 0
        self.final_size = final_size
        self.width_resize = self._compare_size()
        self.print_size()

    def print_size(self):
        
        print(self.origin_size)

    def _compare_size(self):
        
        origin_ratio = self.origin_size[0] / self.origin_size[1]
        final_ratio = self.final_size[0] / self.final_size[1]

        if (origin_ratio < final_ratio):
            return True
        else:
            return False

    def _shrink_img(self):

        if (self.width_resize):

            shrink_ratio = (self.final_size[0] / self.origin_size[0])
            self.final_img = self.origin_img.resize((self.final_size[0], int(shrink_ratio * self.origin_size[1])))

        else:

            shrink_ratio = (self.final_size[1] / self.origin_size[1])
            self.final_img = self.origin_img.resize((int(shrink_ratio * self.origin_size[0]), self.final_size[1]))

        self.origin_size = self.final_img.size
        # print(self.origin_size)
        # self.final_img.show()

    def _crop_img(self):

        box = [0] * 4

        if (self.width_resize):

         
            box[0] = 0
            box[1] = int((self.origin_size[1] - self.final_size[1]) / 2)
            box[2] = self.final_size[0]
            box[3] = box[1] + self.final_size[1]

        else:

            box[0] = int((self.origin_size[0] - self.final_size[0]) / 2)
            box[1] = 0
            box[2] = box[0] + self.final_size[0] 
            box[3] = self.final_size[1]

        self.final_img = self.final_img.crop(box)

        print("size of final image:" + str(self.final_img.size))
        # self.final_img.show()

    def run(self):

        self._shrink_img()
        self._crop_img()
        
if __name__ == '__main__':

    file_names = glob.glob(r'./dataset/pic/*.jpeg')
    file_names.sort()

    print(file_names)

    for file in file_names:

        process_img = ResizeImage(file, (1104, 736))
        process_img.run()

        process_img.final_img.save(file)

    # process_img = ResizeImage("./dataset/pic/0101.jpeg", (1104, 736))
    # process_img.run_save()