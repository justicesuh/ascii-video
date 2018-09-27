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

    video = sys.argv[1]
    extract_images(video)

    for i in range(len(os.listdir('images'))):
        filename = 'images/{0:06d}.jpg'.format(i + 1)

        image = Image.open(filename).convert('L')
        width, height = image.size

        ascii_width = 120
        ascii_height = int(ascii_width / width * height)
        image = image.resize((ascii_width, ascii_height), Image.LANCZOS)

        ascii_art = ''
        for h in range(ascii_height):
            for w in range(ascii_width):
                ascii_art += grayscale[int(image.getpixel((w, h)) * 69 / 255)]
        
        for i in range(0, len(ascii_art), ascii_width):
            print(ascii_art[i:i + ascii_width])

    shutil.rmtree('images')    
