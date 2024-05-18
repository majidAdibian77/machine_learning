import math


def get_training_data():
    ham_file = open('HAM-Train-Test/HAM-Train.txt', 'r', encoding='utf-8')
    # Ham_file = open('temp.txt', 'r')
    # f = open('temp.txt', 'w')
    class_probability = {}
    class_dictionary = {}
    for line in ham_file.readlines():
        index = line.find("@")
        class_str = line[:index]

        if class_str in class_probability.keys():
            class_probability[class_str] += 1
        else:
            class_probability[class_str] = 1

        # class_dictionary[class_str] = {}
        model = {'number_of_words': 0}
        first_index = index + 11  # Going to index of start of first word
        last_index = line[first_index:].find(' ') + first_index  # Going to index of end of first word
        word = line[first_index:last_index]
        model['$ ' + word] = 1  # Probability of start word of sentence
        model[word] = 1  # Probability of first word
        model['$'] = 1  # Probability of new line
        new_word = word
        while last_index < len(line) - 1:
            last_word = new_word
            first_index = last_index + 1  # Going to index of start of next word
            last_index = line[first_index:].find(' ') + first_index  # Going to index of end of next word
            if last_index == first_index - 1:  # If word is last word of line
                if line[-1] == '\n':
                    last_index = len(line) - 1
                else:
                    last_index = len(line)
            new_word = line[first_index:last_index]
            if new_word in model.keys():
                model[new_word] += 1
            else:
                model[new_word] = 1
            model['number_of_words'] += 1
            tow_word = last_word + ' ' + new_word
            if tow_word in model.keys():
                model[tow_word] += 1
            else:
                model[tow_word] = 1
        if class_str in class_dictionary.keys():
            for word in model.keys():
                if word in class_dictionary[class_str].keys():
                    class_dictionary[class_str][word] += model[word]
                else:
                    class_dictionary[class_str][word] = model[word]
        else:
            class_dictionary[class_str] = model
    ham_file.close()
    sum_count_class = 0
    for class_name in class_probability.keys():
        sum_count_class += class_probability[class_name]
    for class_name in class_probability.keys():
        class_probability[class_name] = class_probability[class_name] / sum_count_class
    return class_dictionary, class_probability


def calculate_class_in_unigram(class_dictionary, class_probability):
    test_file = open('HAM-Train-Test/HAM-Test.txt', 'r', encoding='utf-8')
    result = []
    predict_class = {}  # Calculate number of predicted class for all classes
    number_of_incorrect_answer = 0
    number_of_correct_answer = 0
    number_of_line = 0
    for class_name in class_dictionary.keys():
        predict_class[class_name] = {}
    for line in test_file.readlines():
        probability = {}
        for class_name in class_dictionary.keys():
            probability[class_name] = math.log10(class_probability[class_name])
        number_of_line += 1
        index = line.find("@")
        class_str = line[:index]
        last_index = index + 10
        while last_index < len(line) - 1:
            first_index = last_index + 1  # Going to index of start of next word
            last_index = line[first_index:].find(' ') + first_index  # Going to index of end of next word
            if last_index == first_index - 1:  # If word is last word of line
                last_index = len(line) - 1
            word = line[first_index:last_index]
            for class_name in class_dictionary.keys():  # Calculate probability of word in all classes
                # *********************
                # *********************
                if word in class_dictionary[class_name].keys():
                    word_probability = (class_dictionary[class_name][word] / class_dictionary[class_name][
                        'number_of_words']) + 0.000001
                else:
                    word_probability = 0.000001
                probability[class_name] += math.log10(word_probability)

        max_probability = -math.inf
        max_probability_class = ''
        for class_name in probability.keys():
            if probability[class_name] > max_probability:
                max_probability = probability[class_name]
                max_probability_class = class_name
        if max_probability_class == class_str:  # If we recognize the class name correctly
            number_of_correct_answer += 1
            if 'TP' in predict_class[class_str].keys():
                predict_class[class_str]['TP'] += 1
            else:
                predict_class[class_str]['TP'] = 1
            result.append('Line ' + str(number_of_line) + ' has recognized correctly: ' + class_str)
        else:  # If we recognize the class name incorrectly
            number_of_incorrect_answer += 1
            wrong_class = ('FP ' + max_probability_class)
            if wrong_class in predict_class[class_str].keys():
                predict_class[class_str][wrong_class] += 1
            else:
                predict_class[class_str][wrong_class] = 1
            result.append('Line ' + str(number_of_line) + ' has recognized incorrectly: ' +
                          class_str + ' is True and ' + max_probability_class + ' is false')
    test_file.close()
    return [result, number_of_correct_answer, number_of_incorrect_answer, predict_class]


