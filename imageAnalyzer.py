import cv2 as cv
import numpy as np
import math

def imgAnalyzer (caminhoCompleto):
    img = cv.imread(caminhoCompleto, cv.IMREAD_GRAYSCALE)

    imgCorOriginal = cv.imread(caminhoCompleto)
    blue, green, red = cv.split(imgCorOriginal)
    zeros = np.zeros(blue.shape, np.uint8)
    blueBGR = cv.merge((blue, zeros, zeros))
    greenBGR = cv.merge((zeros, green, zeros))
    redBGR = cv.merge((zeros, zeros, red))

    assert img is not None, "file could not be read, check with os.path.exists()"
    # global thresholding
    ret1, th1 = cv.threshold(img, 50, 255, cv.THRESH_BINARY)
    # ret1, th1 = cv.threshold(img, imgCorOriginal.mean(), 255, cv.THRESH_BINARY)
    # Otsu's thresholding
    ret2, th2 = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # Otsu's thresholding after Gaussian filtering
    blur = cv.GaussianBlur(img, (5, 5), 0)
    ret3, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    somenteBranco = cv.inRange(th1, 1, 255)
    somentePreto = cv.inRange(th1, 0, 1)

    pixelsBranco = cv.countNonZero(somenteBranco)
    pixelsPreto = cv.countNonZero(somentePreto)

    reacao = (pixelsPreto / th1.size) * 100

    print(caminhoCompleto, " - ", reacao, "% -- Média de cor dos pixels: ", redBGR.mean(),
          "(quanto menor valor, mais escuro, reação mais intensa)")

    cv.imwrite("C:/Users/andreteixeira/Desktop/testeTH1/" + caminhoCompleto, th1)
    cv.imwrite("C:/Users/andreteixeira/Desktop/testeTH2/" + caminhoCompleto, th2)
    #TESTE QUE AVALIA AREA DE REACAO + INTENSIDADE DA COR NO CARNAL VERMELHO, VALORES AJUSTADOS PARA TH2
    #se reação foi alta e cor escura,  ou se reacao for baixa mas cor escura
    if (reacao > 50 and redBGR.mean() < 40) or (reacao < 50 and redBGR.mean() < 40):
        print("Sugere Indivíduo Normal do ponto de vista sudomotor")
        return "Sugere Indivíduo Normal do ponto de vista sudomotor\n"+ "- Reação: "+str(math.trunc(reacao)) + "% - Média cor pixels: "+str(math.trunc(redBGR.mean()))
    # se reação foi baixa e cor clara,  ou se reacao foi alta mas cor clara,
    elif (reacao < 50 and redBGR.mean() > 40) or (reacao > 50 and redBGR.mean() > 40) :
        print("Sugere Indivíduo com disfunção sudomotora")
        return "Sugere Indivíduo com disfunção sudomotora\n"+ "- Reação: "+str(math.trunc(reacao)) + "% - Média cor pixels: "+str(math.trunc(redBGR.mean()))




