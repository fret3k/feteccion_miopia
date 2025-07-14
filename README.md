# MyopiaAI-Class con CNN

Este proyecto es una aplicación de escritorio desarrollada en Python con una interfaz gráfica (GUI) usando Tkinter, que permite la detección de miopía en imágenes mediante modelos de redes neuronales convolucionales (CNN) preentrenados.

## Características principales
- Interfaz intuitiva para cargar imágenes y seleccionar el modelo de predicción.
- Soporte para tres modelos de CNN: InceptionV3, ResNet50 y DenseNet.
- Modo claro y modo oscuro para mejor experiencia visual.
- Visualización de la imagen cargada y resultado de la predicción.

## Estructura del proyecto
- `main.py`: Código principal de la aplicación.
- `inceptionv3_v2.h5`, `resnet50_v2.h5`, `densenet_v2.h5`: Modelos preentrenados en formato Keras H5.
- `requirements.txt`: Dependencias necesarias para ejecutar la aplicación.
- `version_final/`: (Directorio auxiliar, puede contener versiones previas o recursos adicionales).

## Requisitos
- Python 3.7+
- Las siguientes librerías (pueden instalarse con `pip install -r requirements.txt`):
  - tkinter
  - pillow
  - numpy
  - tensorflow

## Uso
1. Clona este repositorio y asegúrate de tener los modelos `.h5` en la misma carpeta que `main.py`.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   python main.py
   ```
4. Usa la interfaz para:
   - Cambiar entre modo claro y oscuro.
   - Subir una imagen (formatos soportados: PNG, JPG, JPEG).
   - Seleccionar el modelo de CNN a utilizar.
   - Obtener la predicción (Normal o Miopía) y el porcentaje de confianza.

## Funcionamiento general
- **Carga de imagen:** Permite seleccionar una imagen desde el sistema de archivos, la muestra en la interfaz y la prepara para la predicción.
- **Selección de modelo:** Puedes elegir entre tres modelos de CNN preentrenados para realizar la predicción.
- **Predicción:** El modelo seleccionado analiza la imagen y muestra si es "Normal" o "Miopía" junto con el porcentaje de confianza.
- **Modo oscuro/claro:** Puedes alternar entre ambos modos para mayor comodidad visual.

## Créditos
Desarrollado por [fret].

## Licencia
Este proyecto se distribuye bajo la licencia MIT. 