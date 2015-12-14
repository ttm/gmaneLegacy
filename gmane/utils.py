import datetime
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
    try:
        t=msg.get_payload(decode=True)
    except:
        t=msg.get_payload()
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
                t=t.decode(charset,errors="ignore")
            else:
                try:
                    t=t.decode(charset)
                except:
                    try:
                        t=t.decode(charset,errors="ignore")
                    except:
                        if type(t)==type("asid"):
                            return t
                        else:
                            t=t.decode(errors="ignore")

        except LookupError:
            try:
                t=t.decode(charset,errors="ignore")
            except LookupError:
                if type(t)==type("asid"):
                    return t
                else:
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
        line=line.strip()
        if line.startswith(">"):
            pass
        elif line.startswith("<"):
            pass
        elif "style=" in line:
            pass
        elif "]$" in line:
            pass
        elif "=" in line:
            pass
        elif "INFO" in line:
            pass
        elif (sum([(i in line) for i in ("if","while","for","(",")")])>=3):
            pass
        elif ("FLAGS" in line) and ("=" in line):
            pass
        elif line.endswith(");"):
            pass
        elif line.startswith("$ "):
            pass
        elif line.startswith("return "):
            pass
        elif line.startswith("\./"):
            pass
        elif line.startswith("~/"):
            pass
        elif line.startswith("//"):
            pass
        elif line.startswith(" |"):
            pass
        elif line.startswith("| "):
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
        elif sum([line.startswith(i) for i in ("From:","Subject","To","Reply-To:","WARNING")]):
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
import string
#allowed=string.punctuation+string.whitespace
allowed=string.punctuation+" \n\t"
def hardClean(text):
    return "".join(c for c in text if ((c.isalnum()) or (c in allowed)))
import urllib
def urifyID(tid):
#    return tid.strip().replace("@","_-AT-_").replace(">","").replace("<","").replace("[","").replace("]","")
    return urllib.parse.quote(tid.strip().replace("@","_-AT-_").replace(">","").replace("<","").replace("[","").replace("]",""))

class FixedOffset(datetime.tzinfo):
    """Fixed offset in minutes east from UTC."""
    def __init__(self, offset, name):
        self.__offset = datetime.timedelta(minutes=offset)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO
