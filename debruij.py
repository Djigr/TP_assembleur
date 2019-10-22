import argparse

def main():
    parser = argparse.ArgumentParser(prog='debruij.py', description='Assembling by Debruijn graphs')
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'),help='Read my file')
    parser.add_argument('-i', type=str, help='fichier fastq single end')
    parser.add_argument('-k', type=int, default=21, help='kmer size (optional - default = 21)')
    parser.add_argument('-o', type=str, help='config file')

    args = parser.parse_args()

    for i in read_fastq(args.input.name):
        print(i)


def read_fastq(fich):
    adresse = 'data/'+str(fich)
    fichi = open(adresse, 'r')
    for line in fichi:
        if line.startswith('@'):
            lire=True
        elif line.startswith('+'):
            lire=False
        else:
            if lire:
                yield line


def cut_kmer(seq,k):
    for i in seq:
        yield seq[i:i+k]


def build_kmer_dict(fastq_file,k):
    dict_kmer={}
    list_seq = [x[:-1] for x in read_fastq(fastq_file)]
    for kmer in cut_kmer(list_seq, k):
        if kmer not in dict_kmer.keys():
            dict_kmer[kmer] = 1
        else:
            dict_kmer[kmer] += 1
    return dict_kmer   


if __name__=="__main__":
    main()
