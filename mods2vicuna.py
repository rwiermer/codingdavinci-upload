#Converts METS/MODS from StaBi HH set to Wikitext for mass upload of free sets
#Developed as part of the Coding da Vinci Workshop (Nov 21-22 2015 at DNB, Frankfurt)

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLParser
from collections import defaultdict
from string import Template
import os.path
import glob
import re

mapTemplateName="map" 
mapTemplateFields=['title','description','title','accession number','source','medium','dimensions','publisher','date','institution']

def extractMods(filename):
	ns = {'mods': 'http://www.loc.gov/mods/v3'}
	parser=XMLParser(encoding="UTF-8")
	root = ET.parse(filename,parser=parser)
	mods=root.find(".//mods:mods",ns)

	result=defaultdict(lambda: '')
	title=None
	physicalDimension=None
	
	#artist
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
		result['author']=", ".join(result_artists)
	
	#title	
	titleNode=mods.find('mods:titleInfo/mods:title',ns)	
	if (titleNode is not None):
			result["title"]=titleNode.text	

	#source
	sourceNode=mods.find('mods:identifier[@type="purl"]',ns)	
	if (sourceNode is not None):
			result["source_url"]=sourceNode.text
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
	


	#date/publisher/place
	originInfoNode=mods.find('mods:originInfo',ns)
	if originInfoNode is not None:
		dateIssuedNode=originInfoNode.find('mods:dateIssued',ns)
		if (dateIssuedNode is not None):
			result["date"]=dateIssuedNode.text
		placeOfPublicationNode=originInfoNode.find('mods:place/mods:placeTerm',ns)
		publisherNode=originInfoNode.find('mods:publisher',ns)

		if (publisherNode is not None):
			result["publisher"]=publisherNode.text
			if (placeOfPublicationNode is not None):
				result["publisher"]=(result["publisher"]+", "+placeOfPublicationNode.text).replace("[", "").replace("]","")

	#accession number
	urnIdentifierNode=mods.find('mods:identifier[@type="urn"]',ns)
	if (urnIdentifierNode is not None):
			result["accession_number"]=urnIdentifierNode.text
	
	return result
	
def wikitextFilename(variables,imageFilename):
	#TODO
	return ""

def generateWikitext(template, variableMap):
	return Template(template).substitute(variableMap).encode("UTF-8")


modss=glob.glob("C:\\Users\\Gebruiker\\Documents\\codingdavinci\\data\\karten\\karten\\*\\*.xml")	
templatefile=open("stabihh-karten.template.wikitext")
template=templatefile.read().decode("UTF-8")
for mods in modss: 
	result=extractMods(mods)
	print generateWikitext(template,result)
	tifs=glob.glob(os.path.dirname(mods)+"\\*.tif")
	print tifs
