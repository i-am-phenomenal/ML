import sys
import chilkat
import imaplib

def initiateChilkatConnection():
    imap = chilkat.CkImap()
    imap.put_Port(993)
    imap.put_Ssl(True)
    success = imap.Connect("imap.mail.yahoo.com")
    if (success != True):
        print(imap.lastErrorText())
        sys.exit()
    rawResponse = imap.sendRawCommand("ID (\"GUID\" \"1\")")
    if (imap.get_LastMethodSuccess() != True):
        print(imap.lastErrorText())
        sys.exit()
    success = imap.Login("", "")
    if (success != True):
        print(imap.lastErrorText())
        sys.exit()
    print("Login Success!")
    success = imap.SelectMailbox("Inbox")
    if (success != True):
        print(imap.lastErrorText())
        sys.exit()

def getAllMailboxesNames(): 
    mboxes = imap.ListMailboxes("","*")
    if (imap.get_LastMethodSuccess() == False):
        print(imap.lastErrorText())
        sys.exit()
    i = 0
    while i < mboxes.get_Count() :
        print(mboxes.getName(i))
        i = i + 1

def readAllMailsInAMailBox(): 
    fetchUids = True
    messageSet = imap.Search("ALL",fetchUids)
    if (imap.get_LastMethodSuccess() == False):
        print(imap.lastErrorText())
        sys.exit()
    bundle = imap.FetchBundle(messageSet)
    if (imap.get_LastMethodSuccess() == False):
        print(imap.lastErrorText())
        sys.exit()
    i = 0
    numEmails = bundle.get_MessageCount()
    while i < numEmails :
        email = bundle.GetEmail(i)
        print(email.ck_from())
        print(email.subject())
        print("--")
        i = i + 1

def imapConnection(): 
    global IMAP_SERVER
    
    try: 
        status, summary = imap.login("<email>","<pass>")
        return status
    except imaplib.IMAP4.error: 
        print("Error while logging in")
        exit()
    
def getAllMailboxes(): 
    global imap
    status, mailboxes = imap.list()
    if status == "OK": 
        print(mailboxes)
    else: 
        print('Error while fetching mailboxes')

# getAllMailboxesNames()
# readAllMailsInAMailBox()
# Disconnect from the IMAP server.
# success = imap.Disconnect()
IMAP_SERVER = "imap.mail.yahoo.com"
imap = imaplib.IMAP4_SSL(IMAP_SERVER)
status = imapConnection()
if status == "OK": 
    getAllMailboxes()
