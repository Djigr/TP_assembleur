import argparse

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
        for j in cut_kmer(i, k):
            print(j)
    print(build_kmer_dict(args.input.name, k))



def read_fastq(fich):
    """Reads the fastq file by yielding line by line"""
    adresse = 'data/'+str(fich)
    with open(adresse, 'r') as fichi:
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
    print(list_seq)
    for j in list_seq:
        for kmer in cut_kmer(j, k):
            if kmer not in dict_kmer.keys():
                dict_kmer[kmer] = 1
            else:
                dict_kmer[kmer] += 1
    return dict_kmer

#def build_graph(dict_kmer):
    

if __name__ == "__main__":
    main()
