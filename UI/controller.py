import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        n_alb=int(self._view.txtNumAlbumMin.value)
        if n_alb < 0:
            self._view.create_alert("ALZA DA 0")
            return
        else:
            self._model.build_graph(n_alb)
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"{self._model._graph}"))
            self._view.ddArtist.disabled= False
            self._view.btnArtistsConnected.disabled = False
            #mi riferisco a qui(risolto con aiuto professore)
            for e in self._model.lista_artisti_con_nome:
                self._view.ddArtist.options.append(ft.dropdown.Option(key=e[0][0], text=e[0][1]))
            self._view.update_page()


    def handle_connected_artists(self, e):
        a1=int(self._view.ddArtist.value)
        lista_artisti=self._model.artisti_collegati(a1)
        self._view.txt_result.controls.clear()
        #come prima non capisco perchè anche se la lista itera su 3 oggetti mi dice che ne ha solo 1
        for a1, a2, weight in lista_artisti:
            self._view.txt_result.controls.append(ft.Text(f"artista num:{a2} - generi in comune {weight}"))
        self._view.update_page()


