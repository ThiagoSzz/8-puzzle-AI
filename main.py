import copy
from queue import PriorityQueue
import utils


class Nodo:
    """Classe que representa os nodos do grafo de busca.
    """

    def __init__(self, estado, pai, acao, custo):
        """Inicialização da classe Nodo.

        Args:
            estado (str): representa o valor do estado que corresponde a formação da tabela do jogo
            pai (Nodo): nodo pai (None, caso seja raíz)
            acao (str): movimento executado para sair do estado do nodo pai até o estado do nodo filho (None, caso seja raíz)
            custo (int): custo do caminho a partir do estado inicial até o nodo (0, caso seja raíz)
        """

        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo


def sucessor(estado):
    """Recebe um estado (string) e retorna uma lista de tuplas (ação, estado atingido) para cada 
    ação possível no estado recebido. Tanto a ação quanto o estado atingido são strings também.

    Args:
        estado (str): estado de um nodo

    Returns:
        [list]: lista de tuplas <ação, estado atingido>
    """
    
    # procura a posição do espaço vazio
    tabela = utils.estado_para_tabela(estado)
    linha = 0
    achou = False

    for i in tabela:
        for j in i:
            if(j == '_'):
                coluna = i.index(j)
                achou = True
        
        if(not achou):
            linha += 1

    # verifica quais possíveis movimentos do espaço vazio
    movimentos = ['esquerda', 'direita', 'acima', 'abaixo']

    # linha 0 := não pode se mover acima
    # linha 2 := não pode se mover abaixo
    if(linha == 0):
        del(movimentos[2])
    elif(linha == 2):
        del(movimentos[3])
    
    # coluna 0 := não pode se mover para a esquerda
    # coluna 2 := não pode se mover para a direita
    if(coluna == 0):
        del(movimentos[0])
    elif(coluna == 2):
        del(movimentos[1])

    # calcula os resultados com os possíveis movimentos
    possiveis_sucessores = list()

    for i in movimentos:
        nova_tabela = proximo_passo(i, tabela, linha, coluna)
        possiveis_sucessores.append((i, utils.tabela_para_estado(nova_tabela)))

    return possiveis_sucessores
    
def proximo_passo(movimento, tabela, linha, coluna):
    """Calcula o resultado de um possível movimento que pode ser executado pelo espaço vazio.

    Args:
        movimento (str): ação executada por um nodo a fim de atingir um estado diferente
        tabela (list): matriz contendo as peças do jogo
        linha (int): representa uma linha da matriz
        coluna ([type]): representa uma coluna da matriz

    Returns:
        [list]: matriz contendo o resultado da ação executada
    """

    # cria uma cópia da tabela original
    nova_tabela = copy.deepcopy(tabela)

    # executa a troca da peça "_" com algum movimento
    if(movimento == 'esquerda'):
        peca_trocar = tabela[linha][coluna-1]
        nova_tabela[linha][coluna-1] = tabela[linha][coluna]
        nova_tabela[linha][coluna] = peca_trocar
    elif(movimento == 'direita'):
        peca_trocar = tabela[linha][coluna+1]
        nova_tabela[linha][coluna+1] = tabela[linha][coluna]
        nova_tabela[linha][coluna] = peca_trocar
    elif(movimento == 'acima'):
        peca_trocar = tabela[linha-1][coluna]
        nova_tabela[linha-1][coluna] = tabela[linha][coluna]
        nova_tabela[linha][coluna] = peca_trocar
    elif(movimento == 'abaixo'):
        peca_trocar = tabela[linha+1][coluna]
        nova_tabela[linha+1][coluna] = tabela[linha][coluna]
        nova_tabela[linha][coluna] = peca_trocar

    return nova_tabela

