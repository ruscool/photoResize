import os
import argparse
from datetime import datetime
from PIL import Image


class PhotoResizer:
    def __init__(self, photo_directory, new_photo_directory):
        self.photo_directory = photo_directory
        self.new_photo_directory = new_photo_directory

    def resize_photo(self, filename, quality_reduction=10):
        filepath = os.path.join(self.photo_directory, filename)
        with Image.open(filepath) as img:
            width, height = img.size
            quality = 100
            while os.path.getsize(filepath) > 700 * 1024:
                new_directory = self.create_new_directory()
                img.save(os.path.join(new_directory, filename), quality=quality)
                quality -= quality_reduction
                if quality <= 0:
                    break

    def create_new_directory(self):
        current_datetime = datetime.now().strftime('%d.%m.%Y_%H.%M')
        new_directory = os.path.join(os.path.dirname(self.photo_directory),
                                     os.path.basename(self.photo_directory) + '_' + current_datetime)
        os.makedirs(new_directory, exist_ok=True)
        return new_directory

    def process_photos(self):
        for filename in os.listdir(self.photo_directory):
            filepath = os.path.join(self.photo_directory, filename)
            if os.path.isfile(filepath) and filename.lower().endswith('.jpg'):
                self.resize_photo(filename)


def main():
    parser = argparse.ArgumentParser(description='Resize photos in a directory.')
    parser.add_argument('-p', '--path', help='Path to the directory with photos', required=True)
    args = parser.parse_args()

    resizer = PhotoResizer(args.path, '')
    resizer.process_photos()
    print("All ok")


if __name__ == "__main__":
    main()
