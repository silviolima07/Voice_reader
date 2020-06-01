import streamlit as st
import speech_recognition as sr

from textblob import TextBlob

import PyPDF2
from PyPDF2 import PdfFileReader
import pdftotext

import pandas as pd
#from PIL import Image
# Emoji
#import emoji

# Audio
from gtts import gTTS

from bokeh.models.widgets import Div

# Web Scraping Pkg
#from bs4 import BeautifulSoup
#from urllib.request import urlopen

# Fetch Text From Url
#@st.cache
#def get_text(raw_url):
#    page = urlopen(raw_url)
#    soup = BeautifulSoup(page)
#    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
#    return fetched_text

def get_value( my_key, my_dicts):
    for key, value in my_dicts.items():
        if my_key == key:
            return value

def get_key( my_value, my_dicts):
    for key, value in my_dicts.items():
        if my_value == value:
            return key

@st.cache
def lista_idiomas(idioma_original):
    df_idiomas = pd.read_csv('lista_idiomas.csv')
    dict_idiomas = {}
    linhas = len(df_idiomas)
    for i in range(0, linhas):
        if idioma_original != df_idiomas.iloc[i,1]:
            key = df_idiomas.iloc[i,0] # sigla 'pt'
            value = df_idiomas.iloc[i,1] # valor 'Portuguese'
            dict_idiomas[key] = value
    return dict_idiomas

@st.cache
def lista_idiomas_full():
    df_idiomas = pd.read_csv('lista_idiomas.csv')
    dict_idiomas = {}
    linhas = len(df_idiomas)
    for i in range(0, linhas):
        key = df_idiomas.iloc[i,0] # sigla 'pt'
        value = df_idiomas.iloc[i,1] # valor 'Portuguese'
        dict_idiomas[key] = value
    return dict_idiomas

#def area_texto():
#    raw_text = st.text_area("Copie e Cole o texto",'cole aqui')
#    return raw_text


