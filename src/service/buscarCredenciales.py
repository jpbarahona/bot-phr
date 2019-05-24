import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas
import os
import nltk

# array scope
scope = json.loads(os.environ['DRIVE_SHEETS_SCOPE'])["scope"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(os.environ['CLIENT_SECRET']),scope)

# dictionary
dictionaryFile = open('./src/service/dictionaryFile_ArchivoCredenciales.json','r')
dictionaryFile_json = json.load(dictionaryFile)

# google credentials
client = gspread.authorize(creds)

# sheet = client.open(config['archivo']['credencialesSFSF']['sheet'])
sheet = client.open('SFSF Accesos')

# tokenize text o separate each words from the text
def tokenizeText(p_text):
	return nltk.word_tokenize(p_text.lower())


# call worksheet from excel (drive)
def call_worksheet(p_worksheet):
	worksheet = sheet.worksheet(p_worksheet)
	
	# values from excel
	return worksheet.get_all_values()

# get clients from worksheet
def cliente_worksheet(p_worksheet_dict):
	# header -> primera fila es un comentario (missed)
	df = pandas.DataFrame.p_worksheet_dict(wsheet[1:])

	# .values -> array o matriz
	header = (df.loc[df[0] == 'Cliente']).values[0]

	dataSet = (df.loc[df[0] != 'Cliente']).values

	return pandas.DataFrame.from_records(dataSet, columns = header)

# main
def buscarCredenciales(p_text):
	tokens = tokenizeText(p_text)

	# Array interpreting
	interpreting = {}
	worksheet = undefined

	# interpreting or representing data from the dictionaryFile_json
	for tokens_index in tokens:
		if tokens_index in dictionaryFile_json:
			# insert dict / json
			interpreting.update(dictionaryFile_json[tokens_index])
	
	# this feature need to be change in the future to identify diferents API. Abstract that variable "worksheet"	
	if "worksheet" in interpreting:
		# get values of worksheet
		worksheet = call_worksheet(interpreting["worksheet"])

	cliente = cliente_worksheet(worksheet)

	print(worksheet)