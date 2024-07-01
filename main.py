import math
import sys


def k_mean(k, input_data, iter=200):
    # TODO handle excpetions
    #TODO 4 decimals after point
    epsilon = 0.001
    exists_bigger_than_eps = True
    data_points_to_index = init_data_points(input_data,k)  # data point, cluster index
    clusters = [[data_point[0], [i]] for i, data_point in
                enumerate(data_points_to_index[:k])]  # centroid, arr of indices of points

    iterations = 0
    while exists_bigger_than_eps and iterations < iter:
        ##assign all data points to the closest centroids##
        for i, data_point_to_index in enumerate(data_points_to_index):
            assign_dp_to_closest_cluster(data_point_to_index, data_points_to_index, clusters, i)

        ##calc new centroids after the assignment of the data points and checking the epsilon condition##
        exists_bigger_than_eps = False
        for cluster in clusters:
            new_centroid = calc_centroid(cluster[1], data_points_to_index)
            if calc_distance(new_centroid, cluster[0]) >= epsilon:
                exists_bigger_than_eps = True
            cluster[0] = new_centroid

        iterations += 1

    return [cluster[0] for cluster in clusters]


def init_data_points(input_data, k):
    data_points = []
    with open(input_data, 'r') as file:
        for i, line in enumerate(file):
            data_point = list(map(float,line.split(",")))

            index = -1
            if i < k:
                index = i
            data_points.append([data_point, index])
    return data_points


def closest_cluster(data_point, clusters):
    min_dist = sys.maxsize
    min_ind = 0
    centroids = [cluster[0] for cluster in clusters]
    for i, centroid in enumerate(centroids):
        distance = calc_distance(data_point, centroid)
        if distance < min_dist:
            min_dist = distance
            min_ind = i
    return min_ind


def calc_distance(d1, d2):
    sum = 0
    for i in range(len(d1)):
        sum += (d1[i] - d2[i]) ** 2
    return math.sqrt(sum)


def assign_dp_to_closest_cluster(data_point_to_index, data_points_to_index, clusters, i):
    prev_index = data_point_to_index[1]
    if prev_index != -1:
        clusters[prev_index][1].remove(i)
    cluster_index = closest_cluster(data_point_to_index[0],clusters)
    data_points_to_index[i][1] = cluster_index
    clusters[cluster_index][1].append(i)


def calc_centroid(indices, data_points_to_index):
    centroid = []
    num_of_data_points = len(indices)
    dp_in_cluster = [data_points_to_index[i][0] for i in indices]
    for i in range(len(dp_in_cluster[0])):
        sum = 0
        for dp in dp_in_cluster:
            sum += dp[i]
        centroid.append(sum / num_of_data_points)
    return centroid

print(k_mean(3,"data/input_1.txt", iter = 600))
