<div align="center">

# 🎹 LAG: Code & Music — Sample Processing Scripting

# 🔴**O**🟠**R**🟡**C**🟢**H**🔵**E**🟣**S**🔴**T**🟠**R**🟡**A**🟢

# 🔵**P**🟣**I**🔴**Z**🟠**Z**🟡_**🟢**Y**🔵**O**🟣**V**🟣**A🟠

***Orchestra_pizz_Yova*** — это проект, где математика встречается с безумием!

**A modular pipeline for preparing instrument samples for Decent Sampler.**


```mkdir -p "$HOME/.config/DecentSampler/Sample Libraries"```


```git clone https://github.com/LAG-Lagendary/YovaOrcestraDecentSampler "$HOME/.config/DecentSampler/Sample Libraries/YovaOrcestraDecentSampler"```

*Mathematical analysis: onset detection, statistical filtering, RMS normalization.*

</div>

![Orchestra Pizz Yova](https://raw.githubusercontent.com/LAG-Lagendary/YovaOrcestraDecentSampler/main/Orchestra_pizz_Yova/University%20of%20Yova.%20Thanks%20you!(All%20together).jpg)

---

# 📖 The Story: "YOVA" (History of Creation)

The University of “YOVA” and the Mathematics of Attack
When I needed a deep, spiky bass, I didn’t crawl to a studio to beg for gear. I took the raw open-source files from the University of Iowa. But, as happens when you’re deep in the code, the magic of fatigue took over: “Iowa” became “YOVA” in my working notes.

YOW-YOW, YOVA! I loved the vibe. I kept it. Sometimes mistakes create more atmosphere than any sterilized, focus-grouped marketing name.

The Mathematics of Sound: My G-Point
I didn’t want a soft, fuzzy, “polite” instrument. I set myself an engineering challenge: total rhythmic precision. I developed a pipeline that doesn’t just compile a library—it forces the audio into a mathematically calibrated system by calculating the G-Point (transient point) of every single sound.

Analysis: The script identifies the first true mathematical peak of energy (the transient).

Aggression: I force the start point 25ms into the sample. No “air,” no sluggish fade-ins—just a clean, crisp, and immediate attack.

Statistical Cleaning: Using standard deviation analysis (std), I filter out the “bugs”—the samples where the algorithm erred or the recording was flawed.

The “First Pancake” Philosophy
In Russia, we say: “The first pancake is always lumpy.” But my first pancake didn’t come out lumpy—it came out sharp, toothy, and responsive. I built this instrument to the best of my ability, and it stands as my first serious foray into musical engineering. It wasn’t a flop; it’s a tool.

This is my work, and it’s open for constructive critique and actual improvements. I believe in the “Take the baton, pass the baton” philosophy. If you’re a coder or a sound designer and you think you can optimize the RMS normalization logic or refine the attack curves—bring it on. If you have real engineering suggestions to make this engine tighter, speak up. If you’re just here to whine, don’t bother.

This bass is a tribute to free software, a slightly quirky sense of humor, and engineering precision. I hope it gives you exactly the “prickly” sound you’ve been looking for.

That typo? It’s a feature, not a bug.
If you like this idea and want to see what I build next, follow me, please!

P.S. I’m honestly exhausted. I’ll run the project through a tuner later to fix the pitch drift in the high register when I’ve got more energy, but for now, I’m completely out of fuel. 
My apologies—please go easy on the high notes until I get back to it!

# ⚙️ Pipeline (Instructions)

All operations are performed in the venv virtual environment to keep your system clean.

# 🔄 1. Preparation and Conversion

If the source files are in .aif format, convert them to .wav.
Run this in the project folder:

```./1.convert.sh```


# 🧮 2. Environment Activation and Analysis (G-point)

Set up your Python environment and calculate the attack points (transients) of every sample:

```python3 -m venv venv```
```source venv/bin/activate```
```pip install -q librosa numpy pandas```

# Calculate attack points
```python3 2_g_point_tool.py```


# 📉 3. Statistical Filtering

Exclude samples that fall outside 1.1 standard deviations of the mean G-point.

(Works based on the results generated in 2_results_g_point.csv)

```python3 3_filter_trash.py```


# 🗑️ 4. Trash Structure Cleanup

Move abnormal/rejected samples to the trash folder for manual auditing:

```python3 4_move_trash.py```


# 🔊 5. Loudness Check

Amplitude Response Analysis (RMS) to ensure consistent volume levels across the instrument:

```python3 4_check_loudness.py```


# 🎯 6. Final Preset Generation

Generate the final, mathematically precise XML file for Decent Sampler:

```python3 5_gen_perfect_dspreset.py```


# 🧹 7. Exit and Cleanup

Once everything is generated, you can exit the environment and clean it up:

```deactivate```
```rm -rf venv```
