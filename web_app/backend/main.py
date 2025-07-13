from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import os
from typing import Dict, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="MyopiaAI API",
    description="API para detección de miopía usando modelos de deep learning",
    version="1.0.0"
)

# Configurar CORS para permitir conexiones desde React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de modelos
MODELOS = {
    "InceptionV3": "inceptionv3_v2.h5",
    "ResNet50": "resnet50_v2.h5", 
    "DenseNet": "densenet_v2.h5"
}

IMAGE_SIZE = (224, 224)
modelos_cargados = {}

def cargar_modelo(nombre_modelo: str) -> tf.keras.Model:
    """Carga un modelo de TensorFlow"""
    if nombre_modelo not in modelos_cargados:
        try:
            ruta_modelo = MODELOS[nombre_modelo]
            if os.path.exists(ruta_modelo):
                modelos_cargados[nombre_modelo] = tf.keras.models.load_model(ruta_modelo)
                logger.info(f"Modelo {nombre_modelo} cargado exitosamente")
            else:
                raise FileNotFoundError(f"Modelo {ruta_modelo} no encontrado")
        except Exception as e:
            logger.error(f"Error al cargar modelo {nombre_modelo}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error al cargar modelo {nombre_modelo}")
    
    return modelos_cargados[nombre_modelo]

def procesar_imagen(imagen_bytes: bytes) -> np.ndarray:
    """Procesa la imagen para el modelo"""
    try:
        # Abrir imagen con PIL
        imagen = Image.open(io.BytesIO(imagen_bytes)).convert('RGB')
        
        # Redimensionar
        imagen_resized = imagen.resize(IMAGE_SIZE)
        
        # Convertir a array y normalizar
        imagen_array = np.array(imagen_resized) / 255.0
        
        # Agregar dimensión de batch
        imagen_array = np.expand_dims(imagen_array, axis=0)
        
        return imagen_array
    except Exception as e:
        logger.error(f"Error al procesar imagen: {str(e)}")
        raise HTTPException(status_code=400, detail="Error al procesar la imagen")

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {"message": "MyopiaAI API - Detección de Miopía"}

@app.get("/modelos")
async def obtener_modelos():
    """Obtiene la lista de modelos disponibles"""
    return {
        "modelos": list(MODELOS.keys()),
        "tamaño_imagen": IMAGE_SIZE
    }

@app.post("/predecir")
async def predecir_miopia(
    archivo: UploadFile = File(...),
    modelo: str = "InceptionV3"
):
    """
    Predice si una imagen contiene miopía
    
    Args:
        archivo: Imagen del ojo (PNG, JPG, JPEG)
        modelo: Nombre del modelo a usar (InceptionV3, ResNet50, DenseNet)
    """
    try:
        # Validar tipo de archivo
        if not archivo.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
        
        # Validar modelo
        if modelo not in MODELOS:
            raise HTTPException(status_code=400, detail=f"Modelo {modelo} no válido")
        
        # Leer archivo
        contenido = await archivo.read()
        
        # Procesar imagen
        imagen_procesada = procesar_imagen(contenido)
        
        # Cargar modelo
        modelo_cargado = cargar_modelo(modelo)
        
        # Realizar predicción
        prediccion = modelo_cargado.predict(imagen_procesada)[0][0]
        porcentaje = float(prediccion * 100)
        clase = "Normal" if prediccion > 0.5 else "Miopía"
        confianza = float(max(prediccion, 1 - prediccion) * 100)
        
        return {
            "modelo": modelo,
            "prediccion": {
                "clase": clase,
                "porcentaje": round(porcentaje, 2),
                "confianza": round(confianza, 2),
                "probabilidad_miopia": round(prediccion, 4)
            },
            "imagen_info": {
                "nombre": archivo.filename,
                "tamaño": len(contenido),
                "tipo": archivo.content_type
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/health")
async def health_check():
    """Verificar estado del servidor"""
    return {
        "status": "healthy",
        "modelos_disponibles": len(MODELOS),
        "modelos_cargados": len(modelos_cargados)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 