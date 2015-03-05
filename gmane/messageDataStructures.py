#from .loadMessages import LoadMessages
import dateutil.parser
import pytz

class MessageDataStructures:
    """Basic datastructures driven from Gmane email messages.

    Usage
    =====
    Initialize with a LoadMessages() instance.
    If not interested in the textual content, use test="no"

    Attributes
    ==========
    After initialization of class, you get:
    self.messages a dict for infos by message_id as key
    self.message_ids a cronologically ordered list of message_id s
    self.empty_ids list of message_id s of empty messages
    self.author_messages  messages by author email as keys
    self.n_messages # number of messages
    self.n_authors # number of authors 
    self.responses for accessing responses to a message by the message_id
    self.raw_clean_autors keep both the original author field and cleaned email address used as author ID
    self.raw_clean_dates keep both the original date field and compatibilized with dateutil.parser

    Precedent implementation variable names
    =======================================
    For compatibility with algorithms that used previous implementations
    it is worth keeping the track of the variable names.
    This is the correspondence:
    mm changed to messages
    ids to message_ids
    vz to empty_ids
    aa to author_messages
    N to n_messages
    ids_r to responses
    """
    def __init__(self, messagesLoaded=None,text="yes"):
        if not messagesLoaded:
            messagesLoaded=LoadMessages()
        self.messagesLoaded=messagesLoaded
        self.messages=messages={}
        self.message_ids=message_ids=[]
        self.empty_ids=empty_ids=[]
        self.author_messages=author_messages={}
        self.n_messages=len(messagesLoaded.messages)
        self.responses=responses={}
        self.raw_clean_authors=raw_clean_authors=[]
        self.raw_clean_dates=raw_clean_dates=[]
        self.raw_clean_references=raw_clean_references=[]
        for message in messagesLoaded.messages:
            if not message.keys(): # if message is empty
                empty_ids.append(i)
            else:
                author_=message['from']
                author=author_.replace('"','')
                author=author.split("<")[-1][:-1]
                if " " in author: 
                    author=author.split(" ")[0]
                raw_clean_authors.append((author_,author))
                if author not in author_messages:
                    author_messages[author]=[]
                date_=message['date']
                date=date_
#                date=date_.replace("METDST","MEST")
#                date=date.replace("MET DST","MEST")
#                #date=date.replace(" CST"," (CST)")
#                date=date.replace("(GMT Standard Time)","")
#                date=date.replace(" CDT"," (CDT)")
#                date=date.replace(" GMT","")
#                date=date.replace("(WET DST)","")
#                date=date.replace(" PST (-0800)","")
#                date=date.replace("-0600 CST","-0600")
#                #print date
#                if "GMT-" in date:
#                    index=date[::-1].index("-")
#                    date=date[:-index-1]+")"
#                if 'added' in date: date = date.split(" (")[0]
                date=dateutil.parser.parse(date)
                if date.tzinfo==None: # colocando localizador em que não tem, para poder comparar
                    date=pytz.UTC.localize(date)
                raw_clean_dates.append((date_,date))
                if message['references']:
                    id_ant=message['references'].split('\t')[-1]
                    id_ant=id_ant.split(' ')[-1]
                else:
                    id_ant=None
                if id_ant:
                    if id_ant not in responses.keys():
                        responses[id_ant]=[]
                    responses[id_ant].append( (author,message["message-id"],date) )
                    raw_clean_references.append((message['references'],id_ant))
                if text=="no":
                    messages[m["message-id"]]=(au,id_ant,date)
                elif text=="yes":
                    t=message.get_payload()
                    #if type(t)==type("astring"):
                    #    pass
                    #else:
                    #    t=t[0].get_payload()
                    #if type(t)==type("astring"):
                    #    pass
                    #else:
                    #    t=t[0].get_payload()
#                    while type(t)!=type("astring"):
#                        t=t[0].get_payload()
                    #print t
#                    t=self.cleanText(t)
                    messages[message["message-id"]]=(author,id_ant,date,t)
                else:
                    raise TypeError("argument text accepts only 'yes' and 'no'values")
                author_messages[author].append( (message["message-id"], id_ant, date)  )
                message_ids.append(message['message-id'])
                self.n_empty=len(empty_ids)
                self.n_authors=len(author_messages)
