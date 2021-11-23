import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
from sklearn.mixture import GaussianMixture as GMM
import math
class stabelisation_class():
    def __init__(self) -> None:
        pass
        
    def dispertion(self, signal, width = 5, fs = 4):
        """Metoden bruger dispertion til at vurdere hvornår signalet er stabilt. Disperstion bruges i tidsdomænet. 

        Args:
            signal (list<float>): Denne liste indeholder signalet, der ønskes at finde stabiliseringsindexet på
            width (int, optional): Bredden af vinduet angivet i sekunder. Defaults to 20.
            fs (int, optional): Samplefrekvens for signalet. Default er 4, svarende til samplefrekvensen for HRM-Pro og Forerunner.

        Returns:
            index (int): Der returneres et index svarende til den midterste værdi når vinduet har en højde mindre end 10 BPM. De 10 BPM er fundet på baggrund af tidligere testmålinger
        """
        index = 0
        width_index = width*fs
        final_heights_list = []
        for i in range(len(signal)-width_index):
            window_content = []
            for n in range(width_index):
                window_content.append(signal[i+n])
            height = max(window_content) - min(window_content)
            final_heights_list.append(height)
        maximum = max(final_heights_list)
        reached_maximum = False
        n=0
        for height in final_heights_list:
            if(reached_maximum == True and height <=10):
                index = n
                break
            elif(height == maximum):
                reached_maximum=True
            n+=1

        # plt.plot(final_heights_list)
        # plt.show()
        return index

    def gmm(self, signal: list, counter = 0):
        # init_1, init_2 = self.__initial_parameters(signal)
        # means = np.array([[init_1],[init_2]])
        # gmm = GMM(n_components=2, means_init=means)
        gmm = GMM(n_components=2)
        
        reshaped = signal.reshape(-1,1)
        results = gmm.fit(reshaped)
        #print(str(counter) + " Low mean: " + str(min(results.means_)) + " High mean " + str(max(results.means_)))
        reached_maximum = False
        maximum = max(signal)

        self.std_low = math.sqrt(min(results.covariances_))
        self.std_high = math.sqrt(max(results.covariances_))
        self.mean_low = min(results.means_[0])
        self.mean_high = max(results.means_[1])

        limit = min(results.means_) + self.std_low
        n=0
        index = len(signal)-1
        for hr in signal:
            if(reached_maximum == True and hr <= limit):
                index = n
                break
            elif(hr == maximum):
                reached_maximum=True
            n+=1
            
        return index

    def __initial_parameters(self,signal):
        hr_list = self.__remove_X_percentages(signal,0)
        minimum = min(hr_list)
        maximum = max(hr_list)
        split = minimum + int(round((maximum-minimum)/2))
        high = []
        low = []
        for hr in hr_list:
            if(hr <= split):
                low.append(hr)
            else:
                high.append(hr)
        mean_low = sum(low)/len(low)
        mean_high = sum(high)/(len(high))

        return mean_low, mean_high

    def get_means(self):
        return self.mean_low, self.mean_high

    def get_stds(self):
        return self.std_low, self.std_high


    def __remove_X_percentages(self,signal, percentage_to_remove):
        list_to_sort = signal.copy()
        if(percentage_to_remove != 0):
            list_to_sort.sort()
            length_of_list = len(list_to_sort)
            amount_to_remove = int(round((length_of_list/100)*percentage_to_remove))
            from_end = length_of_list-amount_to_remove
            list_to_sort = list_to_sort[amount_to_remove-1:from_end] # Fjerne de laveste og højeste 10 %
            # list_to_sort = list_to_sort[0:from_end] # Fjerner kun de højeste 10 %
        return list_to_sort

