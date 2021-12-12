from PIL import Image
import sys
import os

# ASCII Shade from Dark to Light. The last part represents the characterset length.
asciishade_d2l_l02      = "▓ "
asciishade_d2l_l04      = "▓▒░ "
asciishade_d2l_l09_v1   = "█▇▆▅▄▃▂▁ "
asciishade_d2l_l09_v2   = "█▉▊▋▌▍▎▏ "
asciishade_d2l_l10      = "@%#*+=-:. "
asciishade_d2l_l70      = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """

class Image2Ascii:
    def __init__(self, imagefname):
        self.imagefname  = imagefname
        self.imagefexist = os.path.exists(imagefname)
        self.isprocessed = False
        self.asciicontianer = ''

    def getsize(self):
        if not self.imagefexist: return
        image = Image.open(self.imagefname)
        width, height = image.size
        image.close()
        return (width, height)

    def getrows(self, cols, scale, width, height):
        w = width / cols
        h = w / scale
        rows = height / h

        return int(rows)

    def getcols(self, rows, scale, width, height):
        h = rows / height
        w = h * scale
        cols = width / w

        return int(cols)
    
    def process(self, cols, rows, scale, shade_level=asciishade_d2l_l10):
        if self.isprocessed:
            return

        if not self.imagefexist: return

        self.asciicontianer = ''
        image = Image.open(self.imagefname)

        width, height = image.size
        scale_width  = int(width // cols)
        scale_height = int(scale_width // scale)

        progress_percent = 0.
        progress_total = rows * cols
        
        for y in range(rows):
            y1, y2 = y * scale_height, (y + 1) * scale_height
            if y2 > height: y2 = height

            for x in range(cols):
                x1, x2 = x * scale_width, (x + 1) * scale_width
                if x2 > width: x2 = width

                image_window = image.crop((x1, y1, x2, y2))
                pixel_intensity = 0.

                for j in range(y2 - y1):
                    for i in range(x2 - x1):
                        r, g, b = image_window.getpixel((i, j))
                        greypixel = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                        pixel_intensity += greypixel

                pixel_intensity /= ((y2 - y1) * (x2 - x1))

                asciichar = shade_level[::-1][int(pixel_intensity * len(shade_level))]
                self.asciicontianer += asciichar

                progress_percent = (((y * cols) + x) * 30) // progress_total
                print('[{:30s}] Completed.'.format('#' * int(progress_percent)), end='\r')
            self.asciicontianer += '\n'

        print('[{:30s}] Completed.'.format('#' * int(30)))
        self.isprocessed = True
        pass

    def reprocess(self, imagefname):
        self.imagefname = imagefname
        self.imagefexist = os.path.exists(imagefname)
        self.isprocessed = False
        self.process()

    def save(self, asciifname):
        f = open(asciifname, 'w', encoding="utf-8")
        f.write(self.asciicontianer)
        f.close()


    def print(self):
        print(self.asciicontianer)

def Usage():
    print('Usage:')
    print('python image2ascii.py <image_filename> <ascii_filename> <characterset>')
    varkeys = globals().keys()
    asciishade = ''
    for varkey in varkeys:
        if varkey.find('asciishade') != -1:
            asciishade += varkey + ', '

    print('Available characterset: ' + asciishade[: -2] + '.')

if __name__ == '__main__':
    print(' -------------------------------------------------------')
    print('|                     Image 2 ASCII                     |')
    print(' -------------------------------------------------------')
    if len(sys.argv) == 1:
        Usage()
    else:
        imagefname = sys.argv[1]
        asciifname = ''
        if len(sys.argv) > 2:
            asciifname = sys.argv[2]
        ascii_characterset = asciishade_d2l_l10
        if len(sys.argv) > 3:
            argv_characterset = sys.argv[3]
            if argv_characterset in globals().keys():
                ascii_characterset = globals()[argv_characterset]
            else:
                print('Characterset', argv_characterset, 'unknown! Switching to defauls', ascii_characterset)
        i2a = Image2Ascii(imagefname) 
        if i2a.imagefexist:
            width, height = i2a.getsize()
            cols = 80
            scale = .43
            rows = i2a.getrows(cols, scale, width, height)
            i2a.process(cols, rows, scale, ascii_characterset)
            if asciifname != '':
                i2a.save(asciifname)
                print(imagefname, 'converted to ascii and saved as', asciifname)
        else:
            print('Image file [', imagefname, '] does not exists!')
