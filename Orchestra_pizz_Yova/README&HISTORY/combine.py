import xml.etree.ElementTree as ET
import os
import shutil

# Заданные диапазоны для каждого инструмента
RANGES = {
    'DoubleBass_pizz_Yova.dspreset': {'lo': 24, 'hi': 55},
    'Cello_pizz_Yova.dspreset':      {'lo': 56, 'hi': 70},
    'Viola_pizz_Yova.dspreset':      {'lo': 71, 'hi': 78},
    'Violin_pizz_Yova.dspreset':     {'lo': 79, 'hi': 100}
}

def merge_presets():
    # Создаем корневой элемент нового пресета
    root = ET.Element("DecentSampler")

    # Настраиваем интерфейс
    ui = ET.SubElement(root, "ui", width="812", height="375", bgImage="University of Yova. Thanks you!(All together).jpg")
    tab = ET.SubElement(ui, "tab", name="main")

    # Заголовок для объединенного патча
    ET.SubElement(tab, "label", x="250", y="140", width="312", height="40", text="ORCHESTRA PIZZ YOVA", textColor="ffffff", textSize="28")

    # Настраиваем параметры группы
    groups = ET.SubElement(root, "groups", seqMode="round_robin", attack="0.001", release="0.15", volume="3dB")
    main_group = ET.SubElement(groups, "group", name="Main")

    samples_count = 0

    # Проходим по всем файлам и фильтруем сэмплы
    for filename, note_range in RANGES.items():
        if not os.path.exists(filename):
            print(f"Внимание: Файл {filename} не найден в текущей папке. Проверьте название.")
            continue

        print(f"Обработка {filename} (диапазон {note_range['lo']}-{note_range['hi']})...")
        tree = ET.parse(filename)

        # Ищем все сэмплы в текущем документе
        for sample in tree.findall(".//sample"):
            root_note = int(sample.get("rootNote"))

            # Если rootNote входит в заданный диапазон (от lo до hi включительно)
            if note_range['lo'] <= root_note <= note_range['hi']:
                # Создаем копию тега sample со всеми его атрибутами и добавляем в новый документ
                ET.SubElement(main_group, "sample", sample.attrib)
                samples_count += 1

    # Имя финального документа
    output_filename = "Combined_pizz_Yova.dspreset"

    # Форматирование XML для аккуратных отступов
    if hasattr(ET, 'indent'):
        ET.indent(root, space="    ", level=0)

    tree_out = ET.ElementTree(root)

    # Сохраняем итоговый файл
    tree_out.write(output_filename, encoding="utf-8", xml_declaration=True)

    print("-" * 40)
    print(f"Готово! Финальный документ '{output_filename}' успешно создан.")
    print(f"Всего включено сэмплов в сборку: {samples_count}")

    return output_filename

def cleanup_unused_samples(preset_file):
    print("-" * 40)
    print("Запуск проверки неиспользуемых сэмплов...")

    if not os.path.exists(preset_file):
        print(f"Ошибка: Файл {preset_file} не найден.")
        return

    # 1. Читаем итоговый пресет, чтобы узнать, какие сэмплы используются
    tree = ET.parse(preset_file)
    used_samples = set()

    for sample in tree.findall(".//sample"):
        path = sample.get("path")
        if path:
            # На всякий случай нормализуем слеши для точного сравнения
            used_samples.add(path.replace('\\', '/'))

    samples_dir = "Samples"
    trash_dir = os.path.join(samples_dir, "trash") # Папка trash внутри Samples

    if not os.path.exists(samples_dir):
        print(f"Папка '{samples_dir}' не найдена. Очистка отменена.")
        return

    # Создаем папку trash, если её еще нет
    if not os.path.exists(trash_dir):
        os.makedirs(trash_dir)

    moved_count = 0

    # 2. Перебираем все .wav файлы в папке Samples
    for filename in os.listdir(samples_dir):
        if filename.endswith(".wav"):
            # Формируем путь в таком же виде, как он записан в XML (Samples/имя.wav)
            sample_path = f"Samples/{filename}"

            # Если этого пути нет в итоговом пресете — перемещаем в корзину
            if sample_path not in used_samples:
                src = os.path.join(samples_dir, filename)
                dst = os.path.join(trash_dir, filename)
                shutil.move(src, dst)
                moved_count += 1
                print(f" Перемещено в trash: {filename}")

    print("-" * 40)
    print(f"Очистка завершена! Лишних файлов убрано: {moved_count}.")
    print(f"Все ненужные сэмплы находятся в папке: '{trash_dir}'.")

if __name__ == "__main__":
    # Сначала генерируем или обновляем общий пресет
    final_preset = merge_presets()

    # Затем запускаем очистку папки Samples от неиспользуемых файлов
    if final_preset:
        cleanup_unused_samples(final_preset)
