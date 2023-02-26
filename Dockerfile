# Pobieramy oficjalny obraz Pythona w wersji 3.8
FROM python:3.8-slim-buster

# Ustawiamy katalog roboczy na /app
WORKDIR /app

# Kopiujemy pliki projektu do katalogu /app w kontenerze
COPY . /app

# Instalujemy zależności z pliku requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Wystawiamy port 8002
# EXPOSE 8002

# Uruchamiamy skrypt server.py
CMD ["python", "server.py"]
