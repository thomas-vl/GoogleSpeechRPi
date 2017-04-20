import wiringpi
import pyaudio
import wave
import audioop
from collections import deque
import os
import time
import math
from google.cloud import speech


client = speech.Client()
LANG_CODE = 'en-US'  # Language to use


# Microphone stream config.
CHUNK = 1024  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 1500  # The threshold intensity that defines silence

SILENCE_LIMIT = 2  # Silence limit in seconds to stop the recording

PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                  # is detected, how much of previously recorded audio is
                  # prepended. This helps to prevent chopping the beggining
                  # of the phrase.


def audio_int(num_samples=50):
    """ Gets average audio intensity of your mic sound. You can use it to get
        average intensities while you're talking and/or silent. The average
        is the avg of the 20% largest intensities recorded.
    """

    print ("Getting intensity values from mic.")
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4)))
              for x in range(num_samples)]
    values = sorted(values, reverse=True)
    r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
    print (" Finished ")
    print (" Average audio intensity is ", r)
    stream.close()
    p.terminate()
    return r


def listen_for_speech(threshold=THRESHOLD, num_phrases=-1):
    """
    Listens to Microphone, extracts phrases from it and sends it to
    Google's TTS service and returns response. a "phrase" is sound
    surrounded by silence (according to threshold). num_phrases controls
    how many phrases to process before finishing the listening process
    (-1 for infinite).
    """

    #Open stream
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print ("* Listening mic. ")
    audio2send = []
    cur_data = ''  # current chunk  of audio data
    rel = RATE/CHUNK
    slid_win = deque(maxlen=math.floor(SILENCE_LIMIT * rel))
    #Prepend audio from 0.5 seconds before noise was detected
    prev_audio = deque(maxlen=math.floor(PREV_AUDIO * rel))
    started = False
    n = num_phrases
    response = []

    while (num_phrases == -1 or n > 0):
        cur_data = stream.read(CHUNK)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        #print slid_win[-1]
        if(sum([x > THRESHOLD for x in slid_win]) > 0):
            if(not started):
                print ("Starting record of phrase")
                started = True
            audio2send.append(cur_data)
        elif (started is True):
            stream.stop_stream()
            print ("Finished")
            # The limit was reached, finish capture and deliver.
            filename = save_speech(list(prev_audio) + audio2send, p)
            # Send file to Google and get response
            stt_google_wav(filename)
            # Remove temp file. Comment line to review.
            os.remove(filename)
            # Reset all
            started = False
            slid_win = deque(maxlen=math.floor(SILENCE_LIMIT * rel))
            prev_audio = deque(maxlen=math.floor(0.5 * rel))
            audio2send = []
            n -= 1
            stream.start_stream()
            print ("Listening ...")
        else:
            prev_audio.append(cur_data)

    print ("* Done recording")
    p.terminate()
    return response


def save_speech(data, p):
    """ Saves mic data to temporary WAV file. Returns filename of saved
        file """

    filename = 'output_'+str(int(time.time()))
    # writes data to WAV file
    data = b''.join(data)
    wf = wave.open(filename + '.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)  # TODO make this value a function parameter?
    wf.writeframes(data)
    wf.close()
    return filename + '.wav'


def stt_google_wav(audio_fname):
    """ Sends audio file (audio_fname) to Google's text to speech
        service and returns service's response. We need a FLAC
        converter if audio is not FLAC (check FLAC_CONV). """

    print ("Sending ", audio_fname)
    #Convert to flac first
    with open(audio_fname, 'rb') as stream:
        sample = client.sample(stream=stream,
                               encoding=speech.Encoding.LINEAR16,
                               sample_rate_hertz=16000)
        results = sample.streaming_recognize(language_code='en-US')
        for result in results:
            for alternative in result.alternatives:
                print('=' * 20)
                print('transcript: ' + alternative.transcript)
                print('confidence: ' + str(alternative.confidence))
                if alternative.transcript == "light on":
                    wiringpi.digitalWrite(4,1)
                if alternative.transcript == "lights on":
                    wiringpi.digitalWrite(4,1)
                if alternative.transcript == "light off":
                    wiringpi.digitalWrite(4,0)
                if alternative.transcript == "lights off":
                    wiringpi.digitalWrite(4,0)


if(__name__ == '__main__'):
    try:
        wiringpi.wiringPiSetupGpio()
    except:
        print ("GPIO issue", sys.exc_info()[0])

    wiringpi.pinMode(4,1)
    wiringpi.digitalWrite(4,0)

    listen_for_speech()
