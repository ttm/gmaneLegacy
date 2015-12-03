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
