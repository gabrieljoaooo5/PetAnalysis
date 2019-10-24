from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy import signal
import scipy.fftpack
import numpy as np
import math

def create_list(listaPontos):
    lista = [i.split('\n') for i in listaPontos] # Tirar \n de cada linha
    num_linhas = len(lista) - 1 # Numero de linhas lidas

    for i in range(num_linhas):
        lista[i] = lista[i][0].split(' ') #Separa por espaço, para formar matriz

    for i in range(num_linhas):
        for j in range(6):
            lista[i][j] = float(lista[i][j]) #Transforma em float

    return lista

def list_distance(listaPontos):
    num_linhas = len(listaPontos) - 1 
    for i in range(num_linhas):
        dist = distance(listaPontos[i][0], listaPontos[i][1], listaPontos[i][2], listaPontos[i][3])
        listaDistance.append(dist)

#AR_X, AR_Z, AL_X, AL_Z, SB_X, SB_Z (ordem)
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
                listaIndice.append(i)
                count += 1
            pontoLocal = 1

        elif(isMinPoint):
            if(pontoLocal == 1):
                listaIndice.append(i)
                count += 1
            pontoLocal = 0

    qtdPassos = count//2 + 1
    print("quantidade de passos: %d" %qtdPassos)

#  0  ,  1  ,  2  ,  3  ,  4  ,  5
#AR_X, AR_Z, AL_X, AL_Z, SB_X, SB_Z (ordem)
def tamanho_passo(listaAtual, listaProximo):

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

    #print("dist frente: %f // dist tras: %f // distanciaPasso: %f\n"%(distFrente, distTras, distanciaPasso))
    #print("proj frente: [%f][%f]" %(projFrente[0],projFrente[1]))
    #print("proj tras: [%f][%f]" %(projTras[0],projTras[1]))

    return distanciaPasso

arquivo = open("C:\\Users\\VOXAR\\Documents\\BodyBasics-WPF\\joints.txt", 'r')
listaPontos = arquivo.readlines()
listaDistance = []
listaIndice = []
listaTamanhos = []

listaPontos = create_list(listaPontos)
list_distance(listaPontos)
min_max_graph(listaDistance)
tamTotal = 0
tamLista = len(listaIndice) - 1

for i in range(tamLista):
    indice = listaIndice[i]
    indice2 = listaIndice[i + 1]
    tam = tamanho_passo(listaPontos[indice], listaPontos[indice2])
    tamTotal += tam
    listaTamanhos.append(tam)

print("Lista tamanhos:")
print(listaTamanhos)
tamMedio = tamTotal/tamLista
print("Tamanho medio: %f" %tamMedio)



arquivo.close()

plt.plot(listaDistance)
plt.xlabel('\'frame\'')
plt.ylabel('distance')
plt.title("Distance")
plt.show()