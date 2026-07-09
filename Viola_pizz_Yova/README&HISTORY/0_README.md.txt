# LAG: Code & Music — Скриптовая база обработки сэмплов

Модульный конвейер (pipeline) для подготовки сэмплов инструментов к Decent Sampler.
Математический анализ: onset-детектирование, статистическая фильтрация, нормализация RMS.

## Pipeline (Инструкция)
Все операции проводятся в виртуальном окружении venv.

1. **Конвертация:** `./1.convert.sh`
2. **Анализ (G-point):** `python3 2_g_point_tool.py`
3. **Фильтрация:** `python3 3_filter_trash.py` (отсечение выбросов).
4. **Очистка:** `python3 4_move_trash.py`
5. **Генерация пресета:** `python3 5_gen_perfect_dspreset.py`

*Примечание: При ручном переименовании файлов в `Samples/` необходимо обновить CSV-файлы.*

Подготовка и конвертация
Если исходники в формате .aif, приведите их к wav:  Bash# Выполнить в папке проекта

./1.convert.sh

Активация окружения и анализ (G-point)

Bash
python3 -m venv venv
source venv/bin/activate
pip install -q librosa numpy pandas

# Вычисление точек атаки

python3 2_g_point_tool.py

Статистическая фильтрация
Исключение сэмплов, выходящих за пределы 1.1 стандартных отклонений от среднего G-point:  Bash# Работает на основе результатов 2_results_g_point.csv

python3 3_filter_trash.py

Очистка структуры (Trash)
Перенос аномальных сэмплов в папку trash для ручного аудита:

Bash
python3 4_move_trash.py

Выравнивание громкости (Loudness Check)
Анализ амплитудных характеристик (RMS):

Bash
python3 4_check_loudness.py

Final

Bash
python3 5_gen_perfect_dspreset.py

Завершение работы

Bash
deactivate
rm -rf venv
