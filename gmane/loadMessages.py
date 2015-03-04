import mailbox, os

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
    def __init__(self,list_id=None,n_messages=-1,offset=0,basedir="~/.gmane/",loggin_file="load.log"):
        self.list_id=list_id
        self.n_messages=n_messages
        self.offset=offset
        self._BASE_DIR=basedir.replace("~",os.path.expanduser("~"))
        self.loadMessages()
    def loadMessages(self):
        mfiles=os.listdir(self._BASE_DIR+self.list_id)
        messages=[]
        messagesB=[]
        if self.n_messages != -1:
            tend=self.offset+self.n_messages
        else:
            tend=None
        for mfile in mfiles[self.offset:tend]:
            mbox = mailbox.mbox(self._BASE_DIR+self.list_id+"/"+mfile)
            if mbox.keys():
                messages.append(mbox[0])
                if len(mbox.keys())>1:
                    messagesB.append(mbox)
        self.messages=messages
        self.messagesB=messagesB
        if self.n_messages==-1:
            self.n_messages=len(messages)
