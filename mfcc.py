import numpy as np
import struct
import math


class Mfcc(object):
    length = 2  # 400
    shift = 1  # 160
    record = None

    FRAME_LENGTH = 400
    FFT_LENGTH = 512
    BIN_CENTERS = [2, 5, 8, 11, 14, 18, 23, 27, 33, 38,
                   45, 52, 60, 69, 79, 89, 101, 115, 129, 145,
                   163, 183, 205, 229, 256]
    offset_comp_prev_in = 0.0
    offset_comp_prev_out = 0.0
    input_buffer = []

    def encode(self, samples):
        result = []
        samples = np.fromstring(samples, dtype=np.int16)
        if self.record is None:
            self.record = samples
        else:
            self.record = np.concatenate((self.record, samples))
        while len(self.record) >= self.length:
            result.append("!")
            self.record = self.record[self.shift:]
        return result

    def feed_input(self, samples):
        samples = struct.unpack("<%ih" % (len(samples)/2), samples)
        samples = map(float, samples)
        for sample_in in samples:
            sample_out = sample_in - self.offset_comp_prev_in + 0.999 * self.offset_comp_prev_out
            self.offset_comp_prev_in = sample_in
            self.offset_comp_prev_out = sample_out
            self.input_buffer.append(sample_out)
            if len(self.input_buffer) == self.FRAME_LENGTH:
                self.process_frame(self.input_buffer)
                self.input_buffer = []

    def process_frame(self, samples):
        log_energy = math.log(sum(i*i for i in samples))
        for i in range(1, self.FRAME_LENGTH)[::-1]:
            samples[i] -= 0.97 * samples[i-1]
        for i in xrange(self.FRAME_LENGTH):
            samples[i] *= 0.54 - 0.46 * math.cos((2 * math.pi * i)/(self.FRAME_LENGTH-1))
        while len(samples) < self.FFT_LENGTH:
            samples.append(0.0)
        fft_bins = map(abs, fft(samples))
        bins = [0]*23
        for k in xrange(23):
            for i in xrange(self.BIN_CENTERS[k], self.BIN_CENTERS[k]+1):
                bins[k] += ((i - self.BIN_CENTERS[k] + 1) / (self.BIN_CENTERS[k+1]
                                                             - self.BIN_CENTERS[k] + 1)) * fft_bins[i]
            for i in xrange(self.BIN_CENTERS[k], self.BIN_CENTERS[k]+1):
                bins[k] += (1 - ((i - self.BIN_CENTERS[k+1]) / (self.BIN_CENTERS[k+2]
                                                                - self.BIN_CENTERS[k+1] + 1))) * fft_bins[i]
        bins = [math.log(i + 2e-22) for i in bins]
        cepstrum = [sum(math.cos(math.pi * i * (j + 0.5) / 23.0) * v for j, v in enumerate(bins)) for i in xrange(13)]
        feature_vector = FeatureVector(noise_foor_estimate, log_energy, cepstrum, self.next_fv_number)
        self.next_fv_number += 1
        self.feature_vectors.append(feature_vector)
