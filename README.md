# GoogleSpeechRPi
Use Google Cloud Speech to control Raspberry Pi 

## Objective: 
Control the GPIO Pins of a Raspberry Pi on the fly using Google Cloud Speech.
I've chosen the most visible implmentation of GPIO Pin control, a Light Emitting Diode.

## Install libraries:
pip3:
```bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
```

Versioned version of [Google Cloud SDK](https://cloud.google.com/sdk/downloads#linux):
```
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install google-cloud-sdk
```

cloud-speech:
```bash
pip3 install --upgrade google-cloud-speech
```

[WiringPi-Python](https://github.com/WiringPi/WiringPi-Python):
```bash
sudo apt-get install python3-dev python3-setuptools swig3.0 git

git clone --recursive https://github.com/WiringPi/WiringPi-Python.git
cd WiringPi-Python
git submodule update --init

cd WiringPi
sudo ./build

cd ..
swig3.0 -python wiringpi.i
sudo python3 setup.py install
```



## Setup Google Cloud authentication
```bash
sudo su
gcloud auth application-default login
```

## Download and run App
```bash
git clone https://github.com/thomas-vl/GoogleSpeechRPi.git
cd GoogleSpeechRPi
sudo python3 main.py
```

## Notes
One of the biggest problems i had was that the audio stream from pyAudio could not be read by the Cloud-Speech client. I feel that Java might be better suited for this.
I know that most of the code is ugly please post anything you might feel I could improve.

## Credits
A big thanks to [Jeyson Molina](https://github.com/jeysonmc) for providing a lot of code to calculate silence treshholds 


