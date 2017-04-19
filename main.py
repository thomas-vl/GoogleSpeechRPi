from google.cloud import speech
import pyaudio

client = speech.Client()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()

#pStream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,output=True)

#pStream.start_stream()

print("starting")

with p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,output=True) as stream:
    stream.start_stream()
    sample = client.sample(stream=stream,encoding=speech.Encoding.LINEAR16,sample_rate_hertz=16000)
    results = sample.streaming_recognize(language_code='en-US',single_utterance=True,)
    for result in results:
        for alternative in result.alternatives:
            print('=' * 20)
            print('transcript: ' + alternative.transcript)
            print('confidence: ' + str(alternative.confidence))

print("closing stream")
pStream.stop_stream()
pStream.close()

p.terminate()