def expande(nodo):
    """Recebe um nodo (objeto da classe Nodo) e retorna um iterable de nodos. Cada nodo do iterable
    contém um estado sucessor do nó recebido.

    Args:
        nodo (Nodo): objeto que representa um nodo do grafo

    Returns:
        [list]: lista de nodos expandidos
    """
    
    # obtém os possíveis sucessores de um estado
    possiveis_sucessores = sucessor(nodo.estado)

    # cria um nodo para cada um desses estados e armazena em uma lista
    nodos_sucessores = list()

    for i in possiveis_sucessores:
        nodos_sucessores.append(Nodo(i[1], nodo, i[0], nodo.custo+1))

    return nodos_sucessores


def bfs(estado):
    """Recebe um estado (string), executa a busca em largura e retorna uma lista de ações que leva do
    estado recebido até o objetivo ('12345678_'). Caso não haja solução a partir do estado recebido, retorna None.

    Args:
        estado (str): representa o estado de um nodo

    Returns:
        [list]: lista de ações a serem executadas para levar de um estado especificado até o estado final
    """
    
    # inicializa as estruturas para armazenar os nodos explorados, a fronteira e o caminho
    explorados = set()

    caminho = list()

    fronteira = list()
    fronteira.append(Nodo(estado, None, None, 0))

    #nos_expandidos = 1

    # bfs
    while True:
        if(len(fronteira) == 0):
            return None
        
        # fila := remove o primeiro valor inserido
        atual = fronteira.pop(0)

        # verifica se já atingiu o estado final
        if(atual.estado == '12345678_'):
            procurado = atual
            
            if(procurado.pai is None):
                return []
            
            # encontra o caminho do estado final até o inicial por meio do nodo pai
            caminho.append(procurado.acao)

            while True:
                if(procurado.pai.acao is not None):
                    caminho.append(procurado.pai.acao)
                    procurado = procurado.pai
                else:
                    break

            #return nos_expandidos
            #return len(caminho)
            return list(reversed(caminho))

        # insere apenas o estado de um nodo nos conjunto dos nodos explorados
        if(atual.estado not in explorados):
            explorados.add(atual.estado)
            
            # expande a fronteira, inserindo os nodos vizinhos do último nodo avaliado
            nodos_vizinhos = expande(atual)

            for i in nodos_vizinhos:
                fronteira.append(i)
                #nos_expandidos += 1


def dfs(estado):
    """Recebe um estado (string), executa a busca em profundidade e retorna uma lista de ações que leva do
    estado recebido até o objetivo ('12345678_'). Caso não haja solução a partir do estado recebido, retorna None.

    Args:
        estado (str): representa o estado de um nodo

    Returns:
        [list]: lista de ações a serem executadas para levar de um estado especificado até o estado final
    """
    
    # inicializa as estruturas para armazenar os nodos explorados, a fronteira e o caminho
    explorados = set()

    caminho = list()

    fronteira = list()
    fronteira.append(Nodo(estado, None, None, 0))

    #nos_expandidos = 1

    # dfs
    while True:
        if(len(fronteira) == 0):
            return None
        
        # pilha := remove o último valor inserido
        atual = fronteira.pop(-1)

        # verifica se já atingiu o estado final
        if(atual.estado == '12345678_'):
            procurado = atual
            
            if(procurado.pai is None):
                return []
            
            # encontra o caminho do estado final até o inicial por meio do nodo pai
            caminho.append(procurado.acao)

            while True:
                if(procurado.pai.acao is not None):
                    caminho.append(procurado.pai.acao)
                    procurado = procurado.pai
                else:
                    break

            #return nos_expandidos
            #return len(caminho)
            return list(reversed(caminho))

        # insere apenas o estado de um nodo nos conjunto dos nodos explorados
        if(atual.estado not in explorados):
            explorados.add(atual.estado)
            
            # expande a fronteira, inserindo os nodos vizinhos do último nodo avaliado
            nodos_vizinhos = expande(atual)

            for i in nodos_vizinhos:
                fronteira.append(i)
                #nos_expandidos += 1


