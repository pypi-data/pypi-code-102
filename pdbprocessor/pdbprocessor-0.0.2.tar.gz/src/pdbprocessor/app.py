import sys, os
from interface import Interface
from processor import PDBProcessor
   
class Application:
    def __init__(self):
        self.proc = PDBProcessor()
        self.interface = Interface()
    def run_app(self):
        os.system("cls" if os.name == "nt" else "clear")
        if len(sys.argv) == 1:
            self.interface.display_start()
            self.interface.prompt_path()
            self.proc.set_path(input())
            self.interface.display_menu()
            self.mode = input()
            if self.mode == "elemreport":
                self.proc.do_elem_report("stdout")
            elif self.mode == "elemsearch":
                self.interface.display_elem_count()
                self.interface.prompt_element()
                self.proc.do_elem_search(input(), "stdout")
            elif self.mode == "aareport":
                self.proc.do_aa_report("stdout")
            elif self.mode == "aacount":
                self.interface.display_aa_count()
                self.interface.prompt_aa()
                self.proc.do_aa_search()
            elif self.mode.lower() == "sus":
                print("#AMOGUS#") 
            else:
                print("Wrong mode!")
        else:
            self.proc.set_path(sys.argv[1])
            self.mode = sys.argv[2]
            self.target = "file" if "writefile" in sys.argv else "stdout"
            if self.mode == "elemreport":
                self.proc.do_elem_report(self.target)
            elif self.mode == "elemsearch":
                self.proc.do_elem_search(sys.argv[3], self.target)
            elif self.mode == "aareport":
                self.proc.do_aa_report(self.target)
            elif self.mode == "aacount":
                self.proc.do_aa_search(sys.argv[3].upper(), self.target)
            else:
                print("Wrong mode!")
