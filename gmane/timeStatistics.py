import numpy as n, calendar, datetime

def circularStatistics(population, period):
    pop=n.array(population)
    pop_=pop*2*n.pi/period
    j=n.complex(0,1)
    vec_n=n.e**(j*pop_)
    mean_vec=vec_n.sum()/len(vec_n) # first moment
    mean_angle=n.arctan2(mean_vec.real,mean_vec.imag)
    size_mean_vec=n.abs(mean_vec)
    variance_unity_radius=1-size_mean_vec
    std_unity_radius=n.log(-2*size_mean_vec)
    circular_mean=mean_angle*(period/(2*n.pi))
    circular_variance=variance_unity_radius*(period/(2*n.pi))
    circular_std=std_unity_radius*(period/(2*n.pi))

    second_moment=(vec_n**2).sum()/len(vec_n)
    size_second_moment=n.abs(second_moment)
    circular_dispersion=(1-size_second_moment)/(2*(size_mean_vec**2))

    return mean_vec, mean_angle, size_mean_vec, circular_mean, circular_variance, circular_dispersion

class TimeStatistics:
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
        self.minutesStats()
        self.hoursStats()
        self.weekdaysStats()
        self.monthdaysStats()
        self.monthsStats()
        self.yearsStats()
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
        seconds=[i.second for i in self.datetimes]
        histogram=n.histogram(seconds,bins=list(range(61)))[0]
        max_discrepancy=histogram.max()/histogram.min()
        # medidas circulares
        circular_measures=circularStatistics(seconds,60)
        seconds=dict(
            circular_measures=circular_measures,
            max_discrepancy=max_discrepancy,
            samples=seconds,
            histogram=histogram)
        self.seconds=seconds

    def minutesStats(self):
        samples=[i.minute for i in self.datetimes]
        histogram=n.histogram(samples,bins=list(range(61)))[0]
        max_discrepancy=histogram.max()/histogram.min()
        # medidas circulares
        circular_measures=circularStatistics(samples,60)
        minutes=dict(
            samples=samples,
            histogram=histogram,
            max_discrepancy=max_discrepancy,
            circular_measures=circular_measures
        )
        self.minutes=minutes


    def hoursStats(self):
        samples=[i.hour for i in self.datetimes]
        histogram=n.histogram(samples,bins=list(range(25)))[0]
        max_discrepancy=histogram.max()/histogram.min()
        # medidas circulares
        circular_measures=circularStatistics(samples,24)
        hours=dict(
            samples=samples,
            histogram=histogram,
            max_discrepancy=max_discrepancy,
            circular_measures=circular_measures
        )
        self.hours=hours
    def weekdaysStats(self):
        samples=[i.weekday() for i in self.datetimes]
        histogram=n.histogram(samples,bins=list(range(8)))[0]
        max_discrepancy=histogram.max()/histogram.min()
        # medidas circulares
        circular_measures=circularStatistics(samples,7)
        self.weekdays=dict(
            samples=samples,
            histogram=histogram,
            max_discrepancy=max_discrepancy,
            circular_measures=circular_measures
        )
    def monthdaysStats(self):
        def aux(xx):
            return xx.weekday()/(
                    calendar.monthrange(xx.year, xx.month)[1] )
        samples=[aux(i) for i in self.datetimes]
        mean_month_size=n.mean([calendar.monthrange(xx.year, xx.month)
            for xx in self.datetimes])
        mean_month_size=n.round(mean_month_size)
        histogram=n.histogram(samples,bins=n.linspace(0,1,mean_month_size))[0]
        max_discrepancy=histogram.max()/histogram.min()
        # medidas circulares
        circular_measures=circularStatistics(samples,7)
        self.monthdays=dict(
            mean_month_size=mean_month_size,
            samples=samples,
            histogram=histogram,
            max_discrepancy=max_discrepancy,
            circular_measures=circular_measures
        )
    def monthsStats(self,truncate=True):
        year=365.242199 # days
        if truncate:
            delta=self.datetimes[-1]-self.datetimes[0]
            if delta.days > year:
                delta_=(delta.total_seconds()/(24*60*60))%year
                max_date=self.datetimes[-1]-datetime.timedelta(delta_%year)
            else:
                max_date=self.datetimes[-1]
            samples=[i.month for i in self.datetimes if i <= max_date]
        else:
            samples=[i.month for i in self.datetimes]
        histogram=n.histogram(samples,bins=list(range(13)))[0]
        max_discrepancy=histogram.max()/histogram.min()
        # medidas circulares
        circular_measures=circularStatistics(samples,12)
        self.weekdays=dict(
            samples=samples,
            histogram=histogram,
            max_discrepancy=max_discrepancy,
            circular_measures=circular_measures
        )
    def yearsStats(self):
        samples=[i.year for i in self.datetimes]
        smin=min(samples)
        smax=max(samples)
        histogram=n.histogram(samples,bins=list(range(smin,smax+2)))[0]
        max_discrepancy=histogram.max()/histogram.min()
        self.years=dict(
            samples=samples,
            histogram=histogram,
            max_discrepancy=max_discrepancy,
        )







