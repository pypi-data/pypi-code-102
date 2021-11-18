import os
import re
import time
import csv
from urllib import request


class FileChecker(object):
    def __init__(self, file_path, re_exp_dict):
        self.re_exp_dict = re_exp_dict
        self.file_path = file_path
        self.line_list = self.load_file()

        self.re_exp = r"<a name=\"(.+?)\">.*</a>"
        self.target_list = self.load_target()

    def load_target(self):
        target_list = []
        for line in self.line_list:
            targets = re.findall(self.re_exp, line)
            if len(targets) > 0:
                target_list += targets
        return target_list

    def load_file(self):
        line_list = []
        try:
            with open(self.file_path) as f:
                line_list = f.readlines()
        # except Exception.FileNotFoundError
        except Exception as e:
            print(f"Process {self.file_path}: {e}.")
        return line_list

    def check_line(self, line_str):
        invalid_link_list = []
        for re_exp, test_func in re_exp_dict.items():
            re_results = re.findall(re_exp, line_str)
            for result in re_results:
                if getattr(self, test_func)(result):
                    invalid_link_list.append(result)
        return invalid_link_list

    def __call__(self):
        invalid_link_list = []
        for num, line in enumerate(self.line_list):
            links = self.check_line(line)
            for link in links:
                invalid_link_list.append([self.file_path, num+1, link])
                print(f"{self.file_path}\t{num+1}\t{link}")

        return invalid_link_list

    def check_http(self, http_str):
        try:
            with request.urlopen(http_str) as f:
                if f.status == 200:
                    return False
        except Exception as e:
            pass
        return True

    def check_inter_link(self, tag_str):
        # target_str = f"<a name=\"{tag_str}\"></a>"
        return not tag_str in self.target_list

    def check_exter_link(self, path_str):
        path_str = path_str.split("#")[0]
        target_path = os.path.join(os.path.dirname(self.file_path), path_str)
        if os.path.exists(target_path):
            return False
        return True


def recursive_walk(root_dir, suffix_list):
    file_list = []
    for root, dirs, files in os.walk(root_dir, followlinks=False):
        for name in files:
            for suffix in suffix_list:
                if name.endswith(suffix):
                    file_path = os.path.join(root, name)
                    file_list.append(file_path)
    return file_list


def main():
    file_list = recursive_walk(root_dir, suffix_list)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(f"{len(file_list)} file(s) has beed found.")

    total_invalid_link_list = []
    for file_path in file_list:
        file_checker = FileChecker(file_path, re_exp_dict)
        invalid_link_list = file_checker()
        total_invalid_link_list += invalid_link_list

    with open(save_path, "w+", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["FilePath", "LineNum", "Link"])   # 先写入columns_name
        writer.writerows(total_invalid_link_list)
    print("Done!")

if __name__ == "__main__":
    root_dir = "./"
    suffix_list = [".md"]

    re_exp_dict = {r"^(?!<!--).*\[.+\]\(#(.*?)\)": "check_inter_link", r"^(?!<!--).*\[.+\]\((?!#)(?!http)(.*?)\)": "check_exter_link"}
    # re_exp_dict = {r"^(?!<!--).*\[.+\]\((http.+?)\)": "check_http", r"^(?!<!--).*\"(http.+?)\"": "check_http"}

    save_path = "./check_link.csv"

    main()
