from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy import signal
import scipy.fftpack
import numpy as np
import math

QTDFILTRO = 4

def create_list(listaPontos):
    lista = [i.split('\n') for i in listaPontos] # Tirar \n de cada linha
    num_linhas = len(lista) - 1 # Numero de linhas lidas

    for i in range(num_linhas):
        lista[i] = lista[i][0].split(' ') #Separa por espaço, para formar matriz

    tempoInicial = float(lista[0][6])
    for i in range(num_linhas):
        for j in range(6):
            lista[i][j] = float(lista[i][j]) #Transforma em float
        lista[i][6] = float(lista[i][6]) - tempoInicial
        tempoAtual.append(lista[i][6])

    tempoAtual.pop()

    return lista

def list_distance(listaPontos):
    num_linhas = len(listaPontos) - 1 
    for i in range(num_linhas):
        dist = distance(listaPontos[i][0], listaPontos[i][1], listaPontos[i][2], listaPontos[i][3])
        listaDistance.append(dist)

def distance(AR_X, AR_Z, AL_X, AL_Z):
    dist = math.pow((AR_X - AL_X), 2) + math.pow((AR_Z - AL_Z), 2)
    module = math.sqrt(dist)

    return module

def min_max_graph(listaDistance):
    qtdPassos = 0
    tam = len(listaDistance)
    pontoLocal = 0 #0 = minimo local e 1 = maximo local
    count = 1      #conta o numero de inversoes na curvatura do grafico
    tamVizinhanca = 8
    i = tamVizinhanca 

    for i in range(tam-tamVizinhanca):
        
        atual = listaDistance[i]  #numero central sendo analisado
        j = i-tamVizinhanca                      
        isMinPoint = 1
        isMaxPoint = 1
        for k in range(2*tamVizinhanca - 1):
            if(listaDistance[j] > atual):
                isMaxPoint = 0
            elif(listaDistance[j]<atual):
                isMinPoint = 0

            if(not(isMinPoint) and not(isMaxPoint)):
                break
            j += 1
        
        if(isMaxPoint):
            if(pontoLocal == 0):
                count += 1
            listaIndice.append(i)
            pontoLocal = 1

        elif(isMinPoint):
            if(pontoLocal == 1):
                count += 1
            pontoLocal = 0

    qtdPassos = count//2 + 1
    print("quantidade de passos: %d" %qtdPassos)
    print(listaIndice)

#  0  ,  1  ,  2  ,  3  ,  4  ,  5
#AR_X, AR_Z, AL_X, AL_Z, SB_X, SB_Z (ordem)
def tamanho_passo(listaAtual, listaProximo, flag):

    #vetor[Z, X]
    #define o vetor entre dois SB (atual e proximo)
    vetorReta = [listaProximo[5] - listaAtual[5], listaProximo[4]- listaAtual[4]]
    vetorRetaTras = [(-1)*(listaProximo[5] - listaAtual[5]),(-1)*(listaProximo[4]- listaAtual[4])]

    #print("vetor reta frente: [%f, %f]" %(vetorReta[0],vetorReta[1]))
    #print("vetor reta Tras: [%f, %f]" %(vetorRetaTras[0],vetorRetaTras[1]))

    #vetor[Z, X]
    #se o pe direito ta na frente (AR_Z < AL_Z)
    #define o vetor que representara o pe atualmente na frente e atras
    if(listaAtual[1] < listaAtual[3]):
           vetorPeFrente = [listaAtual[1]-listaAtual[5], listaAtual[0]-listaAtual[4]]
           vetorPeTras = [listaAtual[3]-listaAtual[5], listaAtual[2]-listaAtual[4]]
    else:
        vetorPeTras = [listaAtual[1]-listaAtual[5], listaAtual[0]-listaAtual[4]]
        vetorPeFrente = [listaAtual[3]-listaAtual[5], listaAtual[2]-listaAtual[4]]

    #print("vetor pe frente: [%f, %f]" %(vetorPeFrente[0],vetorPeFrente[1]))
    #print("vetor pe Tras: [%f, %f]" %(vetorPeTras[0],vetorPeTras[1]))

    #projecao pe da frente sobre a reta da frente (spine base)
    coef = ((vetorPeFrente[0]*vetorReta[0])+(vetorPeFrente[1]*vetorReta[1]))/((vetorReta[0]*vetorReta[0])+(vetorReta[1]*vetorReta[1]))
    projFrente = [coef*vetorReta[0], coef*vetorReta[1]]        
    distFrente = projFrente[0]*projFrente[0] + projFrente[1]*projFrente[1]
    #print("coef1: %f\n"%coef)

    #projecao do pe de tras sobre a reta de tras (spine base)
    coef = ((vetorPeTras[0]*vetorRetaTras[0])+(vetorPeTras[1]*vetorRetaTras[1]))/((vetorRetaTras[0]*vetorRetaTras[0])+(vetorRetaTras[1]*vetorRetaTras[1]))
    projTras = [coef*vetorRetaTras[0], coef*vetorRetaTras[1]]
    distTras = projTras[0]*projTras[0] + projTras[1]*projTras[1]
    #print("coef2: %f\n"%coef)

    #o tamanho do passo = soma do tamanho dos dois passos
    distanciaPasso = math.sqrt(distFrente + distTras)

    if (flag):
        if (listaAtual[1] < listaAtual[3]):
            ankleRight.append(distFrente)
            ankleLeft.append(0 - distTras)
        else:
            ankleRight.append(0 - distTras)
            ankleLeft.append(distFrente)
    #print("dist frente: %f // dist tras: %f // distanciaPasso: %f\n"%(distFrente, distTras, distanciaPasso))
    #print("proj frente: [%f][%f]" %(projFrente[0],projFrente[1]))
    #print("proj tras: [%f][%f]" %(projTras[0],projTras[1]))

    return distanciaPasso

