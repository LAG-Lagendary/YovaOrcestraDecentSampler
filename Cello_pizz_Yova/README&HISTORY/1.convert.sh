find . -type f -name "*.aif" | while read -r file; do
    # Заменяем расширение .aif на .wav
    output="${file%.aif}.wav"
    # Конвертируем с помощью ffmpeg
    ffmpeg -i "$file" "$output"
done
