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
        #selezioni gli eventi del nerc
        selectnerc = self.serchnerc(nerc)
        self.loadEvents(selectnerc)
        #chiami la ricorsione
        self.ricorsione([],maxY,maxH,copy.deepcopy(self._listEvents))
        return self._solBest
    def ricorsione(self, parziale, maxY, maxH, pos):
        if len(pos)==0 :
            if self.toppopolo==-1 or self.toppopolo<self.contapopolo(parziale):
                self.toppopolo= self.contapopolo(parziale)
                self._solBest=copy.deepcopy(parziale)
        else:
            for i in pos:
                oreprovv=(i._date_event_finished-i._date_event_began).total_seconds()/3600
                parziale.append(i)
                if self.controlloore(oreprovv,maxH)==True and self.controlloanni(parziale,maxY)==True:
                    c=copy.deepcopy(pos)
                    c.remove(i)
                    self.tempo+=oreprovv
                    print(parziale)
                    print(self.tempo)
                    self.ricorsione(parziale,maxY,maxH,c)
                parziale.pop()

    def contapopolo(self,li):
        popolo=0
        for i in li:
            popolo+=i._customers_affected
        return popolo



    def controlloanni(self,parziale,range):
        if len(parziale)<=1:
            return True
        else:
            ultimoanno = parziale[-1]._date_event_finished.year
            annozero = parziale[0]._date_event_finished.year
            if abs(annozero - ultimoanno) >range:
                return False
            return True




    def controlloore(self,daaggiungere,tmax):
        if (self.tempo+daaggiungere)>tmax:
            return False
        return True


    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc