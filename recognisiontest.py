from google.cloud import speech
client = speech.Client()
with open('pyaudio-output.wav', 'rb') as stream:
    sample = client.sample(stream=stream,
                           encoding=speech.Encoding.LINEAR16,
                           sample_rate_hertz=16000)
    results = sample.streaming_recognize(language_code='en-US')
    for result in results:
        for alternative in result.alternatives:
            print('=' * 20)
            print('transcript: ' + alternative.transcript)
            print('confidence: ' + str(alternative.confidence))
