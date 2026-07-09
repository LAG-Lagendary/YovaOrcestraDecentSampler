#!/usr/bin/env python3
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
import librosa
import numpy as np
import os

CSV_FILE = '3_clean_samples.csv'
OUTPUT_FILE = 'Perfect_Instrument.dspreset'

def get_audio_info(filepath):
    """Возвращает средний RMS и частоту дискретизации файла."""
    # Получаем информацию о файле без полной загрузки (для скорости)
    y, sr = librosa.load(filepath, sr=None, duration=2.0)
    rms = np.mean(librosa.feature.rms(y=y))
    return rms, sr

def generate_preset():
    folder_name = os.path.basename(os.getcwd()).replace('_', ' ').upper()
    bg_image = next((f for f in os.listdir('.') if f.lower().endswith(('.jpg', '.png'))), "background.jpg")

    print("Анализ файлов и расчет нормализации...")
    file_info = {}
    with open(CSV_FILE, mode='r') as f:
        reader = list(csv.DictReader(f))
        for row in reader:
            rms, sr = get_audio_info(os.path.join('Samples', row['filename']))
            file_info[row['filename']] = {'rms': rms, 'sr': sr}

    target_rms = np.mean([info['rms'] for info in file_info.values()])

    root = ET.Element("DecentSampler")
    ui = ET.SubElement(root, "ui", width="812", height="375", bgImage=bg_image)
    ET.SubElement(ui, "tab", name="main").append(
        ET.Element("label", x="250", y="140", width="312", height="40",
                   text=folder_name, textColor="ffffff", textSize="28")
    )

    groups = ET.SubElement(root, "groups", seqMode="round_robin", attack="0.001", release="0.15", volume="3dB")
    group = ET.SubElement(groups, "group", name="Main")

    for row in reader:
        filename = row['filename']
        rms = file_info[filename]['rms']
        sr = file_info[filename]['sr']

        # Расчет Gain
        gain_db = 20 * np.log10(target_rms / rms) if rms > 0 else 0

        # ПЕРЕВОД В СЕМПЛЫ: (start_ms / 1000) * sr
        start_ms = float(row['final_start_ms'])
        start_samples = int((start_ms / 1000) * sr)

        midi_note = librosa.note_to_midi(filename.split('.')[-3])

        ET.SubElement(group, "sample",
                      path=f"Samples/{filename}",
                      start=str(start_samples), # Теперь здесь семплы
                      rootNote=str(midi_note),
                      loNote=str(midi_note),
                      hiNote=str(midi_note),
                      gain=f"{gain_db:.2f}dB")

    pretty_xml = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join([line for line in pretty_xml.splitlines() if line.strip()]))

    print(f"Пресет '{OUTPUT_FILE}' готов. Точки старта указаны в семплах.")

if __name__ == "__main__":
    generate_preset()
