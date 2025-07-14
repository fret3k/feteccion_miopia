# MyopiaAI - Detección de Miopía con FastAPI y React

Aplicación web para la detección de miopía en imágenes de ojos usando modelos de deep learning. El sistema permite a los usuarios subir imágenes, seleccionar el modelo de IA y obtener una predicción de forma rápida y sencilla desde cualquier navegador.

---

## 🏗️ Arquitectura

- **Backend:** FastAPI (Python)  
  API REST para el procesamiento de imágenes y la inferencia de modelos de deep learning (TensorFlow/Keras).
- **Frontend:** React (JavaScript)  
  Interfaz de usuario moderna, responsive y con modo oscuro/claro.
- **Modelos:** TensorFlow/Keras  
  Modelos preentrenados en formato `.h5` (InceptionV3, ResNet50, DenseNet).

---

## 📁 Estructura del Proyecto

```
Deteccion_Miopia/
│
├── backend/
│   ├── main.py                # Servidor FastAPI
│   ├── requirements.txt       # Dependencias Python
│   ├── Dockerfile             # (Opcional) Para despliegue en contenedores
│   └── *.h5                   # Modelos de deep learning
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
│
├── .gitignore
├── README.md
├── start_backend.bat
├── start_frontend.bat
└── start_all.bat
```

---

## 🚀 Instalación y Ejecución

### 1. Clona el repositorio

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd Deteccion_Miopia
```

### 2. Ignora la carpeta `version_final`

Asegúrate de que en `.gitignore` esté la línea:
```
version_final/
```

### 3. Backend (FastAPI)

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt

# Copia los modelos .h5 al directorio backend si no están allí
cp ../*.h5 .

# Ejecuta el servidor
python main.py
```
El backend estará disponible en: [http://localhost:8000](http://localhost:8000)

### 4. Frontend (React)

```bash
cd ../frontend
npm install
npm start
```
El frontend estará disponible en: [http://localhost:3000](http://localhost:3000)

### 5. Scripts de inicio rápido (Windows)

- `start_backend.bat` — Inicia solo el backend
- `start_frontend.bat` — Inicia solo el frontend
- `start_all.bat` — Inicia ambos en ventanas separadas

---

## 📡 Endpoints de la API

- `GET /`  
  Mensaje de bienvenida.
- `GET /modelos`  
  Lista de modelos disponibles y tamaño de imagen requerido.
- `POST /predecir`  
  **Parámetros:**  
  - `archivo`: Imagen (PNG, JPG, JPEG)  
  - `modelo`: Nombre del modelo (`InceptionV3`, `ResNet50`, `DenseNet`)  
  **Respuesta:**  
  ```json
  {
    "modelo": "InceptionV3",
    "prediccion": {
      "clase": "Normal",
      "porcentaje": 87.23,
      "confianza": 87.23,
      "probabilidad_miopia": 0.8723
    },
    "imagen_info": {
      "nombre": "ojo.jpg",
      "tamaño": 123456,
      "tipo": "image/jpeg"
    }
  }
  ```
- `GET /health`  
  Estado del servidor y modelos cargados.

- **Documentación interactiva:**  
  [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🎨 Características del Frontend

- Interfaz moderna y responsive
- Modo oscuro/claro
- Subida de imágenes por drag & drop
- Selección de modelo de IA
- Visualización de resultados y confianza
- Mensajes de error amigables

---

## 🛠️ Desarrollo y Despliegue

### Backend

- **Desarrollo:**  
  `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- **Producción:**  
  `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`
- **Docker:**  
  Construye y ejecuta el backend con Docker usando el `Dockerfile` incluido.

### Frontend

- **Desarrollo:**  
  `npm start`
- **Producción:**  
  `npm run build` y sirve los archivos estáticos con Nginx, Apache, etc.

---

## 🔒 Seguridad

- CORS configurado para permitir solo el frontend local
- Validación de archivos y modelos
- Manejo robusto de errores

---

## 🤝 Contribución

1. Haz un fork del proyecto
2. Crea una rama (`git checkout -b feature/NuevaFeature`)
3. Realiza tus cambios y haz commit (`git commit -m 'Agrega nueva feature'`)
4. Haz push a tu rama (`git push origin feature/NuevaFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

---

## 🆘 Soporte

- Abre un issue en GitHub para soporte o sugerencias
- Contacta al equipo de desarrollo para dudas técnicas

---

## 📢 Notas

- La carpeta `version_final/` está ignorada y no se sube a GitHub.
- Los modelos `.h5` deben estar en el directorio `backend/` para funcionar correctamente.
- Si tienes dudas sobre el despliegue, revisa la documentación o abre un issue.

---

¡Listo! Así tienes una documentación profesional y completa para tu proyecto.  
¿Quieres que la guarde directamente en tu archivo `README.md`?