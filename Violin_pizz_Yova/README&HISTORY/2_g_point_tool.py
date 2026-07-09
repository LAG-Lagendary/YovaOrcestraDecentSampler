import os
import csv
import librosa

# Убедитесь, что путь к папке верный (относительно того места, где вы запускаете скрипт)
SAMPLES_DIR = "Samples"
OUTPUT_FILE = "2_results_g_point.csv"
OFFSET_MS = 25  # Теперь мы прибавляем это значение

def get_onset_ms(filepath):
    """Находит первый транзиент и возвращает его время в мс."""
    try:
        # Загружаем аудио
        y, sr = librosa.load(filepath, sr=None, duration=2.0)
        # Отключаем backtrack для более жесткого определения атаки
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr, backtrack=False)
        if len(onset_frames) > 0:
            return int(librosa.frames_to_time(onset_frames[0], sr=sr) * 1000)
    except Exception as e:
        print(f"Ошибка при обработке {filepath}: {e}")
    return 0

# Проверка существования папки
if not os.path.exists(SAMPLES_DIR):
    print(f"ОШИБКА: Папка '{SAMPLES_DIR}' не найдена. Проверьте путь.")
else:
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "g_point_ms", "offset_ms", "final_start_ms"])

        print(f"Начинаю сканирование: {SAMPLES_DIR}\n")

        for root, dirs, files in os.walk(SAMPLES_DIR):
            for filename in files:
                if filename.lower().endswith((".wav", ".aif", ".aiff")):
                    filepath = os.path.join(root, filename)

                    g_point = get_onset_ms(filepath)

                    # Агрессивный сдвиг: ПРИБАВЛЯЕМ 25 мс
                    final_start = g_point + OFFSET_MS

                    writer.writerow([filename, g_point, OFFSET_MS, final_start])
                    print(f"Файл: {filename:30} | G-point: {g_point:4}ms | Итог: {final_start:4}ms")

    print(f"\n--- Готово! Результаты записаны в {OUTPUT_FILE} ---")
