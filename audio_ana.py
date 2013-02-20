import yaafelib as yaafe
import matplotlib.pyplot as plt
import numpy as np

sep ="/"
Neg_file ="train.negative.txt"
Pos_file ="train.positive.txt"
TRUTH_PATH = "../Data/Truth/AV"
DATA_FILE = "../Data/donnees"
DATA_FORMAT_FILE = "../Data/donneesFormat"
OUT_DIR = "../"

ext_wav = ".wav"
ext_avi = ".avi"
file_f = open(TRUTH_PATH + sep + Pos_file, 'r')

file_u= file_f.readline()
files = file_u.split()
filevideo = files[0]
fileaudio = files[1] 

OUT_format = DATA_FORMAT_FILE + sep +fileaudio + ".datA"
#print fileaudio
#print filevideo
fp = yaafe.FeaturePlan(sample_rate=16000, normalize=None, resample=False)
#fp.addFeature('mfcc: MFCC blockSize=512 stepSize=256')
fp.addFeature('energy: Energy blockSize=1024  stepSize=512')
fp.addFeature('enveloppe: Envelope EnDecim=200  blockSize=32768  stepSize=16384')

audiofile = DATA_FILE + sep + fileaudio + ext_wav
engine = yaafe.Engine()
engine.load(fp.getDataFlow()) 
afp = yaafe.AudioFileProcessor()
afp.processFile(engine,audiofile)
tempfile = engine.readAllOutputs()

#print tempfile['mfcc']
np.savetxt(OUT_format, tempfile['energy'])

plt.plot(tempfile['energy'])
plt.ylabel('some numbers')
plt.title(OUT_format)
plt.show()
