from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutte le Filiali (i nodi) presenti e filtrando i Collegamenti con
        importo medio per bonifico >= threshold (euro)
        """
        self.G.clear()
        self._nodes = DAO.get_filiali()
        self.G.add_nodes_from(self._nodes.values())
        self._edges = DAO.get_collegamenti()

        for f1_id, f2_id, importo_medio in self._edges:
            if importo_medio >= threshold:
                self.G.add_edge(self._nodes[f1_id], self._nodes[f2_id], weight=importo_medio)

    def get_num_edges(self):
        """
        Restituisce il numero di Collegamenti (edges) del grafo
        :return: numero di edges del grafo
        """
        return self.G.number_of_edges()

    def get_num_nodes(self):
        """
        Restituisce il numero di Filiali (nodi) del grafo
        :return: numero di nodi del grafo
        """
        return self.G.number_of_nodes()

    def get_all_edges(self):
        """
        Restituisce tutti i Collegamenti (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        return list(self.G.edges(data=True))