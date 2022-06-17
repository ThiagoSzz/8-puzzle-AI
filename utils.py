def estado_para_tabela(estado):
    """Conversão de uma string que representa o estado para uma matriz 3x3 que 
    representa a tabela do jogo.

    Args:
        estado (str): estado de um nodo

    Returns:
        [list]: matriz (lista de listas) contendo as peças do jogo
    """

    # divisão da string em uma matriz 3x3
    tabela = list()

    tabela.append(list(estado[0:3]))
    tabela.append(list(estado[3:6]))
    tabela.append(list(estado[6:9]))

    return tabela


def tabela_para_estado(tabela):
    """Conversão de uma matriz que representa a tabela do jogo para uma string 
    que representa o estado de um nodo.

    Args:
        tabela (list): matriz contendo as peças do jogo

    Returns:
        [str]: estado de um nodo
    """

    estado = str()

    for i in tabela:
        for j in i:
            estado += j

    return estado


def imprime_tabela(tabela):
    """Impressão da matriz que representa a tabela do jogo

    Args:
        tabela (list): matriz contendo as peças do jogo
    """

    for i in range(3):
        print('|', end='')
        for j in range(3):
            print(f'{tabela[i][j]}', end='')
        print('|', end='')
        print('')

def hamming(estado):
    """Cálculo da distância de Hamming (número de peças fora do lugar) de um estado.

    Args:
        estado (str): representa o estado de um nodo

    Returns:
        [int]: distância de Hamming
    """

    # inicializa a variável que representa a distância
    distancia_hamming = 0

    # converte a string do estado em uma lista de numeros
    # o valor "_" será representado como o número 9
    # e não deve ser considerado uma peça
    lista_char = list()

    for i in estado:
        if(i == '_'):
            i = 9

        lista_char.append(int(i))

    # verifica quantos valores distoam da sequência "12345678_"
    for i in range(0,8):
        if(lista_char[i] != i+1):
            distancia_hamming += 1

    return distancia_hamming


def manhattan(estado):
    """Cálculo da distância Manhattan de um estado.

    Args:
        estado (str): representa o estado de um nodo

    Returns:
        [int]: distância Manhattan
    """

    # inicializa a variável que representa a distância
    distancia_manhattan = 0

    # converte as strings de estado inicial e final para uma tabela
    tabela_estado_inicial = estado_para_tabela(estado)
    tabela_estado_final = estado_para_tabela('12345678_')

    # agrupa os valores que distoam entre estas tabelas em uma lista
    diferente = list()

    for i in range(0,3):
        for j in range(0,3):
            if(tabela_estado_inicial[i][j] != tabela_estado_final[i][j]):
                diferente.append(tabela_estado_inicial[i][j])
    
    # o valor "_" não deve ser considerado uma peça
    if('_' in diferente):
        diferente.remove('_')

    # obtém as posições x e y dos valores nas tabelas dos estados
    # inicial e final
    inicial = list()
    final = list()

    for i in diferente:
        for j in range(0,3):
            for k in range(0,3):
                if(i == tabela_estado_inicial[j][k]):
                    inicial.append((j,k))

                if(i == tabela_estado_final[j][k]):
                    final.append((j,k))

    # calcula a distância manhattan
    for i in range(0, len(diferente)):
        distancia_manhattan += abs(inicial[i][0] - final[i][0]) + abs(inicial[i][1] - final[i][1])

    return distancia_manhattan