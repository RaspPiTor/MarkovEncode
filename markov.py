import base64
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
    def __init__(self, s_list, state_len=10):
        chain = MarkovChain(state_len=state_len)
        for sequence in s_list:
            chain.add(sequence)
        self._chain = chain

    def encode(self, data):
        chain = self._chain
        #data = base64.b64encode(data)
        bits = ''.join(('0'*8+bin(char)[2:])[-8:] for char in data)
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
        length = int(len(bits)/8)
        chars = (bits[i*8:i*8+8] for i in range(length))
        decoded = bytes(int(''.join(map(str, char)),2) for char in chars)
        return decoded#base64.b64decode(decoded)
class MarkovEncode2():
    def __init__(self, s_list, state_len=10):
        chain = MarkovChain(state_len=state_len)
        for sequence in s_list:
            chain.add(sequence)
        self._chain = chain
    def encode(self, data):
        chain = self._chain
        bits = ['0'*8+bin(char)[2:])[-8:] for char in data]
        current = []
        encoded = []
        while bits:
            options = chain.next(current)
            if options:
                bits_to_use = int(math.log(len(options), 2))
                current_bits = 0
                for i in range(1, bits_to_use + 1):
                    current_bits += int(bits.pop(0)) * 2**i
                current += options[current_bits]
            else:
                encoded.extend(current)
                current = []
        encoded.extend(current)
        return encoded
    def decode(self, data):
        chain = self._chain
        bits = []
        current = data.copy()
        simulated = []
        while current:
            options = chain.next(simulated)
            simulated += current[0]
            if options:
                current_bits = options.index(current)
        

def shakespeare():
    import json
    with open('shakespeare.json') as file:
        data = json.load(file)
    return data

