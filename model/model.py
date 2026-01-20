import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.load_all_artists()
        self.lista_artisti=[]
        self.lista_artisti_con_nome=[]

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        self.lista_artisti=DAO.get_artists_with_soglia(min_albums)
        for a in self.lista_artisti:
            self.lista_artisti_con_nome.append(DAO.get_nomi_da_id(a))
        print(self.lista_artisti_con_nome)


    def build_graph(self, min_albums):
        self._graph = nx.Graph()
        self.load_artists_with_min_albums(min_albums)
        for a in self.lista_artisti:
            self._graph.add_node(a)
        lista_archi = DAO.get_archi_with_peso()
        for a1, a2, weight in lista_archi:
            if a1 in self._graph and a2 in self._graph:
                self._graph.add_edge(a1, a2, weight= weight)


    def artisti_collegati(self, a1:int):
        lista_artisti_connessi=[]
        comp=nx.node_connected_component(self._graph, a1)
        for a in comp:
            lista_artisti_connessi.append(DAO.get_peso_from_archi(a1, a))
        return lista_artisti_connessi





