import numpy as np
"""
Test de la fonction de traitement

"""


def make_function_smooth(donnees,number_of_point_median_filter,number_of_point_smooth):
        """
        Applied a median filter to the function to reduce the noise. Then smooth the potential function to avoid noise by computing the mean of number_of_point_smooth for every value.

        Args:
        number_of_point_smooth = number of point in the average to smooth the function
        number_of_point_median_filter = number of point in the median filter
        
        Return:
        The mean of the clean donnnees
        """
        res = []
        for i in range(len(donnees)-number_of_point_median_filter+1):
            liste = []
            for j in range(number_of_point_median_filter):
                liste.append(donnees[i+j])
            
            # median filter
            test_list = liste
            test_list.sort()
            mid = len(test_list) // 2
            resu = (test_list[mid] + test_list[~mid]) / 2
            res.append(float(resu))

        for i in range(number_of_point_median_filter-1,0,-1):
            res.append(donnees[-i])
        
        potential_channel = res.copy()
        # median filter
        res = []
        for i in range(int(np.ceil(number_of_point_smooth/2))):
            res.append(potential_channel[i])
            
        for i in range(len(potential_channel)-number_of_point_smooth):
            mean = 0
            for j in range(number_of_point_smooth):
                mean += potential_channel[i+j]
            mean = mean / number_of_point_smooth
            res.append(mean)

        for i in range(int(np.floor(number_of_point_smooth/2)),0,-1):
            res.append(potential_channel[-i])
       
        return np.mean(potential_channel)

print("Test de la fonction de traitement:\n")
print("Test avec liste proche de 0.5. On doit avoir un résultat proche de 0.5")

print("Test 1 : liste peu bruitée sans valeur abhérente.")
print("%.3f"%make_function_smooth(0.5+np.random.random_sample(200)/100,3,4))

print("Test 2 : liste bruitée sans valeur abhérente." )
print("%.3f"%make_function_smooth(np.random.random_sample(200),3,4))

print("Test 3 : liste bruitée avec valeur abhérente dont 2 consécutives. A noter qu'il faut changer la taille du filtre median")
data = np.random.random_sample(200)
data[50] = 10000
data[150] = 10000
data[151] = 10000
print("%.3f"%make_function_smooth(data,5,7))

print("\nTest avec des listes croissantes. On doit avoir un résultat proche de 100.5")
data = []
data_clean = []
for i in range(200):
    data.append(i + float(np.random.random_sample(1)))
    data_clean.append(i)
print("Test 1 : liste peu bruitée sans valeur abhérente.")
print("%.3f"%make_function_smooth(data_clean,3,4))

print("Test 2 : liste bruitée sans valeur abhérente." )
print("%.3f"%make_function_smooth(data,3,4))

print("Test 3 : liste bruitée avec valeur abhérente. A noter qu'il faut changer la taille du filtre median")
data[50] = 10000
data[150] = 10000
data[151] = 10000
print("%.3f"%make_function_smooth(data,6,7))
