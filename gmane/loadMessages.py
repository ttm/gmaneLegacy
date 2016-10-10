from .downloadMessages import DownloadGmaneData
import mailbox, os, percolation as P
c=P.check

class LoadMessages:
    """Class that loads Gmane messages saved locally
    
    Usage
    =====
    After downloading messages from Gmane lists with the 
    DownloadGmaneData class, see chosen basedir,
    or DownloadGmaneData.downloadedLists after
    DownloadGmaneData.getDownloadedLists()
    or basedir/stats.txt after DownloadGmaneData.downloadedStats()
    to select the list_id
    
    Then go
    LoadMessages(list_id,100)
    to load first 100 messages or see the initialization of such class
    if n_messages=-1, class loads all messages (default)

    OBS: any message M on self.messagesB have both M[0] and M[1]
    (and might have more items).
    Only M[0] is on self.messages, which is used for analysis.
    All M[1] were found empty to date, but it is wise to check.
    """
    def __init__(self,list_id=None,n_messages=None,offset=0,basedir="~/.gmane/",loggin_file="load.log"):
        self._BASE_DIR=basedir.replace("~",os.path.expanduser("~"))
        if not os.path.isdir(self._BASE_DIR):
            os.mkdir(self._BASE_DIR)
        if not list_id:
            dl=DownloadGmaneData() # saves into ~/.gmane/
            dl.getDownloadedLists()
            list_id=dl.downloaded_lists[0]
        self.list_id=list_id
        self.n_messages=n_messages
        self.offset=offset
        self.n_empty=0
        self.loadMessages()
    def loadMessages(self):
        mfiles=os.listdir(self._BASE_DIR+self.list_id)
        mfiles.sort()
        messages=[]
        messagesB=[]
        if self.n_messages:
            tend=self.offset+self.n_messages
        else:
            tend=None
        mcount=0
        for mfile in mfiles[self.offset:tend]:
            mcount+=1
            if mcount%300==0: c("load +300: {}".format(mcount))
            mbox = mailbox.mbox(self._BASE_DIR+self.list_id+"/"+mfile)
            if mbox.keys():
                messages.append(mbox[0])
                if len(mbox.keys())>1:
                    messagesB.append(mbox)
            else:
                self.n_empty+=1
        self.messages=messages
        self.messagesB=messagesB
        if not self.n_messages:
            self.n_messages=len(messages)
