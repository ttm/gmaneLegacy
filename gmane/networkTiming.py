import numpy as n

def circularStatistics(population, period):
    pop=n.array(population)
    pop_=pop*2*n.pi/period
    vec_n=n.e**(j*pop_)
    mean_vec=vec_n.sum()/len(vec_n) # first moment
    mean_angle=n.arctag2(mean_vec.real,mean_vec.imag)
    size_mean_vec=(mean_vec.real**2+mean.imag**2)**0.5
    variance_unity_radius=1-size_mean_vec
    circular_mean=mean_angle*(period/(2*n.pi))
    circular_variance=variance_unity_radius*(period/(2*n.pi))
    return mean_vec, mean_angle, size_mean_vec, circular_mean, circular_variance

class NetworkTiming:
    def __init__(self,list_datastructures=None):
        if not list_datastructures:
            print("input datastructures, please")
        datetimes=[]
        for datetime in list_datastructures.raw_clean_dates:
            datetimes.append(datetime[1])
        self.datetimes=datetimes
        self.n_observations=len(datetimes)
        self.makeStatistics()
    def makeStatistics(self):
        """Make statistics from seconds to years"""
        self.secondsStats()
        self.uniformComparisson()
    def uniformComparisson(self):
        obs60=n.random.randint(0,60,self.n_observations)
        #count_obs60=[obs60.count(i) for i in set(obs60)]
        obs24=n.random.randint(0,24,self.n_observations)
        #count_obs24=[obs24.count(i) for i in set(obs24)]
        obs12=n.random.randint(0,12,self.n_observations)
        #count_obs12=[obs12.count(i) for i in set(obs12)]
        
    def secondsStats(self):
        # contagem para histograma
        seconds=[i.seconds for i in self.datetimes]
        # medidas circulares
        pass
