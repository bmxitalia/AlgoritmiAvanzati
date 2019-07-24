class GraphUpa:
	def __init__(self, m, n):
		self.m = m
		self.n = n
        self.nodeNumbers = []
        self.numNodes = 0

	def DPATrial(m):
		self.numNodes = m

		for i in range(0, m):
			for k in range(0, m):
				self.nodeNumbers.append(i)

	def RunTrial(m, numNodes):
	v = []
	for i in range (1,m*10):
		r = randint(1,m*10)
	#     print(r)
		v.append(nodeNumbers[r])
		nodeNumbers.append(numNodes)

	# merging v
	for i in range(1, len(v)):
		nodeNumbers.append(v[i])
	numNodes = numNodes + 1
	return v



	def main(m, n, numNodes):
	#   graph_upa = dict()
  		graph_upa = createCompleteGraph(m)
  		print(graph_upa)
  		for u in range(m,n):
			v = RunTrial(m, numNodes)
    		graph_upa[u] = []
    		for i in v:
      			# add u => v
      			graph_upa[u].append(i)
      
		#       print(graph_upa[i])
      			# add v => u
      			if u not in graph_upa[i]:
        			graph_upa[i].append(u)
        return graph_upa

	def createCompleteGraph(m):
		graph = dict()
  		for i in range(1,m):
    		graph[i] = []
    		for k in range(1,m):
      			if k != i:
        			graph[i].append(k)
  		return graph


    def build_graph(self):
        return self.main(self.m, self.n, self.numNodes)
