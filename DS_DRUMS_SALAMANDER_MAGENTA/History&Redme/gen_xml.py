import os
import librosa
import xml.etree.ElementTree as ET

# Путь к сэмплам
SAMPLES_DIR = "Samples"
OUTPUT_FILE = "G-point.dspreset"

def get_start_point(filepath):
    # Загружаем только начало файла для скорости (первые 2 секунды)
    y, sr = librosa.load(filepath, sr=None, duration=2.0)
    # Ищем первый транзиент (удар)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    if len(onset_frames) > 0:
        # Возвращаем время в секундах, умноженное на 1000 (для DecentSampler нужно в мс)
        return int(librosa.frames_to_time(onset_frames[0], sr=sr) * 1000)
    return 0

# Создаем структуру XML
root = ET.Element("DecentSampler")
ui = ET.SubElement(root, "ui", width="812", height="375")
groups = ET.SubElement(root, "groups", seqMode="round_robin", attack="0.001", release="0.15")

for filename in sorted(os.listdir(SAMPLES_DIR)):
    if filename.endswith(".wav"):
        filepath = os.path.join(SAMPLES_DIR, filename)
        start_ms = get_start_point(filepath)
        
        # Добавляем сэмпл
        sample = ET.SubElement(groups, "sample", path=f"Samples/{filename}", start=str(start_ms))
        # Здесь можно добавить логику определения MIDI нот из имени файла, если нужно
        print(f"Обработан {filename} -> start={start_ms}ms")

# Сохраняем
tree = ET.ElementTree(root)
tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)
print(f"--- Готово! Файл {OUTPUT_FILE} создан ---")
