import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf

# Rutas de los modelos
MODELOS = {
    "InceptionV3": "inceptionv3_v2.h5",
    "ResNet50": "resnet50_v2.h5",
    "DenseNet": "densenet_v2.h5"
}
IMAGE_SIZE = (224, 224)

# Variables globales
imagen_array = None
panel_imagen = None
modelo_actual = None

# Crear ventana principal
ventana = tk.Tk()
ventana.title("MyopiaAI-Class con CNN")
ventana.geometry("600x400")
ventana.resizable(False, False)

# Variable para seleccionar modelo
modelo_seleccionado = tk.StringVar(value="InceptionV3")

# Función para cargar imagen
def cargar_imagen():
    global panel_imagen, imagen_array
    ruta = filedialog.askopenfilename(filetypes=[("Imagen", "*.png *.jpg *.jpeg")])
    if not ruta:
        return

    img = Image.open(ruta).convert('RGB')
    img_resized = img.resize(IMAGE_SIZE)

    # Mostrar imagen
    img_tk = ImageTk.PhotoImage(img_resized)
    if panel_imagen:
        panel_imagen.config(image=img_tk)
        panel_imagen.image = img_tk
    else:
        panel_imagen = tk.Label(frame_derecha, image=img_tk)
        panel_imagen.image = img_tk
        panel_imagen.pack()

    # Procesar imagen
    img_array = np.array(img_resized) / 255.0
    imagen_array = np.expand_dims(img_array, axis=0)

    # Limpiar resultado
    label_resultado.config(text="")

# Función para predecir
def predecir():
    global modelo_actual
    if imagen_array is None:
        label_resultado.config(text="⚠️ Primero sube una imagen.", fg="orange")
        return

    modelo_nombre = modelo_seleccionado.get()
    ruta_modelo = MODELOS[modelo_nombre]

    try:
        modelo_actual = tf.keras.models.load_model(ruta_modelo)
    except Exception as e:
        label_resultado.config(text=f"❌ Error al cargar el modelo {modelo_nombre}", fg="red")
        return

    pred = modelo_actual.predict(imagen_array)[0][0]
    porcentaje = pred * 100
    clase = "Normal" if pred > 0.5 else "Miopía"

    label_resultado.config(
        text=f"{modelo_nombre} → Predicción: {clase} ({porcentaje:.2f}%)",
        fg="green" if clase == "Normal" else "red"
    )

# Estructura de la interfaz
frame_principal = tk.Frame(ventana)
frame_principal.pack(padx=10, pady=10, fill="both", expand=True)

frame_izquierda = tk.Frame(frame_principal)
frame_izquierda.pack(side="left", fill="y", padx=10)

frame_derecha = tk.Frame(frame_principal, width=300, height=300, bg="#f0f0f0")
frame_derecha.pack(side="right", padx=10, pady=10)
frame_derecha.pack_propagate(False)

# Botón para subir imagen
btn_subir = tk.Button(frame_izquierda, text="📁 Subir Imagen", command=cargar_imagen, font=("Arial", 12), width=20)
btn_subir.pack(pady=10)

# Selección del modelo
frame_modelos = tk.LabelFrame(frame_izquierda, text="Selecciona el modelo", font=("Arial", 12))
frame_modelos.pack(pady=10, fill="x")

for nombre_modelo in MODELOS:
    tk.Radiobutton(
        frame_modelos,
        text=nombre_modelo,
        variable=modelo_seleccionado,
        value=nombre_modelo,
        font=("Arial", 11)
    ).pack(anchor="w", padx=10, pady=2)

# Botón de predicción
btn_predecir = tk.Button(frame_izquierda, text="🔍 Clasificar", command=predecir, font=("Arial", 12), width=20)
btn_predecir.pack(pady=20)

# Frame para el resultado al final de la ventana
frame_inferior = tk.Frame(ventana)
frame_inferior.pack(side="bottom", pady=10)

# Resultado en la parte inferior de toda la ventana
label_resultado = tk.Label(frame_inferior, text="", font=("Arial", 14))
label_resultado.pack()

# Ejecutar ventana
ventana.mainloop()
