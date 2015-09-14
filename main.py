import csv
from win32com.client import Dispatch
import win32con
import time
import datetime

def close_all_windows():
    # Starts anywhere. 
    # Ends with blank screen.
    #print "Calling close_all_windows() at: %s" % time.strftime("%H:%M:%S")
    Auto.WinActivate(apptitle)
    Auto.send("!w")
    Auto.send("a")
    if Auto.WinExists("Recording"):
        time.sleep(2)
        print "'Do you want to record this transaction?' warning message exists."
        Auto.send("n")      
    time.sleep(1)
    for x in range(5):
        if is_color(250,250,grey) == 0:
            Auto.send("{ESC}")
            print "Esc attempt %s" % x
    Auto.Send("{ENTER 2}")
    time.sleep(1)
    if Auto.WinExists("Past Transactions"):
        time.sleep(2)
        print "'Past Transactions' warning message exists."
        Auto.send("n") 
    for x in range(5):
        if is_color(250,250,grey) == 0:
            Auto.send("{ESC}")
            print "Esc attempt %s" % x
    #print "Ended close_all_windows() at: %s" % time.strftime("%H:%M:%S")
    
def open_make_deposits(bank_code): 
    # Starts at blank screen. 
    # Ends with cursor at "Date" textbox.
    #print ("Calling open_make_deposits(bank_code) at: %s" % time.strftime("%H:%M:%S"))
    Auto.send("!b")
    Auto.send("d")
    tile_windows()
    time.sleep(1)
    for letter in bank_code[0:3]:
        Auto.send(letter)
        time.sleep(1)
    if is_color(115,177,blue) == 1: # Can avoid this by typing out bank_code, tabbing, then checking for error message.
        Auto.send("{TAB}") # Now un-highlighted cursor is in "Date" textbox. 
        time.sleep(1)
    elif is_color(135,178,blue) == 1: # Backup highlight checker.
        Auto.send("{TAB}") # Now un-highlighted cursor is in "Date" textbox.
        time.sleep(1)
    else:
        print "Bank_code not recognized. Check is_color() coordinates." 
    # print ("Ended open_make_deposits(bank_code) at: %s" % time.strftime("%H:%M:%S"))

def open_make_credits(bank_code):
    # Starts at blank screen. 
    # Ends with cursor at "Date" textbox.
    print ("Calling open_make_deposits(bank_code) at: %s" % time.strftime("%H:%M:%S"))
    Auto.send("{CTRLDOWN}")
    Auto.send("w")
    Auto.send("{CTRLUP}")
    Auto.send("!k") # Now at "Bank Account" textbox.
    tile_windows()
    time.sleep(1)
    print ("Ended open_make_deposits(bank_code) at: %s" % time.strftime("%H:%M:%S"))


def tile_windows():
    Auto.send("!w")
    Auto.send("h") # Chooses "home" dropdown option. Ends wherever curlor left off. 
     
def is_color(x,y,color):
    PositionColor = Auto.PixelGetColor(x,y)
    if color == PositionColor:
        return 1
    else:
        return 0

def attempt_send_vendor(v,Type): # Starts at
    print ("Calling attempt_send_vendor() at: %s" % time.strftime("%H:%M:%S"))
    print ("Attempting to enter vendor: %s" % v)
    for letter in v[0:3]:
        Auto.send(letter)
        time.sleep(1)
    if is_color(325,452,black) == 1: 
        Auto.send("{TAB}") # Now highlighted cursor is in "From Account" textbox.
        time.sleep(1)
        print "Vendor recognized in drop-down."
        if Type == "debit":
            Auto.send("{TAB }") # Ends with un-highlighted cursor in in "From Account" textbox.
            return 1
        elif Type == "credit":
            pass # Now highlighted cursor is still in Payment textbox.
            return 1
        else:
            print "Type passed though attempt_send_vendor(v,Type) is not recognized."
            return 0
    else:
        print "attempt_send_vendor(v,Type) failed" 
        #Highlight failed. Cursor now at end of Account textbox.
        return 0
    print ("Ended attempt_send_vendor() at: %s" % time.strftime("%H:%M:%S"))

def attempt_send_vendor_deposit(v): # Ends at "Amount" textbox
    #print ("Calling attempt_send_vendor() at: %s" % time.strftime("%H:%M:%S"))
    print ("Attempting to enter vendor: %s" % v)
    for letter in v[0:3]:
        Auto.send(letter)
        time.sleep(1)
    if is_color(170,300,black) == 1:
        Auto.send("{TAB}") # Now hilighted cursor is in "From Account" textbox.
        Auto.send("Income")
        Auto.send("{TAB 4}") # Now un-highlighted cursor is in "Amount" textbox.
        time.sleep(2)
        return 1
    else:
        print "Attempt to send vendor failed." 
        return 0
    #print ("Ended attempt_send_vendor() at: %s" % time.strftime("%H:%M:%S"))
        
