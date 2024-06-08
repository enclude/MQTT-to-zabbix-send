# Używamy oficjalnego obrazu Pythona
FROM python:3.8-slim-buster

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy pliki z obecnego katalogu do katalogu /app w kontenerze
COPY z2m-to-zabbix.py z2m-to-zabbix.py

# Instalujemy wymagane pakiety
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir paho-mqtt
RUN pip3 install --no-cache-dir zabbix_utils

# Uruchamiamy skrypt Pythona po uruchomieniu kontenera
CMD [ "python3", "./z2m-to-zabbix.py" ]
