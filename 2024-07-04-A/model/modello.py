import copy

from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting


class Model:
    def __init__(self):
        self._occorrenzeMese = None
        self._bestScore = None
        self._bestPath = None
        self._edges = None
        self._nodes = None
        self._graph = nx.DiGraph()
        self._idMap = {}

    def getAllYears(self):
        return DAO.get_all_years()

    def getAllShapes(self, year: int):
        return DAO.getAllShapes(year)


    def buildGraph(self, year, shape):
        self._graph.clear()
        self._nodes = DAO.getAllNodes(year, shape)

        for n in self._nodes:
            self._idMap[n.id] = n

        self._edges = DAO.getAllEdges(year, shape, self._idMap)
        self._graph.add_nodes_from(self._nodes)
        self._graph.add_edges_from(self._edges)

        """ 
        !!!! Importante !!!!
        """
        # calcolo degli edges in modo programmatico
        # for i in range(0, len(self._nodes) - 1):
        #     for j in range(i + 1, len(self._nodes)):
        #         if (self._nodes[i].state == self._nodes[j].state and
        #             self._nodes[i].datetime < self._nodes[j].datetime):
        #             self._graph.add_edge(self._nodes[i], self._nodes[j])

    def getLargestWeaklyConnectedComponents(self):
        conn = list(nx.weakly_connected_components(self._graph))
        conn.sort(key=lambda x: len(x), reverse=True)
        return conn[0]

    def getNumConnected(self):
        return nx.number_weakly_connected_components(self._graph)


    # Dato il grafo costruito al punto precedente, si vuole identificare un cammino sul grafo costituito da avvistamenti di
    # durata sempre crescente (strettamente crescente) che massimizzi un punteggio composto dai seguenti termini:
    # •  +100 punti per ogni avvistamento nel cammino
    # • +200 punti per ogni avvistamento del cammino che è occorso nello stesso mese dell’avvistamento
    # precedente (ovviamente non applicabile al primo avvistamento del cammino, dato che non ha un
    # avvistamento che lo precede).
    # Inoltre, il cammino può contenere al massimo 3 avvistamenti dello stesso mese.
    # Nota bene: nel calcolo del cammino un arco può essere percorso solo nella sua direzione, ovvero un arco diretto da
    # A verso B non può essere percorso da B ad A.


    def getBestPath(self):
        self._bestPath = []
        self._bestScore = 0
        self._occorrenzeMese = dict.fromkeys(range(1, 13), 0) # Mesi da 1 a 12, inizializzati a 0

        # {
        #     1: 0,
        #     2: 0,
        #     3: 0,
        #     4: 0,
        #     5: 0,
        #     6: 0,
        #     7: 0,
        #     8: 0,
        #     9: 0,
        #     10: 0,
        #     11: 0,
        #     12: 0
        # }

        for nodo in self._nodes:
            self._occorrenzeMese[nodo.datetime.month] += 1 # incremento il mese di avvistamento
            successiviDurataCrescente = self._calcolaSuccessivi(nodo)
            self._recursion([nodo], successiviDurataCrescente)
            self._occorrenzeMese[nodo.datetime.month] -= 1
        return self._bestPath, self._bestScore


    def _recursion(self, parziale: list[Sighting], successivi: list[Sighting]):
        if len(successivi) == 0:
            score = Model.getScore(parziale)
            if score > self._bestScore:
                self._bestScore = score
                self._bestPath = copy.deepcopy(parziale)
            else:
                for nodo in successivi:
                    # aggiungo il nodo in parziale e aggiorno le occorrenze del mese
                    parziale.append(nodo)
                    self._occorrenzeMese[nodo.datetime.month] += 1
                    # calcolo i successivi del nodo aggiunto
                    nuoviSuccessivi = self._calcolaSuccessivi(nodo)
                    # chiamo ricorsivamente la funzione
                    self._recursion(parziale, nuoviSuccessivi)
                    # rimuovo il nodo da parziale e aggiorno le occorrenze del mese
                    # sto facendo il backtracking
                    self._occorrenzeMese[parziale[-1].datetime.month] -= 1
                    parziale.pop()


    def _calcolaSuccessivi(self, nodo: Sighting) -> list[Sighting]:
        """ Calcola il sottoinsieme dei successivi ad un nodo, che hanno durata superiore a quella
        del nodo, senza eccedere il numero ammissibile di occorrenze per mese. """
        successivi = self._graph.successors(nodo)
        successiviAmmissibili = []
        for s in successivi:
            if s.duration > nodo.duration and self._occorrenzeMese[s.datetime.month] < 3:
                successiviAmmissibili.append(s)
        return successiviAmmissibili


    @staticmethod
    def getScore(cammino: list[Sighting]) -> int:
        """ Funzione che calcola il punteggio di un cammino dato in input.
        :param cammino: il cammino che si vuole valutare.
        :return: il punteggio del cammino
        """
        score = 100 * len(cammino)
        for i in range(1, len(cammino)): # inizio da 1 perché il primo nodo non ha un precedente
            if cammino[i].datetime.month == cammino[i - 1].datetime.month: # se il mese è lo stesso
                score += 200
        return score



