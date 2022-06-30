import spec

global gain, offset
a = spec.x
gain = x.gain

def cal_spec(x):
    return lambda x, gain, offset : x * gain + offset

print(cal_spec(a))