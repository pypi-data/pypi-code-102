from git import Repo

from colorama import Fore
import colorama
import os

class Git:
    def __init__(self, remote_repository_name='origin', repo_path=os.getcwd()):
        self.repository = Repo(repo_path)
        self.remote_repository_name = remote_repository_name


    def __get_remote_repository(self):
        try:             
            remote = self.repository.remote(self.remote_repository_name)
            remote.fetch()
            latest_remote_commit = remote.refs[self.repository.active_branch.name].commit

            return latest_remote_commit
        except:           
            return None


    def check_updates(self):
        latest_local_commit = self.repository.head.commit
        latest_remote_commit = self.__get_remote_repository()

        has_updates = latest_local_commit == latest_remote_commit
        
        print(Fore.YELLOW)
        print(f"Existem mudanças não commitadas/unstaged? {self.repository.is_dirty()}")
        print(f"Arquivos untracked: {len(self.repository.untracked_files)}")

        if latest_remote_commit == None: print(f'Sem repositório remoto: {self.remote_repository_name}')

        print(Fore.LIGHTMAGENTA_EX)
        if not has_updates: raise ValueError(f"Você tem mudanças não commitadas")
        else: print(Fore.GREEN + f"Repositório atualizados")