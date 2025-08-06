import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import time
from multiprocessing import Process
import os
from googlesearch import search
import webbrowser
import subprocess



r = sr.Recognizer()


def voz(texto):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)
    engine.say(texto)
    engine.runAndWait()


def hablar(texto):
    proceso = Process(target=voz, args=(texto,))
    proceso.start()
    proceso.join()

def escuchar_orden_activacion():
    with sr.Microphone() as source:
        print("Di Nova para mi activación")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        try:
            texto = r.recognize_google(audio, language='es')
            return 'nova' in texto.lower()
        except sr.UnknownValueError:
            return False

def escuchar_comando():
    with sr.Microphone() as source:
        print("Te escucho...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        texto = r.recognize_google(audio, language='es')
        print("Reconocido:", texto)
        return texto.lower()
    except sr.UnknownValueError:
        return ""
    
def buscar_app(nombre_app):
    # Nombre del ejecutable esperado
    ejecutable = nombre_app.lower() + ".exe"
    
    # Lista de discos a buscar (puedes agregar más si tienes más unidades)
    discos = ['C:\\', 'D:\\', 'E:\\']
    
    for disco in discos:
        for raiz, carpetas, archivos in os.walk(disco):
            for archivo in archivos:
                if archivo.lower() == ejecutable:
                    ruta_completa = os.path.join(raiz, archivo)
                    return ruta_completa
    return None

def abrir_app(nombre_app):
    ruta = buscar_app(nombre_app)
    if ruta:
        subprocess.Popen(ruta)
        hablar(f"Abriendo {nombre_app}")
    else:
        hablar(f"No encontré la aplicación {nombre_app} en tus discos.")


def main():
    activado = False
    while True:
        if not activado:
            if escuchar_orden_activacion():
                activado = True
                hablar("Sí, ¿en qué puedo ayudarte?")
        else:
            comando = escuchar_comando()

            if comando == "":
                hablar("No detecto ningún comando.")
            elif 'apagar' in comando:
                hablar("Si me necesitas, avísame. Apagando...")
                break

            elif 'reproduce' in comando:
                cancion = comando.replace('reproduce', '').strip()
                if cancion:
                    hablar("Reproduciendo " + cancion)
                    time.sleep(1.5)
                    pywhatkit.playonyt(cancion)
                else:
                    hablar("No dijiste qué canción reproducir.")

            elif 'hora' in comando:
                hora_actual = datetime.datetime.now().strftime('%H:%M:%S')
                hablar("La hora actual es: " + hora_actual)

            elif 'abre' in comando:
                abrir = comando.replace('abre', '').strip()
                hablar("abriendo" + abrir)
                abrir_app(abrir)


            elif 'busca en google' in comando:
                busqueda = comando.replace('busca', '').strip()
                if busqueda:
                    hablar("buscando" + busqueda)
                    time.sleep(1.5)
                    resultados = search(busqueda)
                    primera_url = next(resultados, None)
                    for url in resultados:
                        if "youtube.com" not in url.lower():
                            primera_url = url
                            break
                if primera_url:
                    webbrowser.open(primera_url)
       
            else:
                hablar("No entendí tu comando.")


if __name__ == '__main__':
    main()