def play(raw_text, idioma_key):
    tts = gTTS(text=raw_text, lang=idioma_key)
    tts.save("audio.mp3")
    audio_file = open("audio.mp3","rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

def ouvir_microfone():
    #Habilita o microfone para ouvir o usuario
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    #microfone = sr.Recognizer()
    with microphone as source:
        #Chama a funcao de reducao de ruido disponivel na speech_recognition
        recognizer.adjust_for_ambient_noise(source)
        #Avisa ao usuario que esta pronto para ouvir
        st.subheader("Diga alguma coisa ")
        #Armazena a informacao de audio na variavel
        audio = recognizer.listen(source)
        try:
            #Passa o audio para o reconhecedor de padroes do speech_recognition
            frase = recognizer.recognize_google(audio,language='pt-BR')
            #Após alguns segundos, retorna a frase falada
            #st.subheader('Você disse...')
            #st.success(frase)#Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
        except sr.UnknownValueError:
            st.error("Não entendi")
        return frase


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response




def cria_audio(audio):

 tts = gTTS(audio,lang='en')
 #Salva o arquivo de audio
 tts.save('audio/hello.mp3')
 print("Estou aprendendo o que você disse...")
 #Da play ao audio
 playsound('audio/hello.mp3')
    

def carregar_texto(type):
        file = st.file_uploader("Carregue um arquivo de texto", type=[type])
        if file is not None:
       	    st.success("Arquivo carregado, obrigado")
        else:
            st.write("Um arquivo tipo "+type+" pequeno, por favor.")

        return file   


def convert(file, blob):
    dict_idioma_full = lista_idiomas_full()
    idioma_original = get_value(blob.detect_language(),dict_idioma_full)
    original_key = get_key(idioma_original, dict_idioma_full)
 
    try:
        dict_idioma_full = lista_idiomas_full()
            
        idioma_original = get_value(blob.detect_language(),dict_idioma_full)
        original_key = get_key(idioma_original, dict_idioma_full)
                    
        st.success("Original Language"+":  "+ idioma_original + " ("+original_key+")")
        play(file.getvalue(),original_key)
            
        dict_idioma = lista_idiomas(idioma_original)
        options = st.multiselect("Choose a language", tuple(dict_idioma.values()))
                    
        idioma_final = get_key(idioma_original, dict_idioma)
                       
        for i in range(len(options)):
            value = options[i]
            idioma_final_key = get_key(value, dict_idioma)
            try:
                if (idioma_original != idioma_final_key):
                    texto_convertido = str(blob.translate(to=idioma_final_key))
                    st.success("Language"+": "+ value + " ("+idioma_final_key+")")
                    #st.write(texto_convertido)
                                #st.text(idioma_final_key)
                    play(texto_convertido,idioma_final_key)
                        
            except:
                st.error("ERROR: some languages will fail to play the sound.")
    except:
        st.error("ERROR: some languages will fail to play the sound.")

def main():
    
    """Ouça e Fale App """
    
    st.title("Reader & Voice")
   
    activities = ["Home","PDF","TXT","About"]
    choice = st.sidebar.radio("Home",activities)

    if choice == 'Home':
        st.write("Only files:")
        st.markdown("### PDF or TXT")
        st.write("After uploading you can convert to 7 languages")
        st.markdown("### English, Spanish, French, Italian, Japanese, Russian  and Chinese")

        #st.write("Definitions")
        #st.write("PCA is not a statistical method to infer parameters or test hypotheses. Instead, it provides a method to reduce a complex dataset to lower dimension to reveal sometimes hidden, simplified structure that often underlie it.")
        #st.write("")
        #st.write("PCA is a statistical method routinely used to analyze interrelationships among large numbers of objects.")
        #st.write("")
        #st.write("Principal component analysis (PCA) is a mathematical algorithm that reduces the dimensionality of the data while retaining most of the variation in the data set.")
        
    if choice == 'PDF':
        
        file = carregar_texto('pdf')
        pdf = pdftotext.PDF(file)
            #for page in pdf:
            #    st.text(page)
            
        blob = TextBlob(pdf[0])
        st.text(blob)
        st.write(blob.detect_language())

        #dict_idioma_full = lista_idiomas_full()
        #idioma_original = get_value(blob.detect_language(),dict_idioma_full)
            #original_key = get_key(idioma_original, dict_idioma_full)
                    
            #st.success("Original Language"+":  "+ idioma_original + " ("+original_key+")")

            # Original sound
            #play(raw_text,original_key)
                    
                              
            #dict_idioma = lista_idiomas(idioma_original)
            #options = st.multiselect("Choose a language", tuple(dict_idioma.values()))
                                      
                    

            #for i in range(len(options)):
            #    value = options[i]
            #    idioma_final_key = get_key(value, dict_idioma)
            #    try:
            #        if (idioma_original != idioma_final_key):
            #            texto_convertido = str(blob.translate(to=idioma_final_key))
            #            st.success("Language"+": "+ value + " ("+idioma_final_key+")")
            #            st.write(texto_convertido)
            #            #st.text(idioma_final_key)
            #            play(texto_convertido,idioma_final_key)
            #            
            #    except:
            #        st.error("ERROR: some languages will fail to play the sound.")

            #dict_idioma_full = lista_idiomas_full()
            #idioma_original = get_value(blob.detect_language(),dict_idioma_full)
            #original_key = get_key(idioma_original, dict_idioma_full)
                    
            #st.success("Original Language"+":  "+ idioma_original + " ("+original_key+")")

            # Original sound
            #play(blob,original_key)
            #convert(blob)
        #except:
        #    st.warning("PDF please")

      
    if choice == 'TXT':
        try:
            file = carregar_texto('txt')
            blob= TextBlob(file.getvalue())
            st.markdown(blob)
            #dict_idioma_full = lista_idiomas_full()
            #idioma_original = get_value(blob.detect_language(),dict_idioma_full)
            #original_key = get_key(idioma_original, dict_idioma_full)
                    
            #st.success("Original Language"+":  "+ idioma_original + " ("+original_key+")")
            # Original sound
            #play(file.getvalue(),original_key)

            #st.write(blob.detect_language())
            #st.subheader(blob)
            convert(file, blob)
                          
                              
            #dict_idioma = lista_idiomas(idioma_original)
            #options = st.multiselect("Choose a language", tuple(dict_idioma.values()))
                                      
                    

            #for i in range(len(options)):
            #    value = options[i]
            #    idioma_final_key = get_key(value, dict_idioma)
            #    try:
            #        if (idioma_original != idioma_final_key):
            #            texto_convertido = str(blob.translate(to=idioma_final_key))
            #            st.success("Language"+": "+ value + " ("+idioma_final_key+")")
            #            st.write(texto_convertido)
            #            #st.text(idioma_final_key)
            #            play(texto_convertido,idioma_final_key)
            #            
            #    except:
            #        st.error("ERROR: some languages will fail to play the sound.")

        except:
            st.warning("TXT please")





















    # Creating pdf reader object.
    #pdf_reader = PyPDF2.PdfFileReader(file)
    #pdf = pdftotext.PDF(file)
    # Checking total number of pages in a pdf file.
    #st.write("Total number of Pages:", pdf_reader.numPages)
 
    # Creating a page object.
    #page = pdf_reader.getPage(0)
 
    # Extract data from a specific page number.
    #st.text(page.extractText())
    
    #convert(blob)
    

    #with open('file.txt', 'w') as f:
    #    f.write(pdf)
 
    #file_object  = open("file.txt", "r") 

    
    # Iterate over all the pages
    #for page in pdf:
    #    st.text(page)

    #st.text(file_object)
    # Just read the second page
    #print(pdf.read(2))

    # Or read all the text at once
    #st.text(pdf.read(0))
   
    #if file is not None:
    #st.write("Texto:",file.getvalue())
        #blob= TextBlob(file.getvalue()) # pra text ok
        #blob= TextBlob(page.extractText())
        #blob = TextBlob(pdf[0])
        #st.subheader(blob)

        #dict_idioma_full = lista_idiomas_full()
        #idioma_original = get_value(blob.detect_language(),dict_idioma_full)
        #original_key = get_key(idioma_original, dict_idioma_full)
                    
        #st.success("Original Language"+":  "+ idioma_original + " ("+original_key+")")

        #frase_en = blob.translate(to='en')
        #st.subheader(frase_en)



        #try:
        #        dict_idioma_full = lista_idiomas_full()
            
        #        idioma_original = get_value(blob.detect_language(),dict_idioma_full)
        #        original_key = get_key(idioma_original, dict_idioma_full)
                    
        #        st.success("Original Language"+":  "+ idioma_original + " ("+original_key+")")
            
        #        dict_idioma = lista_idiomas(idioma_original)
        #        options = st.multiselect("Choose a language", tuple(dict_idioma.values()))
                    
        #        idioma_final = get_key(idioma_original, dict_idioma)
                       
        #        for i in range(len(options)):
        #                value = options[i]
        #                idioma_final_key = get_key(value, dict_idioma)
        #                try:
        #                    if (idioma_original != idioma_final_key):
        #                        texto_convertido = str(blob.translate(to=idioma_final_key))
        #                        st.success("Language"+": "+ value + " ("+idioma_final_key+")")
        #                        st.write(texto_convertido)
        #                        #st.text(idioma_final_key)
        #                        play(texto_convertido,idioma_final_key)
                        
        #                except:
        #                    st.error("ERROR: some languages will fail to play the sound.")
        #except:
        #        st.error("ERROR: some languages will fail to play the sound.")

        #play(frase_en,'en')
    # create recognizer and mic instances
    #recognizer = sr.Recognizer()
    #microphone = sr.Microphone()
    
    #image = Image.open("people_speaking.jpg")
    #st.sidebar.image(image,caption="Different languages", use_column_width=True)
    #frase_default = 'Bem vindo por favor diga algo'
    #frase_error ='Tente novamente'
   

    #if st.sidebar.button("Me Fala"):
    #    frase = ouvir_microfone()
    #    #frase = recognize_speech_from_mic(recognizer, microphone)
    #    st.subheader('Você disse...')
    #    st.success(frase) #Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
    #    blob = TextBlob(frase)
    #    frase_en = blob.translate(to='en')
    #    play(frase_en,'en')
        
 
        #st.write('Frase Correta ?')
        #if st.button('Sim'):
        #    st.write("teste")
            #blob= TextBlob(frase) # Identifica o idioma da frase
            #df_idiomas = pd.read_csv('lista_idiomas.csv')
            #dict_idioma_full = lista_idiomas_full()
            #idioma_original = get_value(blob.detect_language(),dict_idioma_full)
            #st.write("Idioma original da frase:", idioma_original)
            #play(frase,'pt')
       
    #if st.sidebar.button("Me Ouça"):
    #    st.write("Frase: ",frase)
    #    st.write("Frase Default: ",frase_default)
    #    if frase != frase_default:
    #        play(frase,'pt')
    #    else:
    #       play(frase_default,'pt') 
        
    

if __name__ == '__main__':
    main()
