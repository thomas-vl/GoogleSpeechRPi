# GoogleSpeechRPi
Use Google Cloud Speech to control Raspberry Pi 

## Objective: 
Control the GPIO Pins of a Raspberry Pi on the fly using Google Cloud Speech.

## Install libraries:
Versioned version of [Google Cloud SDK](https://cloud.google.com/sdk/downloads#linux):
```
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install google-cloud-sdk
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
```
gcloud auth application-default login
```
