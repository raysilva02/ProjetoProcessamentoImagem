import cv2
import numpy as np

#modelos de rosto e nariz
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
nose_cascade = cv2.CascadeClassifier('nose.xml')

#capturar a webcam
cap = cv2.VideoCapture(0)

drawing = False  #desenho ativo/desativo
last_nose_position = None  #posição do nariz

#camada translucida para o desenho
draw_layer = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if draw_layer is None:
        draw_layer = np.zeros_like(frame)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) #reconhece o rosto
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        
        noses = nose_cascade.detectMultiScale(roi_gray, 1.3, 5) #reconhece o nariz
        
        if len(noses) > 0:
            (nx, ny, nw, nh) = noses[0]
            nose_center = (x + nx + nw // 2, y + ny + nh // 2)
            cv2.circle(frame, nose_center, 5, (0, 0, 255), -1)
            
            if drawing: #desenhando
                if last_nose_position:
                    cv2.line(draw_layer, last_nose_position, nose_center, (0, 0, 255), 4)
                last_nose_position = nose_center
        else:
            last_nose_position = None
    
    #combinando o desenho com a tela
    combined_frame = cv2.add(draw_layer, frame)
    
    #exibindo os comandos para o usuário
    cv2.putText(combined_frame, "Pressione 'd' para ativar/desativar o desenho", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(combined_frame, "Pressione 'c' para limpar o desenho", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(combined_frame, "Pressione 'q' para sair", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    #desenho na tela
    cv2.imshow('Nose Brush', combined_frame)
    
    #comandos
    key = cv2.waitKey(1)
    if key == ord('d'):
        drawing = not drawing
        if not drawing:
            last_nose_position = None  
    elif key == ord('c'):
        draw_layer = np.zeros_like(frame)
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
