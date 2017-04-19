from google.cloud import speech
import pyaudio

client = speech.Client()
WIDTH = 2
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()

pStream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True)

pStream.start_stream()

print("start talking")

with pStream as stream:
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
