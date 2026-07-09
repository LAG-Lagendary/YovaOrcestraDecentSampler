import pandas as pd
import librosa

# Используем исходный файл с результатами анализа
INPUT_FILE = '2_results_g_point.csv'
CLEAN_FILE = '3_clean_samples.csv'
TRASH_FILE = '3_bad_samples.csv'

def get_midi(filename):
    """Извлекает MIDI-ноту из имени файла, очищая от всех суффиксов."""
    try:
        # Разбиваем имя и берем часть с нотой (как мы делали раньше)
        parts = filename.split('.')
        # Ищем часть, которая содержит ноту (буква + цифра)
        # В именах типа Violin.pizz.ff.sulA.D6.stereo.wav это пред-последний или пред-пред-последний элемент
        raw_note = next(p for p in parts if any(c.isdigit() for c in p))
        clean_note = "".join([c for c in raw_note if c.isalnum()])
        return librosa.note_to_midi(clean_note)
    except Exception as e:
        print(f"Ошибка парсинга ноты для {filename}: {e}")
        return 0

# 1. Загрузка
df = pd.read_csv(INPUT_FILE)
df['midi'] = df['filename'].apply(get_midi)

# 2. Сортировка по высоте (от низкой к высокой)
df = df.sort_values(by='midi')

# 3. Отсекаем ровно 15 самых высоких (независимо от струны)
# iloc[-15:] берет 15 последних строк из отсортированного списка
top_15 = df.iloc[-15:]
clean_samples = df.iloc[:-15]

# 4. Сохранение
clean_samples.drop(columns=['midi']).to_csv(CLEAN_FILE, index=False)
top_15.drop(columns=['midi']).to_csv(TRASH_FILE, index=False)

print(f"Готово. В {CLEAN_FILE} сохранено {len(clean_samples)} сэмплов.")
print(f"15 самых высоких нот (независимо от струны) отправлены в {TRASH_FILE}.")
print(f"Список удаленных: {top_15['filename'].tolist()}")
