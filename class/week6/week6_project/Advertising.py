import numpy as np
import matplotlib.pyplot as plt
import random
random.seed(100)


class AB_testing():
    def __init__(self, filename):
        self.result = {
            0: {'buy': 0, 'not_buy': 0},
            1: {'buy': 0, 'not_buy': 0},
            2: {'buy': 0, 'not_buy': 0},
            3: {'buy': 0, 'not_buy': 0},
            4: {'buy': 0, 'not_buy': 0},
            5: {'buy': 0, 'not_buy': 0},
            6: {'buy': 0, 'not_buy': 0},
            7: {'buy': 0, 'not_buy': 0},
            8: {'buy': 0, 'not_buy': 0},
        }

        self.cvr = {
            0:[],
            1:[],
            2:[],
            3:[],
            4:[],
            5:[],
            6:[],
            7:[],
            8:[]
        }

        self.customer = np.loadtxt(filename)
        self.N=len(self.customer)
        self.version=len(self.customer[0])

    def sample(self):
        """picks a version of advertisement randomly"""
        ##To do
        raise NotImplementedError

    def update_result(self):
        """updates the self.result and self.cvr based on the purchasing outcome of each customer"""
        ##To do
        raise NotImplementedError

    def best(self):
        """Return the best version of advertisement"""
        ##To do
        raise NotImplementedError

    def draw(self,x_range,title):
        for i in range(0, self.version):
            plt.plot(range(0, x_range), list(self.cvr.values())[i][:x_range], label=i)
            plt.legend()
            plt.xlabel('Number of Customers', fontsize=12)
            plt.ylabel('Conversion Rate', fontsize=12)
        plt.savefig(title)




class Thompson_sampling(AB_testing):

    def sample(self):
        """picks a version of advertisement using Thompson sampling algorithm"""
        ##To do
        raise NotImplementedError


if __name__=="__main__":
    a=AB_testing('custumer.txt')
    a.update_result()
    plt.figure(0)
    a.draw(2000,'AB_Testing.png')


    t=Thompson_sampling('custumer.txt')
    t.update_result()
    plt.figure(1)
    t.draw(2000,'Thompson_Sampling.png')

    print('The best version is:')
    print('AB Testing Result:', a.best())
    print('Thompson Sampling Result:', t.best())
