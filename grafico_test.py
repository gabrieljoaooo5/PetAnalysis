import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import math

QTDFILTRO = 5

def create_list(listaPontos):
    lista = [i.split('\n') for i in listaPontos] # Tirar \n de cada linha
    num_linhas = len(lista) - 1 # Numero de linhas lidas

    for i in range(num_linhas):
        lista[i] = lista[i][0].split(' ') # Separa por espaço, para formar matriz

    tempoInicial = float(lista[0][6])
    for i in range(num_linhas):
        for j in range(6):
            lista[i][j] = float(lista[i][j]) # Transforma em float
        lista[i][6] = float(lista[i][6]) - tempoInicial
        tempoAtual.append(lista[i][6])

    tempoAtual.pop()

    return lista

def create_list2(ar, al, sb):
    with open("C:\\Users\\VOXAR\\Documents\\BodyBasics-WPF\\joints.txt") as file:
        for line in file:
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
                listaPontos.append(linha)

    file.close()

def list_euclidiana(listaPontos):
    num_linhas = len(listaPontos)-1 
    for i in range(num_linhas):
        dist = distance(listaPontos[i][0], listaPontos[i][1], listaPontos[i][2], listaPontos[i][3])
        listaEuclidiana.append(dist)

def distance(AR_X, AR_Z, AL_X, AL_Z):
    dist = math.pow((AR_X - AL_X), 2) + math.pow((AR_Z - AL_Z), 2)
    module = math.sqrt(dist)

    return module

def min_max_graph(listaDistance):
    qtdPassos = 0
    tam = len(listaDistance)
    tamVizinhanca = 8 

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
            listaIndice.append(i)
            qtdPassos += 1

    i = 1
    tamTotal = 0
    for i in range(len(listaIndice)):
        indice = listaIndice[i]
        tamTotal += listaDistance[indice]

    tamMedio = tamTotal/(len(listaIndice))
    print(tamMedio)

    i = 1
    lista = []
    for i in range(len(listaIndice)):
        indice = listaIndice[i]
        if(listaDistance[indice] < 0.80*tamMedio or listaDistance[indice] >= 1.45*tamMedio):
            lista.append(i)

    for i in range(len(lista)):
        ind = listaIndice[lista[i]]
        del(listaIndice[lista[i]])
        j = i
        for j in range(len(lista)):
            lista[j] -= 1
    
    qtdPassos = len(listaIndice)
    print("quantidade de passos: %d" %qtdPassos)
    print(listaIndice)

#  0  ,  1  ,  2  ,  3  ,  4  ,  5
#AR_X, AR_Z, AL_X, AL_Z, SB_X, SB_Z (ordem)
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

    if(vetorReta[0] != 0 or vetorReta[1] != 0):
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

        moduloReta = math.sqrt(math.pow(vetorReta[0],2) + math.pow(vetorReta[1], 2))

        ankleRight.append(testeDistDireito-SB_Z_prx)
        ankleLeft.append(testeDistEsquerdo-SB_Z_prx)
    else:
        ankleRight.append(0)
        ankleLeft.append(0)
    
    return distanciaPasso

# Acima dessa linha são apenas funções
listaPontos = []

#AR_X, AR_Z, AL_X, AL_Z, SB_X, SB_Z, tempoAtual (ordem dos dados na linha)
#arquivo = open("C:\\Users\\VOXAR\\Documents\\BodyBasics-WPF\\joints.txt", 'r')
#listaPontos = arquivo.readlines() # Ler arquivo com os pontos das juntas anlkes e spine base

listaEuclidiana = []        # Lista de distancias euclidianas
listaIndice = []            # Lista de indices com as maximas distâncias entre os pés
listaDistance = []          # Lista com os tamanhos dos passos em todos os momentos
tamanhoPassos = []          # Lista com tamanho dos passos em maxima distancia
ankleRight = []             # Lista com as distancias do calcanhar direito para spine base
ankleLeft = []              # Lista com as distancias do calcanhar esquerdo para spine base
tempoAtual = []             # Lista de tempos de cada acontecimento
listaTempos = []
ankleRPlot = []
ankleLPlot = []
somaVelocidades = 0
tamTotal = 0                             # Tamanho da soma de todos os passos

#listaPontos = create_list(listaPontos)   # Criar a lista (matriz) com os pontos das juntas
create_list2(18, 14, 0)                  # Para usar com o txt de zé
list_euclidiana(listaPontos)             # Criar a lista com as distâncias dos pontos anteriores

lenEuclidiana = len(listaEuclidiana) - 1    # Tamanho da lista distancias

# Criando a lista de distancias euclidianas, para todos os pontos
for i in range(lenEuclidiana):
    tam = tamanho_passo(listaPontos[i], listaPontos[i+1])
    listaDistance.append(tam)

for i in range(QTDFILTRO):
    listaDistance = signal.wiener(listaDistance)

min_max_graph(listaDistance)            # Saber quais os indices de maximo e minimo, e contar passos
lenMaximos = len(listaIndice)           # Tamanho da lista de indices
tamMedio = 0
tempoTotal = 0

# Criando a lista apenas com o tamanho dos passos, quando houver maximas distancias
i = 1
for i in range(lenMaximos):
    indice = listaIndice[i]
    tamTotal += listaDistance[indice]
    tamanhoPassos.append(listaDistance[indice])       #Adicionando os tamanhos dos passos na lista

for i in range(lenMaximos-1):
    indice1 = listaIndice[i]          #Guardando o ponto de máximo em i
    indice2 = listaIndice[i + 1]
    #tempo = tempoAtual[indice2]-tempoAtual[indice1]
    #listaTempos.append(tempo)
    #tempoTotal += tempo


# Printar a lista de tamanhos e o tamanho médio do passo
tamMedio = tamTotal/(lenMaximos-1) # Tamanho médio dos passos
#velocidadeMedia = tamTotal/tempoTotal

print("Tamanho medio: %f" %tamMedio)
#print("velocidade media: %f" %velocidadeMedia)
print("distancia total: %f" %tamTotal)
#print("tempo total: %f" %tempoTotal)
print(tamanhoPassos)
#print(ankleRight)
#print(ankleLeft)

#arquivo.close() #Fechar arquivo

listaEuclidiana.pop()

for i in range(QTDFILTRO):
    ankleRight = signal.wiener(ankleRight)
    ankleLeft = signal.wiener(ankleLeft)
    listaEuclidiana = signal.wiener(listaEuclidiana)


# Plotar gráfico
plt.figure(figsize=(10,7))
plt.plot(listaDistance, color = "blue", label = "Dist Passo")
plt.plot(listaEuclidiana, color = "orange", label = "Dist Euclidiana")
plt.plot(ankleRight, color = "red", label = "Ankle Right")
plt.plot(ankleLeft, color = "green", label = "Ankle Left")
plt.xlabel('tempo(s)')
plt.ylabel('distance(m)')
plt.grid(True)
plt.legend()
plt.title("Distance")
plt.savefig('C:\\Users\\VOXAR\\Documents\\BodyBasics-WPF\\grafico.png')
plt.show()