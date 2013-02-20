import yaafelib as yaafe
import matplotlib.pyplot as plt
import numpy as np
import codecs
import os

sep ="/"
Neg_file ="train.negative.txt"
Pos_file ="train.positive.txt"
TRUTH_PATH = "../Data/Truth/AV"
DATA_FILE = "../Data/donnees"
DATA_FORMAT_FILE = "../Data/donneesFormat"

ext_wav = ".wav"
ext_avi = ".avi"

file_f = codecs.open(TRUTH_PATH + sep + Pos_file, 'r')

def setOutFormatAudio(fileaudio):
	return DATA_FORMAT_FILE + sep + fileaudio + ".datA"
def setOutFormatVideo(filevideo):
	return DATA_FORMAT_FILE + sep + filevideo + ".datV"

def getAudioFile(fileaudio):
	return DATA_FILE + sep + fileaudio + ext_wav

def traitementAudioVideo(fileIndex,typeFeature):
	for line in fileIndex:
		words = line.strip().split(' ')
		listAudioFile = words[1]
		listVideoFile = words[0]
		fp = yaafe.FeaturePlan(sample_rate=16000, normalize=None, resample=False)

		fp.addFeature('Enveloppe: Envelope EnDecim=200  blockSize=32768  stepSize=16384')
		fp.addFeature('Energy: Energy blockSize=1024  stepSize=512')
		
		engine = yaafe.Engine()
		engine.load(fp.getDataFlow()) 
		
		audioFile = getAudioFile(listAudioFile)

		afp = yaafe.AudioFileProcessor()
		afp.processFile(engine,audioFile)
		tempfile = engine.readAllOutputs()

		np.savetxt(setOutFormatAudio(listAudioFile),tempfile[typeFeature])

		
traitementAudio(file_f,'Energy')
