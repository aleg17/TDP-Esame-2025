from model.model import Model

model = Model()
model.buildGraph()
print(model.getGraphDetails())

conn = list(model.getConnesse())
conn.sort(key=lambda x: len(x), reverse=True)
