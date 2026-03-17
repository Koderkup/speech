import os
import json
import sys
import sounddevice as sd
import vosk
import queue
import time

# Настройки
SAMPLE_RATE = 16000  # частота дискретизации (обязательно 16000 для Vosk)
BLOCK_SIZE = 8000    # размер блока данных

print("=" * 60)
print("🎤 РАСПОЗНАВАНИЕ РЕЧИ С МИКРОФОНА")
print("=" * 60)

# Путь к модели
model_path = "vosk-model-small-ru-0.22"

# Проверяем наличие модели
if not os.path.exists(model_path):
    print(f"❌ Модель не найдена по пути: {model_path}")
    print("Скачайте модель по ссылке:")
    print("https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip")
    print("И распакуйте в текущую папку.")
    sys.exit(1)

print(f"✅ Модель найдена: {model_path}")

# Загружаем модель
print("🔄 Загрузка модели... (может занять несколько секунд)")
model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

# Очередь для аудиоданных
audio_queue = queue.Queue()


def callback(indata, frames, time, status):
    """Эта функция вызывается, когда с микрофона поступают данные"""
    if status:
        print(f"⚠️ Статус: {status}", file=sys.stderr)
    audio_queue.put(bytes(indata))


def listen_from_mic():
    """Основная функция прослушивания микрофона"""

    print("\n" + "=" * 60)
    print("🎤 ГОВОРИТЕ (для выхода нажмите Ctrl+C)")
    print("=" * 60)

    # Открываем поток с микрофона
    with sd.RawInputStream(samplerate=SAMPLE_RATE,
                           blocksize=BLOCK_SIZE,
                           channels=1,
                           dtype='int16',
                           callback=callback):

        print("✅ Микрофон активен, слушаю...\n")

        while True:
            # Берём данные из очереди
            data = audio_queue.get()

            # Передаём данные в распознаватель
            if recognizer.AcceptWaveform(data):
                # Когда распознана фраза целиком
                result = json.loads(recognizer.Result())
                text = result.get('text', '')
                if text:
                    print(f"\n🔤 РАСПОЗНАНО: {text}")
                    print("-" * 60)
            else:
                # Частичный результат (пока говорит)
                partial = json.loads(recognizer.PartialResult())
                partial_text = partial.get('partial', '')
                if partial_text:
                    # Очищаем строку и выводим частичный результат
                    sys.stdout.write(f"\r🔄 ... {partial_text[:50]}")
                    sys.stdout.flush()


if __name__ == "__main__":
    try:
        listen_from_mic()
    except KeyboardInterrupt:
        print("\n\n👋 Программа завершена")
