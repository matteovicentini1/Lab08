import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        self._view._txtOut.clean()
        try:
            self.anni = int(self._view._txtYears.value)
            self.ore = int(self._view._txtHours.value)
            if self._view._ddNerc.value is None:
                self._view.create_alert('Nerc non inserito')
            else:
                lista,time,popolo = self._model.worstCase(self._view._ddNerc.value,self.anni,self.ore)
                self._view._txtOut.controls.append(ft.Text(f'Waiting...'))
                self._view.update_page()
                self._view._txtOut.clean()
                self._view._txtOut.controls.append(ft.Text(f'Totale persone colpite: {popolo}'))
                self._view._txtOut.controls.append(ft.Text(f'Totale ore di disservizio: {time}'))
                for i in lista:
                    self._view._txtOut.controls.append(ft.Text(i))
                self._view.update_page()

        except ValueError:
            self._view.create_alert('Ore o anni non inseriti correttamente')

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
