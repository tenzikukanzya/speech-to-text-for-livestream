import sounddevice as sd
import soundcard as sc
import threading
import io
import soundfile as sf
import numpy as np
import librosa


# get a list of valid input devices
def get_valid_input_devices():
    valid_devices = []
    devices = sd.query_devices()
    hostapis = sd.query_hostapis()

    for device in devices:
        if device["max_input_channels"] > 0:
            device["host_api_name"] = hostapis[device["hostapi"]]["name"]
            valid_devices.append(device)
    return valid_devices


# create an audio stream by sd
def sd_create_audio_stream(selected_device, callback):
    RATE = 16000
    CHUNK = 512
    CHANNELS = 1
    DTYPE = "float32"

    stream = sd.InputStream(
        device=selected_device,
        channels=CHANNELS,
        samplerate=RATE,
        callback=callback,
        dtype=DTYPE,
        blocksize=CHUNK,
    )

    return stream

# create and audio steam by sc
def sc_create_audio_stream(callback):
    soundCardStream = SoundCardStream(callback=callback)
    return soundCardStream

def base64_to_audio(audio_data):
    audio_bytes = bytes(audio_data)
    audio_file = io.BytesIO(audio_bytes)
    data, samplerate = sf.read(audio_file)
    # whisper samplerate is 16k
    resample_data = librosa.resample(y=data, orig_sr=samplerate, target_sr=16000)

    return resample_data.astype(np.float32)


class SoundCardStream:
    def __init__(self, callback=None, device=None, samplerate=16000, blocksize=1024, channels=1):
        if device is None:
            self.device = sc.default_microphone()
        else:
            self.device = device
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.channels = channels
        self.callback = callback
        self.recorder = None
        self.recording = False
        self.buffer = []

    def start(self):
        self.recorder = sc.get_microphone(include_loopback=True, id=str(sc.default_speaker().name)).recorder(samplerate=self.samplerate)
        self.recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop(self):
        self.recording = False
        if self.thread.is_alive():
            self.thread.join()
        self.recorder = None

    def close(self):
        self.stop()

    def read(self, num=None):
        if num is None:
            data = np.concatenate(self.buffer)
            self.buffer = []
        else:
            data = np.concatenate(self.buffer[:num])
            self.buffer = self.buffer[num:]
        return data

    def _record(self):
        with self.recorder as rec:
            while self.recording:
                data = rec.record(self.blocksize).astype(np.float32)  # Convert data to float32
                self.buffer.append(data)
                if self.callback:
                    self.callback(data)
