import requests
import os
import json

def options():
    print("1. Run the program\n"
          "2. Register new city\n")
    

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def busca(city, dados):
    index = -1
    for i in range(len(dados)):
        if(dados[i]['cidade'] == city):
            return i
    return -1

clear()

try:
    with open("dados.json", "r") as pull_city:
        dados = json.load(pull_city)
except:
    print("Error.")

#Action options
while True:
    options()
    escolha = input("Type the wanted option: ")
    #"Run the program"
    if escolha == "1":
        clear()
        break
    #"Register new location"
    elif escolha == "2":
        cidade = input("Type the city name: ").upper()
        latitude = input("Type the latitude: ")
        longitude = input("Type the longitude: ")
        #JSON file creation
        nova_cidade = {
            "cidade": cidade,
            "latitude": latitude,
            "longitude": longitude
            }
        try:
            with open("dados.json", "r") as arquivo:
                dados = json.load(arquivo)
        except:
            dados = []

        dados.append(nova_cidade)
        with open("dados.json", "w", encoding= "utf-8") as arquivo:
            json.dump(dados,arquivo,indent=4, ensure_ascii=False, sort_keys=False)
        clear()
    else:
        print("Invalid.")
        continue

#Search coordinates on the JSON file
cidade_encontrada = None
pull_city = input("Which city? ").upper()
index = busca(pull_city, dados)
if (index > -1):
    cid = dados[index]
    print(cid["cidade"])
    print(cid["longitude"])
    print(cid["latitude"])

for cidade in dados:
    if cidade["cidade"] == pull_city:
        cidade_encontrada = cidade
        latitude = cidade_encontrada["latitude"]
        longitude = cidade_encontrada["longitude"]
        break

if cidade_encontrada is None:
    print("City not found. Please register it.")
    exit()
    
#API connection
url = (f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true")

clear()

print("Working...")

response = requests.get(url)
dados_api = response.json()

clear()

temperatura = dados_api["current_weather"]["temperature"]
clima = dados_api["current_weather"]["is_day"]
if clima == 1:
    clima = "day"
else:
    clima = "night"
#Information output for the user
print(
    f"The current temperature in {cidade_encontrada["cidade"]} is {temperatura}°C\n"
    f"At the moment, {cidade_encontrada["cidade"]} is {clima}.\n"
    )
