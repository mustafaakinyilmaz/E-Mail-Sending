import os
import smtplib
import tkinter
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

master = tkinter.Tk()
master.configure(background = "LightCyan4")

Label_your_mail = tkinter.Label(master, text="Your mail address:")
Label_your_mail.place(relx= 0.05, rely= 0.06)
Entry_your_mail = tkinter.Entry(master, bd=5)
Entry_your_mail.place(relx= 0.25, rely= 0.05, width= 200)

Label_password = tkinter.Label(master, text="Password:")
Label_password.place(relx= 0.05, rely= 0.13)
password = tkinter.StringVar()
Entry_password = tkinter.Entry(master, bd=5, textvariable= password, show='*')
Entry_password.place(relx= 0.25, rely=0.13, width= 200)

Label_send_mail = tkinter.Label(master, text="Address to send:")
Label_send_mail.place(relx= 0.05, rely= 0.20)
Entry_send_mail = tkinter.Entry(master, bd=5)
Entry_send_mail.place(relx= 0.25, rely= 0.20, width= 200)

Label_subject = tkinter.Label(master, text="Subject:")
Label_subject.place(relx= 0.05, rely= 0.35)
Entry_subject = tkinter.Entry(master,bd=5)
Entry_subject.place(relx= 0.25, rely= 0.35, width= 200)


text = tkinter.Text(master, height= 10, width= 70)
scroll_bar = tkinter.Scrollbar(master, command= text.yview)
text.place(relx= 0.05,rely= 0.45)
scroll_bar.place(relx = 0.025, rely= 0.45)
scroll_bar.config(command= text.yview)
text.config(yscrollcommand=scroll_bar.set)


Entry_attachment = tkinter.Entry(master, bd=5)
Entry_attachment.place(relx= 0.25, rely= 0.80, width= 300)


def sendMail():
    send_from = Entry_your_mail.get()
    send_to = Entry_send_mail.get()
    password = Entry_password.get()
    subject = Entry_subject.get()
    mail_body = text.get(1.0, tkinter.END)[:-1]

    message = MIMEMultipart()
    message['From'] = send_from
    message['To'] = send_to
    message['Subject'] = subject

    message.attach(MIMEText(mail_body,'plain'))
    filename = Entry_attachment.get()

    try:
        attachment = open(filename,'rb')
        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(filename))
        message.attach(part)
        messagebox.showinfo("Attachment","File attached successfully.")
    except:
        messagebox.showinfo("Attachment", "File NOT attached successfully.")
        pass

    message_text = message.as_string()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(user=send_from, password=password)
        server.sendmail(send_from, send_to, message_text)
        server.close()
        messagebox.showinfo("Mail", "Mail Sent!")
    except:
        messagebox.showinfo("Mail", "Not Sent!")
        pass




def clear_mail_body():
    text.delete(1.0,tkinter.END)

def browse_attachment():
    filename = askopenfilename(initialdir= '/')
    Entry_attachment.delete(0, tkinter.END)
    Entry_attachment.insert(0, filename)



clearButton = tkinter.Button(master, text= "Clear Text", command= lambda:[clear_mail_body()])
clearButton.place(relx= 0.05, rely= 0.90)

sendButton = tkinter.Button(master,text = "Send Mail",command= lambda:[sendMail()])
sendButton.place(relx= 0.25, rely= 0.90)

browseButton = tkinter.Button(master, text="Browse Attachment", command= lambda: [browse_attachment()])
browseButton.place(relx= 0.05, rely = 0.80)

master.title("Send E-Mail")
master.geometry('650x550')
master.mainloop()