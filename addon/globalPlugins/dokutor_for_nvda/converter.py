import re
import codecs

def convertFile(fileName, converted):
	file = codecs.open(fileName,"r","utf-16",errors="replace")
	lines = []
	tmpDic = {}
	for line in file:
		if line.isspace():
			continue
		line=line.rstrip('\r\n')
		if line.startswith('#'):
			continue
		line = line.replace(",", "\t")
		line = line + "\t0\t0"
		patternLength = len(line.split("\t")[0])
		if not patternLength in tmpDic:
			tmpDic[patternLength] = []
		tmpDic[patternLength].append(line)
	for i in sorted(tmpDic.keys(), reverse=True):
		for l in tmpDic[i]:
			lines.append(l)
	with open(converted, mode="w", encoding="utf-8") as f:
		f.write("\r\n".join(lines))
	return True