def calculate_class_in_bigram(class_dictionary, class_probability):
    test_file = open('HAM-Train-Test/HAM-Test.txt', 'r', encoding='utf-8')
    result = []
    predict_class = {}  # Calculate number of predicted class for all classes
    number_of_incorrect_answer = 0
    number_of_correct_answer = 0
    probability = {}
    for class_name in class_dictionary.keys():
        predict_class[class_name] = {}
    for class_name in class_dictionary.keys():
        probability[class_name] = math.log10(class_probability[class_name])
    number_of_line = 0
    for line in test_file.readlines():
        probability = {}
        for class_name in class_dictionary.keys():
            probability[class_name] = math.log10(class_probability[class_name])
        number_of_line += 1
        index = line.find("@")
        class_str = line[:index]
        last_index = index + 10
        last_word = '$'
        while last_index < len(line) - 1:
            first_index = last_index + 1  # Going to index of start of next word
            last_index = line[first_index:].find(' ') + first_index  # Going to index of end of next word
            if last_index == first_index - 1:  # If word is last word of line
                last_index = len(line) - 1
            new_word = line[first_index:last_index]
            tow_word = last_word + ' ' + new_word
            for class_name in class_dictionary.keys():  # Calculate probability of word in all classesپ
                if tow_word in class_dictionary[class_name].keys():
                    word_probability = (class_dictionary[class_name][tow_word] / class_dictionary[class_name][
                        last_word]) * 0.50 + (class_dictionary[class_name][new_word] / class_dictionary[class_name][
                        'number_of_words']) * 0.50 + 0.0000001
                elif new_word in class_dictionary[class_name].keys():
                    word_probability = (class_dictionary[class_name][new_word] / class_dictionary[class_name][
                        'number_of_words']) * 0.50 + 0.0000001
                else:
                    word_probability = 0.0000001
                probability[class_name] += math.log10(word_probability)
            last_word = new_word

        max_probability = -math.inf
        max_probability_class = ''
        for class_name in probability.keys():
            if probability[class_name] > max_probability:
                max_probability = probability[class_name]
                max_probability_class = class_name
        if max_probability_class == class_str:  # If we recognize the class name correctly
            number_of_correct_answer += 1
            if 'TP' in predict_class[class_str].keys():
                predict_class[class_str]['TP'] += 1
            else:
                predict_class[class_str]['TP'] = 1
            result.append('Line ' + str(number_of_line) + ' has recognized correctly: ' + class_str)
        else:  # If we recognize the class name incorrectly
            number_of_incorrect_answer += 1
            wrong_class = ('FP ' + max_probability_class)
            if wrong_class in predict_class[class_str].keys():
                predict_class[class_str][wrong_class] += 1
            else:
                predict_class[class_str][wrong_class] = 1
            result.append('Line ' + str(number_of_line) + ' has recognized incorrectly: ' +
                          class_str + ' is True and ' + max_probability_class + ' is false')
    test_file.close()
    return [result, number_of_correct_answer, number_of_incorrect_answer, predict_class]


def get_precision(TP_FP_class):
    precision_of_class = {}
    for key in TP_FP_class.keys():
        TP_FP = TP_FP_class[key]
        sum_FP = 0
        for key2 in TP_FP:
            # print('      ' + key2 + ': ' + str(TP_FP[key2]))
            if key2 != 'TP':
                sum_FP += TP_FP[key2]
        precision = TP_FP['TP'] / (sum_FP + TP_FP['TP'])
        precision_of_class[key] = precision
        print('      ' + key + ': ' + 'precision: ' + str(precision))
    return precision_of_class


def get_recall(TP_FP_class):
    recall_of_class = {}
    for key in TP_FP_class.keys():
        sum_FP = 0
        for key2 in TP_FP_class.keys():
            for key3 in TP_FP_class[key2].keys():
                if key in key3:
                    sum_FP += TP_FP_class[key2][key3]
                    break
        recall = TP_FP_class[key]['TP'] / (TP_FP_class[key]['TP'] + sum_FP)
        recall_of_class[key] = recall
        print('      ' + key + ': ' + 'recall: ' + str(recall))
    return recall_of_class


class_dictionary, class_probability = get_training_data()
result = calculate_class_in_unigram(class_dictionary, class_probability)
print('unigram: True:' + str(result[1]) + ',  False:' + str(result[2]))
class_precision_unigram = get_precision(result[3])
print()
class_recall_unigram = get_recall(result[3])
print('F_measure')
for class_name in class_precision_unigram.keys():
    precision = class_precision_unigram[class_name]
    recall = class_recall_unigram[class_name]
    F_measure = (2 * precision * recall) / (precision + recall)
    print('      ' + class_name + ': ' + str(F_measure))

print()
result = calculate_class_in_bigram(class_dictionary, class_probability)
print('bigram: True:' + str(result[1]) + ',  False:' + str(result[2]))
class_precision_bigram = get_precision(result[3])
print()
class_recall_bigram = get_recall(result[3])
print('F_measure')
for class_name in class_precision_bigram.keys():
    precision = class_precision_bigram[class_name]
    recall = class_recall_bigram[class_name]
    F_measure = (2 * precision * recall) / (precision + recall)
    print('      ' + class_name + ': ' + str(F_measure))
