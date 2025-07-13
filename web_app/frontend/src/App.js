import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { 
  Upload, 
  Eye, 
  Brain, 
  Sun, 
  Moon, 
  AlertCircle, 
  CheckCircle, 
  XCircle,
  Loader2
} from 'lucide-react';
import './App.css';

function App() {
  const [imagen, setImagen] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [resultado, setResultado] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState(null);
  const [modeloSeleccionado, setModeloSeleccionado] = useState('InceptionV3');
  const [modoOscuro, setModoOscuro] = useState(false);
  const [modelosDisponibles, setModelosDisponibles] = useState([]);

  // Modelos disponibles
  const modelos = ['InceptionV3', 'ResNet50', 'DenseNet'];

  // Colores para modo claro y oscuro
  const colores = {
    claro: {
      bg: '#ffffff',
      bgSecundario: '#f8f9fa',
      texto: '#212529',
      textoSecundario: '#6c757d',
      borde: '#dee2e6',
      boton: '#007bff',
      botonHover: '#0056b3',
      exito: '#28a745',
      error: '#dc3545',
      advertencia: '#ffc107'
    },
    oscuro: {
      bg: '#1a1a1a',
      bgSecundario: '#2d2d2d',
      texto: '#ffffff',
      textoSecundario: '#b0b0b0',
      borde: '#404040',
      boton: '#0d6efd',
      botonHover: '#0b5ed7',
      exito: '#198754',
      error: '#dc3545',
      advertencia: '#ffc107'
    }
  };

  const temaActual = modoOscuro ? colores.oscuro : colores.claro;

  // Configurar dropzone para subir archivos
  const onDrop = useCallback((acceptedFiles) => {
    const archivo = acceptedFiles[0];
    if (archivo) {
      setImagen(archivo);
      setPreviewUrl(URL.createObjectURL(archivo));
      setResultado(null);
      setError(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    multiple: false
  });

  // Función para cambiar tema
  const cambiarTema = () => {
    setModoOscuro(!modoOscuro);
  };

  // Función para predecir
  const predecir = async () => {
    if (!imagen) {
      setError('Por favor, sube una imagen primero.');
      return;
    }

    setCargando(true);
    setError(null);
    setResultado(null);

    try {
      const formData = new FormData();
      formData.append('archivo', imagen);
      formData.append('modelo', modeloSeleccionado);

      const response = await axios.post('/predecir', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResultado(response.data);
    } catch (err) {
      console.error('Error en predicción:', err);
      setError(err.response?.data?.detail || 'Error al procesar la imagen');
    } finally {
      setCargando(false);
    }
  };

  // Función para limpiar
  const limpiar = () => {
    setImagen(null);
    setPreviewUrl(null);
    setResultado(null);
    setError(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
  };

  return (
    <div className="App" style={{ backgroundColor: temaActual.bg, color: temaActual.texto }}>
      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <div className="logo">
              <Eye size={32} color={temaActual.boton} />
              <h1>MyopiaAI</h1>
            </div>
            <button 
              className="tema-btn"
              onClick={cambiarTema}
              style={{ 
                backgroundColor: temaActual.bgSecundario,
                color: temaActual.texto,
                border: `1px solid ${temaActual.borde}`
              }}
            >
              {modoOscuro ? <Sun size={20} /> : <Moon size={20} />}
              {modoOscuro ? ' Modo Claro' : ' Modo Oscuro'}
            </button>
          </div>
        </header>

        {/* Contenido principal */}
        <main className="main-content">
          <div className="content-grid">
            {/* Panel izquierdo - Controles */}
            <div className="control-panel" style={{ backgroundColor: temaActual.bgSecundario }}>
              <h2>Configuración</h2>
              
              {/* Subir imagen */}
              <div className="upload-section">
                <h3>Subir Imagen</h3>
                <div 
                  {...getRootProps()} 
                  className={`dropzone ${isDragActive ? 'active' : ''}`}
                  style={{ 
                    border: `2px dashed ${temaActual.borde}`,
                    backgroundColor: temaActual.bg
                  }}
                >
                  <input {...getInputProps()} />
                  <Upload size={48} color={temaActual.textoSecundario} />
                  <p style={{ color: temaActual.textoSecundario }}>
                    {isDragActive
                      ? 'Suelta la imagen aquí...'
                      : 'Arrastra una imagen aquí, o haz clic para seleccionar'}
                  </p>
                </div>
              </div>

              {/* Selección de modelo */}
              <div className="model-section">
                <h3>Seleccionar Modelo</h3>
                <div className="model-options">
                  {modelos.map((modelo) => (
                    <label key={modelo} className="model-option">
                      <input
                        type="radio"
                        name="modelo"
                        value={modelo}
                        checked={modeloSeleccionado === modelo}
                        onChange={(e) => setModeloSeleccionado(e.target.value)}
                      />
                      <Brain size={16} />
                      <span>{modelo}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Botones de acción */}
              <div className="action-buttons">
                <button
                  className="btn btn-primary"
                  onClick={predecir}
                  disabled={!imagen || cargando}
                  style={{ 
                    backgroundColor: temaActual.boton,
                    color: '#ffffff'
                  }}
                >
                  {cargando ? (
                    <>
                      <Loader2 size={16} className="spinner" />
                      Procesando...
                    </>
                  ) : (
                    <>
                      <Eye size={16} />
                      Clasificar
                    </>
                  )}
                </button>
                
                <button
                  className="btn btn-secondary"
                  onClick={limpiar}
                  disabled={!imagen}
                  style={{ 
                    backgroundColor: temaActual.bgSecundario,
                    color: temaActual.texto,
                    border: `1px solid ${temaActual.borde}`
                  }}
                >
                  Limpiar
                </button>
              </div>
            </div>

            {/* Panel derecho - Visualización */}
            <div className="visualization-panel" style={{ backgroundColor: temaActual.bgSecundario }}>
              <h2>Visualización</h2>
              
              {/* Preview de imagen */}
              {previewUrl && (
                <div className="image-preview">
                  <img src={previewUrl} alt="Preview" />
                </div>
              )}

              {/* Resultados */}
              {resultado && (
                <div className="results">
                  <h3>Resultados</h3>
                  <div className="result-card">
                    <div className="result-header">
                      <Brain size={20} />
                      <span>Modelo: {resultado.modelo}</span>
                    </div>
                    
                    <div className="result-content">
                      <div className={`result-badge ${resultado.prediccion.clase === 'Normal' ? 'success' : 'error'}`}>
                        {resultado.prediccion.clase === 'Normal' ? (
                          <CheckCircle size={20} />
                        ) : (
                          <XCircle size={20} />
                        )}
                        <span>{resultado.prediccion.clase}</span>
                      </div>
                      
                      <div className="result-stats">
                        <div className="stat">
                          <span>Probabilidad:</span>
                          <span className="stat-value">{resultado.prediccion.porcentaje}%</span>
                        </div>
                        <div className="stat">
                          <span>Confianza:</span>
                          <span className="stat-value">{resultado.prediccion.confianza}%</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Mensajes de error */}
              {error && (
                <div className="error-message">
                  <AlertCircle size={20} />
                  <span>{error}</span>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App; 