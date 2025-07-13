# MyopiaAI - Aplicación Web

Aplicación web para detección de miopía usando inteligencia artificial con FastAPI y React.

## 🏗️ Arquitectura

- **Backend**: FastAPI (Python) - API REST para procesamiento de imágenes
- **Frontend**: React (JavaScript) - Interfaz de usuario moderna
- **ML Models**: TensorFlow/Keras - Modelos de deep learning

## 📁 Estructura del Proyecto

```
web_app/
├── backend/
│   ├── main.py              # Servidor FastAPI
│   └── requirements.txt     # Dependencias Python
├── frontend/
│   ├── public/
│   │   └── index.html       # HTML principal
│   ├── src/
│   │   ├── App.js           # Componente principal React
│   │   ├── App.css          # Estilos CSS
│   │   ├── index.js         # Punto de entrada React
│   │   └── index.css        # Estilos globales
│   └── package.json         # Dependencias Node.js
└── README.md               # Esta documentación
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- Node.js 16+
- npm o yarn

### Backend (FastAPI)

1. **Navegar al directorio backend:**
   ```bash
   cd web_app/backend
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Copiar modelos:**
   ```bash
   # Copiar los archivos .h5 desde el directorio raíz
   cp ../../*.h5 .
   ```

6. **Ejecutar servidor:**
   ```bash
   python main.py
   ```

El backend estará disponible en: `http://localhost:8000`

### Frontend (React)

1. **Navegar al directorio frontend:**
   ```bash
   cd web_app/frontend
   ```

2. **Instalar dependencias:**
   ```bash
   npm install
   ```

3. **Ejecutar aplicación:**
   ```bash
   npm start
   ```

El frontend estará disponible en: `http://localhost:3000`

## 🔧 Configuración

### Variables de Entorno

Crear archivo `.env` en el directorio backend:

```env
# Configuración del servidor
HOST=0.0.0.0
PORT=8000

# Configuración CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Configuración de modelos
MODELS_DIR=.
```

### Modelos de Machine Learning

Los modelos deben estar en formato `.h5` y ubicarse en el directorio `backend/`:

- `inceptionv3_v2.h5`
- `resnet50_v2.h5`
- `densenet_v2.h5`

## 📡 API Endpoints

### GET `/`
- **Descripción**: Endpoint raíz
- **Respuesta**: Mensaje de bienvenida

### GET `/modelos`
- **Descripción**: Obtiene lista de modelos disponibles
- **Respuesta**: Lista de modelos y configuración

### POST `/predecir`
- **Descripción**: Predice miopía en una imagen
- **Parámetros**:
  - `archivo`: Imagen (PNG, JPG, JPEG)
  - `modelo`: Nombre del modelo (InceptionV3, ResNet50, DenseNet)
- **Respuesta**: Resultado de la predicción

### GET `/health`
- **Descripción**: Verificar estado del servidor
- **Respuesta**: Estado de salud y modelos cargados

## 🎨 Características del Frontend

- **Interfaz moderna**: Diseño responsive con CSS Grid
- **Modo oscuro/claro**: Cambio de tema dinámico
- **Drag & Drop**: Subida de archivos intuitiva
- **Preview de imagen**: Visualización antes del procesamiento
- **Resultados detallados**: Información completa de predicción
- **Responsive**: Compatible con móviles y tablets

## 🔍 Uso de la Aplicación

1. **Abrir la aplicación** en `http://localhost:3000`
2. **Subir una imagen** arrastrando o haciendo clic en el área de subida
3. **Seleccionar modelo** de la lista disponible
4. **Hacer clic en "Clasificar"** para procesar la imagen
5. **Ver resultados** en el panel derecho
6. **Cambiar tema** usando el botón en el header

## 🛠️ Desarrollo

### Backend

```bash
# Ejecutar con recarga automática
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Documentación automática
# Disponible en: http://localhost:8000/docs
```

### Frontend

```bash
# Modo desarrollo
npm start

# Construir para producción
npm run build

# Ejecutar tests
npm test
```

## 🚀 Despliegue

### Backend (Producción)

```bash
# Usando Gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Usando Docker
docker build -t myopiaai-backend .
docker run -p 8000:8000 myopiaai-backend
```

### Frontend (Producción)

```bash
# Construir
npm run build

# Servir con nginx o similar
# Los archivos estarán en build/
```

## 📊 Monitoreo

- **Logs**: Los logs se muestran en la consola del backend
- **Health Check**: Endpoint `/health` para monitoreo
- **Documentación**: Swagger UI en `/docs`

## 🔒 Seguridad

- **CORS**: Configurado para permitir solo orígenes específicos
- **Validación**: Validación de tipos de archivo
- **Error Handling**: Manejo robusto de errores

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 🆘 Soporte

Para soporte técnico o preguntas:
- Crear un issue en el repositorio
- Contactar al equipo de desarrollo

## 🔄 Actualizaciones

### v1.0.0
- ✅ Backend FastAPI funcional
- ✅ Frontend React con UI moderna
- ✅ Integración completa
- ✅ Documentación completa 