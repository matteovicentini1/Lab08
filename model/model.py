import copy

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self.tempo=0
        self.toppopolo=-1

    def serchnerc(self,nome):
        for i in self._listNerc:
            if i._value==nome:
                return i

    def worstCase(self, nerc, maxY, maxH):
        #reset
        self._solBest=[]
        self.tempo=0
        self.toppopolo=0
        #selezioni gli eventi del nerc
        selectnerc = self.serchnerc(nerc)
        self.loadEvents(selectnerc)
        #chiami la ricorsione
        self.ricorsione([],maxY,maxH,0)
        return self._solBest,self.tempo,self.toppopolo
    def ricorsione(self, parziale, maxY, maxH,pp):
        if (pp)>=len(self._listEvents):
            if (self.toppopolo==-1 or self.toppopolo<self.contapopolo(parziale)) :
                self.toppopolo= self.contapopolo(parziale)
                self.tempo=self.tempistica(parziale)
                self._solBest=copy.deepcopy(parziale)
        else:
            for i in range(pp,len(self._listEvents)):
                pp += 1
                parziale.append(self._listEvents[i])
                if self.controlloanni(parziale,maxY)==True and self.tempistica(parziale)<=maxH:
                    self.ricorsione(parziale,maxY,maxH,pp)
                parziale.pop()

    def tempistica(self,parziale):
        if len(parziale)==0:
            return 0
        else:
            t=0
            for i in parziale:
                t+=(abs(i._date_event_finished-i._date_event_began)).total_seconds()/3600
            return t

    def contapopolo(self,li):
        popolo=0
        for i in li:
            popolo+=i._customers_affected
        return popolo

    def controlloanni(self,parziale,ranges):
        if len(parziale)<=1:
            return True
        else:
            ft=[]
            for i in range(len(parziale)-1):
                ultimoanno = parziale[i+1]._date_event_finished.year
                annozero = parziale[0]._date_event_finished.year
                if abs(annozero - ultimoanno) >ranges:
                    ft.append(False)
            return all(ft)





    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc