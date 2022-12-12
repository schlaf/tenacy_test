import requests
import itertools

total_api_count = 0
api_url = "https://technical-test.tools.tenacy.io/"
bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1hY2hpbkBleGFtcGxlLmNvbSIsImV4cCI6MTY3MjEzNjg4Mn0.Adzp1EenG95HhxQhKafFTYM6d8O77hEqUWdJS5dWsuE"
common_headers = {
                "accept": "accept: application/json",
                "Authorization": "Bearer " + bearer_token
            }
api_risk = { 'method': "risk", 'type': 'GET'}
api_measure = { 'method': "measure", 'type': 'GET'}
api_play = { 'method': "play", 'type': 'POST'}




def call_tenacy_api(api, optionalBody = None):
    add_one_api_call()
    if (api['type'] == 'GET'):
        response = requests.get(api_url + api['method'],
            headers=common_headers
        )

    if (api['type'] == 'POST'):
        response = requests.post(api_url + api['method'],
            headers=common_headers,
            json=optionalBody
        )

    return response.json()

def add_one_api_call():
    global total_api_count
    total_api_count +=1

def explore_risks():
    return call_tenacy_api(api_risk)

def explore_measures():
    return call_tenacy_api(api_measure)

def test_one_measure(measure_id):
    return play([measure_id])

def play(combinaison):
    list_of_measures = []
    for measure in combinaison:
        list_of_measures.append(measure)
    data = {"measures": list_of_measures}
    return call_tenacy_api(api_play, data)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    risks = explore_risks()
    dico_risk = {}
    for risk in risks:
        dico_risk[risk['identifier']] = risk


    measures = explore_measures()
    dico_measure = {}
    for measure in measures:
        score_of_measure = test_one_measure(measure['identifier'])
        measure['risk_coverage'] = score_of_measure
        dico_measure[measure['identifier']] = measure


    # heuristique d'optimisation
    # pick 3 of n measures and compute score
    combinations = list(itertools.combinations(measures, 3))

    best_combination = {}
    best_score = 0
    for combination in combinations:
        score = 0
        cost = 0
        for m in combination:
            score += m['risk_coverage']['score']
            cost += m['cost']
        if cost <= 100:
            if score > best_score:
                best_combination = combination
                best_score = score




    final_result = []
    final_cost = 0
    for m in best_combination:
        final_result.append(m['identifier'])
        final_cost += m['cost']


    play_result = play(final_result)

    print('meilleure combinaison = ' + str(final_result))
    print('---')
    for m in best_combination:
        print('\t' + m['identifier'] + '|' + dico_measure[m['identifier']]['name'] + " cout = " + str(dico_measure[m['identifier']]['cost']))
    print('---')

    print('prix = ' + str(final_cost))
    print('couverture globale = ' + str(play_result['score']))
    print('---')
    for risk_couvert in play_result['risks']:
        print('\t' + dico_risk[risk_couvert['identifier']]['name'] + ' | couverture = ' + str(risk_couvert['coverage']) + '% pour criticite = ' + str(risk_couvert['severity']) )
    print('---')
    print("nb total appels API = " + str(total_api_count))
