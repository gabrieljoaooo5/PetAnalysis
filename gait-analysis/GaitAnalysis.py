import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import math
import os

QTDFILTRO = 5

# Read txt from kinect
def create_list(ar, al, sb):
    frames = 0
    with open(path) as file:
        for line in file:
            frames += 1
            line = line.split('\n')
            line = line[0].split(' ')
            linha = []
            if (line[sb*6] == '2' and line[ar*6] == '2' and line[al*6] == '2'):
                linha.append(line[ar*6 + 1])
                linha.append(line[ar*6 + 3])
                linha.append(line[al*6 + 1])
                linha.append(line[al*6 + 3])
                linha.append(line[sb*6 + 1])
                linha.append(line[sb*6 + 3])

            for i in range (len(linha)):
                linha[i] = linha[i].replace(',', '.')
                linha[i] = float(linha[i])

            if (len(linha) == 6):
                if (len(listaPontos) > 0):
                    if (linha != listaPontos[len(listaPontos) - 1]):
                        listaPontos.append(linha)
                else: listaPontos.append(linha)

    file.close()
    return frames

# Create a list with the Euclidean distance
def list_euclidiana(listaPontos):
    num_linhas = len(listaPontos)

    for i in range(num_linhas):
        dist = distance(listaPontos[i][0], listaPontos[i][1], listaPontos[i][2], listaPontos[i][3])
        listaEuclidiana.append(dist)

# Calculate the Euclidean distance of two points(ankles)
def distance(AR_X, AR_Z, AL_X, AL_Z):
    dist = math.pow((AR_X - AL_X), 2) + math.pow((AR_Z - AL_Z), 2)
    module = math.sqrt(dist)

    return module

# Find the max points(steps) from the ankles's list distance
def min_max_graph(listaDistance):
    tam = len(listaDistance)
    tamVizinhanca = 8 
    lista = []

    for i in range(tam):
        
        atual = listaDistance[i]  #numero central sendo analisado
        j = i-tamVizinhanca                      
        isMinPoint = 1
        isMaxPoint = 1
        for k in range(2*tamVizinhanca - 1):
            if (j >= 0 and j < tam):
                if(listaDistance[j] > atual):
                    isMaxPoint = 0
                elif(listaDistance[j]<atual):
                    isMinPoint = 0

            if(not(isMinPoint) and not(isMaxPoint)):
                break
            j += 1
        
        if(isMaxPoint):
            lista.append(listaDistance[i])
            
    
    return lista


#  0  ,  1  ,  2  ,  3  ,  4  ,  5
#AR_X, AR_Z, AL_X, AL_Z, SB_X, SB_Z (ordem na lista de pontos)
def tamanho_passo(listaAtual, listaProximo):
    #vetor[Z, X]
    #define o vetor entre dois SB (atual e proximo)
    AR_X_at = listaAtual[0]
    AR_Z_at = listaAtual[1]
    AL_X_at = listaAtual[2]
    AL_Z_at = listaAtual[3]
    SB_X_at = listaAtual[4]
    SB_Z_at = listaAtual[5]

    SB_X_prx = listaProximo[4]
    SB_Z_prx = listaProximo[5]

    distanciaPasso = 0
    vetorReta = [SB_Z_prx - SB_Z_at, SB_X_prx- SB_X_at]

    #vetor[Z, X]
    #define o vetor que representara o pe atualmente na frente e atras
    vetorPeDireito = [AR_Z_at-SB_Z_at, AR_X_at-SB_X_at]
    vetorPeEsquerdo = [AL_Z_at-SB_Z_at, AL_X_at-SB_X_at]

    #projecao pe direito sobre a reta da frente (spine base)
    coef = ((vetorPeDireito[0]*vetorReta[0])+(vetorPeDireito[1]*vetorReta[1]))/((vetorReta[0]*vetorReta[0])+(vetorReta[1]*vetorReta[1]))
    projDireito = [coef*vetorReta[0], coef*vetorReta[1]]        
    distDireito = math.sqrt(projDireito[0]*projDireito[0] + projDireito[1]*projDireito[1])

    #projecao do pe esquerdo sobre a reta da frente (spine base)
    coef = ((vetorPeEsquerdo[0]*vetorReta[0])+(vetorPeEsquerdo[1]*vetorReta[1]))/((vetorReta[0]*vetorReta[0])+(vetorReta[1]*vetorReta[1]))
    projEsquerdo = [coef*vetorReta[0], coef*vetorReta[1]]
    distEsquerdo = math.sqrt(projEsquerdo[0]*projEsquerdo[0] + projEsquerdo[1]*projEsquerdo[1])

    #o tamanho do passo = soma do tamanho dos dois passos
    distanciaPasso = distDireito + distEsquerdo

    #define a distância 
    testeDistDireito = math.sqrt(math.pow((SB_Z_prx-projDireito[0]), 2) + math.pow(SB_X_prx-projDireito[1], 2))
    testeDistEsquerdo = math.sqrt(math.pow((SB_Z_prx-projEsquerdo[0]), 2) + math.pow(SB_X_prx-projEsquerdo[1], 2))

    ankleRight.append(distDireito)
    ankleLeft.append(distEsquerdo)
    ankleRightPlot.append(testeDistDireito-SB_Z_prx+first)
    ankleLeftPlot.append(testeDistEsquerdo-SB_Z_prx+first)
    
    return distanciaPasso