# Acima dessa linha são apenas funções

#AR_X, AR_Z, AL_X, AL_Z, SB_X, SB_Z, tempoAtual (ordem dos dados na linha)
arquivo = open("C:\\Users\\VOXAR\\Documents\\BodyBasics-WPF\\joints.txt", 'r')
listaPontos = arquivo.readlines() # Ler arquivo com os pontos das juntas anlkes e spine base

listaDistance = []          # Lista de distancias
listaIndice = []            # Lista de indices com as maximas distâncias entre os pés
distanciaEuclidiana = []    # Lista com os tamanhos dos passos em todos os momentos
tamanhoPassos = []          # Lista com tamanho dos passos em maxima distancia
ankleRight = []             # Lista com as distancias do calcanhar direito para spine base
ankleLeft = []              # Lista com as distancias do calcanhar esquerdo para spine base
tempoAtual = []
velocidadePasso = []
somaVelocidades = 0

listaPontos = create_list(listaPontos) # Criar a lista com os pontos das juntas
list_distance(listaPontos)             # Criar a lista com as distâncias dos pontos anteriores
min_max_graph(listaDistance)           # Saber quais os indices de maximo e minimo, e contar passos

tamTotal = 0                            # Tamanho da soma de todos os passos
lenDistance = len(listaDistance) - 1    # Tamanho da lista distancias
lenMaximos = len(listaIndice) - 1       # Tamanho da lista de indices

# Criando a lista de distancias euclidianas, para todos os pontos
for i in range(lenDistance):
    tam = tamanho_passo(listaPontos[i], listaPontos[i+1], 1)
    distanciaEuclidiana.append(tam)

# Criando a lista apenas com o tamanho dos passos, quando houver maximas distancias
for i in range(lenMaximos):
    indice1 = listaIndice[i]        #Guardando o ponto de máximo em i
    indice2 = listaIndice[i + 1]    #Guardando o próximo ponto de máximo
    tam = tamanho_passo(listaPontos[indice1], listaPontos[indice2], 0) #Distância euclidiana entre os dois pontos de máximo
    tamTotal += tam                 
    tamanhoPassos.append(tam)       #Adicionando os tamanhos dos passos na lista
    somaVelocidades += tam/(tempoAtual[indice2]-tempoAtual[indice1])
    velocidadePasso.append(tam/(tempoAtual[indice2]-tempoAtual[indice1]))

# Printar a lista de tamanhos e o tamanho médio do passo
tamMedio = tamTotal/lenMaximos # Tamanho médio dos passos
print("Tamanho medio: %f" %tamMedio)
velocidadeMedia = somaVelocidades/lenMaximos
print("velocidade media: %f" %velocidadeMedia)
print("tempoTotal: %f" %tempoAtual[len(tempoAtual)-2])
print("distancia total: %f" %tamTotal)
print(tamanhoPassos)

arquivo.close() #Fechar arquivo

listaDistance.pop()

for i in range(QTDFILTRO):
    ankleRight = signal.wiener(ankleRight)
    ankleLeft = signal.wiener(ankleLeft)
    listaDistance = signal.wiener(listaDistance)
    distanciaEuclidiana = signal.wiener(distanciaEuclidiana)


# Plotar gráfico
plt.plot(tempoAtual, distanciaEuclidiana)
plt.plot(tempoAtual, listaDistance)
plt.plot(tempoAtual, ankleRight)
plt.plot(tempoAtual, ankleLeft)
plt.xlabel('\'frame\'')
plt.ylabel('distance')
plt.title("Distance")
plt.savefig('C:\\Users\\VOXAR\\Documents\\BodyBasics-WPF\\grafico.png')
plt.show()