import os
import argparse
from datetime import datetime
from PIL import Image
from pdf2image import convert_from_path


class PhotoResizer:
    def __init__(self, photo_directory, new_photo_directory):
        self.photo_directory = photo_directory
        self.new_photo_directory = new_photo_directory

    def resize_photo(self, filepath, filename, quality_reduction=10):
        # Выводим название файла при его обработке
        print("Обрабатывается файл:", filename)

        # Проверяем формат файла
        if filename.lower().endswith('.pdf'):
            self.convert_pdf_to_images(filepath, filename)
        elif filename.lower().endswith('.jpg'):
            self.process_jpg_file(filepath, filename, quality_reduction)
        else:
            print("Неподдерживаемый формат файла:", filename)

    def convert_pdf_to_images(self, filepath, filename):
        # Создаем папку для сохранения изображений из PDF
        output_directory = os.path.join(self.photo_directory, os.path.splitext(filename)[0])
        os.makedirs(output_directory, exist_ok=True)

        # Извлекаем изображения из PDF и сохраняем их
        images = convert_from_path(filepath)
        for i, image in enumerate(images):
            image_path = os.path.join(output_directory, f"{i + 1}.jpg")
            image.save(image_path, "JPEG")

    def process_jpg_file(self, filepath, filename, quality_reduction):
        # Открываем изображение
        with Image.open(filepath) as img:
            # Определяем начальные размеры изображения
            width, height = img.size
            # Устанавливаем начальное качество изображения
            quality = 100
            # Проверяем размер изображения
            if os.path.getsize(filepath) > 700 * 1024:
                # Постепенно уменьшаем качество до тех пор, пока не будет меньше 700 кб
                while os.path.getsize(filepath) > 700 * 1024:
                    # Создаем путь к новой директории
                    new_directory = self.create_new_directory(self.photo_directory)
                    # Сохраняем уменьшенное изображение в новый каталог с тем же именем файла
                    img.save(os.path.join(new_directory, filename), quality=quality)
                    # Обновляем качество изображения для следующей итерации
                    quality -= quality_reduction
                    # Проверяем, что качество не стало меньше или равным 0
                    if quality <= 0:
                        break
            else:
                # Сохраняем оригинальный файл в новый каталог
                new_directory = self.create_new_directory(self.new_photo_directory)
                img.save(os.path.join(new_directory, filename))

    def create_new_directory(self, directory):
        # Создаем имя для нового каталога на основе текущей даты и времени
        current_datetime = datetime.now().strftime('%d.%m.%Y_%H.%M')
        new_directory = os.path.join(directory, 'photos_' + current_datetime)
        # Создаем новую директорию, если она еще не существует
        os.makedirs(new_directory, exist_ok=True)
        return new_directory

    def process_photos(self):
        # Проходим по каждому файлу в каталоге с фотографиями
        for root, dirs, files in os.walk(self.photo_directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                # Передаем путь к файлу методу для обработки
                self.resize_photo(filepath, filename)


def main():
    # Создаем парсер аргументов командной строки
    # parser = argparse.ArgumentParser(description='Resize photos in a directory.')
    # parser.add_argument('-p', '--path', help='Path to the directory with photos', required=True)
    # args = parser.parse_args()
    f_path = "/Users/rusdev/Downloads/photo/photos"

    # Создаем экземпляр класса PhotoResizer и обрабатываем фотографии
    # resizer = PhotoResizer(args.path, os.getcwd())  # Передаем текущую директорию
    resizer = PhotoResizer(f_path, os.getcwd())  # Передаем текущую директорию
    resizer.process_photos()


if __name__ == "__main__":
    main()
