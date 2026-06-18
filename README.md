# 🌍 City Weather Manager

This is a Python script that allows you to register cities with their respective geographic coordinates (latitude and longitude) in a local JSON file, and then fetch their current weather conditions using the public **Open-Meteo API**.

## 🚀 Features

* **City Registration:** Saves the city name, latitude, and longitude into a local `dados.json` file.
* **Weather Query:** Consumes the Open-Meteo API to retrieve the current temperature and whether it is day or night in the registered cities.
* **Data Persistence:** Stores your location data locally using the JSON format.
* **Terminal Interface:** Interactive and clean CLI menu that automatically clears the screen after each action.

## 🛠️ Prerequisites

Before running the script, make sure you have Python installed on your machine and the `requests` library for handling HTTP requests.

You can install the required library by running:

## bash
pip install requests

## 🔧 How to Run

  1. Clone this repository or download the script file.

  2. Make sure you run the script from its root folder.

  3. Make sure you have the necessary libs. (requests, pandas, matplotlib)

  4. Run the script in your terminal:
    python main.py

## 🚧 Future Improvements / To-Do

  1) Fix the search logic involving the pull_city variable to allow searching for a specific city.

  2) Add current weather descriptions (e.g., sunny, rainy, cloudy) based on the Open-Meteo API WMO weather codes.

  3) Prevent duplicate city entries during registration.
