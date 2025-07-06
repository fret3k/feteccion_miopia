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
modo_oscuro = False

# Definir esquemas de colores
COLORES_CLARO = {
    "bg_principal": "#ffffff",
    "bg_secundario": "#f0f0f0",
    "bg_frame": "#ffffff",
    "fg_principal": "#000000",
    "fg_secundario": "#333333",
    "btn_bg": "#e0e0e0",
    "btn_fg": "#000000",
    "btn_active": "#d0d0d0",
    "resultado_normal": "#28a745",
    "resultado_miopia": "#dc3545",
    "resultado_advertencia": "#ffc107"
}

COLORES_OSCURO = {
    "bg_principal": "#2d2d2d",
    "bg_secundario": "#3d3d3d",
    "bg_frame": "#2d2d2d",
    "fg_principal": "#ffffff",
    "fg_secundario": "#cccccc",
    "btn_bg": "#4d4d4d",
    "btn_fg": "#ffffff",
    "btn_active": "#5d5d5d",
    "resultado_normal": "#28a745",
    "resultado_miopia": "#dc3545",
    "resultado_advertencia": "#ffc107"
}

# Crear ventana principal
ventana = tk.Tk()
ventana.title("MyopiaAI-Class con CNN")
ventana.geometry("600x400")
ventana.resizable(False, False)

# Variable para seleccionar modelo
modelo_seleccionado = tk.StringVar(value="InceptionV3")

# Función para cambiar tema
def cambiar_tema():
    global modo_oscuro
    modo_oscuro = not modo_oscuro
    aplicar_tema()
    
    # Actualizar texto del botón
    if modo_oscuro:
        btn_tema.config(text="☀️ Modo Claro")
    else:
        btn_tema.config(text="🌙 Modo Oscuro")

# Función para aplicar tema
def aplicar_tema():
    colores = COLORES_OSCURO if modo_oscuro else COLORES_CLARO
    
    # Aplicar colores a la ventana principal
    ventana.configure(bg=colores["bg_principal"])
    
    # Aplicar colores a los frames
    frame_principal.configure(bg=colores["bg_principal"])
    frame_izquierda.configure(bg=colores["bg_principal"])
    frame_derecha.configure(bg=colores["bg_secundario"])
    frame_inferior.configure(bg=colores["bg_principal"])
    
    # Aplicar colores a los botones
    btn_subir.configure(
        bg=colores["btn_bg"],
        fg=colores["btn_fg"],
        activebackground=colores["btn_active"],
        activeforeground=colores["btn_fg"]
    )
    btn_predecir.configure(
        bg=colores["btn_bg"],
        fg=colores["btn_fg"],
        activebackground=colores["btn_active"],
        activeforeground=colores["btn_fg"]
    )
    btn_tema.configure(
        bg=colores["btn_bg"],
        fg=colores["btn_fg"],
        activebackground=colores["btn_active"],
        activeforeground=colores["btn_fg"]
    )
    
    # Aplicar colores al frame de modelos
    frame_modelos.configure(
        bg=colores["bg_frame"],
        fg=colores["fg_principal"]
    )
    
    # Aplicar colores a los radiobuttons
    for widget in frame_modelos.winfo_children():
        if isinstance(widget, tk.Radiobutton):
            widget.configure(
                bg=colores["bg_frame"],
                fg=colores["fg_principal"],
                selectcolor=colores["bg_secundario"],
                activebackground=colores["bg_frame"],
                activeforeground=colores["fg_principal"]
            )
    
    # Aplicar colores al label de resultado
    label_resultado.configure(
        bg=colores["bg_principal"],
        fg=colores["fg_principal"]
    )

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
        colores = COLORES_OSCURO if modo_oscuro else COLORES_CLARO
        label_resultado.config(text="⚠️ Primero sube una imagen.", fg=colores["resultado_advertencia"])
        return

    modelo_nombre = modelo_seleccionado.get()
    ruta_modelo = MODELOS[modelo_nombre]

    try:
        modelo_actual = tf.keras.models.load_model(ruta_modelo)
    except Exception as e:
        colores = COLORES_OSCURO if modo_oscuro else COLORES_CLARO
        label_resultado.config(text=f"❌ Error al cargar el modelo {modelo_nombre}", fg=colores["resultado_miopia"])
        return

    pred = modelo_actual.predict(imagen_array)[0][0]
    porcentaje = pred * 100
    clase = "Normal" if pred > 0.5 else "Miopía"

    colores = COLORES_OSCURO if modo_oscuro else COLORES_CLARO
    color_resultado = colores["resultado_normal"] if clase == "Normal" else colores["resultado_miopia"]
    
    label_resultado.config(
        text=f"{modelo_nombre} → Predicción: {clase} ({porcentaje:.2f}%)",
        fg=color_resultado
    )

# Estructura de la interfaz
frame_principal = tk.Frame(ventana)
frame_principal.pack(padx=10, pady=10, fill="both", expand=True)

frame_izquierda = tk.Frame(frame_principal)
frame_izquierda.pack(side="left", fill="y", padx=10)

frame_derecha = tk.Frame(frame_principal, width=300, height=300)
frame_derecha.pack(side="right", padx=10, pady=10)
frame_derecha.pack_propagate(False)

# Botón para cambiar tema (en la parte superior)
btn_tema = tk.Button(frame_izquierda, text="🌙 Modo Oscuro", command=cambiar_tema, font=("Arial", 10), width=15)
btn_tema.pack(pady=(0, 10))

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

# Aplicar tema inicial
aplicar_tema()

# Ejecutar ventana
ventana.mainloop()
