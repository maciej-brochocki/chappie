from random import randint
import audioop
import numpy as np
import cv2
import wave
import os


class Brain(object):
    ears = None  # ears object
    mouth = None  # mouth object
    mode = 0  # 0 - replay last, 1 - replay random
    silence_threshold = 1500
    recording_state = 0
    record = []
    silent_frames = 0
    silent_frames_limit = 5
    record_num = 0

    def __init__(self, ears, mouth):
        self.record_num = len(os.listdir("./sounds"))
        self.ears = ears
        self.mouth = mouth
        return

    def attention(self, sound):
        if self.compete_record(sound):
            self.record = b''.join(self.record)
            if self.mode == 0:
                self.replay_last()
            elif self.mode == 1:
                self.replay_random()
            self.record = []
        self.visualize_sound(sound)
        return

    def visualize_sound(self, sound):
        snd = np.zeros((256, self.ears.chunk), dtype=np.uint8)
        for i in range(self.ears.chunk):
            snd[ord(sound[i*self.ears.get_sample_size()]), i] = 255
        if self.recording_state == 1:
            cv2.rectangle(snd, (self.ears.chunk-11, 256-11), (self.ears.chunk-2, 256-2), 255, cv2.cv.CV_FILLED)
        cv2.imshow('Osc', snd)
        return

    def compete_record(self, sound):
        if self.mouth.is_speaking():
            self.record = []
            return False
        rms = audioop.rms(sound, self.ears.get_sample_size())
        if rms > self.silence_threshold:
            if self.recording_state == 0:
                # start recording
                self.record.append(sound)
                self.recording_state = 1
            else:
                # continue recording
                self.record.append(sound)
            self.silent_frames = self.silent_frames_limit
        else:
            if self.recording_state == 1:
                # append some silence or join close records
                self.record.append(sound)
                self.silent_frames -= 1
                if self.silent_frames == 0:
                    # end recording
                    self.recording_state = 0
                    return True
            else:
                # so we get quite beginnings
                self.record = [sound]
        return False

    def replay_last(self):
        self.mouth.talk(self.record)
        return

    def replay_random(self):
        self.record_num += 1
        # save current record
        wf = wave.open("sounds/rec%d.wav" % self.record_num, 'wb')
        wf.setnchannels(self.ears.channels)
        wf.setsampwidth(self.ears.get_sample_size())
        wf.setframerate(self.ears.rate)
        wf.writeframes(self.record)
        wf.close()
        # open random record
        wf = wave.open("sounds/rec%d.wav" % randint(1, self.record_num), 'rb')
        self.mouth.talk(wf.readframes(wf.getnframes()))
        wf.close()
        return

    def dec_silence_threshold(self):
        self.silence_threshold -= 50
        print "silence level: ", self.silence_threshold
        return

    def inc_silence_threshold(self):
        self.silence_threshold += 50
        print "silence level: ", self.silence_threshold
        return

    def set_cfg(self):
        self.mode = (self.mode + 1) % 2
        print "brain mode: ", self.mode
        return
