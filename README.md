# METAL HITSTER CREATOR
## REQUISITOS
* Tener instalado python 3.13 o superior
* Tener instalado el gestor de paquetes pip y añadir la ruta del ejecutable a la variable PATH.
```
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
```
* Instalar requirements.txt `pip install -r requirements.txt`

## INTRUCCIONES DE USO
* Tener creada la carpeta `qrs` a la altura del ejecutable
* Tener el excel `lista_canciones.xlsx` a la altura del ejecutable. Este excel debe tener al menos 4 columnas en este orden: título canción, artista, año, link canción spotify. La primera fila se descartará por ser la cabecera.
* Ejecutar con `python3 main.py`
* Se creará un pdf con el nombre `metalHitster.pdf` a la altura del ejecutable