import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDYear(self):
        years = self._model.getAllYears()
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(year))
        self._view.update_page()

    def fillDDShape(self, e):
        year = int(self._view.ddyear.value)
        self._view.ddshape.options.clear()
        self._view.ddshape.value = None
        shapes = self._model.getAllShapes(year)
        for shape in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view.update_page()


    def handle_graph(self, e):
        year = int(self._view.ddyear.value)
        shape = self._view.ddshape.value
        if year is None or shape is None:
            self._view.txt_result1.controls.append(ft.Text("Seleziona anno e shape."))
        self._view.update_page()

        self._model.buildGraph(year, shape)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(
            f"Numero di vertici: {self._model._graph.number_of_nodes()}"
        ))
        self._view.txt_result1.controls.append(ft.Text(
            f"Numero di vertici: {self._model._graph.number_of_edges()}"
        ))
        self._view.txt_result1.controls.append(ft.Text(
            f"Il grafo ha {self._model.getNumConnected()} componenti debolmente connesse."
        ))
        # for component in self._model.getWeaklyConnectedComponents():
        #     self._view.txt_result1.controls.append(ft.Text(
        #         f"{component}"
        #     ))
        connessa = self._model.getLargestWeaklyConnectedComponents()
        self._view.txt_result1.controls.append(ft.Text(
            f"La componente connessa più grande ha: {len(connessa)} nodi:"
        ))
        for c in connessa:
            self._view.txt_result1.controls.append(ft.Text(c))
        self._view.btn_path.disabled = False
        self._view.update_page()


    def handle_path(self, e):
        #  avviare l’algoritmo di ricerca
        # Stampare a video il punteggio totale del percorso ottenuto, con il dettaglio della durata e del mese di ogni
        # avvistamento.
        path, score = self._model.getBestPath()
        self._view.txt_result2.controls.clear()
        if path is None:
            self._view.txt_result2.controls.append(ft.Text(f"Nessun percorso trovato."))
        else:
            self._view.txt_result2.controls.append(ft.Text(
                f"Punteggio totale: {score} punti."
            ))
            self._view.txt_result2.controls.append(ft.Text(
                f"Percorso trovato: {len(path)} avvistamenti"
            ))
            for s in path:
                self._view.txt_result2.controls.append(ft.Text(
                    f"Avvistamento {s.id} - {s.datetime} - {s.state} - {s.shape} - Durata: {s.duration} minuti."
                ))
        self._view.update_page()

