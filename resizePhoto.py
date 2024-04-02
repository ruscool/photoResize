import os
import argparse
from datetime import datetime
from PIL import Image


class PhotoResizer:
    def __init__(self, photo_directory, new_photo_directory):
        self.photo_directory = photo_directory
        self.new_photo_directory = new_photo_directory

    def resize_photo(self, filepath, filename, quality_reduction=10):
        with Image.open(filepath) as img:
            width, height = img.size
            quality = 100
            print(f'[img] {filename}')
            while os.path.getsize(filepath) > 700 * 1024:
                new_directory = self.create_new_directory(os.path.dirname(filepath))
                img.save(os.path.join(new_directory, filename), quality=quality)
                quality -= quality_reduction
                if quality <= 0:
                    break

    def create_new_directory(self, directory):
        current_datetime = datetime.now().strftime('%d.%m.%Y_%H.%M')
        new_directory = directory + '_' + current_datetime
        os.makedirs(new_directory, exist_ok=True)
        return new_directory

    def process_photos(self):
        for root, dirs, files in os.walk(self.photo_directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filename.lower().endswith('.jpg'):
                    self.resize_photo(filepath, filename)


def main():
    parser = argparse.ArgumentParser(description='Resize photos in a directory.')
    parser.add_argument('-p', '--path', help='Path to the directory with photos', required=True)
    args = parser.parse_args()

    # Создаем экземпляр класса PhotoResizer и обрабатываем фотографии
    resizer = PhotoResizer(args.path, '')
    resizer.process_photos()
    print("All ok")

if __name__== "__main__":

    main()