import streamlit as st

from textblob import TextBlob

import pdftotext
#import PyPDF2
#import slate3k as slate

from PIL import Image

import pandas as pd

# Audio
from gtts import gTTS

from bokeh.models.widgets import Div

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

def play(raw_text, idioma_key):
    tts = gTTS(text=raw_text, lang=idioma_key)
    tts.save("audio.mp3")
    audio_file = open("audio.mp3","rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")


#def cria_audio(audio):

# tts = gTTS(audio,lang='en')
# #Salva o arquivo de audio
# tts.save('audio/hello.mp3')
# print("Estou aprendendo o que você disse...")
# #Da play ao audio
# playsound('audio/hello.mp3')
    

def carregar_texto(type):
        file = st.file_uploader("Carregue um arquivo de texto", type=[type])
        if file is not None:
       	    st.success("Arquivo carregado, obrigado")
            Flag=True
        else:
            st.write("Um arquivo tipo "+type+" pequeno, por favor.")

        return file   


def convert(dict_idioma,blob):
    try:
        dict_idioma_full = lista_idiomas_full()
      
        #st.write(dict_idioma)
            
        #idioma_original = get_value(blob.detect_language(),dict_idioma_full)
        #original_key = get_key(idioma_original, dict_idioma_full)
                    
        #st.success("Original Language"+":  "+ idioma_original + " ("+original_key+")")
        #play(file.getvalue(),original_key)
            
        #dict_idioma = lista_idiomas(idioma_original)
        options = st.radio("Choose a language", tuple(dict_idioma.values()))
                    
        #idioma_final = get_key(idioma_original, dict_idioma)
        #st.subheader(options)               
        value = options
        idioma_final_key = get_key(value, dict_idioma)
        #st.subheader(idioma_final_key)
        try:
            texto_convertido = str(blob.translate(to=idioma_final_key))
            st.success("Language"+": "+ value + " ("+idioma_final_key+")")
            st.subheader(texto_convertido)
                                #st.text(idioma_final_key)
            play(texto_convertido,idioma_final_key)
                        
        except:
            st.error("ERROR: some languages will fail to play the sound.")
    except:
        st.error("ERROR: some languages will fail to play the sound.")

def main():
    
    """Ouça e Fale App """
    
    #st.title("Reader & Voice")


    html_page = """
    <div style="background-color:tomato;padding=50px">
        <p style='text-align:center;font-size:50px;font-weight:bold'>Reader & Voice</p>
    </div>
              """
    st.markdown(html_page, unsafe_allow_html=True)

    image = Image.open("reader.png")
    st.sidebar.image(image,caption="", use_column_width=True)
   
    activities = ["Home","PDF","TXT","About"]
    choice = st.sidebar.radio("Home",activities)
    Flag=False

    if choice == 'Home':
        st.write("Only files:")
        st.markdown("### PDF or TXT")
        st.write("After uploading you can convert to 7 languages")
        st.markdown("### English, Spanish, French, Italian, Japanese, Russian  and Chinese")
        
    if choice == 'PDF':
        st.subheader("Under construction")
        #file = carregar_texto('pdf')
        #pdfFile = open(file,'rb')
        #pdf = PyPDF2.PdfFileReader(pdfFile)
        #with open(file, 'rb') as f:
        #    doc = slate,PDF(f)
            #for page in pdf:
            #    st.text(page)
        #st.text(doc)    
        #blob = TextBlob(pdf.getPage())
        #st.text(blob)
        #st.write(blob.detect_language())

        
    if choice == 'TXT':
        try:
            file = carregar_texto('txt')
            blob= TextBlob(file.getvalue())
            dict_idioma_full = lista_idiomas_full()
            idioma_original = get_value(blob.detect_language(),dict_idioma_full)
            original_key = get_key(idioma_original, dict_idioma_full)
            dict_idioma = lista_idiomas(idioma_original)
            st.markdown(blob)
            play(file.getvalue(),original_key)
         
            convert(dict_idioma, blob)
                          
        except:
            st.warning("TXT please")

    if choice == 'About':
        st.subheader("I hope you enjoy it and use to learn something")
        st.subheader("Built with Streamlit and Textblob")
        st.write("Problems:")
        st.write(" - sometimes the original language can't be correctly detected")
        st.write(" - sometimes the sound will fail.")
        st.subheader("by Silvio Lima")
        
        if st.button("Linkedin"):
            js = "window.open('https://www.linkedin.com/in/silviocesarlima/')"
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)



if __name__ == '__main__':
    main()
