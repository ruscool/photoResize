import os
import shutil
import argparse
from datetime import datetime
from PIL import Image
from pdf2image import convert_from_path


class PhotoMirrorCreator:
    def __init__(self, photo_directory, mirror_directory):
        self.photo_directory = photo_directory
        self.mirror_directory = mirror_directory

    def create_mirror(self):
        for root, dirs, files in os.walk(self.photo_directory):
            for directory in dirs:
                # Создаем папку в зеркальной структуре
                mirror_dir = os.path.join(self.mirror_directory, directory)
                os.makedirs(mirror_dir, exist_ok=True)

            for filename in files:
                filepath = os.path.join(root, filename)
                if filename.lower().endswith('.pdf'):
                    output_directory = os.path.join(root, os.path.splitext(filename)[0])
                    os.makedirs(output_directory, exist_ok=True)
                    self.convert_pdf_to_images(filepath, output_directory)
                    print(f'[save] pdf file in folder {os.path.splitext(filename)[0]}')
                elif filename.lower().endswith('.jpg'):
                    # Копируем jpg-файлы в зеркальную структуру с сохранением иерархии
                    mirror_filepath = os.path.join(self.mirror_directory,
                                                   os.path.relpath(filepath, self.photo_directory))
                    os.makedirs(os.path.dirname(mirror_filepath), exist_ok=True)
                    shutil.copyfile(filepath, mirror_filepath)
                    print(f'[copy] file {filename}')
                else:
                    print("Неподдерживаемый формат файла:", filename)

    def convert_pdf_to_images(self, filepath, output_directory):
        images = convert_from_path(filepath)
        for i, image in enumerate(images):
            image_path = os.path.join(output_directory, f"{i + 1}.jpg")
            image.save(image_path, "JPEG")


class PhotoResizer:
    def __init__(self, photo_directory, resized_photo_directory):
        self.photo_directory = photo_directory
        self.resized_photo_directory = resized_photo_directory

    def resize_photos(self):
        for root, dirs, files in os.walk(self.photo_directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filename.lower().endswith('.jpg'):
                    self.resize_photo(filepath)

    def resize_photo(self, filepath, quality_reduction=10):
        with Image.open(filepath) as img:
            quality = 100
            while os.path.getsize(filepath) > 700 * 1024:
                new_filepath = os.path.join(self.resized_photo_directory,
                                            os.path.relpath(filepath, self.photo_directory))
                os.makedirs(os.path.dirname(new_filepath), exist_ok=True)
                img.save(new_filepath, quality=quality)
                quality -= quality_reduction
                if quality <= 0:
                    break


def main():
    parser = argparse.ArgumentParser(description='Resize photos and create mirror structure.')
    parser.add_argument('-p', '--path', help='Path to the directory with photos', required=True)
    args = parser.parse_args()
    # f_path = "/Users/rusdev/Downloads/photo/photos"

    mirror_directory = os.path.join(os.path.dirname(args.path),
                                    f'{os.path.basename(args.path)}_{datetime.now().strftime("%d.%m.%Y_%H.%M")}')

    # mirror_directory = os.path.join(os.path.dirname(f_path),
    #                                 f'{os.path.basename(f_path)}_{datetime.now().strftime("%d.%m.%Y_%H.%M")}')
    mirror_creator = PhotoMirrorCreator(args.path, mirror_directory)
    mirror_creator.create_mirror()

    resized_photo_directory = os.path.join(os.path.dirname(args.path),
                                           f'{os.path.basename(args.path)}_new')
    # resized_photo_directory = os.path.join(os.path.dirname(f_path),
    #                                        f'{os.path.basename(f_path)}_new')
    os.makedirs(resized_photo_directory, exist_ok=True)

    resizer = PhotoResizer(mirror_directory, resized_photo_directory)
    resizer.resize_photos()

    # Удаление зеркальной папки после обработки
    delete_folder(mirror_directory)


def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Папка {folder_path} успешно удалена.")
    except OSError as e:
        print(f"Ошибка при удалении папки {folder_path}: {e}")


if __name__ == "__main__":
    main()
    print("End")
