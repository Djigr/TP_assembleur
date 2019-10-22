import argparse
import networkx as nx

def main():
    """Parses the argument and produces the graph expected"""
    parser = argparse.ArgumentParser(prog='debruij.py', description='Assembling by Debruijn graphs')
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'), help='Read my file')
    parser.add_argument('-i', type=str, help='fichier fastq single end')
    parser.add_argument('-k', type=int, default=21, help='kmer size (optional - default = 21)')
    parser.add_argument('-o', type=str, help='config file')

    args = parser.parse_args()
    k = int(args.k)
    for i in read_fastq(args.input.name):
        print(i)
        #for j in cut_kmer(i, k):
            #print(j)
    print(build_kmer_dict(args.input.name, k))
    for i in build_graph(build_kmer_dict(args.input.name, k)):
        print(i)
    graph = build_graph(build_kmer_dict(args.input.name, k))
    for i in get_starting_nodes(graph):
        print(i)
    if len(get_starting_nodes(graph))==0:
        print('This is empty')
    #for i in get_contigs(graph, get_starting_nodes(graph), get_sink_nodes(graph)):
     #   print(i)
    #print(get_contigs(graph, get_starting_nodes(graph), get_sink_nodes(graph)))


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
                    yield line


def cut_kmer(seq, k):
    """Cut a sequence into kmers"""
    for i in range(len(seq)-k):
        yield seq[i:i+k]


def build_kmer_dict(fastq_file, k):
    """Builds the kmer dictionnary"""
    dict_kmer = {}
    list_seq = [x[:-1] for x in read_fastq(fastq_file)]
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
        dg.add_edge(kmer[:-1], kmer[1:len(kmer)], weight=dict_kmer[kmer])
    return dg


def get_starting_nodes(graph):
    """Gets a list of starting nodes"""
    startnodes = []
    for node in graph.nodes:
        if len(list(graph.predecessors(node))) == 0:
            startnodes.append(node)
    return startnodes


def std():
    pass


def get_sink_nodes(graph):
    """Get a list of ending nodes"""
    sinknodes = []
    for node in graph.nodes:
        if len(list(graph.successors(node))) == 0:
            sinknodes.append(node)
    return sinknodes


def path_average_weight():
    pass


def remove_paths():
    pass


def select_best_path():
    pass


def save_contigs():
    pass


def get_contigs(graph, start, sink):
    """Gets a list of tuples in the graph, with each tuple containing a contig and its length"""
    contigs = []
    for startnode in start:
        for sinknode in sink:
            for path in nx.all_simple_paths(graph, startnode, sinknode):
                print(path)
                contigs.append([startnode[0]+sinknode])
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
