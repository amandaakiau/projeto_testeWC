from ast import stmt
import cv2
from cv2 import CHAIN_APPROX_NONE
#from matplotlib import pyplot as plt
import pytesseract
from bdd import Usuario
#from PIL import Image
# importa conexao com banco
import connection
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert
from datetime import datetime
# para a cor
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import utils
import cv2
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


def imagemwebcam():

    webcam = cv2.VideoCapture(0)

    if webcam.isOpened():
        # print("Conectado")
        # print(webcam.read()) vai retornar uma lista com varios codigos RGB
        validacao, frame = webcam.read()

        while validacao:

            validacao, frame = webcam.read()
            cv2.imshow("Video da Webcam", frame)
            key = cv2.waitKey(5)
            if key == 27:  # ESC
                break

        cv2.imwrite("placawebcam.png", frame)

    webcam.release()
    cv2.destroyAllWindows()


def encontrarRoiPlaca(source):

    imagem = cv2.imread(source)
    cv2.imshow('Placa', imagem)

    placa_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Placa Cinza', placa_cinza)

    _, binarizada = cv2.threshold(placa_cinza, 128, 255, cv2.THRESH_BINARY)
    cv2.imshow('Placa Binarizada', binarizada)

    desfocada = cv2.GaussianBlur(binarizada, (5, 5), 0)
    cv2.imshow('Placa Desfocada', desfocada)

    contornos, hierarquia = cv2.findContours(
        desfocada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #cv2.drawContours(imagem, contornos, -1, (0, 255, 0), 2)
    #cv2.imshow('Contorno Placa', imagem)

    #   https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
    #   https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html

    for c in contornos:

        perimetro = cv2.arcLength(c, True)
        aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)

        if perimetro > 120:  # placa 1 e placa 4 limite do perimetro em pixels para nao detectar nenhum ruído
            # https://www.youtube.com/watch?v=WQeoO7MI0Bs 1:26:30 explica essa parte
            # if perimetro > 500 and perimetro < 800: #placa 2
            # if perimetro > 120 and perimetro < 500: #placa 3

            if len(aprox) == 4:
                # pega esses valores dos contornos feitos
                (x, y, altura, largura) = cv2.boundingRect(c)
                cv2.rectangle(imagem, (x, y), (x+altura,
                                               y+largura), (0, 255, 0), 2)
                roi = imagem[y:y + largura, x:x + altura]
                cv2.imwrite(
                    'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/roiwebcam.jpg', roi)

    # cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                # 0.5, (255, 255, 255), 2)
    cv2.imshow('draw', imagem)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def preProcessamentoRoi():

    img_roi = cv2.imread(
        'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/roiwebcam.jpg')
    cv2.imshow("roi", img_roi)

    img_resize = cv2.resize(img_roi, None, fx=4, fy=4,
                            interpolation=cv2.INTER_CUBIC)
    img_cinza = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)

    _, img_binary = cv2.threshold(img_cinza, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("res", img_binary)

    kernel = np.ones((4, 4), np.uint8)

    img_opening = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, kernel)
    cv2.imshow("res", img_opening)

    cv2.imwrite(
        'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/roi_pbwebcam.jpg', img_opening)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # plt.imshow(th3,'gray')
    # plt.xticks([]),plt.yticks([])
    # plt.show()


def ocrImageRoiPlaca():

    img_roi = cv2.imread(
        'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/roi_pbwebcam.jpg')

    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'

    resultado = pytesseract.image_to_string(
        img_roi, lang='eng', config=config)
    #today = date.today()

    app = connection.get_connection()
    db = SQLAlchemy(app)
    color = descricaoCor()
    u1 = Usuario(
        dt_criacao=datetime.now(),
        cd_placa=resultado,
        ds_cor=color,
        hr_entrada="10",
        hr_saida="12",
        hr_total="1",
        vl_pago="0"
    )

    db.session.add(u1)
    db.session.commit()
    print(resultado)

    #lista_teste = list(Usuario.query)
    # print(lista_teste)


def descricaoCor():

    image = cv2.imread(
        'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/placawebcam.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # extrai informações da altura e largura da imagem
    height, width, _ = np.shape(image)

    plt.figure()
    plt.imshow(image)

    # reshape da imagem para ser uma lista de pixels (uma matriz com linhas = [altura*width] colunas = 3 (rgb)
    image2 = image.reshape((height * width, 3))

    # quantidade de clusters
    clt = KMeans(n_clusters=1)
    clt.fit(image2)

    # cria um histograma de clusters e entao cria uma figura
    # que representa o número de pixels rotulados para cada cor
    hist = utils.centroid_histogram(clt)
    bar = utils.plot_colors(hist, clt.cluster_centers_)

    # mostra a paleta de cores
    plt.figure()
    plt.axis("off")
    plt.imshow(bar)  # imagem da paleta de cores
    plt.show()

    # identifica a cor de um pixel (mesma logica do codigo main)

    hsv_frame = cv2.cvtColor(bar, cv2.COLOR_RGB2HSV)

    height, width, _ = bar.shape

    cx = int((width / 2))
    cy = int((height / 2))

    pixel_center = hsv_frame[cy, cx]
    h_value = pixel_center[0]
    s_value = pixel_center[1]
    v_value = pixel_center[2]

    if (s_value <= 40) and (v_value <= 227):
        color = "PRATA"
    elif v_value <= 43:
        color = "PRETO"
    elif s_value <= 44:
        color = "BRANCO"
    elif (h_value <= 7) or (h_value >= 170):
        color = "VERMELHO"
    elif (h_value >= 8) and (h_value <= 20):
        color = "LARANJA"
    elif (h_value >= 21) and (h_value <= 35):
        color = "AMARELO"
    elif (h_value >= 36) and (h_value <= 84):
        color = "VERDE"
    elif (h_value >= 85) and (h_value <= 133):
        color = "AZUL"
    elif (h_value >= 134) and (h_value <= 148):
        color = "VIOLETA"
    elif (h_value >= 149) and (h_value <= 169):
        color = "ROSA"
    else:
        color = "Nao identificado"

    print(color)
    return(color)


if __name__ == "__main__":

    source = 'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/placawebcam.jpg'

    imagemwebcam()
    encontrarRoiPlaca(source)
    preProcessamentoRoi()
    ocrImageRoiPlaca()
