import random
import time
import math
import sys
DEBUG = False
COMPLEXITY = 70
EXTRA_COMPLEX = False
DURRATION = 86400
VERSION = "1.1"
SYMBOLS = ["-", "~", "="]

def get_rand():
    return random.random()

def get_version(version, length):
    prompt = f"VERSION {version}"
    if len(prompt) % 2 != 0:
        prompt = prompt.split()[0] + "  " + prompt.split()[1]
    padding = int(length / 2) - int((len(prompt) + 2) / 2)
    return (("#" * padding) + " " + prompt + " " + ("#" * padding) + "\n", ("#" * length) + "\n")

def get_fingerprint(seed, timestamp, complexity=70, two_dimensional = False, version=VERSION):
    random.seed(seed)

    if version == "1.0":
        TH = get_rand()
        random.seed(str(seed) + str(timestamp))
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
        TH = [get_rand(), get_rand()]
        TH.sort()
        random.seed(str(seed) + str(timestamp))
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

    else:
        return "VERSION NOT DEFINED"


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
                f.write(get_fingerprint(seed, t, complexity=COMPLEXITY))
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
                t += 1
                #time.sleep(1)
            f.write(get_version(VERSION, COMPLEXITY)[1])
    print(f"Elapsed time: {time.time() - st}")