import cv2
import numpy as np
import pyvirtualcam
from gestos import DetectorGestos

# Configuración de resolución (típica de webcams)
WIDTH, HEIGHT = 640, 480

def cargar_meme(ruta):
    """Carga la imagen, la redimensiona y la convierte al formato correcto."""
    img = cv2.imread(ruta)
    if img is None:
        # Si no encuentra la imagen, crea un fondo negro con texto de error
        img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        cv2.putText(img, f"Falta {ruta}", (20, HEIGHT//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    else:
        img = cv2.resize(img, (WIDTH, HEIGHT))
        
    # PyVirtualCam requiere formato RGB, pero OpenCV usa BGR. Lo convertimos.
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def main():
    # 1. Cargar las imágenes de salida (los memes)
    print("Cargando imágenes...")
    memes = {
        "reposo": cargar_meme("assets/reposo.png"),
        "mano_abierta": cargar_meme("assets/mano_abierta.png"),
        "boca_abierta": cargar_meme("assets/boca_abierta.png"),
        "paz": cargar_meme("assets/paz.png"),
        "fuck_you": cargar_meme("assets/fuck_you.png"),
        "silence": cargar_meme("assets/silence.png"),
        "pensativo": cargar_meme("assets/pensativo.png")
    }

    # 2. Inicializar tu cámara física y el detector
    print("Iniciando cámara física...")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    detector = DetectorGestos()

    # 3. Iniciar la cámara virtual
    print("Conectando con la cámara virtual...")
    with pyvirtualcam.Camera(width=WIDTH, height=HEIGHT, fps=30) as cam_virtual:
        print(f'¡Éxito! Cámara virtual iniciada: {cam_virtual.device}')
        print("Presiona la tecla 'q' en la ventana de depuración para salir.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Actuar como espejo (más natural) y convertir colores para MediaPipe
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 4. Procesar el frame y obtener qué gesto estás haciendo
            estado = detector.detectar(frame_rgb)

            # 5. Seleccionar la imagen correspondiente del diccionario
            imagen_salida = memes[estado]

            # 6. Enviar el meme a Discord/Meet a través de la cámara virtual
            cam_virtual.send(imagen_salida)
            cam_virtual.sleep_until_next_frame()

            # 7. Mostrar tu ventana privada de control (Debug)
            # Esto es solo para ti, nadie en la videollamada lo verá
            cv2.putText(frame, f"Estado actual: {estado}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("MemeCam - Tu Vista Privada", frame)
            
            # Salir si presionas la letra 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Limpiar todo al cerrar
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()