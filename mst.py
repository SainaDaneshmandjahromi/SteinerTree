
def readfromfile(filename):
    wholeFileByLine = []
    f = open(filename, "r")
    for line in f:
        wholeFileByLine.append(line)
    return wholeFileByLine


def BuildingGraph(wholeFileByLine):
    Graph= {}
    isNodeNumber = False
    isEdgeNumber = False
    isTerminalNumber = False
    throughEdgeNumber = False
    throughTerminal = False
    edges=[]
    terminals=[]
    for line in wholeFileByLine:
        if line.startswith("Name"):
            Graph.update({'name':MyNum(line,0)})
        elif line.startswith("EOF"):
            break
        elif isNodeNumber:
            isNodeNumber = False
            isEdgeNumber = True
            Graph.update({'numberofnodes': MyNum(line,1)})
        elif line.startswith("SECTION Graph"):
            isNodeNumber = True
        elif line.startswith("Section Terminals"):
            isTerminalNumber = True
        elif line.startswith("End") and throughEdgeNumber:
            throughEdgeNumber = False
            Graph.update({'edges': edges})
        elif throughEdgeNumber:
            edges = MakeEdges(line, edges)
        elif isEdgeNumber:
            EdgeNumber = MyNum(line,1)
            isEdgeNumber = False
            throughEdgeNumber = True
        elif isTerminalNumber:
            TerminalNumber = MyNum(line,2)
            isTerminalNumber = False
            throughTerminal = True
        elif line.startswith("End") and throughTerminal:
            throughTerminal = False
            Graph.update({'terminals': terminals})
        elif throughTerminal:
            terminals = MakeTerminals(line, terminals)

    return Graph


def MyNum(line,ifInt):
    if ifInt==2:
        index=10
    elif ifInt==0:
        index=9
    else:
        index = 6
    myNumber = ""
    while line[index] != '\n' and line[index] != '"':
        myNumber+=line[index]
        index+=1
    if ifInt:
        return int(myNumber)
    else:
        return myNumber


def NumberofNodes(wholeFileByLine):
    isNodeNumber = False
    for line in wholeFileByLine:
        if isNodeNumber:
            NumberofNodes = int(line[6:-1])
            return NumberofNodes
            break;
        if line.startswith("SECTION GRAPH"):
            isNodeNumber = True


def MakeTerminals(line,terminals):
    line = line[2:-1]
    terminals.append(int(line))
    return terminals

def MakeEdges(line,edges):
    line = line[2:]
    myTuple=()
    numbers=[]
    splittedLines = line.split()
    for char in splittedLines:
        numbers.append(int(char))
    edges.append(tuple(numbers))
    return edges

def sortByWeight(Graph):
    edges= Graph["edges"]
    return sorted(edges, key=lambda edges: edges[2])

def MSTWeight(name):
    edges = MakeMST(name)
    weight = 0
    for edge in edges:
        weight += edge[2]
    return weight

#parents,sizes
def MakeMST(name):
    Graph = (BuildingGraph(readfromfile(name)))
    edges = sortByWeight(Graph)
    parent = []
    size = []
    mstedge=[]
    for i in range(Graph['numberofnodes']):
        parent.append(i)
        size.append(1)
    for edge in edges:
        if find(edge[0]-1,parent) != find(edge[1]-1,parent):
            mstedge.append(tuple((edge[0],edge[1],edge[2])))
            parent,size = union(edge[0]-1,edge[1]-1,parent,size)
        else:
            parent,size = union(edge[0]-1,edge[1]-1,parent,size)
    return mstedge

def find(x,parent):
    p = parent[x]
    if(p==x):
        return p
    return parent[x]

def union(x,y,parent,size):
    rx = find(x,parent)
    ry = find(y,parent)
    if(rx == ry):
        return parent,size
    elif(size[ry] > size[rx]):
        for i in range(len(parent)):
            if parent[i]==rx:
                parent[i] = ry
        size[ry] += size[rx]
        return parent,size
    else:
        for i in range(len(parent)):
            if parent[i] == ry:
                parent[i] = rx
        size[rx] += size[ry]
        return parent,size

########################################################SECOND PART

class Node:


    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:

    def __init__(self):
        self.head = None

    def printList(self):
        temp = self.head
        while (temp):
            print (temp.data)
            temp = temp.next

    def AtEnd(self, newdata):
        NewNode = Node(newdata)
        if self.head is None:
            self.head = NewNode
            return
        last = self.head
        while(last.next):
            last = last.next
        last.next=NewNode

    def search(self, x):

        current = self.head

        while current != None:
            if current.data == x:
                return True

            current = current.next

        return False

    def putInList(self):
        list = []
        current = self.head.next
        while current != None:
            list.append(current.data)
            current = current.next
        return list



