#!/usr/bin/python
# -*- coding: utf-8 -*-

import yaafelib as yaafe
import matplotlib.pyplot as plt
import numpy as np
import codecs
import os

#Variables de chemins
sep ="/"
Neg_file ="train.negative.txt"
Pos_file ="train.positive.txt"
TRUTH_PATH = "../Data/Truth/AV"
DATA_FILE = "../Data/donnees"
DATA_FORMAT_FILE = "../Data/donneesFormat"

#Variables d'extensions
ext_wav = ".wav"
ext_avi = ".avi"
ext_datA = ".datA"
ext_datV = ".datV"

#Variable d'ouverture de fichier
file_f = open(TRUTH_PATH + sep + Pos_file, 'r')

#Fonctions de formatage basé sur le chemin abstrait
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

#Fonction qui prends en entré un fichier index vérité qui liste les fichier audio et vidéo qui vont de pair.
#Elle sépare chaque fichier audio et ne traite que ceux-ci
#Pour les fichiers vidéo voir la fonction de reconnaissance de la bouche
# une fois fini les fichiers traités sont stockés dans un dossier a la racine nommé data/format

def traitementAudioVideo(fileIndex,typeFeature):
	for line in fileIndex:
		words = line.strip().split(' ')
		listAudioFile = words[1]
		listVideoFile = words[0]
		fp = yaafe.FeaturePlan(sample_rate=16000, normalize=None, resample=False)

		fp.addFeature('Enveloppe: Envelope EnDecim=200  blockSize=32768  stepSize=16384')
		fp.addFeature('Energy: Energy blockSize=1352  stepSize=676')
		
		engine = yaafe.Engine()
		engine.load(fp.getDataFlow()) 
		
		audioFile = getAudioFile(listAudioFile)

		afp = yaafe.AudioFileProcessor()
		afp.processFile(engine,audioFile)
		tempfile = engine.readAllOutputs()

		np.savetxt(setOutFormatAudio(listAudioFile),tempfile[typeFeature])

#Fonction basique de transformation en 1D array
def transform1Darray(fichier):
	result = []
	
	for line in open(fichier):
		ligne = float(line)
		result.append(ligne)

	return result 
	 

#Fonction qui calcule la correlation entre 2 1D array, en fonction des 2 fichiers donnés en entrées	et retourne le terme non diagonale ( correlation réelle )	
def getCorrelation(fileUn,fileDeux):
	f1 = transform1Darray(fileUn)
	f2 = transform1Darray(fileDeux)
	coef = np.corrcoef(f1,f2)
	return coef[0][1]

#Fonction de calcul de chaque correlation pour les noms de fichiers listés dans un fichier index
#TODO
def calcCorrelationTwo(fileIndex):
	listVideoFile = []
	listAudioFile = []
	for line in fileIndex:
		words = line.strip().split(' ')
		listVideoFile.append(words[0])
		listAudioFile.append(words[1])

	x = 0

	for x in range(len(listVideoFile)):
		fileVideoPath =  DATA_FORMAT_FILE + sep + str(listVideoFile[x]) + ext_datV
		fileAudioPath =  DATA_FORMAT_FILE + sep + str(listAudioFile[x]) + ext_datA
		correlation = getCorrelation(fileVideoPath, fileAudioPath)
		ecrireFileResult(listVideoFile[x],listAudioFile[x],correlation)
		x = x +1
	

def ecrireFileResult(entree1,entree2,correlation):
	fichier = open("resultatCorrelation.txt","w")
	fichier.write(entree1+" "+entree2+" "+correlation)
	fichier.close()
	

	
#Main
fichier1 = DATA_FORMAT_FILE+sep+"aarmorpdhm.datA"
fichier2 = DATA_FORMAT_FILE+sep+"agjwdtuzcz.datA"
fichier11 = "test1.txt"
fichier22 = "test2.txt"


#print transform1Darray(fichier11)
#print "-------------------------"
#print transform1Darray(fichier2)
#print getCorrelation(fichier1,fichier2)
#print getCorrelation(fichier1,fichier2)
#calcCorrelationTwo(file_f)
#ecrireFileResult("entree1","entree2","correlation")
#traitementAudioVideo(file_f,'Energy')
