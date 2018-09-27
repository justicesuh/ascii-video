import sys

from PIL import Image

if __name__ == '__main__':
    grayscale = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '

    filename = sys.argv[1]
    image = Image.open(filename).convert('L')
    width, height = image.size

    ascii_art = ''
    for h in range(height):
        for w in range(width):
            pixel = image.getpixel((w, h))
            index = int(pixel * (len(grayscale) - 1) / 255)
            ascii_art += grayscale[index]
    
    for i in range(0, len(ascii_art), width):
        print(ascii_art[i:i + width])
