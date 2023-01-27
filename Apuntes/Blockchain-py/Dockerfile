#Este ejemplo monta el proyecto blockchain.py

FROM alpine:3.17.0
LABEL maintainer="Juan Crespo Twitter @jpcr3spo"

WORKDIR /app
# copiamos los archivos del repositorio a una carpeta
# donde tendremos la aplicacion
COPY . .
RUN apk add python3 py3-pip curl &&\
        python -m venv env &&\
        source env/bin/activate &&\
        pip install -r req.txt &&\
        rm -rf /var/cache/apt

# La aplicación corre por defecto en el puerto 3000
EXPOSE 3000
ENTRYPOINT env/bin/python blockchain.py

