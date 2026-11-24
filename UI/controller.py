import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_collegamenti(self, e):
        """
        Funzione che controlla prima se il valore dell'importo inserito sia valido (es. non deve essere una stringa) e
        poi popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Filiali presenti
        * Numero di Collegamenti
        * Lista di Collegamenti che superano l'importo indicato come soglia
        """
        valore_input = self._view.importo_medio_minimo.value.strip()
        if valore_input == "":
            self._view.show_alert("Inserire un importo medio minimo!")
            return

        try:
            soglia = float(valore_input.replace(",", "."))
            if soglia < 0:
                self._view.show_alert("L'importo non può essere negativo.")
                return
        except ValueError:
            self._view.show_alert("Inserire un valore numerico valido.")
            return

        self._model.costruisci_grafo(soglia)

        self._view.lista_visualizzazione.controls.clear()

        num_nodi = self._model.get_num_nodes()
        num_archi = self._model.get_num_edges()
        archi = self._model.get_all_edges()

        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di Filiali (nodi): {num_nodi}")
        )
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di Collegamenti (archi): {num_archi}")
        )

        for f1, f2, data in archi:
            importo_medio = data["weight"]
            self._view.lista_visualizzazione.controls.append(
                ft.Text(f"• {f1} <-> {f2} | Importo medio: €{importo_medio:.2f}")
            )

        self._view.update()