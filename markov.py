import math


class MarkovChain():
    def __init__(self, state_len=2):
        self._state_len = state_len
        self._data = {}

    def add(self, sequence):
        for i, item in enumerate(sequence[:self._state_len]):
            key = tuple(sequence[max(0, i-self._state_len):i])
            data = self._data.get(key, dict())
            data[item] = data.get(item, 0)+1
            self._data[key] = data
        for i, item in enumerate(sequence[self._state_len:]):
            key = tuple(sequence[i:i+self._state_len])
            data = self._data.get(key, dict())
            data[item] = data.get(item, 0)+1
            self._data[key] = data

    def next(self, current):
        i = len(current)
        key = tuple(current[max(0, i-self._state_len):i])
        data_dict = self._data.get(key, dict())
        data_list = sorted(([data_dict[i], i] for i in data_dict), reverse=True)
        return [i[1] for i in data_list]

class MarkovEncode():
    def __init__(self, s_list, state_len=5):
        chain = MarkovChain(state_len=state_len)
        for sequence in s_list:
            chain.add(sequence)
        self._chain = chain
    def encode(self, data):
        chain = self._chain
        bits = ''.join(('0'*8+bin(char)[2:])[-8:] for char in data)
        bit_pos = 0
        current = []
        encoded = []
        while bit_pos < len(bits):
            options = chain.next(current)
            if options:
                bits_to_use = int(math.log(len(options), 2))
                current_bits = 0
                current_bits = (bits+'0'*bits_to_use)[bit_pos:bit_pos + bits_to_use]
                bit_pos += bits_to_use
                current += options[int('0' + current_bits, 2)]
            else:
                encoded.extend(current)
                current = []
        encoded.extend(current)
        return encoded
    def decode(self, data):
        chain = self._chain
        bits = []
        pos = 0
        simulated = []
        while pos < len(data):
            options = chain.next(simulated)
            if options:
                simulated += data[pos]
                current_bits = options.index(data[pos])
                bits_to_use = int(math.log(len(options), 2))
                if bits_to_use:
                    new = ('0' * bits_to_use + bin(current_bits)[2:])
                    bits += new[-bits_to_use:]
                pos += 1
            else:
                simulated = []
        length = int(len(bits)/8)
        chars = [''.join(bits[i*8:i*8+8]) for i in range(length)]
        decoded = bytes(int(''.join(map(str, char)),2) for char in chars)
        return decoded

def shakespeare():
    import json
    with open('shakespeare.json') as file:
        data = json.load(file)
    return ['\n'.join(i) for i in data]

