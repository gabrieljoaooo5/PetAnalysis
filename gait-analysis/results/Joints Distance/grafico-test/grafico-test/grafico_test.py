import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import savgol_filter
import scipy.fftpack

arquivo = open("C:\\Users\\VOXAR\\Documents\\BodyBasics-WPF\\Joint_Distances.txt", 'r')
# arquivo = open("C:\\Users\\VOXAR\\Documents\\testeSen.txt", 'r')

listaPontos = arquivo.readlines()

listaFrame = []
tam = len(listaPontos)
i=0
listaPontos = [float(i) for i in listaPontos]
for i in range(tam):
    listaFrame.append(float(i))

filterPontos = signal.wiener(listaPontos) # Filtra os pontos da lista de pontos, para diminuir a sujeira

pontoLocal = 0 #0 = minimo local e 1 = maximo local
count = 0      #conta o numero de inversoes na curvatura do grafico
vizinho = 12
i=vizinho            #tamanho da vizinhanca

for i in range(tam-vizinho):
    atual = filterPontos[i]  #numero central sendo analisado
    j = i-vizinho                     
    isMinPoint = 1
    isMaxPoint = 1
    for k in range(vizinho*2 + 1):
        if(filterPontos[j] > atual):
            isMaxPoint = 0
        elif(filterPontos[j]<atual):
            isMinPoint = 0
        j += 1
        if(not(isMinPoint) and not(isMaxPoint)):
            break
     
    if(isMaxPoint):
        if(pontoLocal == 0):
            count += 1
        pontoLocal = 1
    elif(isMinPoint):
        if(pontoLocal == 1):
            count += 1

        pontoLocal = 0

qtdPassos = count//2
print("quantidade de passos: %d" %qtdPassos)


arquivo.close()

print("fim")

plt.plot(listaFrame, listaPontos, color = '#3CB371')
plt.xlabel('\'frame\'')
plt.ylabel('distance')
plt.title("Joints distance")
plt.savefig("C:\\Users\\VOXAR\\Documents\\BodyBasics-WPF\\historico\\graficoaqui.png")
plt.show()