from tkinter import E
import networkx as nx
import matplotlib.pyplot as plt

class Queue:
    def __init__(self):
        self.traversed = list()
        self.csr = {
            'vertex_id': list(),
            'adjacency_list': list()
        }
        self.queue = list()
        self.bestpath = list()
        self.int_pointer = -1

    def showGraph(self, graphCsr):
        # from documentation of networkx
        G = nx.Graph()
        edge_cache = list()
        path_cache = list()
        idx = 0
        while idx < len(graphCsr['vertex_id'])-1:
            u = graphCsr['vertex_id'][idx][0]
            s = graphCsr['vertex_id'][idx][1]
            e = graphCsr['vertex_id'][idx+1][1]
            edges = graphCsr['adjacency_list'][s:e]
            for edge in edges:
                if (edge[0], u) not in edge_cache:
                    edge_cache.append((u, edge[0]))
                    if edge[2]:
                        path_cache.append((u, edge[0]))
                    G.add_edge(u, edge[0], weight=edge[1])
            idx+=1
        edges_costly = [(u, v) for (u, v) in edge_cache if (u, v) not in path_cache]
        pos = nx.spring_layout(G, seed=7)
        nx.draw_networkx_nodes(G, pos, node_size=700)
        nx.draw_networkx_edges(G, pos, edgelist=edges_costly, width=6)
        nx.draw_networkx_edges(G, pos, edgelist=path_cache, width=6, edge_color="red")
        nx.draw_networkx_labels(G, pos, font_size=20)
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
    
    def getNeighbors(self, node, graph):
        li = list()
        for element in graph:
            try:
                u = element['source']
                v = element['destination']
                w = element['weight']
            except:
                u = element[0]
                v = element[1]
                w = element[2]
            try:
                if 'path' in element.keys():
                    p = element['path']
                else:
                    p = element[3]
            except:
                p = False
            if u == node:
                li.append((u, v, w, p))
        return li

    def generateCsr(self, ip):
        try:
            all_start = set(list(map(lambda x: x['source'], ip)))
        except:
            all_start = set(list(map(lambda x: x[0], ip)))
        idx = 0
        for node in all_start:
            neighbors = self.getNeighbors(node, ip)
            self.csr['vertex_id'].append((node, idx))
            idx+=len(neighbors)
            for neighbor in neighbors:
                self.csr['adjacency_list'].append(list((neighbor[1], neighbor[2], neighbor[3])))
        self.csr['vertex_id'].append(("", len(self.csr['adjacency_list'])+1))

    def startBfs(self, start, end, current = None):
        if current == None:
            current = start
        self.traversed.append(current)
        id_start = [s for idx, s in self.csr['vertex_id'] if idx == current][0]
        id_end = [e for _, e in self.csr['vertex_id'] if e > id_start][0]
        members = self.csr['adjacency_list'][id_start:id_end]
        for member in members:
            self.enqueue(current, member)
        if current == end:
            self.setBestPath(start, end)
            return
        newcurrent = current
        while newcurrent in self.traversed and self.int_pointer < len(self.queue)-1:
            self.int_pointer += 1
            newcurrent = self.queue[self.int_pointer][0][-1]
        if newcurrent == current:
            return
        self.startBfs(start, end, newcurrent)
    
    def setBestPath(self, start, end):
        onlypath = [a for a in self.queue if a[0][0] == start and a[0][-1] == end]
        minimum = None
        min_idx = -1
        for idx, member in enumerate(onlypath):
            _, cost = member
            if minimum == None:
                minimum = cost
                min_idx = 0
            elif cost < minimum:
                minimum = cost
                min_idx = idx
        self.bestpath = onlypath[min_idx]
        idx = 0
        path = self.bestpath[0]
        while idx < len(path):
            first = path[idx]
            if len(path) == idx+1:
                second = ""
            else:
                second = path[idx+1]
            self.setPathCsr(first, second)
            self.setPathCsr(second, first)
            idx+=1

    def setPathCsr(self, first, second):
        idx = 0
        found = False
        while idx < len(self.csr['vertex_id'])-1:
            if first == self.csr['vertex_id'][idx][0]:
                start = self.csr['vertex_id'][idx][1]
                end = self.csr['vertex_id'][idx+1][1]
                adjacency_list = self.csr['adjacency_list'][start:end]
                for idx2, destination in enumerate(adjacency_list):
                    dest,_,_ = destination
                    if dest == second:
                        self.csr['adjacency_list'][start+idx2][2] = True
                        found = True
                        break
                if found:
                    break
            idx+=1

    def enqueue(self, s_node, paths):
        added = False
        for path, cost in self.queue:
            testpath = path.copy()
            v = testpath.pop()
            if v == s_node:
                testpath.append(v)
                testpath.append(paths[0])
                newcost = cost + paths[1]
                newrow = list((testpath, newcost))
                added = True
                self.queue.append(newrow)
        if not added:
            newrow = list((list((s_node, paths[0])), paths[1]))
            self.queue.append(newrow)