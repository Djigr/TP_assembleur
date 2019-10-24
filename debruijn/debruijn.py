import os
import argparse
import statistics
import networkx as nx
import matplotlib as mp

def main():
    """Parses the argument and produces the graph expected"""
    parser = argparse.ArgumentParser(prog='debruijn.py', description='Assembling by Debruijn graphs')
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'), help='Read my file')
    parser.add_argument('-i', type=str, help='fichier fastq single end')
    parser.add_argument('-k', type=int, default=21, help='kmer size (optional - default = 21)')
    parser.add_argument('-o', type=str, help='contig file')

    args = parser.parse_args()
    k = int(args.k)
    #for i in read_fastq(args.input.name):
        #print(i)
        #for j in cut_kmer(i, k):
            #print(j)
    read_fastq(args.input.name)
    build_kmer_dict(args.input.name, k)
    graph = build_graph(build_kmer_dict(args.input.name, k))
    #nx.draw(graph)
    print(get_starting_nodes(graph))
    #for i in get_contigs(graph, get_starting_nodes(graph), get_sink_nodes(graph)):
    #    print(i)
    contigs = get_contigs(graph, get_starting_nodes(graph), get_sink_nodes(graph))
    save_contigs(contigs, args.o)
    test_path = ['AACTCACACTGGTAACTTTG', 'ACTCACACTGGTAACTTTGG', 'CTCACACTGGTAACTTTGGA']
    print(graph.nodes)
    path_average_weight(graph, test_path)
    multipath = [['AACTCACACTGGTAACTTTG', 'ACTCACACTGGTAACTTTGG', 'CTCACACTGGTAACTTTGGA'],['TGGAACTCACACTGGTAACT', 'GGAACTCACACTGGTAACTT', 'GAACTCACACTGGTAACTTT']]
    remove_paths(graph, multipath, True, False)
    #print("la liste des contigs est telle :",get_contigs(graph, get_starting_nodes(graph), get_sink_nodes(graph)))


def read_fastq(fich):
    """Reads the fastq file by yielding line by line"""
    with open(fich, 'r') as fichi:
        for line in fichi:
            if line.startswith('@'):
                lire = True
            elif line.startswith('+'):
                lire = False
            else:
                if lire:
                    yield line[:-1]


def cut_kmer(seq, k):
    """Cut a sequence into kmers"""
    for i in range(len(seq)-k+1):
        yield seq[i:i+k]


def build_kmer_dict(fastq_file, k):
    """Builds the kmer dictionnary"""
    dict_kmer = {}
    list_seq = [x for x in read_fastq(fastq_file)]
    for j in list_seq:
        for kmer in cut_kmer(j, k):
            if kmer not in dict_kmer.keys():
                dict_kmer[kmer] = 1
            else:
                dict_kmer[kmer] += 1
    return dict_kmer


def build_graph(dict_kmer):
    """Builds the graph by taking into account the kmer dictionnary"""
    dg = nx.DiGraph()
    for kmer in dict_kmer:
        dg.add_edge(kmer[:-1], kmer[1:], weight=dict_kmer[kmer])
    return dg


def get_starting_nodes(graph):
    """Gets a list of starting nodes"""
    startnodes = []
    for node in graph.nodes:
        if len(list(graph.predecessors(node))) == 0:
            startnodes.append(node)
    return startnodes



def std(val):
    """Calculates the standard deviation of a list of values"""
    return statistics.stdev(val)


def get_sink_nodes(graph):
    """Get a list of ending nodes"""
    sinknodes = []
    for node in graph.nodes:
        if len(list(graph.successors(node))) == 0:
            sinknodes.append(node)
    return sinknodes


def path_average_weight(graph, path):
    """Takes a graph, a path, and returns an average weight"""
    edges = graph.subgraph(path).edges(data=True)
    somme = 0
    count = 0
    for u,v,e in edges:
        #print(e["weight"])
        somme += e["weight"]
        count += 1
        #print(somme, 'et ', count)
    result = somme/count
    print("le résultat est ", result)
    return result


def remove_paths(graph, multipath, delete_entry_node, delete_sink_node):
    for path in multipath:
        if delete_entry_node == True and delete_sink_node == True:
            for node in path:
                if node in graph.nodes():
                    graph.remove_node(node)
        elif delete_entry_node == False and delete_sink_node == True:
            for node in path[1:]:
                if node in graph.nodes():
                    graph.remove_node(node)
        elif delete_entry_node == True and delete_sink_node == False:
            for node in path[0:-1]:            
                if node in graph.nodes():
                    graph.remove_node(node)
        else:
            for node in path[1:-1]:
                if node in graph.nodes():
                    graph.remove_node(node)
    print(graph.nodes)
    return graph


def select_best_path():
    pass


def save_contigs(contigs, fich_sort):
    """Saves the found contigs in a text file"""
    with open(fich_sort, "w") as fich:
        for i in range(0, len(contigs)):
            text = ">contig_"+str(i)+" len={0}\n".format(contigs[i][1])+contigs[i][0]+"\n"
            fich.write(fill(text))
    print("I have created a file with your contigs.")


def get_contigs(graph, start, sink):
    """Gets a list of tuples in the graph, with each tuple containing a contig and its length"""
    contigs = []
    for startnode in start:
        for sinknode in sink:
            for path in nx.all_simple_paths(graph, source=startnode, target=sinknode):
                #print(path)
                new_cont = []
                new_cont.append(path[0])
                for j in range(1, len(path)):
                    new_cont.append(path[j][-1:])
                new_cont = "".join(new_cont)
                contigs.append([new_cont, len(new_cont)])
    return contigs


def solve_bubble():
    pass


def simplify_bubbles():
    pass


def solve_entry_tips():
    pass


def solve_out_tips():
    pass

def fill(text, width=80):
    """Split text with a line return to respect fasta format"""
    return os.linesep.join(text[i:i+width] for i in range(0, len(text), width))

if __name__ == "__main__":
    main()
