import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R  # Importa Rotation

# Información del autor y asesor
st.title("Simulación de movimientos en SO(2) y SO(3)")
st.markdown("Autor: Vérochka J. Chero Reque")
st.markdown("Asesor: Mg. Oscar Santamaría Santisteban")

# Selección del movimiento
st.sidebar.title("Configuración")
movement = st.sidebar.radio(
    "Selecciona el movimiento:",
    ("Desviación radial", "Desviación cubital", "Flexión", "Extensión", "Circunducción", "SO(3) General")
)

# Límites de los movimientos (AAOS)
limits = {
    "Desviación radial": (-20, 0),  # Negativos para radial
    "Desviación cubital": (0, 30),  # Positivos para cubital
    "Flexión": (0, 80),             # Positivos para flexión
    "Extensión": (-70, 0)           # Negativos para extensión
}

# Función para graficar en SO(2)
def plot_so2(angle, title):
    fig, ax = plt.subplots()
    origin = np.array([0, 0])
    radians = np.radians(angle)
    axis = np.array([np.cos(radians), np.sin(radians)])
    
    ax.quiver(*origin, *axis, color='b', angles='xy', scale_units='xy', scale=1, label=f"Ángulo: {angle}°")
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True)
    ax.legend()
    ax.set_title(title)
    st.pyplot(fig)

# Función para mostrar la matriz de rotación SO(2)
def show_so2_matrix(angle):
    radians = np.radians(angle)
    rotation_matrix = np.array([
        [np.cos(radians), -np.sin(radians)],
        [np.sin(radians),  np.cos(radians)]
    ])
    st.subheader("Matriz de Rotación SO(2):")
    st.write(rotation_matrix)

if movement in ["Desviación radial", "Desviación cubital", "Flexión", "Extensión"]:
    st.header(f"Movimiento: {movement}")
    st.write(f"Límite (AAOS): {limits[movement][0]}° a {limits[movement][1]}°")

    # Seleccionar el ángulo dentro de los límites
    angle = st.slider(f"Ángulo para {movement}", *limits[movement], value=limits[movement][0])
    plot_so2(angle, f"Movimiento: {movement}")
    show_so2_matrix(angle)  # Mostrar la matriz de rotación

elif movement == "Circunducción":
    st.header("Circunducción en \(\\mathbb{R}^2\)")
    radius = st.slider("Radio de la circunducción", min_value=0.1, max_value=1.5, value=1.0, step=0.1)
    steps = st.slider("Número de pasos", min_value=10, max_value=100, value=50)

    theta = np.linspace(0, 2 * np.pi, steps)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    fig, ax = plt.subplots()
    ax.plot(x, y, label="Trayectoria circular", color='b')
    ax.scatter([0], [0], color='r', label="Centro")
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True)
    ax.legend()
    ax.set_title("Circunducción en \(\\mathbb{R}^2\)")
    st.pyplot(fig)

elif movement == "SO(3) General":
    st.header("Rotaciones en SO(3)")
    x_angle = st.slider("Ángulo de rotación en X (grados)", min_value=-180, max_value=180, value=0)
    y_angle = st.slider("Ángulo de rotación en Y (grados)", min_value=-180, max_value=180, value=0)
    z_angle = st.slider("Ángulo de rotación en Z (grados)", min_value=-180, max_value=180, value=0)

    r = R.from_euler('xyz', [x_angle, y_angle, z_angle], degrees=True)
    rotation_matrix_3d = r.as_matrix()

    st.subheader("Matriz de Rotación SO(3):")
    st.write(rotation_matrix_3d)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    origin = np.array([0, 0, 0])
    x_axis = rotation_matrix_3d @ np.array([1, 0, 0])
    y_axis = rotation_matrix_3d @ np.array([0, 1, 0])
    z_axis = rotation_matrix_3d @ np.array([0, 0, 1])

    ax.quiver(*origin, *x_axis, color='r', label='Eje X')
    ax.quiver(*origin, *y_axis, color='g', label='Eje Y')
    ax.quiver(*origin, *z_axis, color='b', label='Eje Z')
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-1.5, 1.5])
    ax.set_xlabel('X', labelpad=10)
    ax.set_ylabel('Y', labelpad=10)
    ax.set_zlabel('Z', labelpad=10)
    ax.view_init(elev=20, azim=45)
    ax.legend()
    st.pyplot(fig)
