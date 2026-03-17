from gtts import gTTS
import tempfile
import sounddevice as sd
import soundfile as sf
import os
import time

print("=" * 60)
print("📢 ПРОГРАММА TEXT-TO-SPEECH (с sounddevice)")
print("=" * 60)

# Доступные языки
LANGUAGES = {
    'ru': 'Русский',
    'en': 'Английский',
    'de': 'Немецкий',
    'fr': 'Французский',
    'es': 'Испанский'
}

current_lang = 'ru'
slow_mode = False

print("Доступные языки:")
for code, name in LANGUAGES.items():
    print(f"  {code}: {name}")
print("=" * 60)
print("Команды:")
print("  'выход' - завершить программу")
print("  'язык ru' - выбрать русский")
print("  'язык en' - выбрать английский")
print("  'медленно' - включить медленный режим")
print("  'быстро' - выключить медленный режим")
print("=" * 60)

while True:
    text = input("\n📝 Введите текст: ")

    if text.lower() == 'выход':
        print("👋 До свидания!")
        break

    if text.lower().startswith('язык'):
        try:
            lang_code = text.split()[1]
            if lang_code in LANGUAGES:
                current_lang = lang_code
                print(f"🌐 Язык: {LANGUAGES[lang_code]}")
            else:
                print(f"❌ Доступны: {', '.join(LANGUAGES.keys())}")
        except:
            print("❌ Используйте: язык ru")
        continue

    if text.lower() == 'медленно':
        slow_mode = True
        print("🐢 Медленный режим")
        continue

    if text.lower() == 'быстро':
        slow_mode = False
        print("🐇 Быстрый режим")
        continue

    if text.strip():
        print(f"🔊 Озвучиваю...")

        try:
            # Создаём временный файл
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                temp_filename = f.name

            # Генерируем речь
            print("🔄 Генерация...")
            tts = gTTS(text=text, lang=current_lang, slow=slow_mode)
            tts.save(temp_filename)

            # Читаем и воспроизводим через sounddevice
            print("▶️ Воспроизведение...")
            data, samplerate = sf.read(temp_filename)
            sd.play(data, samplerate)
            sd.wait()  # ждём окончания

            # Удаляем файл
            os.unlink(temp_filename)

            print("✅ Готово!")

        except Exception as e:
            print(f"❌ Ошибка: {e}")
    else:
        print("❌ Пустой текст")