def attempt_send_amount(a,Type):       
    Auto.send(a) #Amount
    time.sleep(2)
    if Type == "debit":
        Auto.send("{ENTER}") # Now at "Deposit To" textbox for a new transaction.
        if Auto.WinExists("Past Transactions"):
            Auto.send("y")
            print "Saving transaction >30 days in the past." # Can just delete this message in preferences.          
        print "amount entered for debit in attempt_send_amount(a,Type)"
        print "Sending amount"
        time.sleep(2)
        return 1
    elif Type == "credit":
        Auto.send("{TAB 3}")# End up in Accounts after 3 tabs from Payments
        print "amount entered for credit in attempt_send_amount(a,Type)"
        return 1
    else:
        print "Failure occured : %s" % time.strftime("%H:%M:%S")
        print "Function 'attempt_send_amount' failed."
        print "LMAOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
        print "Entering Type: %s" % Type
        return 0            

def attempt_send_account(Type):
    if Type == "debit":
        account = "income"
        Auto.send(account)
        print "account entered for deposit in attempt_send_account(Type)"
        return 1
        
    elif Type == "credit":
        paste_account()
        print "account entered for deposit in attempt_send_account(Type)"
        return 1
    
    
    else:
        print "Failure occured : %s" % time.strftime("%H:%M:%S")
        print "Function 'attempt_send_account' failed."
        return 0 # Might make individual for Deposit and Credit

def attempt_send_date(d,Type): 
    # Starts  
    # Ends with cursor in "Received From" textbox.
    #print ("Called attempt_send_date(d) at: %s" % time.strftime("%H:%M:%S"))
    time.sleep(1)
    Auto.send(d)
    if Type == "debit":
        Auto.send("{TAB 2}")
    elif Type == "credit":
        Auto.send("{TAB 7}")
        print "Should be at Account"
        time.sleep(2)
    else:
        print "Not credit or debit. Check Type. "
    #print ("Ended attempt_send_date() at: %s" % time.strftime("%H:%M:%S"))
    time.sleep(2)
   
def DepositEntry(d,v,a,Type,transaction): # starts with Date in deposits highlighted
    #print ("Calling DepositEntry() at: %s" % time.strftime("%H:%M:%S"))
    attempt_send_date(d, Type) # Ends with cursor in "Received From (vendor)" textbox.
    if attempt_send_vendor_deposit(v) == 1: # Ends with cursor at "Amount" textbox.
        print "attempt_send_vendor(v) == 1"
        time.sleep(1)
        if attempt_send_amount(a,Type) == 1:
            print "DepositEntry sucess"
            time.sleep(1)
            return 1 
    else:
        print "DepositEntry failure"
        return  0
        time.sleep(1)
    #print ("Ended DepositEntry() at: %s" % time.strftime("%H:%M:%S"))
        
def CreditEntry(d,v,a,Type,transaction):
    #print ("Attempting to credit:  %s to [bank_code]: " % transaction) #######
    #print "CreditEntry pass on name: %s " % v
    attempt_send_date(d,Type) # Ends with cursor in "Pay to the order of (vendor)" textbox. 

def Process(statement):
    Auto.WinActivate(apptitle)
    with open(statement) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        counter = 0
        for transaction in readCSV:
            date = transaction[0]
            vendor = transaction[1]
            amount = transaction[2]
            
            if float(amount) > 0: # Debit.
                Type = "debit"
                close_all_windows()
                open_make_deposits(bank_code) # Ends with cursor at "Date" textbox.
                time.sleep(1)
                DepositEntry(date,vendor,amount,Type,transaction)
                
            elif float(amount) < 0: # Credit.
                close_all_windows()
                Type = "credit"
                #copy_account(vendor)
                open_make_credits(bank_code) # Starts at blank screen. # Ends with cursor at "Date" textbox.
                #CreditEntry(date,vendor,amount,Type,transaction)
                time.sleep(1)
                print ("Credited %s to [eventual location]: " % transaction)

            else:
                Skipped_List.append(transaction)
                #print ("Added %s to Skipped_List: " % transaction) # does print run the function??
                print "Error in in Process(), amount is not > or < 0."
            print "Finished Transaction number: %s" % counter
            counter += 1 
            print "______________________________"
            print ""
                
        print "Processed all transactions at: %s" % current_time
         
            
Auto = Dispatch("AutoItX3.Control")
current_time = time.strftime("%H:%M:%S")
black = 0x000000 
grey = 0xABABAB 
blue = 0x3399FF
Skipped_List = []

#### Settings ####
apptitle = "Yuliya"
statement = "C:\Python27\Scripts\QB\stmtsampleclean.txt"
bank_code = "Bank of America Bus"
#### Settings ####


Process(statement)

