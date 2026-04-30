import mediapipe as mp
import math

class DetectorGestos:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
        
        self.mp_hands = mp.solutions.hands
        # ¡CAMBIO IMPORTANTE! max_num_hands ahora es 2 para el gesto pensativo
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

    def detectar(self, frame_rgb):
        estado = "reposo"
        
        # Procesamos rostro y manos al mismo tiempo
        resultados_rostro = self.face_mesh.process(frame_rgb)
        resultados_manos = self.hands.process(frame_rgb)
        
        rostro = None
        if resultados_rostro.multi_face_landmarks:
            rostro = resultados_rostro.multi_face_landmarks[0]

        if resultados_manos.multi_hand_landmarks:
            manos = resultados_manos.multi_hand_landmarks
            
            # --- 1. GESTO PENSATIVO (Requiere 2 manos) ---
            if len(manos) == 2:
                mano1 = manos[0]
                mano2 = manos[1]
                
                # Distancia entre la punta de los dedos índices de ambas manos
                dist_indices = math.hypot(mano1.landmark[8].x - mano2.landmark[8].x, mano1.landmark[8].y - mano2.landmark[8].y)
                # Distancia entre la punta de los dedos medios
                dist_medios = math.hypot(mano1.landmark[12].x - mano2.landmark[12].x, mano1.landmark[12].y - mano2.landmark[12].y)
                
                # Si las puntas de los dedos están cerca (< 0.1), están unidos como planeando algo
                if dist_indices < 0.1 and dist_medios < 0.1:
                    return "pensativo"

            # --- 2. GESTOS DE UNA SOLA MANO ---
            # Usamos la primera mano detectada para estos gestos
            mano = manos[0]
            
            # Saber qué dedos están arriba (Y del nudillo mayor a Y de la punta)
            indice_arriba = mano.landmark[8].y < mano.landmark[6].y
            medio_arriba = mano.landmark[12].y < mano.landmark[10].y
            anular_arriba = mano.landmark[16].y < mano.landmark[14].y
            menique_arriba = mano.landmark[20].y < mano.landmark[18].y
            
            # Gesto: Fuck You (Solo el medio arriba)
            if not indice_arriba and medio_arriba and not anular_arriba and not menique_arriba:
                return "fuck_you"
                
            # Gesto: Silencio (Solo el índice arriba y cerca de la boca)
            if indice_arriba and not medio_arriba and not anular_arriba and not menique_arriba:
                if rostro:
                    labio = rostro.landmark[13] # Punto superior del labio
                    punta_indice = mano.landmark[8]
                    # Calculamos distancia entre el dedo índice y el labio
                    dist_boca = math.hypot(labio.x - punta_indice.x, labio.y - punta_indice.y)
                    
                    if dist_boca < 0.15: # Umbral de cercanía a la cara
                        return "silence"
            
            # Gesto: Paz (Índice y medio arriba)
            if indice_arriba and medio_arriba and not anular_arriba and not menique_arriba:
                return "paz"
                
            # Gesto: Mano Abierta (Todos arriba)
            elif indice_arriba and medio_arriba and anular_arriba and menique_arriba:
                return "mano_abierta"

        # --- 3. GESTOS DE ROSTRO (Si no hay manos detectadas o haciendo acciones) ---
        if rostro:
            labio_sup = rostro.landmark[13]
            labio_inf = rostro.landmark[14]
            distancia_boca = math.hypot(labio_sup.x - labio_inf.x, labio_sup.y - labio_inf.y)
            
            if distancia_boca > 0.05: 
                estado = "boca_abierta"

        return estado