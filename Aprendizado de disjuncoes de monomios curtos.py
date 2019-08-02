import numpy.random as rd
import itertools as it
import random
import copy

##***ALUNO: Claudemir Woche Vasconcelos Carvalho - 389575
##***ALUNO: Francisco Yuri Martins Costa - 391379


#Amostra Não tem repetidos e não tem vetor nulo
#Hipótese Pode ter repetição e não tem vetor nulo

#rd.seed(45)
#random.seed(45)

##---------------------------FUNÇÕES---------------------------##

def generateHipo(k,numMonomios):
    l = [0]*k
    hipotese = [0]*numMonomios
    prob = 0.35
    
    #Cria a hipotese toda zerada de numMonomiosxnumMonomios
    for i in range (numMonomios):
        hipotese[i] = [0]*k
      
    #Preenche a hipótese com -1,0 ou 1    
    for i in range (numMonomios):
        for j in range (k):
            a = rd.rand()
            if a<= prob:
                l[j] = 1
            elif prob < a <= prob*2:
                l[j] = -1
            else:
                l[j] = 0

        hipotese[i] = copy.deepcopy(l)
    
    ##obs: não usei rd.rand(size=k) na linha 25 pq 
    #retornaria um array do numpy,que é algo que eu não quero usar
    
    return hipotese

def generateAmostra(k,n,am):
    #espacoAmostra recebe o produto k-cartesiano de [0,1]
    espacoAmostra = it.product([0,1], repeat=k)
    espacoAmostra = [list(i) for i in espacoAmostra]
    amostra0 = []
    amostra = [0]*am
    
    #amostra0 recebe os monomios de grau 1 a n
    for monomio in espacoAmostra:
        c = [abs(v) for v in monomio]
        if 1 <= sum(c) <= n:
            amostra0.append(monomio)
    
    #aux recebe uma lista de am números num intervalo (0,am) sem repetição
    aux = random.sample(range(am),am)
    
    #aux[i] é usado pra indície 
    for i in range (am):
        amostra[i] = amostra0[aux[i]]

    return amostra


def generateConceito(hipotese,amostra,am):
    conceito = [0]*am
    
    for i in range (am):
        conceito[i]=checkHipo(hipotese,amostra[i])
            
    return conceito    
 

def generateM(k,n):
    # Guarda em M apenas os monomios de grau 1,...,n
    A = [0,1,-1]
    Todos = it.product(A, repeat=k)
    Todos = [list(i) for i in Todos]
    M = []
    for monomio in Todos:
        c = [abs(v) for v in monomio]
        if 1 <= sum(c) <= n:
            M.append(monomio)
            
    print('Monomios de grau 1 a {} com {} variáveis'.format(n,k))
    print(M,end = '\n\n')
    
    return M

def checkMonomio(m,x):
    if m!= 0:
        # m = monomio
        # x = amostra
        tam = len(m)
        #Verifica se tem algo na amostra e se tem no monômio
    
        for i in range(tam):
            if x[i] == 1 and m[i]!=0:                         
                if m[i] == -1:                  #Se tiver -1(falso) o monômio já não é válido
                   return 0
        return 1
    else:
        pass

def checkHipo(M,x):
    #Checa uma amostra para cada monomio da hipotese
    #Se pelo menos 1 monômio é True, pronto. 
    for T in M:                                     
        if checkMonomio(T,x): return 1                
    
    return 0

    

def testHipote(hipotese1,hipotese2,amostra,conceito):
    tam = len(conceito)
    cont1 = 0
    cont2 = 0
    for i in range (tam):
        if checkHipo(hipotese1,amostra[i]) == conceito [i]:
            cont1+=1
        if checkHipo(hipotese2,amostra[i]) == conceito [i]:
            cont2+=1

    if cont1==tam and cont2 == tam:
        print('\nAs duas hipóteses são válidas')
    
    
def printarM(M):
    for i in M:
        if i is not 0:
            print(i,end=',')    


def entradaDeDados():
    n = int(input('Digite o grau dos monômios\n'))
    k = int(input('Digite o número de variáveis\n'))
    am = int(input('Digite o número de amostras\n'))
    numMonomios = int(input('Digite o número de monômios da hipótese aleatória\n'))

    return n,k,am,numMonomios          

##-----------------------------------------------------------##



##---------------------------MAIN----------------------------##

#n -> Grau dos monômios
#k -> Número de variáveis
#am -> Número de amostras
#numMonomios -> Número de monômios na hipótese aleatória    




##******SE NÃO QUISER FICAR DIGITANDO OS DADOS, 
##******DESCOMENTE AS LINHAS 167,168,169,170,
##******PREENCHA SABIAMENTE E COMENTE A LINHA 172 




#n =  3                                          
#k =  4                                          
#am = 5                                                                                 
#numMonomios = 3                                 

n,k,am,numMonomios = entradaDeDados()

M = generateM(k,n)
amostra = generateAmostra(k,n,am)
hipotese = generateHipo(k,numMonomios) 
conceito = generateConceito(hipotese,amostra,am)
print('Amostra:\n{}\n'.format(amostra))
print('Hipótese aleatória:\n{}\n \nClasse da hipótese aleatória:\n{}\n'.format(hipotese,conceito))


##----Algoritmo de aprendizado de formulas disjuntivas----##

j=-1
for x in amostra:
    j+=1
    if conceito[j]==0 and checkHipo(M,x)==1:
        for i in range(len(M)):
            if M[i] is not 0:
                if checkMonomio(M[i], x):
                    M[i] = 0                                        ###Tentei fazer uma função mais bonitinha, 
                                                                    ##mas o método remove da classe list simplesmente não estava funcionando.
                                                                    #Mas esse aqui funciona perfeitamente ;) 
            
##--------------------------------------------------------##

        
print('Hipótese aprendida:\n')
printarM(M)
testHipote(M,hipotese,amostra,conceito)
print('\nTamanho da hipotese aprendida: {}'.format(len(M))) 

