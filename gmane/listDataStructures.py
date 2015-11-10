import dateutil.parser
import parsedatetime as pdt
parser=pdt.Calendar()
import pytz

def getcharsets(msg):
    charsets = set({})
    for c in msg.get_charsets():
        if c is not None:
            charsets.update([c])
    return charsets
def handleerror2(errmsg, t,charset):
    print(errmsg, charset)
    print("This is the body:",t)
def getBody(msg):
    while msg.is_multipart():
        msg=msg.get_payload()[0]
    t=msg.get_payload(decode=True)
    ignore=0
    for charset in getcharsets(msg):
        try:
            if charset=="iso-8859-2:utf-8":
                charset="iso-8859-2"
            elif charset=="us-ascii:utf-8":
                charset="utf-8"
                ignore=1
            elif charset=="unknown-8bit":
                charset="ascii"
                ignore=1
            if ignore:
                t=t.decode(charset,"ignore")
            else:
                try:
                    t=t.decode(charset)
                except:
                    try:
                        t=t.decode(charset,"ignore")
                    except:
                        t=t.decode(errors="ignore")

        except LookupError:
            try:
                t=t.decode(charset,"ignore")
            except LookupError:
                handleerror2("LookupError for unknown charset:",t,charset)
    if not getcharsets(msg):
        try:
            t=t.decode()
        except:
            try:
                t=t.decode("latin-1")
            except:
                t=t.decode(errors="ignore")
    return t
def cleanText(text):
#    return text
    t=text.splitlines()
    t=[line for line in t if line]
    t_=[]
    for line in t:
        if line.startswith(">"):
            pass
        elif line.startswith("On Mon"):
            pass
        elif line.startswith("On Jan"):
            pass
        elif line.startswith("On Tue"):
            pass
        elif line.startswith("On Wed"):
            pass
        elif line.startswith("On Thu"):
            pass
        elif line.startswith("On Fri"):
            pass
        elif line.startswith("On Sat"):
            pass
        elif line.startswith("On Sun"):
            pass
        elif line.endswith("wrote:"):
            pass
        # uma palavra soh sem ponto final
        elif len(line.split()) == 1 and line[-1]!=".":
            pass
        # duas palavras separadas, com a primeira letra caixa alta em cada
        elif line.istitle():
            pass
        elif line.startswith("-----BEGIN"):
            pass
        elif line.startswith("Hash: "):
            pass
        elif line.startswith("--"):
            break
        elif line[:4].count("-")>=3:
            break
        elif "----" in line:
            pass
        else:
            t_.append(line)
    t_="\n".join(t_)
    return t_


class ListDataStructures:
    """Basic datastructures driven from Gmane email messages.

    Usage
    =====
    Initialize with a LoadMessages() instance.
    If not interested in the textual content, use test="no"
    to avoid the overhead.

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
    self.spurious_author should keep only messages with no true sender
    self.raw_clean_dates keep both the original date field and compatibilized with dateutil.parser

    Precedent implementation variable names
    =======================================
    For compatibility with algorithms that used previous implementations
    it is worth keeping the track of the variable names.
    This is the correspondence:
    mm changed to messages
    ids to message_ids
    aa to author_messages
    N to n_messages
    ids_r to responses
    vz to spurious_empty_ids
    """


    def __init__(self, messagesLoaded=None,text="yes"):
        if "messages" in dir(messagesLoaded):
            messagesLoaded=messagesLoaded.messages
        self.messagesLoaded=messagesLoaded
        self.messages=messages={}
        self.message_ids=message_ids=[]
        self.author_messages=author_messages={}
        self.n_messages=len(messagesLoaded)
        self.responses=responses={}
        self.raw_clean_authors=raw_clean_authors=[]
        self.raw_clean_dates=raw_clean_dates=[]
        self.raw_clean_references=raw_clean_references=[]
        #self.spurious_empty_ids=spurious_empty_ids=[]
        self.spurious_authors=spurious_authors=[]
        self.n_empty=n_empty=0#messagesLoaded.n_empty
        self.bad_text_message_ids=[]
        for message in messagesLoaded:
            if not message.keys(): # if message is empty
                #spurious_empty_ids.append(i)
                self.n_empty+=1
            else:
                author_=message['from']
                if "replace" not in dir(author_):
                    spurious_authors.append(message)
                    continue

                author=author_.replace('"','')
                author=author.split("<")[-1][:-1]
                if " " in author: 
                    author=author.split(" ")[0]
                raw_clean_authors.append((author_,author))
                if author not in author_messages:
                    author_messages[author]=[]
                date_=message['date']
                try:
                    date = date_.split(" (")[0]
                except:
                    continue
                if date.split(" ")[-1].islower():
                    date=date.replace(date.split(" ")[-1],date.split(" ")[-1].upper())
                if date.split(" ")[-1].isupper() and date.split(" ")[-1].isalpha():
                    date=date.replace(date.split(" ")[-1],"")
                #date=date.replace("GMT","")
                #date=date.replace(" CST","")
                #date=date.replace(" CDT","")
                date=date.replace("Thur","Thu")
                if "-" in date and len(date.split("-")[1])==3:
                    date=date+"0"
                date=date.replace("--","-")
                date=dateutil.parser.parse(date)
                if date.tzinfo==None: # colocando localizador em que não tem, para poder comparar
                    date=pytz.UTC.localize(date)
                raw_clean_dates.append((date_,date))
                if message['references']:
                    try:
                        id_ant=message['references'].split('\t')[-1]
                        id_ant=id_ant.split(' ')[-1]
                    except:
                        print("AQUI AQUI")
                        continue
                else:
                    id_ant=None
                if id_ant:
                    if id_ant not in responses.keys():
                        responses[id_ant]=[]
                    responses[id_ant].append( (author,message["message-id"],date) )
                    raw_clean_references.append((message['references'],id_ant))
                if text=="no":
                    messages[message["message-id"]]=(author,id_ant,date)
                elif text=="yes":
                    try:
                        t=getBody(message)
                        t=cleanText(t)
                        messages[message["message-id"]]=(author,id_ant,date,t)
                    except:
                        messages[message["message-id"]]=(author,id_ant,date,"")
                        self.bad_text_message_ids.append(message["message-id"])
                else:
                    raise TypeError("argument text accepts only 'yes' and 'no'values")
                author_messages[author].append( (message["message-id"], id_ant, date)  )
                message_ids.append(message['message-id'])
                #self.n_empty=len(spurious_empty_ids)
                self.n_authors=len(author_messages)