def angulo(vetorPe, vetorReta):
    moduloPe = math.sqrt(math.pow(vetorPe[0],2) + math.pow(vetorPe[1],2))
    moduloReta = math.sqrt(math.pow(vetorReta[0],2) + math.pow(vetorReta[1],2))
    cos = (vetorPe[0]*vetorReta[0] + vetorPe[1]*vetorReta[1])/moduloPe*moduloReta
    angulo = math.acos(cos)
    return angulo

def delete(list):
    tamTotal = 0
    listHelp = []
    for i in range(len(list)):
        tamTotal += list[i]

    tamMedio = tamTotal/(len(list))

    for i in range (len(list)):
        if (list[i] <= 1.8*tamMedio and list[i] >= 0.2*tamMedio):
            listHelp.append(list[i])

    return listHelp

# Acima dessa linha são apenas funções

# Ler os três txts do kinect:
for i in range (3):
    first = 0
    listaPontos = []

    # Ecolhendo txt para ler e nome do gráfico para salvar
    print("")
    if (i == 0): 
        path = os.path.abspath(os.path.dirname(__file__)) + "\\recordings\\twokinect-data.txt"
        fig = os.path.abspath(os.path.dirname(__file__)) + "\\info\\twokinect-data.png"
        print("Two Kinects info:")

    elif (i == 1): 
        path = os.path.abspath(os.path.dirname(__file__)) + "\\recordings\\localkinect-data.txt"
        fig = os.path.abspath(os.path.dirname(__file__)) + "\\info\\localkinect-data.png"
        print("Local Kinect info:")

    else: 
        path = os.path.abspath(os.path.dirname(__file__)) + "\\recordings\\netkinect-data.txt"
        fig = os.path.abspath(os.path.dirname(__file__)) + "\\info\\netkinect-data.png"
        print("Net Kinect info:")

    # Declarando listas
    listaEuclidiana = []        # Lista de distancias euclidiana
    ankleRightPlot = []         # Plotar tornozelo direito
    ankleLeftPlot = []          # Plotar tornozelo esquerdo
    listaDistance = []          # Lista com os tamanhos dos passos em todos os momentos
    tamanhoPassos = []          # Lista com tamanho dos passos em maxima distancia                         
    ankleRight = []             # Lista com as distancias do calcanhar direito para spine base
    ankleLeft = []              # Lista com as distancias do calcanhar esquerdo para spine base
    stepVel = []                # Lista com velocidades dos passos

    # Chamando funcoes
    frames = create_list(18, 14, 0)     # AnkleRight(18), AnkleLeft(14), SpineBase(0)
    list_euclidiana(listaPontos)        # Criar a lista com as distâncias euclidianas dos pontos anteriores
    first = listaPontos[0][1]           # Primeiro ponto da SpineBase

    # Criando a lista de distâncias entre tornozelos, para todos os pontos
    for i in range(len(listaEuclidiana) - 1):
        tam = tamanho_passo(listaPontos[i], listaPontos[i+1])
        listaDistance.append(tam)

    # Cria lista com maximos dos passos e dos lados direito e esquerdo
    listaMaxStep = min_max_graph(listaDistance)
    listaMaxRight = min_max_graph(ankleRight)
    listaMaxLeft = min_max_graph(ankleLeft)
    lenMaximos = len(listaMaxStep)

    # Calcula algumas medias e o tempo total
    tempoTotal = (frames*1/30)                   
    distTotal = sum(listaMaxStep) - listaMaxStep[0]
    stepRight = 2*sum(listaMaxRight)/len(listaMaxRight)    
    stepLeft = 2*sum(listaMaxLeft)/len(listaMaxLeft)
    tamMedioPasso = distTotal/(lenMaximos-1)

    for i in range(lenMaximos - 1):
        frame = abs(listaMaxStep[i]-listaMaxStep[i+1])
        stepVel.append(frame*2/30)

    stepVel = np.asarray(stepVel)
    incertezaVel = stepVel.std()/math.sqrt(len(stepVel))
    velocidadeMedia = distTotal/tempoTotal

    listaMaxStep = np.asarray(listaMaxStep)
    incertezaPasso = listaMaxStep.std()/math.sqrt(len(listaMaxStep))
    incertezaPassada = 2*incertezaPasso
    
    listaMaxRight = np.asarray(listaMaxRight)
    incertezaDireito = listaMaxRight.std()/math.sqrt(len(listaMaxRight))
    
    listaMaxLeft = np.asarray(listaMaxLeft)
    incertezaEsquerdo = listaMaxLeft.std()/math.sqrt(len(listaMaxLeft))

    qtdPassos = len(listaMaxStep)
    strideLen = 2*tamMedioPasso

    print("Frames: %d" %frames)
    print("Tamanho medio passo: (%.2f +- %.2f) cm" %(100*tamMedioPasso, 100*incertezaPasso))
    print("Tamanho medio passada: (%.2f +- %.2f) cm" %(100*strideLen, 100*incertezaPassada))
    # print("Tamanho passo direito: (%.2f +- %.2f) cm" %(100*stepRight, 100*incertezaDireito))
    # print("Tamanho passo esquerdo: (%.2f +- %.2f) cm" %(100*stepLeft, 100*incertezaEsquerdo))
    print("Velocidade media do passo: %.2f +- %.2f cm/s" %(100*velocidadeMedia, 100*incertezaVel))
    print("distancia total: %.2fm" %distTotal)
    print("tempo total: %.2fs" %tempoTotal)
    print("quantidade de passos: %d" %qtdPassos)

    listaEuclidiana.pop()

    # Aplicar filtro
    for i in range(QTDFILTRO):
        ankleRightPlot = signal.wiener(ankleRightPlot)
        ankleLeftPlot = signal.wiener(ankleLeftPlot)
        listaEuclidiana = signal.wiener(listaEuclidiana)
        listaDistance = signal.wiener(listaDistance)

    # Plotar gráfico
    plt.figure(figsize=(10,7))
    plt.plot(listaDistance, color = "blue", label = "Dist Passo")
    plt.plot(listaEuclidiana, color = "orange", label = "Dist Euclidiana")
    plt.plot(ankleRightPlot, color = "red", label = "Ankle Right")
    plt.plot(ankleLeftPlot, color = "green", label = "Ankle Left")
    plt.xlabel('frame')
    plt.ylabel('distance(m)')
    plt.grid(True)
    plt.legend()
    plt.title("Distance")
    plt.savefig(fig)

    plt.show()
