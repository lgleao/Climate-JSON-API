import requests
import os
import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from time import sleep

def options():
    print("1. Run the program\n"
          "2. Register new city\n"
          "3. Temperature graphic\n"
          "4. Sair\n")
    

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

def main():
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
    dia = dados_api["current_weather"]["is_day"]
    clima = dados_api["current_weather"]["weathercode"]

    #weathercode
    if clima == 0 or 1:
        clima = "sunny"
    elif clima in [2,3]:
        clima = "nublado"
    elif clima in [45,46,47,48]:
        clima = "foggy"
    elif clima in [51,52,53,54,55]:
        clima = "rainy"
    elif clima in [61,63,65,95,96,97,98,99]:
        clima = "raining"
    elif clima in [71,72,73,74,75,80,81,82,85,86]:
        clima = "snow"
    elif clima in [95,96,97,98,99]:
        clima = "thundering"
        
    #is_day
    if dia == 1:
        dia = "day"
    else:
        dia = "night"

    #Output de informações para o usuário
    print(f"The temperature in {cidade_encontrada["cidade"]} is {temperatura}°C")
    print(f"{cidade_encontrada["cidade"]} is {dia}, and is {clima}.")

def buscar_coordenadas(nome_cidade):
    #Search lat, long and timezone from every city
    url_geo = f"https://geocoding-api.open-meteo.com/v1/search?name={nome_cidade}&count=1&language=pt&format=json"
    resposta = requests.get(url_geo).json()
    
    if "results" in resposta:
        cidade = resposta["results"][0]
        return {
            "lat": cidade["latitude"],
            "lon": cidade["longitude"],
            "nome": f"{cidade['name']}, {cidade.get('admin1', '')} - {cidade.get('country', '')}",
            "timezone": cidade["timezone"]
        }
    return None

def exibir_grafico_historico():
    print("=== CLIMATE HISTORIC CONSULT ===")
    cidade_input = input("Type the city name: (Ex: New York): ")

    localizacao = buscar_coordenadas(cidade_input)

    if not localizacao:
        print("City not found. Try again.")
        return # Interrompe a função e volta pro menu

    print(f"Found: {localizacao['nome']}")
    
    try:
        ano = int(input("Type the year (Ex: 2025): "))
        mes = int(input("Type a month (Ex: 1 for january, 12 for december): "))
        
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        
        start_date = f"{ano}-{mes:02d}-01"
        end_date = f"{ano}-{mes:02d}-{ultimo_dia}"
        
    except ValueError:
        print("Error: Please, try using valid numbers only.")
        return

    url_historico = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": localizacao["lat"],
        "longitude": localizacao["lon"],
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": localizacao["timezone"]
    }

    print(f"\nSearching data beetween {start_date} and {end_date}...")
    
    try:
        resposta = requests.get(url_historico, params=params)
        resposta.raise_for_status()
        dados = resposta.json()
        
        df = pd.DataFrame({
            "Data": dados["daily"]["time"],
            "Máxima": dados["daily"]["temperature_2m_max"],
            "Mínima": dados["daily"]["temperature_2m_min"]
        })
        
        print("\n--- DATA ---")
        print(df.to_string(index=False))
        
        # --- PLOTAGEM DO GRÁFICO ---
        plt.figure(figsize=(12, 6))
        plt.plot(df['Data'], df['Máxima'], label='Temp Máxima (°C)', color='darkorange', marker='o')
        plt.plot(df['Data'], df['Mínima'], label='Temp Mínima (°C)', color='teal', marker='o')
        
        plt.title(f'Histórico de Temperaturas - {localizacao["nome"]} ({mes:02d}/{ano})')
        plt.xlabel('Dias do Mês')
        plt.ylabel('Temperatura (°C)')
        
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        plt.tight_layout()
        
        print("\n Opening graphic...")
        sleep(2)
        clear()
        plt.show()
        
    except requests.exceptions.RequestException as e:
        print(f"Error: could not find historical climate.")
        sleep(2)
        clear()

file = Path("dados.json")
if file.exists() == False:
    os.System("touch dados.json)

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
        main()
        sair = input("Press enter to leave. ")
        if sair == "":
            clear()
            continue
        else:
            clear()
            continue
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
    elif escolha == "3":
        clear()
        exibir_grafico_historico()
    elif escolha == "4":
        print("Leaving...")
        exit()
    else:
        clear()
        continue