def ConnectionsInLink(name):
    edges = MakeMST(name)
    Graph = BuildingGraph(readfromfile(name))
    linkListArr = []
    for i in range(1,Graph['numberofnodes']+1):
        llist = LinkedList()
        llist.head = Node(i)
        linkListArr.append(llist)

    for edge in edges:
        if linkListArr[edge[0] - 1].head.next == None:
            linkListArr[edge[0] - 1].head.next = Node(edge[1])
        else:
            linkListArr[edge[0] - 1].AtEnd(edge[1])
        if linkListArr[edge[1] - 1].head.next == None:
            linkListArr[edge[1] - 1].head.next = Node(edge[0])
        else:
            linkListArr[edge[1] - 1].AtEnd(edge[0])


    return linkListArr


def SteinerTree(name):
    weight = 0
    finded = []
    canAdd = True
    linkListArr = ConnectionsInLink(name)
    Graph = BuildingGraph(readfromfile(name))
    terminals = Graph['terminals']
    mstVertixes = MakeMST(name)
    throughList = terminals
    newGraph = []
    for terminal in terminals:
        if terminal not in finded:
            if(sorted(terminals) == sorted(finded)):
                break;

            paths = findOthers(linkListArr,throughList[:],terminal)
            for i in range(len(paths) - 1):
                for vertix in mstVertixes:
                    canAdd = True
                    if((vertix[0] == paths[i] and vertix[1] == paths[i+1]) or (vertix[1] == paths[i] and vertix[0] == paths[i+1])):
                        for gr in newGraph:
                            if ((gr[0] == vertix[0] and gr[1] == vertix[1]) or (gr[1] == vertix[0] and gr[0] == vertix[1])):
                                canAdd = False;
                        if(canAdd):
                            weight += vertix[2]
                            newGraph.append(tuple((vertix[0],vertix[1],vertix[2])))
                            if vertix[0] in terminals:
                                finded.append(vertix[0])
                            if vertix[1] in terminals:
                                finded.append(vertix[1])

    return newGraph,weight


def findOthers(linkListArr,throughList,terminal):

    terminals=[]
    first = [terminal]
    terminals.append(first)
    throughList.remove(terminal)
    newterminals = terminals[:]
    isIn = False
    while(not isIn):
        index = 0
        terminals = newterminals[:]
        i = 0
        for myterminal in terminals:
            vertixes = linkListArr[myterminal[-1]-1].putInList()
            for i in range(index,index + len(vertixes)-1):
                    newterminals.insert(i,myterminal[:])
            i = index
            for element in vertixes:
                newterminals[i].append(element)
                if element in throughList:
                    isIn=True;
                    return newterminals[i]
                i+=1
            index = index + len(vertixes)
            j = 0


def writeInFile(name):
    graphs, weight = SteinerTree(name)
    f = open(name[:-4]+".out", "w")
    f.write("Cost   "+str(weight)+'\n')
    f.write("Edges "+str(len(graphs))+'\n')
    for graph in graphs:
        f.write('E '+str(graph[0]) + ' ' +str(graph[1]) + ' '+ str(graph[2])+'\n')



def writeInAllFiles(nameArray):
    for name in nameArray:
        writeInFile(name)


nameArray = ["bip42p.stp",
            "bipe2p.stp",
             "bipe2u.stp",
             "cc3-10p.stp",
             "cc3-10u.stp",
             "cc3-4p.stp",
             "cc3-4u.stp",
             "cc3-5p.stp",
             "cc3-5u.stp",
             "cc5-3p.stp",
             "cc5-3u.stp",
             "cc6-2p.stp",
             "cc6-2u.stp",
             "cc6-3p.stp",
             "cc6-3u.stp",
             "cc9-2p.stp",
             "cc9-2u.stp",
             "hc6p.stp",
             "hc6u.stp",
             "hc7p.stp",
             "hc7u.stp",
             "hc8p.stp",
             "hc8u.stp",
             "hc9p.stp",
             "hc9u.stp",
             ]

def writeBoth(nameArray):
    f = open("result.out", "w")
    for name in nameArray:
        mstWeught = MSTWeight(name)
        graphs, weight = SteinerTree(name)
        f.write( name )
        f.write("Costpart1 :" + str(mstWeught) + "      ")
        f.write("Costpart2 : " + str(weight) + '\n')

writeInAllFiles(nameArray)
