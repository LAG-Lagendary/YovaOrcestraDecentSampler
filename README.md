# LAG: Code & Music — Sample Processing Scripting

A modular pipeline for preparing instrument samples for Decent Sampler.
Mathematical analysis: onset detection, statistical filtering, RMS normalization.

## Pipeline (Instructions)
All operations are performed in the venv virtual environment.

1. **Conversion:** `./1.convert.sh`
2. **Analysis (G-point):** `python3 2_g_point_tool.py`
3. **Filtering:** `python3 3_filter_trash.py` (outlier removal).
4. **Cleanup:** `python3 4_move_trash.py`
5. **Preset generation:** `python3 5_gen_perfect_dspreset.py`

*Note: If you manually rename files in `Samples/`, you must update the CSV files.*

Preparation and conversion
If the source files are in .aif format, convert them to wav: Bash# Run in the project folder

./1.convert.sh

Environment activation and analysis (G-point)

Bash
python3 -m venv venv
source venv/bin/activate
pip install -q librosa numpy pandas

# Calculate attack points

python3 2_g_point_tool.py

Statistical filtering
Exclude samples that are outside 1.1 standard deviations of the mean G-point: Bash# Works based on the results of 2_results_g_point.csv

python3_3_filter_trash.py

Trash Structure Cleanup
Move abnormal samples to the trash folder for manual auditing:

Bash
python3_4_move_trash.py

Loudness Check
Amplitude Response Analysis (RMS):

Bash
python3_4_check_loudness.py

Final

Bash
python3_5_gen_perfect_dspreset.py

Exit

Bash
deactivate
rm -rf venv