def astar_hamming(estado):
    """Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do estado recebido até o objetivo ('12345678_'). Caso não
    haja solução a partir do estado recebido, retorna None.

    Args:
        estado (str): representa o estado de um nodo

    Returns:
        [list]: lista de ações a serem executadas para levar de um estado especificado até o estado final
    """
    
    # inicializa as estruturas para armazenar os nodos explorados, a fronteira e o caminho
    explorados = set()

    caminho = list()

    # fronteira implementada utilizando a fila de prioridades (min-heap)
    # como o nodo raíz tem custo zero, a função custo será determinada apenas pela distância de Hamming
    fronteira = PriorityQueue()
    fronteira.put((utils.hamming(estado), Nodo(estado, None, None, utils.hamming(estado))))

    #nos_expandidos = 1

    # a* hamming
    while True:
        if(fronteira.empty()):
            return None
        
        # fila de prioridades := remove a tupla de menor custo
        atual = fronteira.get()[-1]

        # verifica se já atingiu o estado final
        if(atual.estado == '12345678_'):
            procurado = atual
            
            if(procurado.pai is None):
                return []
            
            # encontra o caminho do estado final até o inicial por meio do nodo pai
            caminho.append(procurado.acao)

            while True:
                if(procurado.pai.acao is not None):
                    caminho.append(procurado.pai.acao)
                    procurado = procurado.pai
                else:
                    break

            #return nos_expandidos
            #return len(caminho)
            return list(reversed(caminho))

        # insere apenas o estado de um nodo nos conjunto dos nodos explorados
        if(atual.estado not in explorados):
            explorados.add(atual.estado)
            
            # expande a fronteira, inserindo os nodos vizinhos do último nodo avaliado
            nodos_vizinhos = expande(atual)

            for i in nodos_vizinhos:
                # insere a tupla <função de custo, id do objeto, nodo> na fronteira
                fronteira.put((i.custo + utils.hamming(i.estado), id(i), i))
                #nos_expandidos += 1


def astar_manhattan(estado):
    """Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do estado recebido até o objetivo ('12345678_'). Caso não
    haja solução a partir do estado recebido, retorna None.

    Args:
        estado (str): representa o estado de um nodo

    Returns:
        [list]: lista de ações a serem executadas para levar de um estado especificado até o estado final
    """
    
    # inicializa as estruturas para armazenar os nodos explorados, a fronteira e o caminho
    explorados = set()

    caminho = list()

    # fronteira implementada utilizando a fila de prioridades (min-heap)
    # como o nodo raíz tem custo zero, a função custo será determinada apenas pela distância Manhattan
    fronteira = PriorityQueue()
    fronteira.put((utils.manhattan(estado), Nodo(estado, None, None, utils.manhattan(estado))))

    #nos_expandidos = 1

    # a* manhattan
    while True:
        if(fronteira.empty()):
            return None
        
        # fila de prioridades := remove a tupla de menor custo
        atual = fronteira.get()[-1]

        # verifica se já atingiu o estado final
        if(atual.estado == '12345678_'):
            procurado = atual
            
            if(procurado.pai is None):
                return []
            
            # encontra o caminho do estado final até o inicial por meio do nodo pai
            caminho.append(procurado.acao)

            while True:
                if(procurado.pai.acao is not None):
                    caminho.append(procurado.pai.acao)
                    procurado = procurado.pai
                else:
                    break

            #return nos_expandidos
            #return len(caminho)
            return list(reversed(caminho))

        # insere apenas o estado de um nodo nos conjunto dos nodos explorados
        if(atual.estado not in explorados):
            explorados.add(atual.estado)
            
            # expande a fronteira, inserindo os nodos vizinhos do último nodo avaliado
            nodos_vizinhos = expande(atual)

            for i in nodos_vizinhos:
                # insere a tupla <função de custo, id do objeto, nodo> na fronteira
                fronteira.put((i.custo + utils.manhattan(i.estado), id(i), i))
                #nos_expandidos += 1

print(astar_manhattan('2_3541687'))