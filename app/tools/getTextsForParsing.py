#!c:/Python27/python.exe
#!/usr/bin/python

import os,subprocess,sys,glob,datetime, codecs
sys.path.insert(0, '../lib')
import conll, trees2train, treebankfiles, updateTrees, newconvert
from database 	import SQL

def extractConllFiles(project,outfolder):
	"""
	creates the empty files with a word per line as a first step to mate parsing
	"""
	if outfolder[-1]!="/": outfolder=outfolder+"/"
	texts={}
	sql = SQL(project)
	db, cursor = sql.open()
	command = """select distinct texts.textname, sentences.nr, features.nr, features.value 
		from features, trees, texts, sentences, users
		where attr = "t" and trees.rowid=features.treeid --and sentences.textid=13 
		and trees.sentenceid=sentences.rowid and sentences.textid=texts.rowid and users.user="parser";"""
	cursor.execute(command)
	a = cursor.fetchall()
	#print a
	for nr, (textname, snr, num, token) in enumerate(a):
		#sql.exportAnnotations(textid, textname, "lastconll")
		texts[textname]= texts.get(textname,[])+[(snr, num,token)]
	newfiles=[]
	for textname in texts:
		print "processing",textname
		f=codecs.open(outfolder+textname, "w", "utf-8")
		for c, (snr, num, tok) in enumerate(sorted(texts[textname])):
			if num == 1 and c > 0:
				f.write('\n')
			f.write("\t".join([str(num), tok]+["_"]*12)+'\n')
		print c+1, "tokens"
		f.close()
		newfiles+=[outfolder+textname]
	return newfiles

def getEmptyConlls(project,outfolder, lemma):
	newfiles=[]
	path="projects/"+project+"/export/"
	for conllfile in glob.glob(path+"*.most.recent.trees.conll10"):
		newfilename=conll.makeEmpty(conllfile, outfolder=outfolder, lemma=lemma)
		newfiles+=[newfilename]
	return newfiles


def main(project, outfolder):
	extractConllFiles(project)
	
	return toparse


if __name__ == '__main__':
	#toparse=extractConllFiles("OrfeoGold2016", "./mate/test_trees/")
	toparse=extractConllFiles("HongKongTVMandarin", "./mate/")
	
