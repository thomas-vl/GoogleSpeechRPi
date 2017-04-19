from google.cloud import speech
import pyaudio
import wave
import sys
import time


client = speech.Client()
CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()

wf = wave.open('test','wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)


def callback(data, frame_count, time_info, flag):
    wf.writeframes(data)
    with open(wf, 'rb') as stream:
        sample = client.sample(stream=stream,
                               encoding=speech.Encoding.LINEAR16,
                               sample_rate_hertz=16000)
        results = sample.streaming_recognize(language_code='en-US')
        for result in results:
            for alternative in result.alternatives:
                print('=' * 20)
                print('transcript: ' + alternative.transcript)
                print('confidence: ' + str(alternative.confidence))
    return (data, pyaudio.paContinue)


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(1)

stream.stop_stream()
stream.close()
p.terminate()
