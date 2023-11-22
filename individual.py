class Individual():
    def __init__(self, elment , puzleorder):
        self.elements = elment
        self.puzzelorder = puzleorder
        self.numtags = 0
        self.numevent = 0
        self.numxss = 0
        self.fitness = 0
        self.update()
        
    def update(self):
        count_tag=0
        count_xss =0
        count_event_or_attr =0
        for p in self.puzzelorder:
            if p == 1 :
                count_tag +=1
            elif p in [3,2]:
                count_event_or_attr +=1
            elif p ==4:
                count_xss +=1
        self.numtags =count_tag
        self.numevent = count_event_or_attr
        self.numxss = count_xss

    def __str__(self):
        return 'Fitness {0}: {1} - {2}'.format(self.fitness, self.puzzelorder,self.elements).ljust(10) 


# c = ['<iframe', 'onpause=', "alert(document.cookie)'", '>']
# pord = [1,3,4,5]
# ind = Individual(elment=c,puzleorder=pord)
# # ind.update()
# print(ind)