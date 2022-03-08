#  https://www.youtube.com/watch?v=r8Qg3NfdiHc
import cv2

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

    cv2.imwrite("FotoPlaca.png", frame)

webcam.release()
cv2.destroyAllWindows()
