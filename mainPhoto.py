import os
from PIL import Image


class PhotoResizer:
    def __init__(self, photo_directory, new_photo_directory):
        self.photo_directory = photo_directory
        self.new_photo_directory = new_photo_directory
        os.makedirs(self.new_photo_directory, exist_ok=True)

    def resize_photo(self, filename, percent_reduction=10):
        filepath = os.path.join(self.photo_directory, filename)
        with Image.open(filepath) as img:
            width, height = img.size
            percent = 100
            while os.path.getsize(filepath) > 700 * 1024:
                new_width = int(width * percent / 100)
                new_height = int(height * percent / 100)
                resized_img = img.resize((new_width, new_height))
                resized_img.save(os.path.join(self.new_photo_directory, filename))
                percent -= percent_reduction
                if percent <= 0:
                    break

    def process_photos(self):
        for filename in os.listdir(self.photo_directory):
            filepath = os.path.join(self.photo_directory, filename)
            if os.path.isfile(filepath) and filename.lower().endswith('.jpg'):
                self.resize_photo(filename)


if __name__ == '__main__':
    resizer = PhotoResizer('photo', 'new_photo')
    resizer.process_photos()
    print("All ok")
