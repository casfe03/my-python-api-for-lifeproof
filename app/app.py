from flask import Flask, request, render_template, jsonify
import cv2
import dlib
import numpy as np

app = Flask(__name__)

def compare_faces(image1, image2, threshold=0.6):
    # Inicializa o detector de faces do dlib e o alinhador de faces
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    # Converte as imagens para escala de cinza
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Detecta as faces nas duas imagens
    rects1 = detector(gray1, 1)
    rects2 = detector(gray2, 1)

    # Verifica se foi detectada apenas uma face em cada imagem
    if len(rects1) != 1 or len(rects2) != 1:
        return False, None

    # Obtém os pontos faciais das duas faces
    shape1 = predictor(gray1, rects1[0])
    shape2 = predictor(gray2, rects2[0])

    # Extrai as coordenadas dos pontos faciais
    landmarks1 = np.array([[shape1.part(i).x, shape1.part(i).y] for i in range(68)], dtype=np.int32)
    landmarks2 = np.array([[shape2.part(i).x, shape2.part(i).y] for i in range(68)], dtype=np.int32)

    # Calcula a distância euclidiana entre os pontos faciais
    distances = np.sqrt(np.sum((landmarks1 - landmarks2) ** 2, axis=1))

    # Calcula a similaridade normalizada
    similarity = np.mean(distances)

    # Verifica se a similaridade está abaixo do limite
    if similarity < threshold:
        return True, similarity
    else:
        return False, similarity

@app.route('/', methods=['GET', 'POST'])
def upload_images():
    if request.method == 'POST':
        # Obtém as imagens enviadas pelo usuário
        cnh_image = request.files['cnh_image']
        face_image = request.files['face_image']

        # Carrega as imagens usando o OpenCV
        cnh_cv_image = cv2.imdecode(np.frombuffer(cnh_image.read(), np.uint8), cv2.IMREAD_COLOR)
        face_cv_image = cv2.imdecode(np.frombuffer(face_image.read(), np.uint8), cv2.IMREAD_COLOR)

        # Realiza a comparação de rostos
        faces_match, similarity = compare_faces(cnh_cv_image, face_cv_image)

        # Retorna o resultado como uma resposta JSON
        return jsonify({'faces_match': faces_match, 'similarity': similarity})

    return render_template('upload.html')

if __name__ == '__main__':
    app.run()
