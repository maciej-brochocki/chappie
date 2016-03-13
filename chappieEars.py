import pyaudio


class Ears(object):
    channels = 1
    rate = 8000
    format = pyaudio.paInt16
    chunk = 1024
    p = None
    stream = None

    def __init__(self, p):
        self.p = p
        info = self.p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        index = 0
        for i in range(0, num_devices):
            if self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
                if self.p.get_device_info_by_host_api_device_index(0, i).get('name').startswith("Microsoft"):
                    index = i
        if self.p.is_format_supported(self.rate,
                                      input_device=index,
                                      input_channels=self.channels,
                                      input_format=self.format):
            self.stream = self.p.open(input=True, input_device_index=index, channels=self.channels, rate=self.rate,
                                      format=self.format, frames_per_buffer=self.chunk)
        return

    def hear(self):
        try:
            return self.stream.read(self.chunk)
        except IOError:
            return self.stream.read(self.chunk)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        return

    def get_sample_size(self):
        return self.p.get_sample_size(self.format)
