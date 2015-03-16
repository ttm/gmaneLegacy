import numpy as n

def circularStatistics(population, period):
    pop=n.array(population)
    pop_=pop*2*n.pi/period
    vec_n=n.e**(j*pop_)
    mean_vec=vec_n.sum()/len(pop) # first moment
    mean_angle=n.arctag2(mean_vec.real,mean_vec.imag)
    size_mean_vec=(mean_vec.real**2+mean.imag**2)**0.5
    circular_variance=1-size_mean_vec
    circular_mean=period*mean_angle/(2*n.pi)
    return mean_vec, mean_angle, circular_mean, circular_variance

class NetworkTiming:
    def __init__(self,list_datastructures=None):
        if not list_datastructures:
            print("input datastructures, please")
        datetimess=[]
        for datetime in list_datastructures.raw_clean_dates:
            datetimes.append(datetimes[1])
        self.datetimes=datetimes
        self.n_observations=len(datetimes)
        self.makeStatistics()
    def makeStatistics(self):
        """Make statistics from seconds to years"""
        self.secondsStats()
        self.uniformComparisson()
    def uniformComparisson(self):
        obs60=n.random.randint(0,60,self.n_observations)
        count_obs60=[obs60.count(i) for i in set(obs60)]
        obs24=n.random.randint(0,24,self.n_observations)
        count_obs24=[obs24.count(i) for i in set(obs24)]
        obs12=n.random.randint(0,12,self.n_observations)
        count_obs12=[obs12.count(i) for i in set(obs12)]
        
    def secondsStats(self):
        seconds=[i.second for i in self.datetimes]
        self.seconds_mean=n.mean(seconds)
        distances=[]
        for second in seconds:
            distance=abs(second-second__mean)
            if < 30:
                distances.append(distance)
            elif second < second_mean:
                distances.append(second+60-seconds_mean)
            elif:
                distances.append(seconds_mean+60-second)
        self.seconds_std=n.sqrt((n.array(distances)**2).sum()/len(distances))
        seconds_count=[seconds.count(second) for second in set(seconds)]
        self.seconds_frac=max(seconds_count)/min(seconds_count)
