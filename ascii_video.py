import os
import shutil
import subprocess
import sys
import time

from PIL import Image


class AVFile():
    def __init__(self, filename, mode, debug=False):
        '''
        Signature Width Height Frame_Count FPS Data
        '''
        self.grayscale = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
        self.filename = filename.rsplit('.', 1)[0]
        self.mode = mode
        self.debug = debug
        self.handle = open(self.filename + '.avf', mode + 'b')

        if mode == 'r':
            self.signature = self.read_str(3)
            self.width = self.read_int(1)
            self.height = self.read_int(1)
            self.frame_count = self.read_int(3)
            self.fps = self.read_int(1)

        if mode == 'w':
            self.signature = 'AVF'
            self.write_str(self.signature)
            self.create_ascii_video(self.filename)

    def extract_images(self, video):
        '''
        extract frames from image using ffmpeg
        '''
        if os.path.exists('images'):
            shutil.rmtree('images')
        os.makedirs('images')

        log = 'ffmpeg.log'
        with open(log, 'w') as f:
            subprocess.call(['ffmpeg', '-i', video + '.mp4', 'images/%06d.jpg'], stdout=f, stderr=subprocess.STDOUT)

        self.fps = 60
        with open(log, 'r') as f:
            output = f.read()
            self.fps = round(float(output[:output.index('fps') - 1].rsplit(' ', 1)[1]))

        os.remove(log)

    def create_ascii_video(self, video):
        self.extract_images(video)

        self.frame_count = len(os.listdir('images'))
        video_width, video_height = Image.open('images/000001.jpg').size
        self.width = 180
        self.height = int(self.width / video_width * video_height / 1.5)

        self.write_int(self.width, 1)
        self.write_int(self.height, 1)
        self.write_int(self.frame_count, 3)
        self.write_int(self.fps, 1)

        for i in range(1, self.frame_count + 1):
            if self.debug:
                print('Processing frame {} of {}'.format(i, self.frame_count))
            image = Image.open('images/{0:06d}.jpg'.format(i)).convert('L').resize((self.width, self.height), Image.LANCZOS)
            for h in range(self.height):
                for w in range(self.width):
                    self.write_str(self.grayscale[int(image.getpixel((w, h)) * 69 / 255)])

    def play(self):
        for i in range(self.frame_count):
            frame = self.handle.read(self.width * self.height).decode('utf-8')
            for r in range(0, len(frame), self.width):
                print(frame[r:r + self.width])
            time.sleep(1.0 / self.fps)

    def read_str(self, n):
        return self.handle.read(n).decode('utf-8')

    def read_int(self, n):
        return int.from_bytes(self.handle.read(n), byteorder='big')

    def write_str(self, data):
        self.handle.write(data.encode())

    def write_int(self, data, n):
        self.handle.write(data.to_bytes(n, byteorder='big'))

    def close(self):
        if os.path.exists('images'):
            shutil.rmtree('images')
        self.handle.close()

if __name__ == '__main__':
    command = sys.argv[1]
    filename = sys.argv[2]

    if command == 'create':
        avf = AVFile(filename, 'w')
        avf.close()

    elif command == 'play':
        avf = AVFile(filename, 'r', True)
        avf.play()
        avf.close()
