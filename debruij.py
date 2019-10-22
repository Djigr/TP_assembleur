import argparse

def main():
    parser = argparse.ArgumentParser(prog='debruij.py', description='Assembling by Debruijn graphs')
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'),help='Read my file')
    parser.add_argument('-i', action="store_true", help='fichier fastq single end')
    parser.add_argument('-k', type=int, default=21, help='kmer size (optional - default = 21)')
    parser.add_argument('-r', action='store_true', help='reference genome (optional)')
    parser.add_argument('-o', action='store_true', help='config file')

    args = parser.parse_args()


if __name__=="__main__":
    main()
