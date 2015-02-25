from lxml import html
import requests, urllib, os, pickle


class LoadGmaneData:
    """Class for loading Gmane data

    Methods
    =======
    downloadLists(count=-1) :: downloads all GMANE lists IDs
    downloadList(list_id,count=10,offset=0) :: downloads
    at most count messages from list with list_id and offset.
    updateList(list_id,count=-1) :: downloads new messages from
    list
    loadList(list_id,count=-1) :: loads list messages saved locally
    saveState() :: saves current state in a binary python file.
    loadState() :: saves current state in a binary python file.
    """
    BASE_DIR=os.path.expanduser("~")+"/.gmane/"
    def __init__(self):
        if not os.path.isdir(self.BASE_DIR):
            os.mkdir(self.BASE_DIR)
        self._empty_messages_count=0
    def downloadListIDS(self,count=-1,load_local=True):
        """Downloads at most count GMANE list_ids"""
        if load_local and os.path.isfile(self.BASE_DIR+"lists.pickle"):
            with open(self.BASE_DIR+"lists.pickle","rb") as f:
                self.list_ids=pickle.load(f)
                print("self.list_ids loaded from pickle")
        else:
            page = requests.get('http://gmane.org/lists.php')
            tree = html.fromstring(page.text)
            list_ids = tree.xpath('//a/text()')
            list_ids=list(set(i for i in list_ids if i.startswith("gmane.")))
            self.list_ids=list(list_ids)
            with open(self.BASE_DIR+"lists.pickle","wb") as f:
                pickle.dump(list_ids,f)
            print("self.list_ids created")
    def downloadListMessages(self,list_id=None,start=0,end=10,threshold=2000,replace=False):
        """Download messages form a GMANE email list"""
        if not list_id:
            list_id=self.list_ids[0]
        if not os.path.isdir(self.BASE_DIR+list_id):
            os.mkdir(self.BASE_DIR+list_id)
        for i in range(start,end):
            afile = "{}{}/{}".format(self.BASE_DIR,list_id,str(i))
            if replace or not os.path.isfile(afile):
                url="http://download.gmane.org/{}/{}/{}".format(list_id,i,i+1)
                print(url, "->", afile)
                urllib.request.urlretrieve(url, afile, self.reporthook)
                if self._empty_messages_count>=threshold:
                    print("download stopped after {} empty messages".format(threshold))
                    for i in range(i,i-threshold,-1):
                        afile = "{}{}/{}".format(self.BASE_DIR,list_id,str(i))
                        os.remove(afile)
                    break
            else:
                print("{} exists".format(afile))
    def reporthook(self,a,b,c): 
    #print("% 3.1f%% of %d bytes\r" % (min(100, float(a * b) / c * 100), c))
        print(a,b,c)
        if c:
            self._empty_messages_count=0
        else:
            self._empty_messages_count+=1
            

