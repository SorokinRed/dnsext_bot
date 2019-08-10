import argparse
import os
import time

import cv2
import imagehash
import numpy as np
from PIL import Image


class CrackCaptcha():
    hash_symbols = {'c31e7c613b61b4c3': '#',
                'c5921f4a39b562b5': 'e',
                '918d68354bca373b': '3',
                '953e1e704bcb6e0c': 'd',
                '80082a220aa2a00a': '*',
                'c0944bda3f611f27': 'p',
                'a5720e996e8d7b0c': 'u',
                'c14f62961f4a35ad': 's',
                'c04e1fb51a5b61e6': '6',
                'd3964cd71f781849': '@',
                '8011a0442a102a15': 'z',
                '90e04bb70fc86f6a': '5',
                'c06337cd2fb30ea4': 'k',
                '921b2fe06e3d33a4': 'a',
                'c2e4351f1d7b4ab0': 'x',
                'c0953d663f6a6e48': 'r',
                '95c31e8f6a346b32': 'q',
                '80400a4128152015': 'o',
                'f0d85b333b262e26': 'n',
                '95e44a1f4ff1344c': '9',
                'd1f93e862e162c47': 'w',
                'c5001e007a006800': 'c',
                '8044200520410a14': '%',
                'c4b0e7cc59433e66': '7',
                'c14e36f12d4e72a5': '&',
                '82000a0028002000': '0',
                'fcd6562c2e292b29': 'm',
                '81e56a3d1f4265b3': '$',
                '9032c14b1e372fbd': '2',
                'c5903d2d38d2726f': 'f',
                '95e41e8d6a726cd2': 'g',
                '921e3cb11bce64d3': '8',
                'c6e5399b3a18331e': 'v',
                'c6b265191b4e3a4f': 'y',
                '920e3cf16327e47a': '4',
                'e04b6b371e941b33': 'h',
                'cde1344f6a9670b4': 't',
                '88002a00a2002a00': '+',
                'c06b4b251e9e3dd8': 'b'}
    def only_symbols(self, img_path):
        low_red = (0,50,0)
        high_red = (255, 255, 255)

        img = cv2.imread(img_path, 1)

        return cv2.inRange(img, low_red, high_red)

    def detect_vertical(self, img):
        '''
        разрезаю картинку на символы по вертикали
        возвращается массив маленьких картинок
        '''
        black = np.zeros_like(img)
        black = np.rot90(black)
        rot = np.rot90(img.copy())

        index = 0
        for row in rot:
            if 255 in row:
                    black[index] = [
                    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                    255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
            index += 1

        black = np.rot90(black)
        black = np.rot90(black)
        black = np.rot90(black)

        index = 0
        x1 = 0
        x2 = 0
        vert = []
        for p in black[1]:
            if 255 != black[1][index-1] and 255 == p:
                    x1 = index
            if 255 == p and 255 != black[1][index+1]:
                    x2 = index
            index += 1
            if x1 != 0 and x2 != 0:
                    vert.append(img[0:49, x1-1:x2+2])
                    #os.remove(filename)
                    x1 = 0
                    x2 = 0
        return vert

    def horisont(self, img):
        index = 0
        y1 = 0
        y2 = 0
        for i in img:
            if 255 in i and 255 not in img[index-1]:
                y1 = index
            if 255 in i and 255 not in img[index+1]:
                y2 = index

            if y1 != 0 and y2 != 0:
                hor = img[y1-1:y2+2, 0:len(img)]
                y1 = 0
                y2 = 0
                return hor
            index += 1

    def image_hash(self, temp_img):
        img = Image.open(temp_img)
        img_hash = str(imagehash.phash(img))
        return img_hash

    def recognize_symbol(self, img_hash):
        return self.hash_symbols[img_hash]

    def crack_it(self, img_path):
        img = self.only_symbols(img_path)
        chars = []
        result = ''
        for i in self.detect_vertical(img):
            chars.append(self.horisont(i))
        
        for i in chars:
            cv2.imwrite('tmp.png', i)
            result = result + self.recognize_symbol(self.image_hash('tmp.png'))
            os.remove('tmp.png')
        return result

if __name__ == '__main__':
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", required=True, help="path to input image to be OCR'd")
        args = vars(ap.parse_args())
        crack = Crack_captcha()
        print(crack.crack_it(args["image"]))
