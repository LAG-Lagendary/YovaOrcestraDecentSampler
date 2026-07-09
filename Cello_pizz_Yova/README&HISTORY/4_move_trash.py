import os
import shutil
import csv

# Настройки
CSV_FILE = '3_bad_samples.csv'
BASE_DIR = 'Samples'  # Папка, где лежат ваши сэмплы
TRASH_DIR = os.path.join(BASE_DIR, 'trash')

def move_bad_samples():
    if not os.path.exists(CSV_FILE):
        print(f"Ошибка: Файл {CSV_FILE} не найден.")
        return

    # Создаем папку trash, если её нет
    if not os.path.exists(TRASH_DIR):
        os.makedirs(TRASH_DIR)
        print(f"Создана папка: {TRASH_DIR}")

    # Читаем список файлов
    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row['filename']

            # Ищем файл рекурсивно внутри Samples
            found = False
            for root, dirs, files in os.walk(BASE_DIR):
                if filename in files:
                    src_path = os.path.join(root, filename)
                    dest_path = os.path.join(TRASH_DIR, filename)

                    try:
                        shutil.move(src_path, dest_path)
                        print(f"Перемещено: {filename}")
                        found = True
                        break
                    except Exception as e:
                        print(f"Ошибка при перемещении {filename}: {e}")

            if not found:
                print(f"Файл не найден (или уже перемещен): {filename}")

if __name__ == "__main__":
    move_bad_samples()
    print("\nОперация завершена.")
