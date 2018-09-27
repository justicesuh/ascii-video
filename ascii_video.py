import sys

from PIL import Image

if __name__ == '__main__':
    grayscale = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '

    filename = sys.argv[1]
    image = Image.open(filename).convert('L')
    width, height = image.size

    ascii_width = 80
    ascii_height = int(ascii_width / width * height)
    print(Image.NEAREST)
    image = image.resize((ascii_width, ascii_height), Image.LANCZOS)

    ascii_art = ''
    for h in range(ascii_height):
        for w in range(ascii_width):
            ascii_art += grayscale[int(image.getpixel((w, h)) * 69 / 255)]
    
    for i in range(0, len(ascii_art), ascii_width):
        print(ascii_art[i:i + ascii_width])
