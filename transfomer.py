import json


# from Calgary

def transform(filename):
    with open(filename) as f:
        json_content = f.read()
        # print(json_content)

        frames = json.loads(json_content)

    # print(frames)

    utterances = []
    i = 0
    record_num = 1000
    for frame in frames:
        if i > record_num:
            print('more than ', record_num, ', break outer_for')
            break
        turns = frame['turns']
        # for turn in turns:
        turn = turns[0]
        if turn['author'] == 'user':
            i += 1
            if i > record_num:
                print('more than ', record_num, ', break inner_for')
                break

            utterance = {}

            # get text
            text = turn['text']
            if text.find('USD') > 0:
                index = text.find('USD')
                text_list = list(text)
                text_list[index] = ''
                text_list[index+1] = ''
                text_list[index+2] = ''
                text = ''.join(text_list)


            # if text.find('\'') > 0:
            #     index = text.find('\'')
            #     text_list = list(text)
            #     text_list[index] = ','
            #
            #     text = ''.join(text_list)

            utterance['text'] = text

            frame = turn['labels']['frames'][0]
            info = frame['info']

            # get intent
            if 'intent' in info:
                intent_val = info['intent'][0]['val']
                utterance['intent'] = intent_val
            else:
                utterance['intent'] = 'None'

            # get entities
            entities = []
            if 'budget' in info:
                budget_val = info['budget'][0]['val']
                if is_num(budget_val):
                    real_budget_val = str(int(float(budget_val)))
                    startPos_b = text.find(real_budget_val)
                    if startPos_b > 0:
                        endPos_b = startPos_b + len(real_budget_val) - 1
                        entity = {"entity": "budget", "startPos": startPos_b, "endPos": endPos_b}
                        entities.append(entity)

            if 'dst_city' in info:
                dst_city_val = info['dst_city'][0]['val']
                startPos_d = text.find(dst_city_val)
                if startPos_d > 0:
                    endPos_d = startPos_d + len(dst_city_val) - 1
                    entity = {"entity": "dst_city", "startPos": startPos_d, "endPos": endPos_d}
                    entities.append(entity)

            if 'or_city' in info:
                or_city_val = info['or_city'][0]['val']
                startPos_o = text.find(or_city_val)
                if startPos_o > 0:
                    endPos_o = startPos_o + len(or_city_val) - 1
                    entity = {"entity": "or_city", "startPos": startPos_o, "endPos": endPos_o}
                    entities.append(entity)

            if 'str_date' in info:

                str_date_val = info['str_date'][0]['val']
                startPos_s = text.find(budget_val)
                if startPos_s > 0:
                    endPos_s = startPos_s + len(budget_val) - 1
                    entity = {"entity": "str_date", "startPos": startPos_s, "endPos": endPos_s}
                    entities.append(entity)

            if 'n_adults' in info:
                n_adults_val = info['n_adults'][0]['val']
                startPos_n = text.find(n_adults_val)
                if startPos_n > 0:
                    endPos_n = startPos_n + len(n_adults_val) - 1
                    if judge_isl(text, startPos_n, endPos_n):
                        entity = {"entity": "n_adults", "startPos": startPos_n, "endPos": endPos_n}
                        entities.append(entity)

            utterance['entities'] = entities

            utterances.append(utterance)

    frames_to_rewrite = {
        "luis_schema_version": "2.1.0",
        "versionId": "0.1",
        "name": "MyTravleAgent",
        "desc": "",
        "culture": "en-us",
        "intents": [
            {
                "name": "book"
            },
            {
                "name": "None"
            }
        ],
        "entities": [
            {
                "name": "budget"
            },
            {
                "name": "dst_city"
            },
            {
                "name": "or_city"
            },
            {
                "name": "str_date"
            },
            {
                "name": "n_adults"
            }
        ],
        "composites": [],
        "closedLists": [],
        "bing_entities": [
            "datetimeV2",
            "number"
        ],
        "model_features": [],
        "regex_features": [],
        "utterances": utterances
    }
    # print(utterances)

    # write into new files
    with open('frames-rewrite_' + str(record_num) + '.json', 'w') as f:
        json.dump(frames_to_rewrite, f, indent=2)

def judge_isl(text, startPos, endPos):
    if startPos == 0:
        next1 = text[endPos + 1]
        if next1.isdigit() or next1.isalpha():
            return False
        else:
            return True
    elif endPos == len(text) - 1:
        prev1 = text[startPos - 1]
        # next = text[endPos + 1]
        if prev1.isdigit() or prev1.isalpha():
            return False
        else:
            return True
    else:
        prev = text[startPos-1]
        next = text[endPos+1]
        if prev.isdigit() or prev.isalpha() or next.isdigit() or next.isalpha():
            return False
        else:
            return True


def is_num(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

if __name__ == '__main__':
    jsonfile = 'frames.json'
    transform(jsonfile)
