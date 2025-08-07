import speech_recognition as sr
import sys

# Capturar la salida estándar y errores en un archivo
sys.stdout = open("log.txt", "w")
sys.stderr = sys.stdout


r = sr.Recognizer()

with sr.Microphone() as source:
    print("Habla algo...")
    audio = r.listen(source)

try:
    texto = r.recognize_google(audio, language='es')
    print("Dijiste:", texto)
except Exception as e:
    print("Error:", e)
