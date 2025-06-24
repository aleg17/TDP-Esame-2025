from model.model import Model

mymodel = Model()
mymodel.buildGraph(60*60*1000)
print(mymodel.getGraphDeails())
mymodel.getNodeI(261)

mymodel._getSetAlbum(mymodel._getNodeI(261), )