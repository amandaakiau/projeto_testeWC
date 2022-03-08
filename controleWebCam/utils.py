import numpy as np
import cv2

def centroid_histogram(clt):
	# pega o numero de clusters diferentes e cria um histograma
	# com base no numero de pixels atribuido a cada cluster
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)
	# normaliza o histogram, tal que soma com um
	hist = hist.astype("float")
	hist /= hist.sum()
	# retorna o histograma
	return hist


def plot_colors(hist, centroids):
#inicializa a paleta de cores representando a frequencia relativa de cada cor

	bar = np.zeros((50, 300, 3), dtype="uint8")
	startX = 0

#loop sobre a porcentagem de cada cluster e a cor de cada cluster

	for (percent, color) in zip(hist, centroids):
		# plota a porcentagem relativa de cada cluster
		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
					  color.astype("uint8").tolist(), -1)
		startX = endX

	# retorna a paleta de cores
	return bar