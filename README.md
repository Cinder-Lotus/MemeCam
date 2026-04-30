MemeCam 
MemeCam es un programa interactivo en Python que utiliza Inteligencia Artificial para detectar tus gestos y expresiones faciales en tiempo real, reemplazando tu salida de video con memes dinámicos que reaccionan a lo que haces. ¡Es la herramienta perfecta para bromear con amigos en videollamadas de Discord, Zoom, Google Meet u OBS!

* **Detección en tiempo real:** Utiliza MediaPipe de Google para rastrear los puntos clave de tus manos y tu rostro simultáneamente.
* **Cámara Virtual Integrada:** Envía la salida directamente a cualquier aplicación de videollamadas engañando al sistema operativo.
* **Gestos 
  *  Reposo:
  *  Mano Abierta:
  *  Boca Abierta
  *  Dedo Medio (Fuck you).
  *  Silencio:** Dedo índice posado cerca de los labios.
  *  Pensativo: Dedos de ambas manos unidos como planeando algo.

Requisitos Previos

Para que la cámara virtual funcione correctamente, tu sistema necesita los controladores virtuales instalados:
* **OBS Studio** (La forma más sencilla de obtener los controladores de cámara virtual en Windows/Mac).
* **Python 3.8 a 3.11** (MediaPipe es más estable en estas versiones).

##  Instalación

1. **Clona este repositorio en tu computadora:**
   ```bash
   git clone [https://github.com/TU_USUARIO/MemeCam-Gestos.git](https://github.com/TU_USUARIO/MemeCam-Gestos.git)
   cd MemeCam-Gestos

2. **Crea y activa un entorno virtual (Recomendado para no romper otras librerías):**
   ```bash
   # En Windows
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. **Instala las dependencias necesarias:**
   ```bash
   pip install opencv-python mediapipe==0.10.14 pyvirtualcam numpy
   ```

##  Cómo usarlo

1. Asegúrate de tener tus imágenes personalizadas en la carpeta `assets/` (ej. `reposo.png`, `hamster.png`, `silence.png`).
2. Con tu entorno virtual activado, ejecuta el motor principal:
   ```bash
   python main.py
   ```
3. Se abrirá una ventana de depuración privada solo para ti.
4. Abre Discord (o tu app de preferencia), ve a los ajustes de voz y video, y selecciona **OBS Virtual Camera** como tu cámara principal.
5. ¡Haz gestos a tu cámara física y disfruta las reacciones! Para cerrar el programa, presiona la tecla `q` en la ventana de depuración

Estructura del Código

* `main.py`: Se encarga del flujo de video, la asignación de memes y la conexión con `pyvirtualcam`.
* `gestos.py`: Es el "cerebro" matemático; configura MediaPipe y calcula la posición de los dedos y los labios.
* `assets/`: Carpeta destinada a guardar las imágenes en formato PNG.
