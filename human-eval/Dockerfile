# Schritt 1: Ubuntu als Basis-Image
FROM ubuntu:20.04

# Schritt 2: Installiere grundlegende Abhängigkeiten
RUN apt-get update && \
    apt-get install -y python3 python3-pip git && \
    apt-get clean

# Schritt 3: Installiere Conda (optional, wenn du Conda verwenden möchtest)
RUN apt-get install -y wget bzip2 && \
    wget https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh -O /tmp/anaconda.sh && \
    bash /tmp/anaconda.sh -b -p /opt/anaconda && \
    rm /tmp/anaconda.sh && \
    export PATH=/opt/anaconda/bin:$PATH

# Schritt 4: Kopiere das Projekt in das Docker-Image
# Hier wird das gesamte Projekt in das Docker-Image kopiert
COPY . /app/human-eval

# Schritt 5: Installiere die Abhängigkeiten
WORKDIR /app/human-eval
RUN pip3 install -r requirements.txt

# Schritt 6: Installiere das Paket im 'editable' Mode
RUN pip3 install -e .

# Schritt 7: Setze das Arbeitsverzeichnis zurück
WORKDIR /app

# Schritt 8: Stelle sicher, dass Python3 auch standardmäßig verfügbar ist
RUN ln -s /usr/bin/python3 /usr/bin/python

# Schritt 9: Führe den Python-Befehl aus
CMD ["python3", "human_eval/evaluate_functional_correctness.py", "samples.jsonl"]
