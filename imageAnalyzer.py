import cv2 as cv
import numpy as np
import math

def imgAnalyzer (diabetes, caminhoCompleto):
    resultado = ""
    img = cv.imread(caminhoCompleto, cv.IMREAD_GRAYSCALE)

    imgCorOriginal = cv.imread(caminhoCompleto)
    blue, green, red = cv.split(imgCorOriginal)
    zeros = np.zeros(blue.shape, np.uint8)
    blueBGR = cv.merge((blue, zeros, zeros))
    greenBGR = cv.merge((zeros, green, zeros))
    redBGR = cv.merge((zeros, zeros, red))

    assert img is not None, "file could not be read, check with os.path.exists()"
    # global thresholding
    #ret1, th1 = cv.threshold(img, 60, 255, cv.THRESH_BINARY)
    ret1, th1 = cv.threshold(img, imgCorOriginal.mean(), 255, cv.THRESH_BINARY)
    # Otsu's thresholding
    ret2, th2 = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # Otsu's thresholding after Gaussian filtering
    blur = cv.GaussianBlur(img, (5, 5), 0)
    ret3, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    #somenteBranco = cv.inRange(th1, 1, 255)
    somentePretoTH1 = cv.inRange(th1, 0, 1)
    somentePretoTH2 = cv.inRange(th2, 0, 1)

    #pixelsBranco = cv.countNonZero(somenteBranco)
    pixelsPretoTH1 = cv.countNonZero(somentePretoTH1)
    pixelsPretoTH2 = cv.countNonZero(somentePretoTH2)

    reacaoTH1 = (pixelsPretoTH1 / th1.size) * 100
    reacaoTH2 = (pixelsPretoTH2 / th2.size) * 100

    print(caminhoCompleto, " - ", reacaoTH2, "%(th2) -- Média de cor dos pixels (RED): ", redBGR.mean(),
          "(quanto menor valor, mais escuro, reação mais intensa)")
    print(caminhoCompleto, " - ", reacaoTH1, "%(th1) -- Média de cor dos pixels (RGB): ", imgCorOriginal.mean(),
          "(quanto menor valor, mais escuro, reação mais intensa)")

    cv.imwrite("C:/Users/dezao/testeTH1/" + caminhoCompleto, th1)
    cv.imwrite("C:/Users/dezao/testeTH2/" + caminhoCompleto, th2)

    resultado = "Reação: "+ str(math.trunc(reacaoTH2)) + "% (th2) - " +  str(math.trunc(reacaoTH1)) + "% (th1)"
    resultado += "Média cor pixels: "+str(math.trunc(redBGR.mean())) + "(RED) - " + str(math.trunc(imgCorOriginal.mean())) +" (RGB) ****"
   #Método 1 resposta apenas em relação a suor
    if (reacaoTH1 > 50 and imgCorOriginal.mean() < 62) or (reacaoTH1 < 50 and imgCorOriginal.mean() > 62):
        print("Sugere Indivíduo com disfunção sudomotora")
        resultado += "Sugere Indivíduo com disfunção sudomotora (th1+rgb)"
    else:
        print("Sugere Indivíduo Normal do ponto de vista sudomotor (th1+rgb)")
        resultado += "Sugere Indivíduo Normal do ponto de vista sudomotor (th1+rgb)"


    # Método 1 resposta considerando diabetes
    if (reacaoTH1 > 50 and imgCorOriginal.mean() < 62) or (reacaoTH1 < 50 and imgCorOriginal.mean() > 62):
        if diabetes == "true":
            print("Diabético com neuropatia (apresenta baixa sudorese, eliminando-se outros fatores, sugere risco aumentado para neuropatia periférica)")
            resultado += "Diabético com neuropatia (apresenta baixa sudorese, eliminando-se outros fatores, sugere risco aumentado para neuropatia periférica)"
        else:
            print(
                "Indivíduo Normal, com baixa sudorese. Sugere-se investigar hiposudorese, diabetes não detectada, hanseníase, charcot marie etc.")
            resultado += "Indivíduo Normal, com baixa sudorese. Sugere-se investigar hiposudorese, diabetes não detectada, hanseníase, charcot marie etc."
    else:
        if diabetes == "true":
            print("Diabético sem neuropatia (apresenta sudorese satisfatória, afasta risco de neuropatia periférica)")
            resultado += "Diabético sem neuropatia (apresenta sudorese satisfatória, afasta risco de neuropatia periférica)"
        else:
            print("Indivíduo Normal (não é diabético e sudorese satisfatória)")
            resultado = resultado + "Indivíduo Normal (não é diabético e sudorese satisfatória)"


    # resultado = resultado + "**** Método 2: "
    # #Método 2 resposta apenas em relação a suor
    # #se reação foi alta e cor escura,  ou se reacao for baixa mas cor escura
    # if (reacaoTH2 > 50 and redBGR.mean() < 40) or (reacaoTH2 < 50 and redBGR.mean() < 40):
    #     print("Sugere Indivíduo Normal do ponto de vista sudomotor")
    #     resultado += "Sugere Indivíduo Normal do ponto de vista sudomotor (th2+red)"
    # # se reação foi baixa e cor clara,  ou se reacao foi alta mas cor clara,
    # elif (reacaoTH2 < 50 and redBGR.mean() > 40) or (reacaoTH2 > 50 and redBGR.mean() > 40) :
    #     print("Sugere Indivíduo com disfunção sudomotora")
    #     resultado += "Sugere Indivíduo com disfunção sudomotora (th2+red)"
    #
    # #Método 2 resposta considerando diabetes
    # if diabetes == "true" and (reacaoTH1 in (30, 87.5) or imgCorOriginal.mean() < 67):
    #     print("Diabético sem neuropatia (apresenta sudorese satisfatória, afasta risco de neuropatia periférica)")
    #     resultado += "Diabético sem neuropatia (apresenta sudorese satisfatória, afasta risco de neuropatia periférica)"
    # elif diabetes == "true" and (reacaoTH1 < 30 and imgCorOriginal.mean() > 67):
    #     print("Diabético com neuropatia (apresenta baixa sudorese, eliminando-se outros fatores, sugere risco aumentado para neuropatia periférica)")
    #     resultado += "Diabético com neuropatia (apresenta baixa sudorese, eliminando-se outros fatores, sugere risco aumentado para neuropatia periférica)"
    # else:
    #     if (reacaoTH1 > 50 or imgCorOriginal.mean() < 67):
    #         print("Indivíduo Normal (não é diabético e sudorese satisfatória)")
    #         resultado = resultado + "Indivíduo Normal (não é diabético e sudorese satisfatória)"
    #     else:
    #         print("Indivíduo Normal, com baixa sudorese. Sugere-se investigar hiposudorese, diabetes não detectada, hanseníase, charcot marie etc.")
    #         resultado += "Indivíduo Normal, com baixa sudorese. Sugere-se investigar hiposudorese, diabetes não detectada, hanseníase, charcot marie etc."

    return resultado


