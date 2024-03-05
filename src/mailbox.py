# Stub code for mailbox functions
# All functions may also be subject to return error message


# Mailbox ROUTE
# View all received/incoming e-invoices for specified user through userId. Returns senderAddress, timeSent and invoiceSubject
def mailbox(userId):
    

    return


# View received e-invoice through userId and incomingInvoiceId, returns list that contains senderAddress, timeSent, invoiceSubject, 
# invoiceBody, list of eInvoices containing name, content, timeCreated and owner.
def incomingInvoiceId(userId, incomingInvoiceId):

    return list


# Lookup e-invoice in mailbox using lookupString and userId, returns list that contains senderAdress, timeSent and invoiceSubject.
def incomingLookup(userId: str, lookupString: str) -> list or str:

    return list


# Sends e-invoice to desired recepient given userId, recepientAddress, invoiceSubject, 
# invoiceBody and list of eInvoices containing name, content, timeCreated and owner. Returns list for sentReport containing content
# and sentReportId.
def sending(userId: str, recepientAdresses: list, invoiceSubject: str, invoiceBody: str, eInvoices: list) -> list or str:

    return list


# View outgoing sent e-invoices given userId, returns recepientAddres, timeSent and invoiceSubject.
def sent(userId: str) -> list or str:

    return list


# View sent e-invoice through userId and sentInvoiceId, returns list that contains recepientAddress, timeSent, invoiceSubject, 
# invoiceBody, list of eInvoices containing name, content, timeCreated and owner, and sendReport list which contains content and sentReportId.
def sentInvoiceId(userId: str, sentInvoiceId: int) -> list or str:

    return list


# Lookup e-invoice in mailbox using lookupString and userId, returns list that contains recepientAdress, timeSent and invoiceSubject.
def sentLookup(userId: str, lookupString: str) -> list or str:

    return list
  

# View report for sent e-invoice given userId, sentInvoiceId and sentReportId. Returns sentReport list containing content and sentReportId.
def sentReportId(userId: str, sentInvoiceId: int, sentReportId: int) -> list or str:

    return list


# verifies sent e-invoice given userId and sentInvoiceId. Returns deliveryStatusReport list containing content and deliveryStatusReportId.
def verifySent(userId: str, sentInvoiceId: int) -> list or str:

    return list


# Deletes received e-inovice given userId and incomingIncoiveId. Returns nothing.
def deleteIncomingInvoice(userId: str, incomingInvoiceId: int) -> None or str:

    return None


# Deletes sent e-inovice given userId and sentIncoiveId. Returns nothing.
def deleteSentInvoice(userId: str, sentInvoiceId: int) -> None or str:

    return None
