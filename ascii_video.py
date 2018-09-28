import os
import shutil
import subprocess
import sys

from PIL import Image

def extract_images(video):
    if not os.path.exists('images'):
        os.makedirs('images')
    subprocess.call(['ffmpeg', '-i', video, 'images/%06d.jpg'])

if __name__ == '__main__':
    grayscale = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '

    command = sys.argv[1]
    filename = sys.argv[2]

    if command == 'create':
        extract_images(filename)

        num_frames = len(os.listdir('images'))
        width, height = Image.open('images/000001.jpg').size
        ascii_width = 120
        ascii_height = int(ascii_width / width * height)

        output = open('{}.avf'.format(filename.rsplit('.', 1)[0]), 'wb')
        for i in range(1, num_frames + 1):
            print('Processing Frame {} of {}'.format(i, num_frames))
            image = Image.open('images/{0:06d}.jpg'.format(i)).convert('L').resize((ascii_width, ascii_height), Image.LANCZOS)
            for h in range(ascii_height):
                for w in range(ascii_width):
                    output.write(grayscale[int(image.getpixel((w, h)) * 69 / 255)].encode())
        output.close()

        shutil.rmtree('images')

    elif command == 'play':
        pass
        
        # for i in range(0, len(ascii_art), ascii_width):
        #     print(ascii_art[i:i + ascii_width])

