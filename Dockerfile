FROM python:3.10.6

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf

#Opcional para quitar el error en el server de la libreria libQt5Core.so.5
RUN strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5

WORKDIR /code/

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./main.py /code/

#COPY ./anexoII.html /code/templates/

#ENTRYPOINT ["wkhtmltopdf"]

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8085"]