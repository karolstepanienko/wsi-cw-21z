# Autor: Karol Stepanienko


import yaml
import os
from time import time
from pprint import pprint

from Statistics import Stats
from Constants import Constants


class Results:
    def create_dict_to_save(self, ID, u, pm, pc, t_max, n_stat, average, standard_deviation, best_individual, time_of_calc):
        return dict({
                "u": u,
                "pm": pm,
                "pc": pc,
                "t_max": t_max,
                "n_stat": n_stat,
                "u*n_stat": u * n_stat,
                "average": average,
                "standard_deviation": standard_deviation,
                "best_individual": best_individual.to_dict(),
                "time_of_calc": time_of_calc
            }
        )


# Zapisuje pliki yaml
class Saving:
    def __init__(self):
        self.file_name = str(time())

    def save(self, dic_to_save):
        with open("./CW2/Results/" + self.file_name + '.yaml', 'a+') as file:
            documents = yaml.dump(dic_to_save, file)


# Ładuje pliki yaml
class Loading:
    def __init__(self, file_name=None):
        self.files = os.listdir('./CW2/Results')
        self.file_name = file_name
        self.loaded = self.load()

    def load(self):
        if self.file_name is None:
            self.file_name = self.files[0]
        with open('./CW2/Results/' + self.file_name) as file:
            return(yaml.load(file, Loader=yaml.Loader))


class CreateData:
    def __init__(self):
        self.c = Constants()
        self.to_save = dict()
        self.u_list = self.generate_u_to_test()
        self.results = Results()
        self.saving = Saving()

    def init(self):
        self.stats = Stats(self.c)

    def generate_u_to_test(self):
        u_list = []
        u = 10
        for i in range(1, 10):
            u_list.append(u)
            u = u + 10
        u_list.append(100)
        u_list.append(150)
        u_list.append(200)
        # for i in range(1, 21):
        #     u_list.append(u)
        #     u = u + 100
        return u_list

    def run_auto(self):
        previous_individual = None

        for ID, u in zip(range(len(self.u_list)), self.u_list):
            self.init()
            
            self.c.u = u
            print("ID: ", ID)
            print("u: ", self.c.u)

            time_of_calc, best_individual, average, standard_deviation = self.stats.run_offline()

            # Upewnianie, że nie ma powtarzających się elementów
            if not previous_individual is None:
                while previous_individual.compare(best_individual):
                    time_of_calc, best_individual, average, standard_deviation = self.stats.run_offline()
                    print(average)
                    print(best_individual.to_string())
            

            # Kiedy nowy osobnik zostanie zaakceptowany
            previous_individual = best_individual

            to_save_dic = self.results.create_dict_to_save(ID, self.c.u, self.c.pm, \
                self.c.pc, self.c.t_max, self.c.n_stat, average, standard_deviation, \
                best_individual, time_of_calc)
            # Dodaj ID testu
            self.to_save[ID] = to_save_dic
        
        self.saving.save(self.to_save)


if __name__ == "__main__":
    # create_data = CreateData()
    # create_data.run_auto()
    loaded = Loading()
    loaded.load()
