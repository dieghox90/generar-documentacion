from ast import List
from fastapi import FastAPI, Body
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

import jinja2
import pdfkit
import os


load_dotenv()



#CREAR INSTANCIA DE FASTAPI
app = FastAPI()
app.title='Generar Documentacion'
app.version='1.0.1'

#Activamos Cors
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




#Creamos el modelo
class Documento(BaseModel):
    path_html:str
    path_save:str
    data:dict


@app.post('/generar/documentos/',tags=['Generar - Documentos'])
#def generar(documentos:list[Documento]=Body()):
def generar(documentos:list[Documento]=Body(),logos:list[str]=Body()):
    
    
    
    for documento in documentos:
        
    
        ruta_template = os.getenv('FILE_MANAGER_FOLDER_DOCKER')+documento.path_html
        nombre_template=ruta_template.split('/')[-1]
        ruta_template = ruta_template.replace(nombre_template,'')
        

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template))
        template=env.get_template(nombre_template)

        #Uniendo diccionarios
        myDict = {}
        myDict["logos"] = []
        #cuando hay logos
        if(len(logos)>0):
            myDict["logos"]=logos
            c = documento.data | myDict
            html = template.render(c)
        else:
            html = template.render(documento.data)    
       
        
        
        
            
        config = pdfkit.configuration(wkhtmltopdf=os.getenv('PATH_WKHTMLTOPDF'))
        options={
            'encoding':'UTF-8'
        }
        
        pdf = pdfkit.from_string(html,False,configuration=config,options=options)
        #with open(os.getenv('FILE_MANAGER_FOLDER')+documento.path_save+'/'+nombre_template.replace('.html','')+".pdf", 'wb') as output:
         #   output.write(pdf)
        
        with open(os.getenv('FILE_MANAGER_FOLDER_DOCKER')+documento.path_save+'/'+nombre_template.replace('.html','')+".pdf", 'wb') as output:
            output.write(pdf)  
          
          
            
        #response = Response( content=pdf, media_type="application/pdf") #pdf, content_type='application/pdf'
    return True



    