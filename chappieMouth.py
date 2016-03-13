import pyaudio
import cStringIO

rec = None


def callback(in_data, frame_count, time_info, status):
    global rec
    if rec is None:
        return None, pyaudio.paAbort
    else:
        data = rec.read(frame_count)
        if len(data) < frame_count:
            rec.close()
            rec = None
        return data, pyaudio.paContinue


class Mouth(object):
    p = None
    stream = None

    def __init__(self, ears):
        self.p = ears.p
        self.stream = self.p.open(output=True, channels=ears.channels, rate=ears.rate, format=ears.format)
        #                          stream_callback=callback, start=False)
        return

    def talk(self, record):
        self.stream.write(record)
        # global rec
        # rec = cStringIO.StringIO(record)
        # self.stream.start_stream()
        return

    def close(self):
        self.stream.close()
        return

    def done(self):
        if self.stream.is_active():
            return False
        else:
            self.stream.stop_stream()
            return True
