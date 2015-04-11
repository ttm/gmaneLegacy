from lxml import html
import requests, urllib, os, pickle, logging
import numpy as n

class DownloadGmaneData:
    """Class for downloading Gmane data to local file system

    initialize with a basedir to store email messages
    and with a logging_file to store download information:
    dl=DownloadGmaneData() # OR
    dl=DownloadGmaneData("~/gmane2/","dl.log")

    Methods
    =======
    downloadListIDS(load_local=True) :: retrieves all self.list_ids from Gmane
    downloadListMessages(list_id) :: downloads messages from a GMANE email list with list_id (use self.list_ids[n] if id not at hand)
    getDownloadedLists() :: retrieves all list_ids whose messages have been downloaded
    cleanDownloadedLists() :: cleans lists from empty messages at the end and at the beggining of non-empty messages (empty messages in between are left for coherence).
    downloadedStats() :: raises elementary info about downloaded lists in _BASE_DIR/stats.txt. Generates self.stats and self.lists, the first a dictionary of stats for each list_id and "all" (overall stats). The second a list of each list statistics ordered from the lists with more messages to the ones with the fewest.

    Deprecated methods
    ==================
    correctFilenames() :: corrects the filenames to be 8 digit integers
    """
    def __init__(self,basedir="~/.gmane/",logging_file="download.log"):
        self._BASE_DIR=basedir.replace("~",os.path.expanduser("~"))
        if not os.path.isdir(self._BASE_DIR):
            os.mkdir(self._BASE_DIR)
        self._empty_messages_count=0
        logging.basicConfig(filename=logging_file,format='%(asctime)s: %(message)s',level=logging.DEBUG)
        self.getDownloadedLists()
    def correctFilenames(self):
        """Ensure that all message filenames are 8 digit integers"""
        try:
            self.downloaded_lists
        except AttributeError:
            self.getDownloadedLists()
        for elist in self.downloaded_lists:
            mfiles=os.listdir(self._BASE_DIR+elist)
            mfiles=[i for i in mfiles if i.isdigit()]
            for mfile in mfiles:
                oldname="{}{}/{}".format(self._BASE_DIR,elist,mfile)
                newname="{}{}/{}".format(self._BASE_DIR,elist,"%08d"%int(mfile))
                os.rename(oldname,newname)
    def cleanDownloadedLists(self):
        """Remove empty messages from the beggining or end of each list"""
        try:
            self.downloaded_lists
        except AttributeError:
            self.getDownloadedLists()
        for elist in self.downloaded_lists:
            mfiles=os.listdir(self._BASE_DIR+elist)
            mfiles.sort()
            sizes=[os.path.getsize("{}{}/{}".format(self._BASE_DIR,elist,i)) for i in mfiles]
            sizes_=[i==0 for i in sizes]
            # remove suffix
            try:
                findex=-sizes_[::-1].index(False)
            except ValueError:
                logging.info("no messages for list {}".format(elist))
                for ind, filename in enumerate(mfiles):
                    logging.info("removing file {}/{} of size {}".format(elist,filename,sizes[ind]))
                    os.remove("{}{}/{}".format(self._BASE_DIR,elist,filename))
            else:
                if (findex>0) and (sum(sizes_[findex:])==-findex):
                    # remove todos os arquivos de findex até o final
                    for ind,filename in enumerate(mfiles[findex:]):
                        logging.info("removing file {}/{} of size {}".format(elist,filename,sizes[findex+ind]))
                        os.remove("{}{}/{}".format(self._BASE_DIR,elist,filename))
                    logging.info("file {}/{} have size {}".format(elist,mfiles[findex-1],sizes[findex-1]))
                else:
                    logging.info("no empty suffix for list {}".format(elist))
            # remove prefix
                findex=sizes_.index(False)
                if findex and (sum(sizes_[:findex])==findex):
                    for ind,filename in enumerate(mfiles[:findex]):
                        logging.info("removing file {}/{} of size {}".format(elist,filename,sizes[ind]))
                        os.remove("{}{}/{}".format(self._BASE_DIR,elist,filename))
                    logging.info("file {}/{} have size {}".format(elist,mfiles[findex],sizes[findex]))
                else:
                    logging.info("no empty prefix for list {}".format(elist))

    def getDownloadedLists(self):
        """Retrieves all list_ids from Gmane"""
        dirs=[i for i in os.listdir(self._BASE_DIR) if os.path.isdir(self._BASE_DIR+i)]
        dirs.sort()
        self.downloaded_lists=dirs
    def downloadListIDS(self,count=-1,load_local=True):
        """Downloads at most count GMANE list_ids"""
        if load_local and os.path.isfile(self._BASE_DIR+"lists.pickle"):
            with open(self._BASE_DIR+"lists.pickle","rb") as f:
                self.list_ids=pickle.load(f)
                logging.info("self.list_ids loaded from pickle")
        else:
            page = requests.get('http://gmane.org/lists.php')
            tree = html.fromstring(page.text)
            list_ids = tree.xpath('//a/text()')
            list_ids=list(set(i for i in list_ids if i.startswith("gmane.")))
            self.list_ids=list(list_ids)
            with open(self._BASE_DIR+"lists.pickle","wb") as f:
                pickle.dump(list_ids,f)
            logging.info("self.list_ids created")
    def downloadedStats(self):
        """Raises elementary info about downloaded lists in _BASE_DIR/stats.txt"""
        try:
            self.downloaded_lists
        except AttributeError:
            self.getDownloadedLists()
        stats={}
        sizes_all=[]
        for elist in self.downloaded_lists:
            stats[elist]={}
            mfiles=os.listdir(self._BASE_DIR+elist)
            mfiles.sort()
            sizes=[os.path.getsize("{}{}/{}".format(self._BASE_DIR,elist,i)) for i in mfiles]
            sizes_all+=sizes
            sizes_=[i==0 for i in sizes]
            stats[elist]["n_messages"]=len(mfiles)
            stats[elist]["total_B"]=sum(sizes)
            stats[elist]["average_B"]=n.mean(sizes)
            stats[elist]["std_B"]=n.std(sizes)
            stats[elist]["n_empty"]=sum(sizes_)
        lists=sorted(stats.items(),key=lambda tlist: tlist[1]["n_messages"],reverse=True)
        stats["all"]={}
        stats["all"]["n_lists"]=len(self.downloaded_lists)
        stats["all"]["n_messages"]=len(sizes_all)
        stats["all"]["total_B"]=sum(sizes_all)
        stats["all"]["average_B"]=n.mean(sizes_all)
        stats["all"]["std_B"]=n.std(sizes_all)
        stats["all"]["n_empty"]=sum([i==0 for i in sizes_all])
        with open(self._BASE_DIR+"stats.txt","w") as f:
            f.write("overall downloaded GMANE database stats:\n")
            f.writelines(["{}: {}\n".format(i[0],i[1]) for i in stats['all'].items()])
            f.write("\nstats per list:\n")
            f.write("\n".join([str(i) for i in lists]))
        logging.info("see file {}".format(self._BASE_DIR+"stats.txt"))
        self.stats=stats
        self.lists=lists
    def downloadListMessages(self,list_id=None,start=1,end=10,threshold=5000,replace=False):
        """Download messages form a GMANE email list"""
        self.current_list=list_id
        if not list_id:
            list_id=self.list_ids[0]
        if not os.path.isdir(self._BASE_DIR+list_id):
            os.mkdir(self._BASE_DIR+list_id)
        for i in range(start,end):
            afile = "{}{}/{}".format(self._BASE_DIR,list_id,"%08d"%i)
            self.current_file=afile
            if replace or not os.path.isfile(afile):
                url="http://download.gmane.org/{}/{}/{}".format(list_id,i,i+1)
                self.current_url=url
                urllib.request.urlretrieve(url, afile, self.reporthook)
                if self._empty_messages_count>=threshold:
                    logging.info("download stopped after {} empty messages".format(threshold))
                    for ii in range(i,i-threshold,-1):
                        afile = "{}{}/{}".format(self._BASE_DIR,list_id,str(ii))
                        os.remove(afile)
                    self._empty_messages_count=0
                    with open(self._BASE_DIR+"finishedLists.txt","a") as f:
                        f.write(list_id+"\n")
                    break
            else:
                logging.info("{} exists".format(afile))
    def reporthook(self,a,b,c): 
        if c:
            self._empty_messages_count=0
        else:
            self._empty_messages_count+=1
        logging.info("{} -> {}, {}\nhook {}, {}, {}".format(
                     self.current_url,self.current_file,self._empty_messages_count,a,b,c))
