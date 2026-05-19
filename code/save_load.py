import json
from utils import *

def save_file(data):
    with open(get_save_path('data.txt'), 'w') as test_file:
        json.dump(data, test_file)

def load_file(filename):
    with open(f'{filename}.txt') as test_file:
        data = json.load(test_file)
        return data


def save_simulation_file(data):
    with open(get_save_path('simulation_file.txt'), 'w') as test_file:
        json.dump(data, test_file)



def save_results(data): # TASK: add date and number of result
    try:
        results = open(get_save_path('results.txt'), 'r')
        old_data = json.load(results)
        data = data + '\n' + '\n' + old_data
        results.close()
    except:
        pass
    with open(get_save_path('results.txt'), 'w') as results_file:
        json.dump(data, results_file)
        results_file.close()
