class Student:

    def __init__(self, fullname, gender, birth_year):
        self.fullname = fullname
        self.gender = gender
        self.birth_year = birth_year
    def print_details(self):
        print(f'Fullname: {self.fullname}, Gender: {self.gender}, Birth Year: {self.birth_year}')

