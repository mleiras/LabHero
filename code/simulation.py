import json
import sys

from save_load import *
from options_values import *

def run_simul():
    from mewpy.simulation import get_simulator

    data_simul = load_file(get_save_path('simulation_file'))

    method, objective, genes, reactions = data_simul

    method = method['method'][0][0]
    objective_name = objective['objective'][0][0]
    # objective_fraction = objective['obj_fraction']

    envconditions = {}

    # initial simulation:
    simul = get_simulator(model) #, envcond=envconditions)


    reactions_original = simul.find_reactions('EX') # dataframe
    
    
    count = 0 # to access reactions
    count_2 = 0 # to access flow in and out inside each reaction (pair by pair)
    for i,(k,x) in enumerate(reactions.items()):
        if count_2 % 2 == 0: # if it's even, it means the toggle for the flow in
            envconditions[REACTIONS.index[count]] = (reactions_original.lb.iloc[count], reactions_original.ub.iloc[count])
            if not x:
                envconditions[REACTIONS.index[count]] = (0, envconditions[REACTIONS.index[count]][1])
            else:
                envconditions[REACTIONS.index[count]] = (-1000, envconditions[REACTIONS.index[count]][1])
            count_2 += 1
        else:
            if not x: # if it's uneven, it means the toggle for the flow out
                envconditions[REACTIONS.index[count]] = (envconditions[REACTIONS.index[count]][0], 0)
            else:
                envconditions[REACTIONS.index[count]] = (envconditions[REACTIONS.index[count]][0], 1000)
            count_2 += 1
            count += 1
        

    # print(envconditions)

    # REACTIONS WITH RANGE - deactivated
    # count = 0
    # for i,(k, x) in enumerate(reactions.items()):
    #     if k == REACTIONS.index[count]:
    #         if reactions_original.lb[count] != x[0] or reactions_original.ub[count] != x[1]:
    #             envconditions[k] = (x[0], x[1])
    #     else:
    #         count += 1
    #         if not x:
    #             envconditions[REACTIONS.index[count-1]] = (0, 0)


    for i,(k,x) in enumerate(genes.items()):
        if not x:
            # print(k)
            # print(simul.find_genes().reactions[i])
            list_react = simul.find_genes().reactions.iloc[i]
            for react in list_react:
                envconditions[react] = (0,0)

    # gene knockout:
    # model.genes.b1524.knock_out()


    # print(envconditions)

    # choose objective (by default Biomass):
    # objective = ''
    simul.objective = objective_name

    # add constraints here (modifications on the game)
    constraints = {}
    constraints = envconditions
    # constraints = {'GND': 0, # deletion
    #                'PYK': 0, # deletion
    #                'ME2': 0, # deletion
    #               }

    # chooose simulation method (by default FBA):
    sim_method = method

    # run a simulation accounting with the new constraint
    result = simul.simulate(method=sim_method, constraints=constraints)

    # print(constraints)
    results_str = str(result)
    # print(results_str)

    
    try:
        if str(results_str.splitlines()[1]) == 'Status: INFEASIBLE':
            results = 'Status: INFEASIBLE'
        else:
            results = round(float(str(results_str.splitlines()[0])[11:]), 3)
    except:
        results = results_str

    # print(result_str)

    # save_results(result)

    return objective_name, results

    # print(simul.objective)



def _build_request_payload():
    data_simul = load_file(get_save_path('simulation_file'))
    method, objective, genes, reactions = data_simul

    method_name = method['method'][0][0]
    objective_name = objective['objective'][0][0]

    reactions_original = REACTIONS

    env_conditions = {}
    count = 0
    count_2 = 0
    for i, (k, x) in enumerate(reactions.items()):
        rid = reactions_original.index[count]
        if count_2 % 2 == 0:
            lb = -1000 if x else 0
            env_conditions[rid] = [lb, reactions_original.ub.iloc[count]]
            count_2 += 1
        else:
            ub = 1000 if x else 0
            env_conditions[rid] = [env_conditions[rid][0], ub]
            count_2 += 1
            count += 1

    gene_knockouts = [k for k, x in genes.items() if not x]

    return {
        'method': method_name,
        'objective': objective_name,
        'gene_knockouts': gene_knockouts,
        'env_conditions': env_conditions,
    }


def _http_post_json(url, payload):
    body = json.dumps(payload)
    if sys.platform == 'emscripten':
        # pygbag's pyodide does not expose `from js import XMLHttpRequest`
        # as a constructable JsProxy (XMLHttpRequest.new is None and the
        # plain JsProxy is not callable), so we instantiate via js.eval.
        # Synchronous XHR lets us stay inside the sync pygame_menu callback
        # at window.py:229 — no async bridge needed for the simulate call.
        import js
        xhr = js.eval("new XMLHttpRequest()")
        xhr.open('POST', url, False)
        xhr.setRequestHeader('Content-Type', 'application/json')
        xhr.send(body)
        return json.loads(xhr.responseText)
    import urllib.request
    req = urllib.request.Request(
        url,
        data=body.encode('utf-8'),
        headers={'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def run_simul_remote(backend_url):
    payload = _build_request_payload()
    try:
        response = _http_post_json(backend_url.rstrip('/') + '/simulate', payload)
    except Exception as e:
        return payload['objective'], f'Error: {e}'

    if response.get('status') == 'ok':
        return response['objective'], response['result']
    if response.get('status') == 'infeasible':
        return response['objective'], 'Status: INFEASIBLE'
    return response.get('objective', payload['objective']), f'Error: {response.get("message", "unknown")}'


if __name__ == '__main__':
     print(run_simul())
    