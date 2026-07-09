import os
import librosa
import numpy as np
import csv

# Ищем папку Samples везде, где бы она ни была
SAMPLES_DIR = 'Samples'
OUTPUT_FILE = '4_loudness_report.csv'

def get_rms(filepath):
    try:
        y, sr = librosa.load(filepath, sr=None, duration=1.0) # грузим 1 сек для скорости
        rms = librosa.feature.rms(y=y)
        return np.mean(rms)
    except Exception as e:
        print(f"Ошибка чтения {filepath}: {e}")
        return 0

def check_volume():
    loudness_data = []
    print(f"Сканирую директории в поисках файлов...")

    # Проходим по всему дереву папок из текущей директории
    for root, dirs, files in os.walk('.'):
        for filename in files:
            # Игнорируем файлы, которые мы уже создали (отчеты)
            if filename.lower().endswith(('.wav', '.aif', '.aiff', '.flac')):
                path = os.path.join(root, filename)
                print(f"Анализирую: {filename}")
                rms = get_rms(path)
                if rms > 0:
                    loudness_data.append({'filename': filename, 'rms': rms})

    if not loudness_data:
        print("Файлы не найдены! Проверьте, в той ли папке вы запускаете скрипт.")
        return

    # Считаем среднее
    all_rms = [d['rms'] for d in loudness_data]
    mean_rms = np.mean(all_rms)
    std_rms = np.std(all_rms)

    print(f"\nВсего проанализировано: {len(loudness_data)} файлов.")
    print(f"Средняя громкость (RMS): {mean_rms:.4f}")

    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'rms', 'deviation'])

        for item in loudness_data:
            deviation = item['rms'] - mean_rms
            if abs(deviation) > (std_rms * 1.5): # Порог 1.5 для чувствительности
                writer.writerow([item['filename'], item['rms'], deviation])

    print(f"Отчет готов: {OUTPUT_FILE}")

if __name__ == "__main__":
    check_volume()
