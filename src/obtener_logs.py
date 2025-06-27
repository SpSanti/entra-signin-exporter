import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

client_id = os.getenv("GRAPH_CLIENT_ID")
client_secret = os.getenv("GRAPH_CLIENT_SECRET")
tenant_id = os.getenv("GRAPH_TENANT_ID")
scope = "https://graph.microsoft.com/.default"
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

# Obtener token
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': scope
}
token_r = requests.post(token_url, data=token_data)
access_token = token_r.json().get('access_token')

# Encabezados
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Obtener logs
signins_url = 'https://graph.microsoft.com/v1.0/auditLogs/signIns'
signins = []
while signins_url:
    response = requests.get(signins_url, headers=headers)
    data = response.json()
    signins.extend(data.get('value', []))
    signins_url = data.get('@odata.nextLink')

# Guardar CSV
os.makedirs('data', exist_ok=True)
df = pd.json_normalize(signins)
df.to_csv('data/signins_logs.csv', index=False)
print("✅ Logs guardados en 'data/signins_logs.csv'")
