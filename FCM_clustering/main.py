from FCM import FCM
import math
import matplotlib.pyplot as plt


def best_number_of_center(method, data):
    """
    This def returns best number of clusters according name of method
    :param method: name of method
    :param data: result of this method for range of number of clusters
    :return: best number of clusters
    """
    if method == 'entropy':
        ent_min = math.inf
        best_number_of_cluster = 0
        for i in range(len(data)):
            if data[i] < ent_min:
                best_number_of_cluster = i
                ent_min = data[i]
        return best_number_of_cluster
    elif method == 'reconstruction_error' or 'cost':
        for i in range(len(data[:-1])):
            if data[i] - data[i+1] < 2:
                return i


def finding_best_number_of_clusters(file_path):
    """
    This def uses different method to find best number of clusters
    :param file_path: path to data file
    :return: best number of clusters for all methods
    """
    all_ent = []
    all_reconstruction_error = []
    all_costs = []
    all_centers = [i for i in range(2, 10)]
    for i in range(2,10):
        f = FCM(file_path, i, 2)
        f.run(show_plots=False)
        ent = f.compute_entropy()
        reconstruction_error = f.compute_reconstruction_error()
        cost = f.compute_cost()
        all_ent.append(ent)
        all_reconstruction_error.append(reconstruction_error)
        all_costs.append(cost)
    best_number_of_cluster1 = best_number_of_center('entropy', all_ent) + 2
    best_number_of_cluster2 = best_number_of_center('reconstruction_error', all_reconstruction_error) + 2
    best_number_of_cluster3 = best_number_of_center('cost', all_costs) + 2

    fig, diagram = plt.subplots(1, 3, figsize=(20, 10))
    diagram[0].plot(all_centers, all_ent)
    diagram[0].set_xlabel('X0')
    diagram[0].set_ylabel('X1')
    diagram[0].set_title('entropy')
    diagram[1].plot(all_centers, all_reconstruction_error)
    diagram[1].set_xlabel('X0')
    diagram[1].set_ylabel('X1')
    diagram[1].set_title('reconstruction error')
    diagram[2].plot(all_centers, all_costs)
    diagram[2].set_xlabel('X0')
    diagram[2].set_ylabel('X1')
    diagram[2].set_title('costs')
    plt.show()
    return best_number_of_cluster1, best_number_of_cluster2, best_number_of_cluster3


a1 = input('1.finding number of clusters\n2.run algorithm\n')
a2 = input('1.sample1.csv\n2.sample2.csv\n3.sample3.csv\n4.sample4.csv\n')
if a1 == '1':
    best = finding_best_number_of_clusters('sample{}.csv'.format(a2))
    print('Best number of clusters for this samples is:')
    print('     from entropy diagram: ' + str(best[0]))
    print('     from reconstruction error diagram: ' + str(best[1]))
    print('     from cost diagram: ' + str(best[2]))
else:
    number_of_clusters = input('Inter number of clusters:\n')
    F = FCM('sample{}.csv'.format(a2), int(number_of_clusters), 1.1)
    centers = F.run()
    print('Centers of this samples:')
    for c in centers:
        print(c)
