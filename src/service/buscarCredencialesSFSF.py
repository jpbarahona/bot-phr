import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas
import os

config_file = open('./src/service/config.json','r')
config = json.load(config_file)

scope = config['scope']
creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(os.environ['CLIENT_SECRET']),scope)
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
                                'topLabel': 'Link',
                                'content': row.Link
                              }
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
                          },
                          {
                              'keyValue': {
                                'topLabel': 'Comentario',
                                'content': row[''] if row[''] != '' else '.' 
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
  cliente    = dff['Cliente'].str.contains(pCliente, case=False)
  isPassword = dff['Contraseña'] != ''
  comentario = ~dff[''].str.contains('no funciona', case=False)
  isLink     = dff['Link'] != ''
  
  cliente_isPassword_comentario = (cliente & isPassword & comentario & isLink)

  if (pAmbiente != ''):
    
    ambiente = dff['Tipo Acceso'].str.contains(pAmbiente, case=False)
    ci_ambiente = (cliente_isPassword_comentario & ambiente)

    rowDff = dff.loc[ci_ambiente].drop_duplicates(['Cliente','Tipo Acceso'])
    lenDff = len(rowDff)

    if (lenDff <= 6 and lenDff > 0):
      return outCardsCredencialesSFSF(rowDff)
    elif lenDff >= 7:
      return {'text': 'Srry hay muchas credenciales y aún soy incapaz de mostrarlas'}
    else:
      return {'text': 'Wut? Aún no entiendo'}
      #return {'text': 'Existen muchas credenciales de %s para %s' % (dff.loc[cliente & ambiente]['Tipo Acceso'].iloc[0], dff.loc[cliente].Cliente.iloc[0]) }

  else: 

    rowDff = dff.loc[cliente_isPassword_comentario].drop_duplicates(['Cliente','Tipo Acceso'])
    lenDff = len(rowDff)

    if (lenDff <= 6 and lenDff > 0):
      return outCardsCredencialesSFSF(rowDff)
    elif lenDff >= 7:
      return {'text': 'Srry hay muchas credenciales para %s y aún soy incapaz de mostrarlas' % (rowDff.Cliente.iloc[0])}
    else:
      return {'text': 'Wut? Aún no entiendo'}
      #return {'text': 'Existen muchas credenciales para %s, especifica si necesitas DEV TST o PRD' % (dff.loc[cliente].Cliente.iloc[0])}       
    
