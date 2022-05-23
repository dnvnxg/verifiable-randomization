import random
import time
import math
import sys
import hashlib
DEBUG = False
COMPLEXITY = 70
EXTRA_COMPLEX = False
DURRATION = 86400
VERSION = "1.2"
SYMBOLS = ["-", "~", "="]
SPEEDS = [10, 10, 10, 10]

def get_rand():
    return random.random()

def get_version(version, length):
    prompt = f"VERSION {version}"
    if len(prompt) % 2 != 0:
        prompt = prompt.split()[0] + "  " + prompt.split()[1]
    padding = int(length / 2) - int((len(prompt) + 2) / 2)
    return (("#" * padding) + " " + prompt + " " + ("#" * padding) + "\n", ("#" * length) + "\n")

def get_fingerprint(seed, timestamp, complexity=70, two_dimensional = False, version=VERSION):
    payload = str(seed) + str(timestamp) + str(sum(SPEEDS) / len(SPEEDS))

    if version == "1.0":
        random.seed(seed)
        TH = get_rand()
        random.seed(payload)
        line = ""
        for i in range(1 if not two_dimensional else COMPLEXITY):
            for j in range(COMPLEXITY):
                rand = random.random()
                if rand < TH:
                    line += SYMBOLS[0]
                else:
                    line += SYMBOLS[1]
            line += "\n"
        if DEBUG: print(f"Time Diff: {abs(time.time() - t)}")
        return line

    elif version == "1.1":
        random.seed(seed)
        TH = [get_rand(), get_rand()]
        TH.sort()
        random.seed(payload)
        line = ""
        for i in range(1 if not two_dimensional else COMPLEXITY):
            for j in range(COMPLEXITY):
                rand = random.random()
                if rand <= TH[0]:
                    line += SYMBOLS[0]
                elif rand > TH[0] and rand <= TH[1]:
                    line += SYMBOLS[1]
                else:
                    line += SYMBOLS[2]
            line += "\n"
        if DEBUG: print(f"Time Diff: {abs(time.time() - t)}")
        return line

    elif version == "1.2":
        return "   " + hashlib.sha3_256(payload.encode()).hexdigest() + "   \n"
    else:
        return "VERSION NOT DEFINED\n"


if __name__ == "__main__":
    st = time.time()
    if sys.argv[1] == "-g":
        seed = sys.argv[2]
        start_time = math.floor(time.time())
        t = start_time
    
        with open("clock.trace", "w+") as f:
            f.write(f"Start Timestamp: {start_time}\n")
            f.write(get_version(VERSION, COMPLEXITY)[0])
            for a in range(DURRATION):
                if a == 6000: SPEEDS[3] = 25
                if a == 7000: SPEEDS[3] = 10
                f.write(get_fingerprint(seed, t, complexity=COMPLEXITY))
                if DEBUG: print(get_fingerprint(seed, t, complexity=COMPLEXITY)[:-1])
                t += 1
                #time.sleep(1)
            f.write(get_version(VERSION, COMPLEXITY)[1])
    if sys.argv[1] == "-s":
        seed = sys.argv[2]
        start_time = int(sys.argv[3])
        t = start_time

        with open("validation_clock.trace", "w+") as f:
            f.write(f"Start Timestamp: {start_time}\n")
            f.write(get_version(VERSION, COMPLEXITY)[0])
            for a in range(DURRATION):
                f.write(get_fingerprint(seed, t, complexity=COMPLEXITY))
                if DEBUG: print(get_fingerprint(seed, t, complexity=COMPLEXITY)[:-1])
                t += 1
                #time.sleep(1)
            f.write(get_version(VERSION, COMPLEXITY)[1])
    print(f"Elapsed time: {time.time() - st}")