from google.cloud import speech
import pyaudio
import wave
import sys


client = speech.Client()
CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()

sample = client.sample(stream=stream,
                       encoding=speech.Encoding.LINEAR16,
                       sample_rate_hertz=16000)
results = sample.streaming_recognize(language_code='en-US')
for result in results:
    for alternative in result.alternatives:
        print('=' * 20)
        print('transcript: ' + alternative.transcript)
        print('confidence: ' + str(alternative.confidence))


stream.close()
p.terminate()
