#import Libraries
import time
import pyrebase
import cups
from fpdf import FPDF

#Firebase Configuration

config = {
    "apiKey": "AIzaSyBVvy1j5wdfr_RhwFNeVCHZ6K-eb627XvM",
    "authDomain": "thank-you-bot.firebaseapp.com",
    "databaseURL": "https://thank-you-bot.firebaseio.com",
    "projectId": "thank-you-bot",
    "storageBucket": "thank-you-bot.appspot.com",
    "messagingSenderId": "713594089830"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

conn = cups.Connection()
printers = conn.getPrinters()
printer_name = printers.keys()[0]

#While loop to run until user kills program
while(True):
    messages = db.child("messages").order_by_child("status").equal_to("").get()

    for message in messages.each():
        body = message.val().get("original", "")

        #Print thank you message and update status to printed
        print(body)

        db.child("messages").child(message.key()).update({"status": "printed", "original":body})
        
        print("key", message.key())
        print("val", message.val())

        pdf = FPDF('P', 'mm', (55, 100))
        pdf.add_page()
        pdf.ln(10)
        pdf.image('Thank_You.png', 10, 8 , 33)
        pdf.ln(3)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 5, message_text)
        pdf.ln(40)
        print_id = conn.printFile(printer_name, "testpdf.pdf" , "Thank you", {})
        
        #Check again after 15 minutes
        time.sleep(60)   
