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
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


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

        # if perimetro > 120:  # placa 1 e placa 4
        # if perimetro > 500 and perimetro < 800: #placa 2
        if perimetro > 120 and perimetro < 500:  # placa 3

            aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)

            if len(aprox) == 4:
                # pega esses valores dos contornos feitos
                (x, y, altura, largura) = cv2.boundingRect(c)
                cv2.rectangle(imagem, (x, y), (x+altura,
                                               y+largura), (0, 255, 0), 2)
                roi = imagem[y:y + largura, x:x + altura]
                cv2.imwrite(
                    'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/roi3.jpg', roi)

    # cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                # 0.5, (255, 255, 255), 2)
    cv2.imshow('draw', imagem)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def preProcessamentoRoi():

    img_roi = cv2.imread(
        'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/roi3.jpg')
    cv2.imshow("roi", img_roi)

    img_resize = cv2.resize(img_roi, None, fx=4, fy=4,
                            interpolation=cv2.INTER_CUBIC)
    img_cinza = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)

    _, img_binary = cv2.threshold(
        img_cinza, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("res", img_binary)

    kernel = np.ones((4, 4), np.uint8)

    img_opening = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, kernel)
    cv2.imshow("res", img_opening)

    cv2.imwrite(
        'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/roi_pb3.jpg', img_opening)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # plt.imshow(th3,'gray')
    # plt.xticks([]),plt.yticks([])
    # plt.show()


def ocrImageRoiPlaca():

    img_roi = cv2.imread(
        'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/roi_pb3.jpg')

    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'

    resultado2 = pytesseract.image_to_string(
        img_roi, lang='eng', config=config)
    #today = date.today()

    app = connection.get_connection()
    db = SQLAlchemy(app)

    u1 = Usuario(
        dt_criacao=datetime.now(),
        cd_placa=resultado2,
        ds_cor="vermelho",
        hr_entrada="10",
        hr_saida="12",
        hr_total="1",
        vl_pago="40"
    )

    db.session.add(u1)
    db.session.commit()
    print(resultado2)

    lista_teste = list(Usuario.query)
    print(lista_teste)


if __name__ == "__main__":

    source = 'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/placa3.jpg'

    encontrarRoiPlaca(source)
    preProcessamentoRoi()
    ocrImageRoiPlaca()
