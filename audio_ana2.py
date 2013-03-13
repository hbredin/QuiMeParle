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
ext_datA = ".datA"
ext_datV = ".datV"

file_f = open(TRUTH_PATH + sep + Pos_file, 'r')

def setOutFormatAudio(fileaudio):
	return DATA_FORMAT_FILE + sep + fileaudio + ext_datA
def setOutFormatVideo(filevideo):
	return DATA_FORMAT_FILE + sep + filevideo + ext_datV

def getAudioFile(fileaudio):
	return DATA_FILE + sep + fileaudio + ext_wav

def getFormatAudioFile(filePointdatA):
	return DATA_FORMAT_FILE + sep + filePointdatA + ext_datA

def getFormatAudioFile(filePointdatV):
	return DATA_FORMAT_FILE + sep + filePointdatV + ext_datV

def traitementAudioVideo(fileIndex,typeFeature):
	for line in fileIndex:
		words = line.strip().split(' ')
		listAudioFile = words[1]
		listVideoFile = words[0]
		fp = yaafe.FeaturePlan(sample_rate=16000, normalize=None, resample=False)

		fp.addFeature('Enveloppe: Envelope EnDecim=200  blockSize=32768  stepSize=16384')
		fp.addFeature('Energy: Energy blockSize=1024  stepSize=688')
		
		engine = yaafe.Engine()
		engine.load(fp.getDataFlow()) 
		
		audioFile = getAudioFile(listAudioFile)

		afp = yaafe.AudioFileProcessor()
		afp.processFile(engine,audioFile)
		tempfile = engine.readAllOutputs()

		np.savetxt(setOutFormatAudio(listAudioFile),tempfile[typeFeature])

def calcNum(fichier):
	resultat = 0
	
	for line in open(fichier):
		resultat = resultat + 1
	
	return resultat

def calcMax(fichier):
	resultat = 0

	for line in open(fichier):		
		ligne = int(line)
		if (ligne > resultat):
			resultat = ligne
		else:
			 continue
	return resultat

def calcMean(fichier):
	res = 0
	i= 0
	
	for line in open(fichier):
		ligne = int(line)
		res = res + ligne
		i=i+1

	resultat = float(float(res)/float(i))
	return resultat

def transform1Darray(fichier):
	result = []
	
	for line in open(fichier):
		ligne = float(line)
		result.append(ligne)

	return result 

def match(dataUn,datadeux):	
	return null
		
def getCorrelation(fileUn,fileDeux):
	f1 = transform1Darray(fileUn)
	f2 = transform1Darray(fileDeux)

	return null
		
fichier1 = "test1.txt"
fichier2 = "test2.txt"
#print calcMax(fichier)
#print calcMean(fichier)
#print calcNum(fichier)
print transform1Darray(fichier1)
print transform1Darray(fichier2)
#print getCorrelation(fichier1,fichier2)
traitementAudioVideo(file_f,'Energy')
