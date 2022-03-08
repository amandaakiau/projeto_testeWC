import cv2
from cv2 import CHAIN_APPROX_NONE
import pytesseract
from matplotlib import pyplot as plt
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

    _, binarizada = cv2.threshold(placa_cinza, 160, 255, cv2.THRESH_BINARY)
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
        aprox = cv2.approxPolyDP(c, 0.04 * perimetro, True)

        if len(aprox) == 4:
            #x,y,w,h = cv2.boundingRect(c)
            x1 = 255
            x2 = 503
            y1 = 266
            y2 = 361
            cv2.rectangle(imagem, (x1, y1), (x2, y2), (0, 255, 0), 2)
            roi = imagem[y1:y2, x1:x2]
            cv2.imwrite(
                'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/roiwebcam.jpg', roi)

            # cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
            # 0.5, (255, 255, 255), 2)

            plt.imshow(imagem, 'gray')
            plt.show()

            #cv2.imshow('draw', imagem)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


def preProcessamentoRoi():

    img_roi = cv2.imread(
        'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/roiwebcam.jpg')
    cv2.imshow("roi", img_roi)

    # img_resize = cv2.resize(img_roi, None, fx=4, fy=4,
    # interpolation=cv2.INTER_CUBIC)
    img_cinza = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)

    _, img_binary = cv2.threshold(img_cinza, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("res", img_binary)

    # colocar o filtro opening aqui
    cv2.imwrite(
        'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/roiwebcam_pb.jpg', img_binary)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def ocrImageRoiPlaca():

    img_roi = cv2.imread(
        'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/roiwebcam_pb.jpg')

    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'

    saida = pytesseract.image_to_string(img_roi, lang='eng', config=config)
    print(saida)


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


if __name__ == "__main__":

    source = 'C:/Users/isaah/Documents/Projeto/reconhecimentoPlaca/images/placawebcam.jpg'

    # imagemwebcam()
    encontrarRoiPlaca(source)
    # preProcessamentoRoi()
    # ocrImageRoiPlaca()
    # descricaoCor()
