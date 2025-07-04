//CREAZIONE GRAFO

    def __init__(self):
        self.grafo = nx.Graph()
        self._drivers = []
        self._idMap = {}

    def buildGraph(self, anno):
        self._graph.clear()
        self._drivers = DAO.getAllDriversbyYear(anno)
        for d in self._drivers:
            self._idMap[d.driverID] = d

        self._graph.add_nodes_from(self._drivers)

        allEdges = DAO.getDriverYearResults(anno, self._idMap)
        for e in allEdges:
                self._graph.add_edge(e[0], e[1], weight=e[2])



    def buildGraph(self, year, shape):
        self._graph.clear()
        self._nodes = DAO.getAllNodes(year, shape)

        for n in self._nodes:
            self._idMap[n.id] = n

        self._edges = DAO.getAllEdges(year, shape, self._idMap)
        self._graph.add_nodes_from(self._nodes)
        self._graph.add_edges_from(self._edges)

        # calcolo degli edges in modo programmatico
        for i in range(0, len(self._nodes) - 1):
            for j in range(i + 1, len(self._nodes)):
                if (self._nodes[i].state == self._nodes[j].state and
                    self._nodes[i].datetime < self._nodes[j].datetime):
                    self._graph.add_edge(self._nodes[i], self._nodes[j])


//METODO 1 ARCHI -> creo le connessioni che sono generiche non solo dei nodi del grafo
//per usare questo metodo la idMap deve essere generica 
// in base alle necessita le connessioni possono includere o meno il peso

    def addEdgesPesati(self):
        self._grafo.clear_edges()
        allEdges = DAO.getAllEdges()
        for edge in allEdges:
            u = self._idMapFermate[edge.id_stazP]
            v = self._idMapFermate[edge.id_stazA]

            if self._grafo.has_edge(u, v):
                self._grafo[u][v]["weight"] += 1
            else:
                self._grafo.add_edge(u, v, weight=1)

    def addEdges(self, *):
        self.grafo.clear_edges()
        allEdges = DAO.getConnessioni()
        for connessione in allEdges:
            nodo1 = self._idMap[connessione.v1]
            nodo2 = self._idMap[connessione.v2]
            if nodo1 in self.grafo.nodes and nodo2 in self.grafo.nodes:
                if self.grafo.has_edge(nodo1, nodo2) == False:
                    peso = DAO.getPeso(forma, anno, connessione.v1, connessione.v2)
                    self.grafo.add_edge(nodo1, nodo2, weight=peso)


//METODO 2 ARCHI -> itero sui nodi

    def addEdgesV1(self):
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getPeso(u, v)
                if (peso != None):
                    self._graph.add_edge(u, v, weight=peso)


    def build_graph(self, ch_min, ch_max):
        self._graph.clear()
        nodes = DAO.get_nodes(ch_min, ch_max)
        self._graph.add_nodes_from(nodes)

        for i in range(len(nodes)-1):
            for j in range(i+1, len(nodes)):
                if (self.get_localization_gene(nodes[i]) == self.get_localization_gene(nodes[j]) and
                        nodes[i].GeneID != nodes[j].GeneID and
                        (nodes[i].GeneID, nodes[j].GeneID) in self._correlations_map):
                    peso = self._correlations_map[(nodes[i].GeneID, nodes[j].GeneID)]
                    if nodes[i].Chromosome < nodes[j].Chromosome:
                        self._graph.add_edge(nodes[i], nodes[j], weight=peso)
                    elif nodes[i].Chromosome > nodes[j].Chromosome:
                        self._graph.add_edge(nodes[j], nodes[i], weight=peso)
                    else:
                        self._graph.add_edge(nodes[i], nodes[j], weight=peso)
                        self._graph.add_edge(nodes[j], nodes[i], weight=peso)

// CREAZIONE DI IdMap AL BISOGNO
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)


// CREAZIONE DEGLI EDGES PER GRAFO A MAGLIA COMPLETA
        myedges = list(itertools.combinations(self._allTeams, 2))
        self._grafo.add_edges_from(myedges)
        salariesOfTeams = DAO.getSalyOfTeams(year, self._idMapTeams)
        for e in self._grafo.edges:
            self._grafo[e[0]][e[1]]["weight"] = salariesOfTeams[e[0]] + salariesOfTeams[e[1]]

// ORDINA ARCHI
    def getSortedEdges(self):
        """Ordina gli archi del grafo in base al peso in ordine decrescente."""
        return sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)

// ORDINA NEIGHBORS
    def getSortedNeighbors(self, node):
        neighbors = self._graph.neighbors(node) # self._graph[node]
        neighbTuples = []
        for n in neighbors:
            neighbTuples.append((n, self._graph[node][n]["weight"]))

        neighbTuples.sort(key=lambda x: x[1], reverse=True)
        return neighbTuples

// DIFFERNZA FRA ARCHI USCENTI ED ENTRANTI
    def getDifference(self, node):
        migliori = {}
        pesoUscenti = 0
        pesoEntranti = 0
        peso = 0
        for n in self._grafo.nodes():
            peso = 0
            pesoEntranti = 0
            pesoUscenti = 0
            for v in self._grafo.out_edges(n):
                pesoUscenti += self._grafo[n][v[1]]['weight']
            for e in self._grafo.in_edges(n):
                pesoEntranti += self._grafo[e[0]][n]['weight']
            peso = pesoEntranti - pesoUscenti
            migliori[n] = peso
        miglioriOrdinati = sorted(migliori.items(), key=lambda x: x[1], reverse=False)
        return miglioriOrdinati[0]

// TROVA NODO MASSIMO USCENTE
    def get_node_max_uscenti(self):
        sorted_nodes = sorted(self._graph.nodes(), key=lambda n: self._graph.out_degree(n), reverse=True)
        result = []
        for i in range(min(len(sorted_nodes), 5)):
            peso_tot = 0.0
            for e in self._graph.out_edges(sorted_nodes[i], data=True):
                peso_tot += float(e[2].get("weight"))
            result.append((sorted_nodes[i], self._graph.out_degree(sorted_nodes[i]), peso_tot))
        return result


//COMPONENTE CONNESSA CONTENENTE UN NODO
        nodiConnessi = list(nx.node_connected_component(self.grafo,album))
                          

//ORDINARE LISTA DI TUPLE 
    ordinaLista = sorted(lista,key=lambda x:x[2], reverse=False)

//ORDINARE DIZIONARIO per valore
    dizioOrdinato = dict(sorted(dizio.items(), key=lambda item: item[1], reverse=True))


// CAMMINI

// CAMMINO PIU' LUNGO A PARTIRE DA UN NODO
    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._graph, source)
        nodi = list(tree.nodes())
        return nodi[1:]

    def getCammino(self, sourceStr):
        source = self._idMap[int(sourceStr)]
        lp = []

        #for source in self._graph.nodes:
        tree = nx.dfs_tree(self._graph, source)
        nodi = list(tree.nodes())

        for node in nodi:
            tmp = [node]

            while tmp[0] != source:
                pred = nx.predecessor(tree, source, tmp[0])
                tmp.insert(0, pred[0])

            if len(tmp) > len(lp):
                lp = copy.deepcopy(tmp)

        return lp


//SE ESISTE IL PERCORSO TRA DUE NODI TROVA IL MINIMO
    def esistePercorso(self, v0, v1):
        connessa = nx.node_connected_component(self._grafo, v0)
        if v1 in connessa:
            return True
        return False

    def trovaCamminoD(self, v0, v1):
        return nx.dijkstra_path(self._grafo, v0, v1)
