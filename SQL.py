from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import customtkinter as ctk
import mysql.connector as mc

root = ctk.CTk()
root.title('USER LOGIN')
root.geometry("800x600")

def insert(id_num,name_num,age_num,phone_num,pwd_num,blood_num,add_num):
  cnx = mc.connect(host = "127.0.0.1",user = "root",passwd = "root",db = "blood_bank")
  cur = cnx.cursor()
  cur.execute("SELECT * FROM USER_DETAILS WHERE ID = '"+id_num.get()+"';");
  result = cur.fetchall()
  if result == []:
    cur.execute("INSERT INTO USER_DETAILS VALUES ('{}','{}',{},{},'{}','{}','{}');".format(id_num.get(),name_num.get(),age_num.get(),phone_num.get(),pwd_num.get(),blood_num.get(),add_num.get()))
    cnx.commit()
    messagebox.showinfo('SUCCESS', "Successfully created!")
  else:
    messagebox.showinfo('SORRY', "User Id already exists!")

def create():
  root.withdraw()
  new = ctk.CTkToplevel(root)
  new.title('NEW USER')
  new.geometry('800x600')

  bg1 = ctk.CTkImage(dark_image=Image.open("D:\save.jpg"),size = (800,600))
  label1 = ctk.CTkLabel(new,text = '',image=bg1)
  label1.place(x=0,y=0)
  
  id_label = ctk.CTkLabel(new,text = 'ID',bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  id_label.place(relx = 0.15,rely = 0.15,anchor = CENTER)
  name_label = ctk.CTkLabel(new,text = 'NAME',bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  name_label.place(relx = 0.15,rely = 0.25,anchor = CENTER)
  age_label = ctk.CTkLabel(new,text = 'AGE',bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  age_label.place(relx = 0.15,rely = 0.35,anchor = CENTER)
  phone_label = ctk.CTkLabel(new,text = 'PHONE NO',bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  phone_label.place(relx = 0.15,rely = 0.45,anchor = CENTER)
  pwd_label = ctk.CTkLabel(new,text = 'PASSWORD',bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  pwd_label.place(relx = 0.15,rely = 0.55,anchor = CENTER)
  blood_label = ctk.CTkLabel(new,text = 'BLOOD TYPE',bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  blood_label.place(relx = 0.15,rely = 0.65,anchor = CENTER)
  add_label = ctk.CTkLabel(new,text = 'ADDRESS',bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  add_label.place(relx = 0.15,rely = 0.75,anchor = CENTER)

  id_num = ctk.CTkEntry(new,width=150,bg_color = "#d32920",font = ('Comic Sans MS',15,'bold'))
  id_num.place(relx = 0.3,rely = 0.15,anchor = 'w')
  name_num = ctk.CTkEntry(new,width=150,bg_color = "#d32920",font = ('Comic Sans MS',15,'bold'))
  name_num.place(relx = 0.3,rely = 0.25,anchor = 'w')
  age_num = ctk.CTkEntry(new,width=150,bg_color = "#d32920",font = ('Comic Sans MS',15,'bold'))
  age_num.place(relx = 0.3,rely = 0.35,anchor = 'w')
  phone_num = ctk.CTkEntry(new,width=150,bg_color = "#d32920",font = ('Comic Sans MS',15,'bold'))
  phone_num.place(relx = 0.3,rely = 0.45,anchor = 'w')
  pwd_num = ctk.CTkEntry(new,width=150,bg_color = "#d32920",font = ('Comic Sans MS',15,'bold'))
  pwd_num.place(relx = 0.3,rely = 0.55,anchor = 'w')
  blood_num = ctk.CTkEntry(new,width=150,bg_color = "#d32920",font = ('Comic Sans MS',15,'bold'))
  blood_num.place(relx = 0.3,rely = 0.65,anchor = 'w')
  add_num = ctk.CTkEntry(new,width=150,bg_color = "#d32920",font = ('Comic Sans MS',15,'bold'))
  add_num.place(relx = 0.3,rely = 0.75,anchor = 'w')

  insert_btn_1 = ctk.CTkButton(new,text = 'CREATE',bg_color = "#d32920",font = ('Comic Sans MS',18,'bold'),command = lambda:insert(id_num,name_num,age_num,phone_num,pwd_num,blood_num,add_num))
  insert_btn_1.place(relx = 0.25,rely = 0.85,anchor = CENTER)

  id_num.delete(0,END)
  name_num.delete(0,END)
  age_num.delete(0,END)
  phone_num.delete(0,END)
  pwd_num.delete(0,END)
  blood_num.delete(0,END)
  add_num.delete(0,END)
  
def pat1(units_num,res,patt):
  cnx = mc.connect(host = "127.0.0.1",user = "root",passwd = "root",db = "blood_bank")
  cur = cnx.cursor()
  cur.execute("DELETE FROM DONOR WHERE TIMESTAMPDIFF(MONTH, DONATION_DATE, CURRENT_DATE()) > 1;")
  cnx.commit()
  cur.execute("SELECT BLOOD_TYPE,PHONE_NO FROM USER_DETAILS WHERE ID = '"+res+"';")
  res1 = cur.fetchone()
  num = int(units_num.get())
  cur.execute("SELECT SUM(NUMBER_OF_UNITS) FROM USER_DETAILS NATURAL JOIN DONOR WHERE BLOOD_TYPE = '"+res1[0]+"';")
  res2 = cur.fetchone()
  if res2[0] != None:
    resnum = int(res2[0])
    if resnum >= num:
      cur.execute("SELECT ID,NUMBER_OF_UNITS FROM USER_DETAILS NATURAL JOIN DONOR WHERE BLOOD_TYPE = '"+res1[0]+"';")
      res3 = cur.fetchall()
      ind = 0
      tnum = num
      while num > 0:
        if res3[ind][1] <= num:
          num = num-res3[ind][1]
          cur.execute("DELETE FROM DONOR WHERE ID = '"+res3[ind][0]+"';")
          cnx.commit()
          ind = ind + 1
        else:
          temp = res3[ind][1] - num
          num = 0
          cur.execute("UPDATE DONOR SET NUMBER_OF_UNITS = "+str(temp)+" WHERE ID = '"+res3[ind][0]+"';")
          cnx.commit()
          break
      cur.execute("INSERT INTO PATIENT VALUES ('"+res+"',CURRENT_DATE(),"+str(tnum)+",'YES');")
      cnx.commit()
      messagebox.showinfo('SUCCESS',"Blood available! Thanks for choosing us.\nYou can collect blood from our office!")
    else:
      cur.execute("INSERT INTO PATIENT VALUES ('"+res+"',CURRENT_DATE(),"+str(num)+",'NO');")
      cnx.commit()
      messagebox.showinfo('SORRY', "Sorry, We currently don't have the blood.We will contact you in the following phone number as soon as we get the blood!\n"+str(res1[1]),icon = 'info')
  else:
    cur.execute("INSERT INTO PATIENT VALUES ('"+res+"',CURRENT_DATE(),"+str(num)+",'NO');")
    cnx.commit()
    messagebox.showinfo('SORRY', "Sorry, We currently don't have the blood type.We will contact you in the following phone number as soon as we get the blood!\n"+str(res1[1]),icon = 'info')
  units_num.delete(0,END)
  cur.close()
  cnx.close()
  
def pat(res,main):
  main.withdraw()
  patt = ctk.CTkToplevel(main)
  patt.title('REQUEST')
  patt.geometry('800x600')
  
  bg1 = ctk.CTkImage(dark_image=Image.open("save.jpg"),size = (800,600))
  label1 = ctk.CTkLabel(patt,text = '',image=bg1)
  label1.place(x=0,y=0)
  
  id_label = ctk.CTkLabel(patt,text = res[0],bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  id_label.place(relx = 0.3,rely = 0.3,anchor = CENTER)
  name_label = ctk.CTkLabel(patt,text = res[1],bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  name_label.place(relx = 0.3,rely = 0.4,anchor = CENTER)
  type_label = ctk.CTkLabel(patt,text = res[5],bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  type_label.place(relx = 0.3,rely = 0.5,anchor = CENTER)
  units_label = ctk.CTkLabel(patt,text = 'No.of.units required',bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  units_label.place(relx = 0.28,rely = 0.6,anchor = 'e')
  
  units_num = ctk.CTkEntry(patt,width = 150,bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  units_num.place(relx = 0.32,rely = 0.6,anchor = 'w')

  submit = ctk.CTkButton(patt,text = 'SUBMIT',bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'),command = lambda:pat1(units_num,res[0],patt))
  submit.place(relx = 0.3,rely = 0.7,anchor = CENTER)

def donate1(units_num,res,don):
  cnx = mc.connect(host = "127.0.0.1",user = "root",passwd = "root",db = "blood_bank")
  cur = cnx.cursor()
  cur.execute("SELECT * FROM DONOR WHERE ID = '"+res+"';")
  res1 = cur.fetchone()
  cur.execute("SELECT AGE FROM USER_DETAILS WHERE ID = '"+res+"';")
  res2 = cur.fetchone()
  age = int(res2[0])
  num = int(units_num.get())
  units_num.delete(0,END)
  if num <= 3 and age >= 18:
    if res1 == None:
      cur.execute("INSERT INTO DONOR VALUES ('"+res+"',CURRENT_DATE(),"+str(num)+");")
      cnx.commit()
    else:
      cur.execute("UPDATE DONOR SET DONATION_DATE = CURRENT_DATE(),NUMBER_OF_UNITS = "+str(num)+" WHERE ID = '"+res+"';")
      cnx.commit()
    messagebox.showinfo('SUCCESS', 'Successfully updated details!',icon = 'info')
  elif age < 18:
    messagebox.showwarning('INPUT WARNING', 'You cannot donate blood at your age!')
  else:
    messagebox.showwarning('INPUT WARNING', 'You cannot donate more than 3 units of blood!')
  cur.close()
  cnx.close()
  
def donate(res,main):
  main.withdraw()
  don = ctk.CTkToplevel(main)
  don.title('DONATE')
  don.geometry('800x600')

  bg1 = ctk.CTkImage(dark_image=Image.open("save.jpg"),size = (800,600))
  label1 = ctk.CTkLabel(don,text = '',image=bg1)
  label1.place(x=0,y=0)
    
  id_label = ctk.CTkLabel(don,text = res[0],bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  id_label.place(relx = 0.3,rely = 0.3,anchor = CENTER)
  name_label = ctk.CTkLabel(don,text = res[1],bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  name_label.place(relx = 0.3,rely = 0.4,anchor = CENTER)
  type_label = ctk.CTkLabel(don,text = res[5],bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  type_label.place(relx = 0.3,rely = 0.5,anchor = CENTER)
  units_label = ctk.CTkLabel(don,text = 'No.of.units',bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
  units_label.place(relx = 0.26,rely = 0.6,anchor = 'e')
  
  units_num = ctk.CTkEntry(don,width = 150,bg_color = "#d32920",font = ('Comic Sans MS',18,'bold'))
  units_num.place(relx = 0.31,rely = 0.6,anchor = 'w')

  submit = ctk.CTkButton(don,text = 'SUBMIT',bg_color = "#d32920",font = ('Comic Sans MS',15,'bold'),command = lambda:donate1(units_num,res[0],don))
  submit.place(relx = 0.3,rely = 0.7,anchor = CENTER)

def submit():
  cnx = mc.connect(host = "127.0.0.1",user = "root",passwd = "root",db = "blood_bank")
  cur = cnx.cursor()
  cur.execute("SELECT * FROM USER_DETAILS WHERE ID = '"+id_num.get()+"' AND PWD = '"+pwd.get()+"';")
  res = cur.fetchone()
  cur.close()
  cnx.close()
  if res == None:
    messagebox.showerror('LOGIN ERROR', 'User Id or Password Incorrect!')
  else:
    root.withdraw()
    main = ctk.CTkToplevel(root)
    main.title('WELCOME')
    main.geometry('800x600')
    
    bg1 = ctk.CTkImage(dark_image=Image.open("save.jpg"),size = (800,600))
    label1 = ctk.CTkLabel(main,text = '',image=bg1)
    label1.place(x=0,y=0)
    
    id_num_label = ctk.CTkLabel(main,text = 'Welcome '+res[1],bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
    id_num_label.place(relx = 0.25,rely = 0.4,anchor = CENTER)
    donor_btn = ctk.CTkButton(main,text = 'I AM A DONOR',bg_color = "#d32920",font = ('Comic Sans MS',18,'bold'),command = lambda:donate(res,main))
    donor_btn.place(relx = 0.25,rely = 0.5,anchor = CENTER)
    pat_btn = ctk.CTkButton(main,text = 'I AM A PATIENT',bg_color = "#d32920",font = ('Comic Sans MS',18,'bold'),command = lambda:pat(res,main))
    pat_btn.place(relx = 0.25,rely = 0.6,anchor = CENTER)
  id_num.delete(0,END)
  pwd.delete(0,END)

bg = ctk.CTkImage(dark_image=Image.open("D:\save.jpg"),size = (800,600))
label = ctk.CTkLabel(root,text = '',image=bg)
label.place(x=0,y=0)

title = ctk.CTkLabel(root,text = 'BLOOD CARE',bg_color = "#bf1a14",font = ('Comic Sans MS',30,'bold'))
title.place(relx = 0.57,rely = 0.15,anchor='e')

id_num = ctk.CTkEntry(root,width=150,bg_color = "#d32920",font = ('Comic Sans MS',15,'bold'))
id_num.place(relx = 0.3,rely = 0.4,anchor = 'w')
pwd = ctk.CTkEntry(root,width = 150,bg_color = "#d32920",show = '*')
pwd.place(relx = 0.3,rely = 0.5,anchor = 'w')

id_num_label = ctk.CTkLabel(root,text = 'USER ID',bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
id_num_label.place(relx = 0.2,rely = 0.4,anchor = 'e')
pwd_label = ctk.CTkLabel(root,text = 'PASSWORD',bg_color = "#d32920",font = ('Comic Sans MS',20,'bold'))
pwd_label.place(relx = 0.22,rely = 0.5,anchor = 'e')

submit_btn = ctk.CTkButton(root,text = 'SUBMIT',bg_color = "#d32920",font = ('Comic Sans MS',18,'bold'),command = submit)
submit_btn.place(relx = 0.25,rely = 0.65,anchor = CENTER)

insert_btn = ctk.CTkButton(root,text = 'NEW USER',bg_color = "#d32920",font = ('Comic Sans MS',18,'bold'),command = create)
insert_btn.place(relx = 0.25,rely = 0.75,anchor = CENTER)
          
root.mainloop()
