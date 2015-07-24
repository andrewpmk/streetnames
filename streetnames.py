# http://oreilly.com/catalog/pythonxml/chapter/ch01.html

TYPE="way"
KEY="highway"
VALUES=["motorway","trunk","primary","secondary","tertiary","residential","unclassified","service"]

import xml.sax
import xml.sax.handler
import sys

def isin(x,list):
	if len(list)==0: return 1
	for i in list:
		if (i==x): return 1
	return 0

class OsmHandler(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.streetnames=[]
		self.inway=0
	def startElement(self,name,attributes):
		if name==TYPE:
			self.inway=1
			self.streettype=""
			self.streetname=""
		elif name=="tag":
			self.key=attributes["k"]
			self.value=attributes["v"]
			if self.key==KEY and self.inway==1:
				self.streettype=self.value
			elif self.key=="name" and self.inway==1:
				self.streetname=self.value
#			print [self.key,self.value]

	def endElement(self,name):
		if name==TYPE:
			self.inway=0
			if (isin(self.streettype,VALUES) and self.streetname!=""):
				self.streetnames.append(self.streetname)
			self.streettype=self.streetname=""

def rmduplicates(list):
	list2=[]
	last=0
	for i in list:
		if (last!=i): list2.append(i)
		last=i
	return list2

parser=xml.sax.make_parser()
handler=OsmHandler()
parser.setContentHandler(handler)
filename=""
good=0
commandline=0
if (len(sys.argv)==2):
	filename=sys.argv[1]
	commandline=1
while (good==0):
	if (filename==""):
		print "Enter name of OSM file to parse:"
		filename=str(raw_input())
	try:
		parser.parse(filename)
	except IOError:
		print "Invalid filename"
		if (commandline): good=1
		filename=""
	else:
		good=1
list=handler.streetnames
list.sort()
list=rmduplicates(list)
for i in list:
	print str(i)
