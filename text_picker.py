import json


def pick(filename, record_num):
    with open(filename) as f:
        json_content = f.read()
        frames = json.loads(json_content)

    utterances = []
    i = 0
    # record_num = 100
    for frame in frames:
        if i > record_num:
            print('more than ', record_num, ', break outer_for')
            break
        turns = frame['turns']
        for t in range(0, len(turns)-1, 2):
            i += 1
            if i > record_num:
                print('more than ', record_num, ', break inner_for')
                break

            turn_q = turns[t]
            turn_a = turns[t+1]

            # get text
            text_q = turn_q['text']
            text_a = turn_a['text']
            utterance = text_q + '\t' + text_a

            utterances.append(utterance)

    # write into new files
    with open('text_' + str(record_num) + '.tsv', 'w') as f:
        f.write('\n'.join(utterances))


# dunplicated
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

# dunplicated
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
    pick(jsonfile, 10000)