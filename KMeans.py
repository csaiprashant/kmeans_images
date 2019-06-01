class KmeansSegmentation:

    def segmentation_grey(self, image, k=2):
        """Performs segmentation of an grey level input image using KMeans algorithm, using the intensity of the pixels
        as features. Takes as input:
        image: a grey scale image
        return an segemented image
        -----------------------------------------------------
        Sample implementation for K-means
        1. Initialize cluster centers
        2. Assign pixels to cluster based on (intensity) proximity to cluster centers
        3. While new cluster centers have moved:
            1. compute new cluster centers based on the pixels
            2. Assign pixels to cluster based on the proximity to new cluster centers

        """

        imgHeight = image.shape[0]
        imgWidth = image.shape[1]

        cluster_center = []  # List to store intensities of centroids of all clusters
        cluster = [[] for _ in
                   range(k)]  # Creates K lists of [x,y] lists where x,y give the position of the pixel in the cluster
        intensity = [[] for _ in
                     range(k)]  # Creates K lists to store the intensity values of all the pixels in a given cluster

        # Generate K equi-distant cluster centers
        for i in range(k):
            cluster_center.append(int((255 * i) / (k + 1)))

        print(cluster_center)

        # List to store and calculate minimum distance of each pixel from the K cluster centers
        euclid_distance = []

        def loop(argument_list):
            for i in range(imgHeight):
                for j in range(imgWidth):
                    px = image[i, j]
                    for z in range(k):
                        euclid_distance.append(abs(px - argument_list[z]))
                    # Get the index at which minimum distance occurs and append the (x,y) and intensity value to
                    # corresponding list
                    least = euclid_distance.index(min(euclid_distance))
                    cluster[least].append([i, j])
                    intensity[least].append(px)
                    # Clear the distance list so that the next pixel has an empty list to work with
                    del euclid_distance[:]

            means = []  # List to store the mean of intensities of all the pixels in the clusters
            for i in range(k):
                means.append(int(sum(intensity[i]) / len(intensity[i])))

            print(means)

            # Because of the way python typecasts float to int, convergence on a single integer value takes a lot of
            # time.(Sometimes never happens). Therefore I have allowed a +/- 1 difference in the intensities of the
            # previous centers and the new means.
            threshold = 0
            for i in range(k):
                if sorted(argument_list)[i] - 1 <= sorted(means)[i] <= sorted(argument_list)[i] + 1:
                    threshold += 1
            if threshold == k:
                # Change intensities of all the pixels in the cluster to its cluster center's intenisty
                for i in range(k):
                    for j in range(len(cluster[i])):
                        x = cluster[i][j][0]
                        y = cluster[i][j][1]
                        image[x, y] = means[i]
            else:
                # Clear the cluster and intensity lists and call the function recursively till convergence is achieved
                for i in range(k):
                    cluster[i] = []
                    intensity[i] = []
                loop(means)

        # Initial call to the function
        loop(cluster_center)
        return image

    def segmentation_rgb(self, image, k=2):
        """Performs segmentation of a color input image using KMeans algorithm, using the intensity of the pixels (R, G,
        B) as features
        takes as input:
        image: a color image
        return an segemented image"""

        imgHeight = image.shape[0]
        imgWidth = image.shape[1]

        cluster_center = [[] for _ in range(k)]  # List to store [b,r,g] of centers of all clusters
        cluster = [[] for _ in
                   range(k)]  # Creates K lists of [x,y] lists where x,y give the position of the pixel in the cluster
        intensity = [[] for _ in
                     range(k)]  # Creates K lists to store the [b,r,g] values of all the pixels in a given cluster

        # Generate and store [b,r,g] of all k cluster centers
        for i in range(k):
            for j in range(3):
                cluster_center[i].append(int(255 * i / (k + 1)))

        print(cluster_center)

        # List to store and calculate minimum euclidean distance of each pixel from the K cluster centers
        euclid_distance = []

        def loop(argument_list):
            for i in range(imgHeight):
                for j in range(imgWidth):
                    px = image[i, j]
                    for z in range(k):
                        # Calculate euclidean distance and append it to the list
                        euclid_distance.append(
                            (px[0] - argument_list[z][0]) ** 2 + (px[1] - argument_list[z][1]) ** 2 + (
                                    px[2] - argument_list[z][2]) ** 2)
                    # Get the index at which minimum distance occurs and append respective attributes to corresponding
                    # list
                    least = euclid_distance.index(min(euclid_distance))
                    cluster[least].append([i, j])
                    intensity[least].append([px[0], px[1], px[2]])
                    # Clear the distance list so that the next pixel has an empty list to work with
                    del euclid_distance[:]

            means = []  # List to store the mean [b,r,g] of all the pixels in the clusters

            # Create 3 lists to store the blue, red and green values of all the pixels in a clusters respectively
            blue, green, red = ([] for i in range(3))
            for i in range(k):
                for j in range(len(intensity[i])):
                    blue.append(intensity[i][j][0])
                    green.append(intensity[i][j][1])
                    red.append(intensity[i][j][2])
                # Compute the mean [b,r,g] and append to means list
                means.append([int(sum(blue) / len(blue)), int(sum(green) / len(green)), int(sum(red) / len(red))])
                # Clear the lists so that the next pixel has empty ones to work with
                del blue[:]
                del green[:]
                del red[:]

            print(sorted(means))

            # Because of the way python typecasts float to int, convergence on a single integer value takes a lot of
            # time.(Sometimes never happens). Therefore I have allowed a +/- 1 difference in respective [b,r,g] in the
            # intensities of the previous centers and the new means
            blue_threshold = 0
            green_threshold = 0
            red_threshold = 0
            for i in range(k):
                if sorted(argument_list)[i][0] - 1 <= sorted(means)[i][0] <= sorted(argument_list)[i][0] + 1:
                    blue_threshold += 1
                if sorted(argument_list)[i][1] - 1 <= sorted(means)[i][1] <= sorted(argument_list)[i][1] + 1:
                    green_threshold += 1
                if sorted(argument_list)[i][2] - 1 <= sorted(means)[i][2] <= sorted(argument_list)[i][2] + 1:
                    red_threshold += 1

            if blue_threshold + green_threshold + red_threshold == 3 * k:
                # Change [b,r,g] of all the pixels in the cluster to its cluster center's intenisty
                for i in range(k):
                    for j in range(len(cluster[i])):
                        x = cluster[i][j][0]
                        y = cluster[i][j][1]
                        image[x, y] = means[i]
            else:
                # Clear the cluster and intensity lists and call the function recursively till convergence is achieved
                for i in range(k):
                    cluster[i] = []
                    intensity[i] = []
                loop(means)

        # Initial call to the function
        loop(cluster_center)
        return image
