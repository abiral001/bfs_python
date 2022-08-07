import modules.queue as queue
import modules.localInput as ip

if __name__ == "__main__":
    ip_graph = queue.Queue()
    ip_graph.generateCsr(ip.INPUT)
    ip_graph.showGraph(ip_graph.csr)
    start = input("Please provide the starting node = ")
    end = input("Please provide the destination node = ")
    if start not in list([x for x, _ in ip_graph.csr['vertex_id']]) and end not in list([x for x, _ in ip_graph.csr['vertex_id']]):
        print("Provided node not found")
        exit(1)
    ip_graph.startBfs(start, end)
    # print(ip_graph.csr)
    ip_graph.showGraph(ip_graph.csr)