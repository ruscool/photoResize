import os
import argparse
import shutil
from datetime import datetime
from PIL import Image
from pdf2image import convert_from_path


class PhotoMirrorCreator:
    def __init__(self, photo_directory, mirror_directory):
        self.photo_directory = photo_directory
        self.mirror_directory = mirror_directory

    def create_mirror(self):
        # current_datetime = datetime.now().strftime('%d.%m.%Y_%H.%M')
        # mirror_directory_with_date = os.path.join(self.mirror_directory, f'зеркало_{current_datetime}')
        # os.makedirs(mirror_directory_with_date, exist_ok=True)
        count = 1
        main_output_directory = ""
        output_directory = ""
        main_output_directory_main = os.path.join(self.mirror_directory)
        first_folder: str = ""
        for root, dirs, files in os.walk(self.photo_directory):

            for dir in dirs:
                if count >= 2:
                    main_output_directory = os.path.join(main_output_directory, dir)
                    os.makedirs(output_directory, exist_ok=True)
                    for root2, dirs2, files2 in os.walk(main_output_directory):
                        for dir2 in dirs2:
                            # main_output_directory = os.path.join(main_output_directory, dir2)
                            output_directory = os.path.join(main_output_directory, dir2)
                            os.makedirs(output_directory, exist_ok=True)
                elif count == 1:
                    main_output_directory = os.path.join(main_output_directory_main, dir)
                    output_directory = os.path.join(main_output_directory)
                    first_folder = output_directory
                    os.makedirs(output_directory, exist_ok=True)
            for filename in files:
                filepath = os.path.join(root, filename)

                if filename.lower().endswith('.pdf'):
                    print(f'find [pdf] file: {filename}')
                    output_directory = os.path.join(first_folder, os.path.splitext(filename)[0])
                    os.makedirs(output_directory, exist_ok=True)
                    self.convert_pdf_to_images(filepath, output_directory)
                elif filename.lower().endswith('.jpg'):
                    print(f'find [jpg] file: {filename}')
                    new_filepath = os.path.join(self.mirror_directory, os.path.basename(root), filename)
                    os.makedirs(os.path.dirname(new_filepath), exist_ok=True)
                    # main_output_directory = main_output_directory_main
                    # add if

                    shutil.copyfile(filepath, new_filepath)
                else:
                    print("Неподдерживаемый формат файла:", filename)
            count += 1

    def convert_pdf_to_images(self, filepath, output_directory):
        images = convert_from_path(filepath)
        for i, image in enumerate(images):
            image_path = os.path.join(output_directory, f"{i + 1}.jpg")
            image.save(image_path, "JPEG")
            print(f'create jpg: {image_path}')

    def create_new_directory(self, new_directory: str):
        # current_datetime = datetime.now().strftime('%d.%m.%Y_%H.%M')
        # new_directory = os.path.join(os.path.dirname(self.mirror_directory),
        #                              os.path.basename(self.photo_directory) + '_' + current_datetime)
        # new_directory = self.mirror_directory
        os.makedirs(new_directory, exist_ok=True)
        return new_directory


class PhotoResizer:
    def __init__(self, photo_directory, resized_photo_directory):
        self.photo_directory = photo_directory
        self.resized_photo_directory = resized_photo_directory

    def resize_photos(self, ):
        for root, dirs, files in os.walk(self.photo_directory):
            output_directory: str = ""
            for dir in dirs:
                output_directory = os.path.join(self.resized_photo_directory, dir)
                os.makedirs(output_directory, exist_ok=True)
            for filename in files:
                new_filepath = os.path.join(self.photo_directory, os.path.basename(root), filename)
                # filepath = os.path.join(root, filename)
                folder_in = os.path.basename(root)
                if filename.lower().endswith('.jpg'):
                    self.resize_photo(new_filepath, folder_in)

    def resize_photo(self, filepath: str, folder_in, quality_reduction=10):
        with Image.open(filepath) as img:
            quality = 100
            while os.path.getsize(filepath) > 700 * 1024:
                new_filepath = os.path.join(self.resized_photo_directory, os.path.basename(folder_in),
                                            os.path.basename(filepath))
                img.save(new_filepath, quality=quality)
                quality -= quality_reduction
                if quality <= 0:
                    break


def delete_folder(folder_path):
    try:
        # Удаляем папку и все ее содержимое
        shutil.rmtree(folder_path)
        print(f"Папка {folder_path} успешно удалена.")
    except OSError as e:
        print(f"Ошибка при удалении папки {folder_path}: {e}")


def main():
    # parser = argparse.ArgumentParser(description='Resize photos and create mirror structure.')
    # parser.add_argument('-p', '--path', help='Path to the directory with photos', required=True)
    # args = parser.parse_args()
    f_path = "/Users/rusdev/Downloads/photo/photos"
    # 1 step
    # Определяем путь к зеркальной папке с учетом указанного пути в аргументе -p
    # mirror_directory = os.path.join(os.path.dirname(args.path), f'зеркало_{datetime.now().strftime("%d.%m.%Y_%H.%M")}')
    mirror_directory = os.path.join(os.path.normpath(f_path),
                                    f'{os.path.normpath(f_path)}_{datetime.now().strftime("%d.%m.%Y_%H.%M")}')

    mirror_creator = PhotoMirrorCreator(f_path, mirror_directory)
    mirror_creator.create_new_directory(mirror_directory)
    mirror_creator.create_mirror()

    # 2 step
    resized_photo_directory = os.path.join(os.path.dirname(f_path),
                                           f'{os.path.dirname(f_path)}_new')
    os.makedirs(resized_photo_directory, exist_ok=True)

    # 3 step
    resizer = PhotoResizer(mirror_directory, resized_photo_directory)
    resizer.resize_photos()

    # step 4  remove folder
    # delete_folder(mirror_directory)


if __name__ == "__main__":
    main()
    print("End")
