import os
from appinfo import AppInfo

class PDBProcessor:
    def __init__(self):
        self.elemtotal = 0
        self.elemcounts = {}
        self.aatotal = 0
        self.aacounts = {}
        self.totalaacounts = {}
        self.path = "/Home"
        self.searchelem = ""
        self.searchaa = ""
        self.elemcount = 0
        self.aacount = {}
        self.aatotalcount = 0
        self.outpath = ""
    
    def set_path(self, path):
        if path.startswith('/'):
            self.path = path
        else:
            self.path = os.getcwd() + '/' + path
    
    def process_pdb_elems(self):
        with open(self.path, 'r') as pdb:
            for line in pdb.readlines():
                l = line.split()
                if l[0] == "ATOM":
                    self.elemtotal += 1
                    if l[-1] not in self.elemcounts.keys():
                        self.elemcounts[l[-1]] = 1
                    else:
                        self.elemcounts[l[-1]] += 1
                        
    def process_pdb_aas(self):
        with open(self.path, 'r') as pdb:
            for line in pdb.readlines():
                l = line.split()
                if l[0] == "SEQRES":
                    chain = l[2]
                    if chain not in self.aacounts.keys():
                        self.aacounts[chain] = {}
                    for aa in l[4:]:
                        if aa not in self.aacounts[chain].keys():
                            self.aacounts[chain][aa] = 1
                        else:
                            self.aacounts[chain][aa] += 1
        for chain in list(self.aacounts.keys()):
            for aa in self.aacounts[chain].items(): 
                if aa[0] not in self.totalaacounts.keys():
                    self.totalaacounts[aa[0]] = int(aa[1])
                else:
                    self.totalaacounts[aa[0]] += int(aa[1])

    def elem_search(self):
        with open(self.path, 'r') as pdb:
            self.elemcount = 0
            for line in pdb.readlines():
                l = line.split()
                if l[0] == "ATOM" and l[-1] == self.searchelem:
                    self.elemcount += 1
                    
    def aa_search(self):
        with open(self.path, 'r') as pdb:
            self.elemcount = 0
            for line in pdb.readlines():
                l = line.split()
                if l[0] == "SEQRES":
                    if l[2] not in self.aacount.keys():
                        self.aacount[l[2]] = sum([1 for i in l if i == self.searchaa])
                    else:
                        self.aacount[l[2]] += sum([1 for i in l if i == self.searchaa])
        for chain in self.aacount.items():
            self.aatotalcount += chain[1]
                    
    def set_elem(self, elem):
        self.searchelem = elem
        
    def set_aa(self, aa):
        self.searchaa = aa
        
    def make_outpath(self):
        self.outpath = self.path.split('/')[-1].split('.')[0]
                
    def print_elem_report(self):
        print("#PDB PROCESSOR ELEMENT REPORT#")
        print()
        print(f"Finished analyzing PDB file: {self.path}")
        print()
        print(f"Atoms found: {self.elemtotal}")
        print()
        print("Summary of elements found:")
        for elem in self.elemcounts.items():
            print(f"{elem[0]}: {elem[1]}")
        print()
        print("#END OF REPORT#")
        
    def write_elem_report(self, path):
        with open(path, 'w') as f:
            f.write(f"PDBProcessor by {AppInfo.AUTHOR}, version {AppInfo.VERSION}\n")
            f.write("#PDB PROCESSOR ELEMENT REPORT#\n")
            f.write('\n')
            f.write(f"Finished analyzing PDB file: {self.path}\n")
            f.write('\n')
            f.write(f"Atoms found: {self.elemtotal}\n")
            f.write('\n')
            f.write("Summary of elements found:\n")
            for elem in self.elemcounts.items():
                f.write(f"{elem[0]}: {elem[1]}\n")
            f.write('\n')
            f.write("#END OF REPORT#")
        
    def print_aa_report(self):
        print("#PDB PROCESSOR AMINO ACID REPORT#")
        print()
        print(f"Finished analyzing PDB file: {self.path}")
        print()
        print("Amino acids found:")
        print(f"Total: {sum(self.totalaacounts.values())}")
        for chain in sorted(self.aacounts.items()):
            print(f"In chain {chain[0]}: {sum([int(aa[1]) for aa in chain[1].items()])}")
        print()
        print("Summary of amino acids found:")
        print("In all chains:")
        for aa in sorted(self.totalaacounts.items()):
            print(f"{aa[0]}: {aa[1]}")
        for chain in self.aacounts.items():
            print(f"In chain {chain[0]}:")
            for aa in sorted(chain[1].items()):
                print(f"{aa[0]}: {aa[1]}")
        print()
        print("#END OF REPORT#")
        
    def write_aa_report(self, path):
        with open(path, 'w') as f:
            f.write(f"PDBProcessor by {AppInfo.AUTHOR}, version {AppInfo.VERSION}\n")
            f.write("#PDB PROCESSOR AMINO ACID REPORT#\n")
            f.write('\n')
            f.write(f"Finished analyzing PDB file: {self.path}\n")
            f.write('\n')
            f.write("Amino acids found:\n")
            f.write(f"Total: {sum(self.totalaacounts.values())}\n")
            for chain in sorted(self.aacounts.items()):
                f.write(f"In chain {chain[0]}: {sum([int(aa[1]) for aa in chain[1].items()])}\n")
            f.write('\n')
            f.write("Summary of amino acids found:\n")
            f.write("In all chains:\n")
            for aa in sorted(self.totalaacounts.items()):
                f.write(f"{aa[0]}: {aa[1]}\n")
            for chain in self.aacounts.items():
                f.write(f"In chain {chain[0]}:\n")
                for aa in sorted(chain[1].items()):
                    f.write(f"{aa[0]}: {aa[1]}\n")
            f.write('\n')
            f.write("#END OF REPORT#")
                
    def print_aa_debug(self):
        print(self.aacounts)
        print(self.aacounts.keys())
        print(self.totalaacounts)
        print(self.debugtracker)
        
        
    def print_elem_count(self):
        print("#PDB PROCESSOR ELEMENT COUNT#")
        print(f"Finished analyzing PDB file: {self.path}")
        print(f"Looked for element: {self.searchelem}")
        print(f"Instances found: {self.elemcount}")
        print("#END OF REPORT#")
        
    def write_elem_count(self, path):
        with open(path, 'w') as f:
            f.write(f"PDBProcessor by {AppInfo.AUTHOR}, version {AppInfo.VERSION}\n")
            f.write("#PDB PROCESSOR ELEMENT COUNT#\n")
            f.write(f"Finished analyzing PDB file: {self.path}\n")
            f.write(f"Looked for element: {self.searchelem}\n")
            f.write(f"Instances found: {self.elemcount}\n")
            f.write("#END OF REPORT#")
        
    def print_aa_count(self):
        print("#PDB PROCESSOR AMINO ACID COUNT#")
        print(f"Finished analyzing PDB file: {self.path}")
        print(f"Looked for amino acid: {self.searchaa}")
        print("Instances found:")
        print(f"Total: {self.aatotalcount}")
        for chain in self.aacount.items():
            print(f"In chain {chain[0]}: {chain[1]}")
        print("#END OF REPORT#")
    
    def write_aa_count(self, path):
        with open(path, 'w') as f:
            f.write(f"PDBProcessor by {AppInfo.AUTHOR}, version {AppInfo.VERSION}\n")
            f.write("#PDB PROCESSOR AMINO ACID COUNT#\n")
            f.write(f"Finished analyzing PDB file: {self.path}\n")
            f.write(f"Looked for amino acid: {self.searchaa}\n")
            f.write("Instances found:\n")
            f.write(f"Total: {self.aatotalcount}\n")
            for chain in self.aacount.items():
                f.write(f"In chain {chain[0]}: {chain[1]}\n")
            f.write("#END OF REPORT#")
        
    def do_elem_report(self, target):
        if target == "stdout":
            self.process_pdb_elems()
            self.print_elem_report()
        elif target == "file":
            self.make_outpath()
            self.process_pdb_elems()
            self.outpath += "_elem_report.pdpr"
            self.write_elem_report(self.outpath)
            
    def do_elem_search(self, elem, target):
        self.searchelem = elem
        if target == "stdout":
            self.elem_search()
            self.print_elem_count()
        elif target == "file":
            self.make_outpath()
            self.elem_search()
            self.outpath = self.outpath + "_elem_search_" + elem + ".pdpr"
            self.write_elem_count(self.outpath)
            
    def do_aa_report(self, target):
        if target == "stdout":
            self.process_pdb_aas()
            self.print_aa_report()
        elif target == "file":
            self.make_outpath()
            self.process_pdb_aas()
            self.outpath += "_aa_report.pdpr"
            self.write_aa_report(self.outpath)
            
    def do_aa_search(self, aa, target):
        self.searchaa = aa
        if target == "stdout":
            self.aa_search()
            self.print_aa_count()
        elif target == "file":
            self.make_outpath()
            self.aa_search()
            self.outpath = self.outpath + "_aa_search_" + aa + ".pdpr"
            self.write_aa_count(self.outpath)
            