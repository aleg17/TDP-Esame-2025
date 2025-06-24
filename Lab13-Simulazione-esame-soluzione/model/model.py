from database.DAO import DAO
import networkx as nx
import copy
class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._drivers = []
        self._idMap = {}

        self._bestPath = []
        self._bestScore = 0

    def getDreamTeam(self, k):
        self._bestPath = []
        self._bestScore = 1000

        parziale = []
        self._ricorsione(parziale, k)
        return self._bestPath, self._bestScore
    def _ricorsione(self, parziale, k):
        if len(parziale) == k:
            if self.getScore(parziale) < self._bestScore:
                self._bestScore = self.getScore(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return

        for n in self._graph.nodes():
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, k)
                parziale.pop()

    def getScore(self, team):
        score = 0
        for e in self._graph.edges(data=True):
            if e[0] not in team and e[1] in team:
                score += e[2]["weight"]
        return score


    def getYears(self):
        return DAO.getAllYears()

    def buildGraph(self, anno):
        self._graph.clear()
        self._drivers = DAO.getAllDriversbyYear(anno)
        for d in self._drivers:
            self._idMap[d.driverID] = d

        self._graph.add_nodes_from(self._drivers)

        allEdges = DAO.getDriverYearResults(anno, self._idMap)
        for e in allEdges:
                self._graph.add_edge(e[0], e[1], weight=e[2])

        #self.getBestDriver()
    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()
    def getBestDriver(self):
        best = 0
        bestdriver = None
        for n in self._graph.nodes:
            score = 0
            for e_out in self._graph.out_edges(n, data=True):
                score += e_out[2]["weight"]
            for e_in in self._graph.in_edges(n, data=True):
                score -= e_in[2]["weight"]

            if score > best:
                 bestdriver = n
                 best = score

        print(f"Best driver: {bestdriver}, with score {best}")
        return bestdriver, best


