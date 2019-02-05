import tkinter as tk

class GUIClass:

    itemDict = {}
    pairDict = {}
    listPairKeys = []
    nameList = []
    keyList = []
    def __init__(self,itemDict,pairDict,listPairKeys):
        self.itemDict = itemDict
        self.pairDict = pairDict
        self.listPairKeys = listPairKeys

    def getRecommandationList(self,purchaseItem):
        # init recommandation list
        recommandList = []
        
        # find out frequently bought together items in a trained model
        for aKey in self.pairDict.keys():
            #print(listPairKeys[aKey])
            if purchaseItem in self.listPairKeys[aKey]:
                # id found then add in recommandation list
                recommandList.extend(self.listPairKeys[aKey])
        #print('Recommandation')
        try:
            while(True):
                # remove self item
                recommandList.remove(purchaseItem)
        except Exception:
            #do nothing
            tIgnore = False
        
        # print recommandation item list
        if len(recommandList)==0:
            #print('No Items found for Recommandation')
            return []
        else :
            tmpList = list(set(recommandList))
            recommValueList = []
            for itemId in tmpList :
                recommValueList.append(self.itemDict[itemId])
            return recommValueList 

        
    def dialog(self,val):
        otherList = self.getRecommandationList(val)
        #print(otherList )
        Lb2 = tk.Listbox(self.top,width=25)
        Lb2.configure(exportselection=False)
        #Lb2.configure(state=tk.DISABLED)
        Lb2.grid(row=1,column=1)
        Lb2.delete(0, tk.END)
        for i in otherList :
            Lb2.insert(tk.END,i)
        

    def CurSelet(self,event):
        widget = event.widget
        selection=widget.curselection()
        # selected index
        index = selection[0]
        self.dialog(self.keyList[index])
        
    def displayGUI(self):
        self.top = tk.Tk()
        self.top.title('Food Menu List')
        
        for key,value in self.itemDict.items():
            self.nameList.append(value)
            self.keyList.append(key)
        
        tk.Label(self.top, text="Menu (Item List)").grid(row=0,column=0)
        tk.Label(self.top, text="Recommandation Items").grid(row=0,column=1)
        
        frm = tk.Frame(self.top)
        frm.grid(row=1,column=0,sticky=tk.N+tk.S)
        
        self.top.rowconfigure(1, weight=1)
        self.top.columnconfigure(1, weight=1)

        
        scrollbar = tk.Scrollbar(frm, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        Lb1 = tk.Listbox(frm,width=25,yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=Lb1.yview)        
        Lb1.pack(expand=True, fill=tk.Y)
        Lb2 = tk.Listbox(self.top,width=25)
        Lb2.grid(row=1,column=1,sticky=tk.E+tk.W+tk.N+tk.S)
        Lb2.configure(exportselection=False)
        #Lb2.configure(state=tk.DISABLED)
        
        Lb1.bind('<<ListboxSelect>>',self.CurSelet)
        
        for i in self.nameList:
            Lb1.insert(tk.END,i)
            
        #Lb1.pack()
        #Lb2.pack()
        self.top.mainloop()
