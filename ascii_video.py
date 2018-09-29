import os
import shutil
import subprocess
import sys
import time

from PIL import Image


class AVFile():
    def __init__(self, filename, mode, debug=False):
        '''
        Signature Width Height Frame_Count Data
        '''
        self.grayscale = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
        self.filename = filename.rsplit('.', 1)[0]
        self.mode = mode
        self.debug = debug
        self.handle = open(self.filename + '.avf', mode + 'b')

        if mode == 'r':
            self.signature = self.handle.read(3).decode('utf-8')
            self.width = int.from_bytes(self.handle.read(1), byteorder='big')
            self.height = int.from_bytes(self.handle.read(1), byteorder='big')
            self.frame_count = int.from_bytes(self.handle.read(3), byteorder='big')

        if mode == 'w':
            self.signature = 'AVF'
            self.handle.write(self.signature.encode())
            self.create_ascii_video(self.filename)

    def extract_images(self, video):
        '''
        extract frames from image using ffmpeg
        '''
        if os.path.exists('images'):
            shutil.rmtree('images')
        os.makedirs('images')
        subprocess.call(['ffmpeg', '-i', video + '.mp4', 'images/%06d.jpg'])

    def create_ascii_video(self, video):
        self.extract_images(video)

        self.frame_count = len(os.listdir('images'))
        video_width, video_height = Image.open('images/000001.jpg').size
        self.width = 120
        self.height = int(self.width / video_width * video_height)

        self.handle.write(self.width.to_bytes(1, byteorder='big'))
        self.handle.write(self.height.to_bytes(1, byteorder='big'))
        self.handle.write(self.frame_count.to_bytes(3, byteorder='big'))

        for i in range(1, self.frame_count + 1):
            if self.debug:
                print('Processing frame {} of {}'.format(i, self.frame_count))
            image = Image.open('images/{0:06d}.jpg'.format(i)).convert('L').resize((self.width, self.height), Image.LANCZOS)
            for h in range(self.height):
                for w in range(self.width):
                    self.handle.write(self.grayscale[int(image.getpixel((w, h)) * 69 / 255)].encode())

    def play(self):
        for i in range(self.frame_count):
            frame = self.handle.read(self.width * self.height).decode('utf-8')
            for r in range(0, len(frame), self.width):
                print(frame[r:r + self.width])
            time.sleep(0.001)

    def close(self):
        if os.path.exists('images'):
            shutil.rmtree('images')
        self.handle.close()

if __name__ == '__main__':
    command = sys.argv[1]
    filename = sys.argv[2]

    if command == 'create':
        avf = AVFile(filename, 'w', True)
        avf.close()

    elif command == 'play':
        avf = AVFile(filename, 'r', True)
        avf.play()
        avf.close()
