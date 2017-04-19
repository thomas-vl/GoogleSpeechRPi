from google.cloud import speech
import pyaudio

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
                frames_per_buffer=CHUNK)

print("starting")
while (True):    
    sample = client.sample(stream=stream,encoding=speech.Encoding.LINEAR16,sample_rate_hertz=16000)
    results = sample.streaming_recognize(language_code='en-US',single_utterance=True,)
    for result in results:
        for alternative in result.alternatives:
            print('=' * 20)
            print('transcript: ' + alternative.transcript)
            print('confidence: ' + str(alternative.confidence))

print("closing stream")
stream.stop_stream()
stream.close()

p.terminate()
