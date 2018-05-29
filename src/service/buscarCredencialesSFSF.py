import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas
import os

config_file = open('./src/service/config.json','r')
config = json.load(config_file)

scope = config['scope']
creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(os.environ['CLIENT_SECRET_TEST']),scope)
client = gspread.authorize(creds)

sheet = client.open(config['archivo']['credencialesSFSF']['sheet'])
worksheet = sheet.worksheet(config['archivo']['credencialesSFSF']['workSheet'])

wsheet = worksheet.get_all_values()

# header -> primera fila es un comentario
df = pandas.DataFrame.from_records(wsheet[1:])

# .values -> array o matriz
header = (df.loc[df[0] == 'Cliente']).values[0]
dataSet = (df.loc[df[0] != 'Cliente']).values

dff = pandas.DataFrame.from_records(dataSet, columns = header)

# out json
def outCardsCredencialesSFSF(payload):
    cards = []

    for index, row in payload.iterrows():
        cards.append(
            {
              'header': {
                  'title': row.Cliente,
                  'subtitle': 'Company ID: '+row['Company ID']
                },
                'sections': [
                  {
                    'widgets': [
                          {
                          'buttons': [
                                  {
                                    'textButton': {
                                      'text': 'Link '+ row['Tipo Acceso'],
                                      'onClick': {
                                        'openLink': {
                                          'url': row.Link
                                        }
                                      }
                                    }
                                  }
                              ]
                          },
                          {
                              'keyValue': {
                                'topLabel': 'Usuario',
                                'content': row.Usuario
                              }
                          },
                          {
                              'keyValue': {
                                'topLabel': 'Contraseña',
                                'content': row.Contraseña
                              }
                          }
                    ]
                  }
                ]
              }
        )

    return {'cards': cards}

def BuscarCredenciales (pCliente, pAmbiente = ''): 
  # case = false, no sensitive case
  cliente = dff.Cliente.str.contains(pCliente, case=False)

  if (pAmbiente != ''):
    ambiente = dff['Tipo Acceso'].str.contains(pAmbiente, case=False)

    if (len(dff.loc[cliente & ambiente]) <= 6 and len(dff.loc[cliente & ambiente]) > 0):
      return outCardsCredencialesSFSF(dff.loc[cliente & ambiente]) 
    elif len(dff.loc[cliente & ambiente]) >= 7:
      return {'text': 'Srry hay muchas credenciales y aún soy incapaz de mostrarlas'}
    else:
      return {'text': 'Wut? Aún no entiendo'}
      #return {'text': 'Existen muchas credenciales de %s para %s' % (dff.loc[cliente & ambiente]['Tipo Acceso'].iloc[0], dff.loc[cliente].Cliente.iloc[0]) }

  else: 

    if (len(dff.loc[cliente]) <= 6 and len(dff.loc[cliente]) > 0):
      return outCardsCredencialesSFSF(dff.loc[cliente])
    elif len(dff.loc[cliente]) >= 7:
      return {'text': 'Srry hay muchas credenciales para %s y aún soy incapaz de mostrarlas' % (dff.loc[cliente].Cliente.iloc[0])}
    else:
      return {'text': 'Wut? Aún no entiendo'}
      #return {'text': 'Existen muchas credenciales para %s, especifica si necesitas DEV TST o PRD' % (dff.loc[cliente].Cliente.iloc[0])}       
    
