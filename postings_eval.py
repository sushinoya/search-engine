#superset is all the postings
#evaluate_not remove posting from the superset 
def evaluate_not(posting, superset):
    answer = []
    posting_index = 0
    superset_index = 0
    while posting_index != len(posting) and superset_index != len(superset):
        if posting[posting_index] == superset[superset_index]: #ignore postings that are the same
            posting_index += 1
            superset_index += 1
        elif posting[posting_index] < superset[superset_index]:
            answer.append(posting[posting_index])
            posting_index += 1
        else:
            answer.append(superset[superset_index])
            superset_index += 1

    while superset_index < len(superset):
        answer.append(superset[superset_index])
        superset_index += 1

    return answer


def evaluate_or(postings_1, postings_2):
    return list_union(postings_1, postings_2)

#union 2 lists together 
def list_union(list_1, list_2):
    answer = []
    list_1_index = 0
    list_2_index = 0
    while list_1_index != len(list_1) and list_2_index != len(list_2):
        if list_1[list_1_index] == list_2[list_2_index]:
            answer.append(list_1[list_1_index])
            list_1_index += 1
            list_2_index += 1
        elif list_1[list_1_index] < list_2[list_2_index]:
            answer.append(list_1[list_1_index])
            list_1_index += 1
        else:
            answer.append(list_2[list_2_index])
            list_2_index += 1

    while list_1_index < len(list_1):
        answer.append(list_1[list_1_index])
        list_1_index += 1

    while list_2_index < len(list_2):
        answer.append(list_2[list_2_index])
        list_2_index += 1

    return answer


def evaluate_and(postings_1, postings_2):
    return list_intersection(postings_1, postings_2)


#use the mergeing algorithm in lecture
def list_intersection(list_1, list_2):
    answer = []
    list_1_index = 0
    list_2_index = 0
    while list_1_index != len(list_1) and list_2_index != len(list_2):
        if list_1[list_1_index] == list_2[list_2_index]:
            answer.append(list_1[list_1_index])
            list_1_index += 1
            list_2_index += 1
        elif list_1[list_1_index] < list_2[list_2_index]:
            list_1_index += 1
        else:
            list_2_index += 1

    return answer
