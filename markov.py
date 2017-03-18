import base64
import math


class MarkovChain():
    def __init__(self, state_len=2):
        self._state_len = state_len
        self._data = {}

    def add(self, sequence):
        for i, item in enumerate(sequence):
            key = tuple(sequence[max(0, i-self._state_len):i])
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
    def __init__(self, s_list, state_len=2):
        chain = MarkovChain(state_len=state_len)
        for sequence in s_list:
            chain.add(sequence)
        self._chain = chain

    def encode(self, data):
        chain = self._chain
        data = base64.b64encode(data)
        bits = ''.join(('0'*7+bin(char)[2:])[-7:] for char in data)
        current = []
        encoded = []
        for bit in bits:
            while True:
                options = chain.next(current)
                if not options:
                    current = []
                elif len(options) > 1:
                    current.append(options[int(bit)])
                    encoded.append(options[int(bit)])
                    break
                else:
                    current.append(options[0])
                    encoded.append(options[0])
        return encoded
    def decode(self, data):
        chain = self._chain
        current = []
        bits = []
        for item in data:
            while True:
                options = chain.next(current)
                if not options:
                    current = []
                elif len(options) > 1:
                    bits.append(options.index(item))
                    current.append(item)
                    break
                else:
                    current.append(item)
                    break
        length = int(len(bits)/7)
        chars = (bits[i*7:i*7+7] for i in range(length))
        decoded = bytes(int(''.join(map(str, char)),2) for char in chars)
        return base64.b64decode(decoded)

def shakespeare():
    import json
    with open('shakespeare.json') as file:
        data = json.load(file)
    return [i.split(' ') for i in data]
SHAKESPEARE = shakespeare()
ME = MarkovEncode(SHAKESPEARE)
encoded = ME.encode(b'Hi there'+bytes(range(100)))
print(' '.join(encoded))
decoded = ME.decode(encoded)
print(decoded)
