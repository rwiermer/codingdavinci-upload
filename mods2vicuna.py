import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLParser
import os.path
import glob
import re
def extractMods(filename):
	ns = {'mods': 'http://www.loc.gov/mods/v3'}
	parser=XMLParser(encoding="UTF-8")
	root = ET.parse(filename,parser=parser)
	mods=root.find(".//mods:mods",ns)

	result={}
	title=None
	physicalDimension=None
	
	#artist
	#TODO vorname nachname
	result_artists=[]
	names=mods.findall('.//mods:name',ns)
	for a in names:
		artistNode=a.find('mods:role[mods:roleTerm="art"]',ns)
		if (artistNode is not None):
			name=""
			givenNameNode=a.find('mods:namePart[@type="given"]',ns)
			familyNameNode=a.find('mods:namePart[@type="family"]',ns)
			if givenNameNode is not None:
				name=givenNameNode.text
			if familyNameNode is not None:
				name=name+" "+familyNameNode.text	
			result_artists.append(name)
	if result_artists:
		result['artist']=result_artists
	
	#title	
	titleNode=mods.find('mods:titleInfo/mods:title',ns)	
	if (titleNode is not None):
			result["title"]=titleNode.text	

	#source
	sourceNode=mods.find('mods:identifier[@type="purl"]',ns)	
	if (sourceNode is not None):
			result["source"]=sourceNode.text+" "+u'Staats- und Universit\u00e4tsbibliothek Hamburg'
	#medium/dimensions
	physicalDescriptionNodes=mods.findall('mods:physicalDescription/mods:extent',ns)
	for extendNode in physicalDescriptionNodes:
		if re.search(".* x .* cm",extendNode.text) is not None:
			result["dimensions"]=extendNode.text
		else:
			if result.get("medium",None) is not None:
				result["medium"]=result["medium"]+", "+extendNode.text
			else:
				result["medium"]=extendNode.text
	
	#description
	#TODO copy from title ?


	#date/publisher/place
	originInfoNode=mods.find('mods:originInfo',ns)
	if originInfoNode is not None:
		dateIssuedNode=originInfoNode.find('mods:dateIssued',ns)
		if (dateIssuedNode is not None):
			result["date"]=dateIssuedNode.text
		placeOfPublicationNode=originInfoNode.find('mods:place/mods:placeterm',ns)
		publisherNode=originInfoNode.find('mods:publisher',ns)

		if (publisherNode is not None):
			result["publisher"]=publisherNode.text
			if (placeOfPublicationNode is not None):
				result["publisher"]=result["publisher"]+", "+placeOfPublicationNode.text.translate(None, '[]')
	#institution
	result["institution"]=u'Staats- und Universit\u00e4tsbibliothek Hamburg'

	#accession number
	urnIdentifierNode=mods.find('mods:identifier[@type="urn"]',ns)
	if (urnIdentifierNode is not None):
			result["accession number"]=urnIdentifierNode.text
	
	return result
	
def wikitextFilename(imageFilename)
def generateWikitext(variableMap):
	header=""
	filledTemplate=""
	footer=""
	return(header+filledTemplate+footer)


modss=glob.glob("C:\\Users\\Gebruiker\\Documents\\codingdavinci\\data\\karten\\karten\\*\\*.xml")	

for mods in modss: 
	result=extractMods(mods)
	print result
	print generateWikitext(mods)
	#print os.path.dirname(mods)+"\\*.tif"
	#tifs=glob.glob(os.path.dirname(mods)+"\\*.tif")
	#print tifs	
