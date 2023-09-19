import json

def save_file(data):
    with open('data.txt', 'w') as test_file:
        json.dump(data, test_file)

def load_file(filename):
    with open(f'{filename}.txt') as test_file:
        data = json.load(test_file)
        return data
        # for entry in data:
        #     print(entry)
# save_file()
# load_file('data')



def save_simulation_file(data):
    with open('simulation_file.txt', 'w') as test_file:
        json.dump(data, test_file)


def save_mission(data, n):
    with open(f'mission0{n}.txt', 'w') as test_file:
        json.dump(data, test_file)


def save_results(data):
    try:
        results = open('results.txt', 'r')
        old_data = json.load(results)
        data = data + '\n' + '\n' + old_data
        results.close()
    except:
        pass
    with open(f'results.txt', 'w') as results_file:
        json.dump(data, results_file)
        results_file.close()
