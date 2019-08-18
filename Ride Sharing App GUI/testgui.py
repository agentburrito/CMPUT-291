'''Due to time constraints and superstition, we did not change the name of the source code to something more pleasant
however this software should be considered our final submission for mini project 1
Under no circumstance should this software be distributed or copied without the authors permission
Developed by: Max Melendez and Leshan Masikonte'''




import tkinter as tk

from tkinter import messagebox as tm

import sys

import sqlite3

import datetime
db=sys.argv[1]
print(db)
conn=sqlite3.connect(str(db))
conn.row_factory=sqlite3.Row
c=conn.cursor()
user=''
rid=1
rno=1
bno=1


class Database(tk.Tk,):
    def __init__(self,master=None):
        tk.Tk.__init__(self,master)
        self._frame = None
        self.switch_frame(main_menu)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=640,y=360,anchor="center")



class main_menu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        global user
        user=''
        self.label_greeting = tk.Label(self, text="Welcome,agent")
        self.label_useremail = tk.Label(self, text="User Email")
        self.label_password = tk.Label(self, text="Password")

        self.entry_useremail = tk.Entry(self)
        self.entry_password = tk.Entry(self, show=" ")

        self.label_greeting.grid(row=0, sticky=tk.E)
        self.label_useremail.grid(row=1, sticky=tk.E)
        self.label_password.grid(row=2, sticky=tk.E)
        self.entry_useremail.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)

        self.logbtn = tk.Button(self, text="Login", command=self._login_btn_clicked).grid(columnspan=2)
        self.newacc=tk.Button(self,text="New Agent? Create Account",command=lambda: master.switch_frame(create_account)).grid(columnspan=6)

    def _login_btn_clicked(self):
        # print("Clicked")
        global user
        useremail = self.entry_useremail.get()
        password = self.entry_password.get()
        # print(username, password)

        with conn:
            true_member=('''SELECT * FROM members WHERE email= ? AND pwd= ?''')
            c.execute(true_member,[(useremail),(password)])
            qresults=c.fetchall()
            if qresults:
                for i in qresults:
                    user+=i[0]
                    self.master.switch_frame(LoginScreen)
            


class create_account(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tm.showinfo("Attention","Registration will be successful when another pop up window appears")
        self.useremail=tk.StringVar(self)
        self.username=tk.StringVar(self)
        self.phone=tk.StringVar(self)
        self.password=tk.StringVar(self)
        tk.Label(self, text="Enter New Email:").grid(row=0, sticky=tk.E)
        self.useremail = tk.Entry(self)
        self.useremail.grid(row=0,column=1)
        tk.Label(self, text="Enter New Password:").grid(row=1, sticky=tk.E)
        self.password = tk.Entry(self, show="*")
        self.password.grid(row=1,column=1)
        tk.Label(self, text="Enter New Name:").grid(row=2, sticky=tk.E)
        self.username = tk.Entry(self)
        self.username.grid(row=2,column=1)
        tk.Label(self, text="Enter New Phone Number: (ddd-ddd-dddd)").grid(row=3, sticky=tk.E)
        self.phone = tk.Entry(self)
        self.phone.grid(row=3,column=1)
        tk.Button(self,text="Register",command=self.register).grid(columnspan=2)
        tk.Button(self,text="Already have an account? Log in!",command=lambda: master.switch_frame(main_menu)).grid(columnspan=6)
    def register(self):
        email=self.useremail.get()
        pwd=self.password.get()
        name=self.username.get()
        phone=self.phone.get()
        print(email,phone,name,pwd)
        print(type(email),type(phone),type(name),type(pwd))
        register=('''INSERT into members(email,name,phone,pwd) VALUES(?,?,?,?)''')
        with conn:
            c.execute(register,[(email),(name),(phone),(pwd)])
            tm.showinfo("SUCCESS","Registration Successful, please return to log in screen")



class LoginScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        global user
        var = tk.StringVar(self)
        var.set('Select Option')
        Lb = tk.Listbox(self, height = 8, width = 100,font=("arial", 12)) 
        Lb.grid(row=0,sticky=tk.E)
        Lb.insert(0, 'Welcome, agent ---REDACTED---')
        Lb.insert(1, 'email                 |msgTimeStamp                   |sender             |content            |rno            |seen')
        scroll = tk.Scrollbar(self, orient = tk.VERTICAL) # set scrollbar to list box for when entries exceed size of list box
        scroll.config(command = Lb.yview)
        scroll.grid(row=0,column=2,rowspan=4)
        Lb.config(yscrollcommand = scroll.set) 
        options = {'Search for Rides', 'Offer a Ride', 'Edit Bookings','Request Ride','Search Ride Requests'}
        opt = tk.OptionMenu(self, var, *options) #For 1st drop down list 
        opt.grid(row=2,sticky=tk.W)
        def option():
            if var.get() == "Search for Rides":
                master.switch_frame(search_for_rides)
            elif var.get() == "Request Ride":
                master.switch_frame(request_ride)
            elif var.get() == "Search Ride Requests":
                master.switch_frame(search_request)
            elif var.get() == "Offer a Ride":
                master.switch_frame(offer_ride)
            elif var.get() == "Edit Bookings":
                master.switch_frame(edit_bookings)
        tk.Button(self, text="Confirm Option",
                  command=option).grid(columnspan=2)
        tk.Button(self, text="Log Out",
                  command=lambda: master.switch_frame(main_menu)).grid(columnspan=6)
        with conn:
            inbox=("SELECT * FROM 'inbox' WHERE email= ? ")
            updateinbox=("UPDATE inbox SET seen='y' WHERE email= ?")
            c.execute(updateinbox,[(user)])
            c.execute(inbox,[(user)])
            inboxresults=c.fetchall()
        for row in inboxresults:
            line=''
            for i in row:
                line+=str(i)+' | '
            Lb.insert(2,line)
            line=''



class offer_ride(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        global user
        global rno
        self.s=0
        self.e=5
        self.l=0
        self.qresults=''
        self.year=tk.IntVar(self)
        self.day=tk.IntVar(self)
        self.month=tk.IntVar(self)
        self.hour=tk.IntVar(self)
        self.minute=tk.IntVar(self)
        self.second=0
        self.pickup=tk.StringVar(self)
        self.dropoff=tk.StringVar(self)
        self.cost=tk.IntVar(self)
        self.numseats=tk.IntVar(self)
        self.luggage=tk.StringVar(self)
        self.enroute=tk.StringVar(self)
        self.cno=tk.IntVar(self)
        self.location=tk.StringVar(self)
        tk.Label(self, text="Enter Year (YYYY):").grid(row=0,column=0)
        self.year = tk.Entry(self)
        self.year.grid(row=0,column=1)
        tk.Label(self, text="Enter Month (M)").grid(row=1,column=0)
        self.month = tk.Entry(self)
        self.month.grid(row=1,column=1)
        tk.Label(self, text="Enter Day (DD)").grid(row=2,column=0)
        self.day = tk.Entry(self)
        self.day.grid(row=2,column=1)
        tk.Label(self, text="Enter Hour (24 HR)").grid(row=3,column=0)
        self.hour = tk.Entry(self)
        self.hour.grid(row=3,column=1)
        tk.Label(self, text="Enter Minute (M)").grid(row=4,column=0)
        self.minute = tk.Entry(self)
        self.minute.grid(row=4,column=1)
        tk.Label(self, text="Enter Pick Up location (lcode):").grid(row=5,column=0)
        self.pickup = tk.Entry(self)
        self.pickup.grid(row=5,column=1)
        tk.Label(self, text="Enter Drop Off location (lcode):").grid(row=6,column=0)
        self.dropoff = tk.Entry(self)
        self.dropoff.grid(row=6,column=1)
        tk.Label(self, text="Enter price per seat (int):").grid(row=7,column=0)
        self.cost = tk.Entry(self)
        self.cost.grid(row=7,column=1)
        tk.Label(self, text="Enter luggage description: ").grid(row=8,column=0)
        self.luggage = tk.Entry(self)
        self.luggage.grid(row=8,column=1)
        tk.Label(self, text="Enter Number of seats offered: (int)").grid(row=9,column=0)
        self.numseats = tk.Entry(self)
        self.numseats.grid(row=9,column=1)
        tk.Label(self, text="Enter enroute destinations separated by a comma: (lcode,lcode,..)").grid(row=10,column=0)
        self.enroute = tk.Entry(self)
        self.enroute.grid(row=10,column=1)
        tk.Label(self, text="Enter car number (cno)").grid(row=11,column=0)
        self.cno = tk.Entry(self)
        self.cno.grid(row=11,column=1)
        tk.Label(self, text="Enter location to search ").grid(row=12,column=0)
        self.location = tk.Entry(self)
        self.location.grid(row=12,column=1)
        self.Lb = tk.Listbox(self, height = 8, width = 60,font=("arial", 12)) 
        self.Lb.grid(row=13,columnspan=1)
        scroll = tk.Scrollbar(self, orient = tk.HORIZONTAL) # set scrollbar to list box for when entries exceed size of list box
        scroll.config(command = self.Lb.xview)
        scroll.place(x=550,y=300)
        self.Lb.config(yscrollcommand = scroll.set)
        tk.Button(self,text="Go Back",command=lambda:master.switch_frame(LoginScreen)).grid(columnspan=2)
        tk.Button(self,text="submit",command=self.submit).grid(columnspan=2)
        tk.Button(self,text="show more",command=self.show_more).grid(columnspan=2)
        tk.Button(self,text="search",command=self.search).grid(columnspan=2)
        query=("SELECT * from rides")
        rno=1
        with conn:
            c.execute(query)
            qresults=c.fetchall()
            for row in qresults:
                if int(row[0])==rno:
                    rno+=1
                else:
                    break

    def submit(self):
        global user
        global rno
        check=0
        year=int(self.year.get())
        day=int(self.day.get())
        month=int(self.month.get())
        hour=int(self.hour.get())
        minute=int(self.minute.get())
        second=0
        pickup=self.pickup.get()
        dropoff=self.dropoff.get()
        cost=str(self.cost.get())
        email=user
        numseats=str(self.numseats.get())
        luggage=self.luggage.get()
        enroute=self.enroute.get()
        cno=str(self.cno.get())
        rno1=str(rno)
        if enroute:
            query2=('''INSERT into enroute (rno,lcode) VALUES (?,?)''')
            enroute=enroute.split(",")
            for i in enroute:
                with conn:
                    c.execute(query2,[(rno1),(str(i))])
        rdate=str(datetime.datetime(year,month, day, hour, minute, second))
        count=0
        query1=('''INSERT into rides(rno,price,rdate,seats,lugDesc,src,dst,driver,cno) VALUES (?,?,?,?,?,?,?,?,?)''')
        if cno:
            cno=cno
            check=self.check()
            if check==1:
                if rdate and pickup and dropoff and cost and luggage and numseats:
                    with conn:
                        c.execute(query1,[(rno1),(cost),(rdate),(numseats),(luggage),(pickup),(dropoff),(email),(cno)])
                        tm.showinfo("SUCCESS","Ride Submitted")
                        rno+=1
        elif not cno:
            cno="NULL"
            if rdate and pickup and dropoff and cost and luggage and numseats:
                with conn:
                    c.execute(query1,[(rno1),(cost),(rdate),(numseats),(luggage),(pickup),(dropoff),(email),(cno)])
                    tm.showinfo("SUCCESS","Ride Submitted")
        else:
            tm.showerror("ERROR", "Invalid car number or format")
        query=("SELECT * from rides")
        rno=1
        with conn:
            c.execute(query)
            qresults=c.fetchall()
            for row in qresults:
                if int(row[0])==rno:
                    rno+=1
                else:
                    break
    
    def check(self):
        cno=self.cno.get()
        global user
        check=0
        query=('''SELECT * FROM cars WHERE owner like ?''')
        c.execute(query,[(user)])
        qresults=c.fetchall()
        for row in qresults:
            if row[0]==int(cno):
                check=1
                return check
        if check==0:
            return check 

    def show_more(self):
        self.s+=5
        self.e+=5
        self.l+=5
        for i in range(self.s,self.e):
            line=''
            for j in range(0,4):
                line+=str(self.qresults[i][j])+' | '
            self.Lb.insert(self.l,line)
            line=''
    
    def search(self):
        self.s=0
        self.e=5
        self.l=0
        self.Lb.delete(0, tk.END)
        query=('''SELECT * FROM locations WHERE lcode like ? OR city like ? OR prov like ? OR address like ?''')
        location=self.location.get()
        with conn:
            c.execute(query,[(location),(location),(location),(location)])
            self.qresults=c.fetchall()
            for i in range(self.s,self.e):
                line=''
                for j in range(0,4):
                    line+=str(self.qresults[i][j])+' | '
                self.Lb.insert(2,line)
                line=''



class search_for_rides(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        global user
        self.location1=tk.StringVar(self)
        self.location2=tk.StringVar(self)
        self.location3=tk.StringVar(self)
        self.var1 = tk.StringVar(self)
        self.var1.set('Select Format')
        self.var2 = tk.StringVar(self)
        self.var2.set('Select Format')
        self.var3 = tk.StringVar(self)
        self.var3.set('Select Format')
        self.Lb = tk.Listbox(self, height = 8, width = 60,font=("arial", 12)) 
        self.Lb.grid(row=0,columnspan=1)
        scroll = tk.Scrollbar(self, orient = tk.HORIZONTAL) # set scrollbar to list box for when entries exceed size of list box
        scroll.config(command = self.Lb.xview)
        scroll.place(x=550,y=0)
        self.Lb.config(yscrollcommand = scroll.set)
        options = {'address', 'city', 'lcode','province'}
        tk.Label(self, text="Enter 'Location 1' (location) and choose its format (address,city,province,lcode):").grid(row=2,column=0)
        self.location1 = tk.Entry(self)
        self.location1.grid(row=2,column=1)
        tk.Label(self, text="Enter 'Location 2' (location) and choose its format (address,city,province,lcode):").grid(row=3,column=0)
        self.location2 = tk.Entry(self)
        self.location2.grid(row=3,column=1)
        tk.Label(self,text="Enter 'Location 3' (location) and choose its format (address,city,province,lcode):").grid(row=4,column=0)
        self.location3= tk.Entry(self)
        self.location3.grid(row=4,column=1)
        tk.Button(self,text="Go Back",command=lambda:master.switch_frame(LoginScreen)).grid(columnspan=2)
        opt1 = tk.OptionMenu(self, self.var1, *options) #For 1st drop down list 
        opt1.grid(row=2,column=2,sticky=tk.E)
        opt2 = tk.OptionMenu(self, self.var2, *options) #For 1st drop down list 
        opt2.grid(row=3,column=2,sticky=tk.E)
        opt3 = tk.OptionMenu(self, self.var3, *options) #For 1st drop down list 
        opt3.grid(row=4,column=2,sticky=tk.E)
        tk.Button(self, text="Search",
                  command=self.search).grid(columnspan=2)
        
    def search(self):
        self.Lb.delete(0, tk.END)
        location1=self.location1.get()
        location2=self.location2.get()
        location3=self.location3.get()
        var1=self.var1
        var2=self.var2
        var3=self.var3
        if location1:
            location1="'"+location1+"'"
        if location2:
            location2="'"+location2+"'"
        if location3:
            location3="'"+location3+"'"
        location=("SELECT * FROM rides R left outer join cars C using(cno) left outer join enroute E using(rno),locations L WHERE r.src=L.lcode ")
        if var1.get()=='city' and location1!='':
            location1='AND L.city like '+location1
        elif var1.get()=='address'and location1!='':
            location1='AND L.address like '+location1
        elif var1.get()=='lcode'and location1!='':
            location1='AND L.lcode like '+location1+' OR E.lcode like'+location1
        elif var1.get()=='province'and location1!='':
            location1='AND L.prov like '+location1
        
        if var2.get()=='city' and location2!='':
            location2='AND L.city like '+location2
        elif var2.get()=='address'and location2!='':
            location2='AND L.address like '+location2
        elif var2.get()=='lcode'and location2!='':
            location2='AND L.lcode like '+location2+' OR E.lcode like'+location2
        elif var2.get()=='province'and location2!='':
            location2='AND L.prov like '+location2
        
        if var3.get()=='city' and location3!='':
            location3='AND L.city like '+location3
        elif var3.get()=='address'and location3!='':
            location3='AND L.address like '+location3
        elif var3.get()=='lcode'and location3!='':
            location3='AND L.lcode like '+location3+' OR E.lcode like'+location3
        elif var3.get()=='province'and location3!='':
            location3='AND L.prov like '+location3
        self.s=0
        self.e=5
        self.l=0
        def execute(location1,location2,location3):
            query=location+location1+' '+location2+' '+location3 
            print(query)
            c.execute(query)
            qresults=c.fetchall()
            return qresults
        self.qresults=execute(location1,location2,location3)
        self.check=1
        for i in range(self.s,self.e):
            line=''
            for j in range(0,14):
                line+=str(self.qresults[i][j])+' | '
            self.Lb.insert(2,line)
            line=''
        self.recipient= tk.StringVar(self)
        self.message=tk.StringVar(self)
        self.rno=tk.StringVar(self)
        tk.Label(self, text="Enter email of user you would like to request a ride from (email)").grid(row=7,column=0, sticky=tk.E)
        self.recipient=tk.Entry(self)
        self.recipient.grid(row=7,column=1)
        tk.Label(self, text="Enter your message (message)").grid(row=8,column=0, sticky=tk.E)
        self.message=tk.Entry(self)
        self.message.grid(row=8,column=1)
        tk.Label(self, text="Enter ride number (rno)").grid(row=9,column=0, sticky=tk.E)
        self.rno=tk.Entry(self)
        self.rno.grid(row=9,column=1)
        tk.Button(self, text="Show More",
                command=self.show_more).grid(row=1,column=0)
        tk.Button(self, text="Message Owner",
                command=self.send_email).grid(row=10,column=1)
    def show_more(self):
        self.s+=6
        self.e+=5
        self.l+=5
        for i in range(self.s,self.e):
            line=''
            for j in range(0,14):
                line+=str(self.qresults[i][j])+' | '
            self.Lb.insert(self.l,line)
            line=''
    
    def send_email(self):
        global user
        recipient=self.recipient.get()
        timestamp=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        sender=user
        message=self.message.get()
        rno=self.rno.get()
        seen="n"
        print("hello")
        print(rno)
        query=('''INSERT into inbox(email,msgTimestamp,sender,content,rno,seen) VALUES (?,?,?,?,?,?)''')
        if recipient and message and rno and user:
            with conn:
                c.execute(query,[(recipient),(timestamp),(sender),(message),(rno),(seen)])
                tm.showinfo("SUCCESS","Message Sent")
        else:
            tm.showerror("WRONG FORMAT", "Please Enter Correct Format")



class edit_bookings(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        global user
        global bno
        self.s=0
        self.e=5
        self.rno1=''
        self.check=0
        self.check2=0
        self.recipient=''
        self.message=''
        self.availableseats=0
        self.bno1=tk.StringVar(self)
        self.member=tk.StringVar(self)
        self.numseats=tk.StringVar(self)
        self.cost=tk.StringVar(self)
        self.pickup=tk.StringVar(self)
        self.dropoff=tk.StringVar(self)
        self.rno=tk.StringVar(self)
        self.Lb = tk.Listbox(self, height = 8, width = 60,font=("arial", 12)) 
        self.Lb.grid(row=0,columnspan=1)
        scroll = tk.Scrollbar(self, orient = tk.HORIZONTAL) # set scrollbar to list box for when entries exceed size of list box
        scroll.config(command = self.Lb.xview)
        scroll.place(x=550,y=0)
        self.Lb.config(yscrollcommand = scroll.set)
        tk.Label(self, text="Enter booking number of booking you wish to delete").grid(row=1,column=0)
        self.bno1 = tk.Entry(self)
        self.bno1.grid(row=1,column=1)
        tk.Label(self, text="Enter email of member you wish to book:").grid(row=2,column=0)
        self.member = tk.Entry(self)
        self.member.grid(row=2,column=1)
        tk.Label(self, text="Enter number of seats you wish to wish to book").grid(row=3,column=0)
        self.numseats = tk.Entry(self)
        self.numseats.grid(row=3,column=1)
        tk.Label(self, text="Enter cost per seat: ").grid(row=4,column=0)
        self.cost = tk.Entry(self)
        self.cost.grid(row=4,column=1)
        tk.Label(self, text="Enter pickup location code (lcode) ").grid(row=5,column=0)
        self.pickup = tk.Entry(self)
        self.pickup.grid(row=5,column=1)
        tk.Label(self, text="Enter dropoff location code (lcode) ").grid(row=6,column=0)
        self.dropoff = tk.Entry(self)
        self.dropoff.grid(row=6,column=1)
        tk.Label(self, text="Enter ride number to book a member on: (rno) ").grid(row=7,column=0)
        self.rno = tk.Entry(self)
        self.rno.grid(row=7,column=1)
        tk.Button(self,text="Go Back",command=lambda:master.switch_frame(LoginScreen)).grid(columnspan=2)
        tk.Button(self, text="Delete booking",
                  command=self.delete).grid(columnspan=2)
        tk.Button(self, text="Show More",
                  command=self.show_more).grid(columnspan=2)
        tk.Button(self, text="Submit",
                  command=self.submit).grid(columnspan=2)
        self.Lb.insert(0,"Your Bookings:")
        greeting="|bno|  |email|   |rno|     |cost|   |seats|   |pickup|   |dropoff|"
        self.Lb.insert(1,greeting)
        query3=('''SELECT R.rno,R.price,R.rdate,R.seats,R.lugDesc,R.src,R.dst,R.driver,R.cno,C.seats FROM rides R, cars C  WHERE C.owner like ? AND R.cno=C.cno''')
        query2=('''SELECT * FROM bookings''')
        query=('''SELECT B.bno,B.email,B.rno,B.cost,B.seats,B.pickup,B.dropoff FROM bookings B,rides R WHERE R.driver like ? AND B.rno=R.rno''')
        self.index=0
        self.index2=1
        self.list=[]
        self.ridelist=[]
        bno=1
        qresults=''
        self.qresults2=''
        self.qresults3=''
        self.qresults=''
        with conn:
            c.execute(query,[(user)])
            self.qresults=c.fetchall()
            for row in self.qresults:
                line=''
                self.index+=1
                self.list.append(row[0])
                for i in row:
                    line+=str(i)+' | '
                self.Lb.insert(2,line)
                line=''
        self.list.reverse()
        with conn:
            c.execute(query2)
            self.qresults2=c.fetchall()
            for row in self.qresults2:
                if int(row[0])==bno:
                    bno+=1
                else:
                    break
        self.l=self.index+7
        with conn:
            c.execute(query3,[(user)])
            self.qresults3=c.fetchall()
            greeting2="|rno|  |price|    |rdate|                |seats|   |lugDesc|      |src|   |dst|  |driver|    |cno|  |available seats|"
            self.Lb.insert(self.index+2,"Rides :")
            self.Lb.insert(self.index+3,greeting2)
            if self.qresults3:
                for i in range(self.s,self.e):
                    line=''
                    for j in range(0,9):
                        line+=str(self.qresults3[i][j])+' | '
                    self.availableseats=int(self.qresults3[i][9])-int(self.qresults3[i][3])
                    line+=str(self.availableseats)+' |'
                    self.Lb.insert(self.l,line)
                    self.availableseats=0
                    line=''
                for row in self.qresults3:
                    self.ridelist.append(row[0])
                    self.index2+=1
            else:
                tm.showerror("ATTENTION","You have no rides")
                master.switch_frame(LoginScreen)
    
    def delete(self):
        global user
        count=0
        member=''
        check=0
        query=('''DELETE FROM bookings WHERE bno=? AND email like ?''')
        for i in self.list:
            for j in self.qresults:
                if i==int(self.bno1.get()) and i==j[0]:
                    check=1
                    member=str(j[1])
                    self.rno1=str(j[2])
                    with conn:
                        c.execute(query,[(self.bno1.get()),(str(j[1]))])
                        tm.showinfo("SUCCESS","Request Deleted")
                        break
        if check==0:
            tm.showerror("ERROR", "Please Enter Correct Booking")
        for i in self.list :
            if i==int(self.bno1.get()):
                self.Lb.delete(count+2)
                self.list.remove(int(self.bno1.get()))
            else:
                count+=1
        if check==1:
            self.recipient=member
            self.message="Your booking was cancelled"
            self.send_email()
            self.recipient=''
            self.message=''
            self.rno1=''     
    
    def submit(self):
        global bno
        rno=self.rno.get()
        member=self.member.get()
        numseats=self.numseats.get()
        cost=self.cost.get()
        pickup=self.pickup.get()
        dropoff=self.dropoff.get()
        self.check=0
        self.check2=0
        for item in self.ridelist:
            if int(rno)==item:
                self.check2=1
        if not rno or not member or not numseats or self.check2==0:
            tm.showerror("WRONG FORMAT", "Please Enter Correct Format")
        else:
            for i in range(0,self.index2+1):
                if int(rno)==self.qresults3[i][0]:
                    self.availableseats=int(self.qresults3[i][9])-int(self.qresults3[i][3])
                    if self.availableseats==0 or self.availableseats-int(numseats)<=0:
                        result=tm.askyesno("Ride Overbooked","Would you like to book anyway?")
                        if result:
                            query=('''INSERT into Bookings(bno,email,rno,cost,seats,pickup,dropoff) VALUES(?,?,?,?,?,?,?)''')
                            if not cost:
                                cost='NULL'
                            if not pickup:
                                pickup='NULL'
                            if not dropoff:
                                dropoff='NULL'
                            self.rno1=rno
                            c.execute(query,[(str(bno)),(member),(rno),(cost),(numseats),(pickup),(dropoff)])
                            self.check=1
                            break
                        else:
                            tm.showinfo("ATTENTION","Booking was not made")
                            break
        bno=1
        query2=('''SELECT * FROM bookings''')
        with conn:
            c.execute(query2)
            qresults=c.fetchall()
            for row in qresults:
                if int(row[0])==bno:
                    bno+=1
                else:
                    break
        if self.check==1:
            self.recipient=member
            self.message="Your booking is confirmed"
            self.send_email()
            self.recipient=''
            self.message=''
            self.rno1=''
            

    def send_email(self):
        global user
        recipient=self.recipient
        timestamp=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        sender=user
        message=self.message
        rno=self.rno1
        if not rno:
            rno='NULL'
        seen="n"
        query=('''INSERT into inbox(email,msgTimestamp,sender,content,rno,seen) VALUES (?,?,?,?,?,?)''')
        if recipient and message and rno and user:
            with conn:
                c.execute(query,[(recipient),(timestamp),(sender),(message),(rno),(seen)])
                tm.showinfo("SUCCESS","Message Sent")
        else:
            tm.showerror("WRONG FORMAT", "Please Enter Correct Format")
    
    def show_more(self):
        self.s+=5
        self.e+=5
        self.l+=5
        for i in range(self.s,self.e):
            line=''
            print(i)
            print(self.index2)
            if i<self.index2:
                for j in range(0,9):
                    line+=str(self.qresults3[i][j])+' | '
                self.availableseats=int(self.qresults3[i][9])-int(self.qresults3[i][3])
                line+=str(self.availableseats)+' |'
                self.Lb.insert(self.l,line)
                self.availableseats=0
                line=''
            else:
                break



class request_ride(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        global user
        global rid
        self.year=tk.IntVar(self)
        self.day=tk.IntVar(self)
        self.month=tk.IntVar(self)
        self.hour=tk.IntVar(self)
        self.minute=tk.IntVar(self)
        self.second=0
        self.pickup=tk.StringVar(self)
        self.dropoff=tk.StringVar(self)
        self.cost=tk.IntVar(self)
        tk.Label(self, text="Enter Year (YYYY):").grid(row=0,column=0)
        self.year = tk.Entry(self)
        self.year.grid(row=0,column=1)
        tk.Label(self, text="Enter Month (M)").grid(row=1,column=0)
        self.month = tk.Entry(self)
        self.month.grid(row=1,column=1)
        tk.Label(self, text="Enter Day (DD)").grid(row=2,column=0)
        self.day = tk.Entry(self)
        self.day.grid(row=2,column=1)
        tk.Label(self, text="Enter Hour (24 HR)").grid(row=3,column=0)
        self.hour = tk.Entry(self)
        self.hour.grid(row=3,column=1)
        tk.Label(self, text="Enter Minute (M)").grid(row=4,column=0)
        self.minute = tk.Entry(self)
        self.minute.grid(row=4,column=1)
        tk.Label(self, text="Enter Pick Up location (lcode):").grid(row=5,column=0)
        self.pickup = tk.Entry(self)
        self.pickup.grid(row=5,column=1)
        tk.Label(self, text="Enter Drop Off location (lcode):").grid(row=6,column=0)
        self.dropoff = tk.Entry(self)
        self.dropoff.grid(row=6,column=1)
        tk.Label(self, text="Enter amount willing to pay (int):").grid(row=7,column=0)
        self.cost = tk.Entry(self)
        self.cost.grid(row=7,column=1)
        tk.Button(self,text="Go Back",command=lambda:master.switch_frame(LoginScreen)).grid(columnspan=2)
        tk.Button(self,text="Request",command=self.request).grid(columnspan=2)
        query=("SELECT * from requests")
        rid=1
        with conn:
            c.execute(query)
            qresults=c.fetchall()
            for row in qresults:
                if int(row[0])==rid:
                    rid+=1
                else:
                    break

    def request(self):
        global user
        global rid
        year=int(self.year.get())
        day=int(self.day.get())
        month=int(self.month.get())
        hour=int(self.hour.get())
        minute=int(self.minute.get())
        second=0
        pickup=self.pickup.get()
        dropoff=self.dropoff.get()
        cost=int(self.cost.get())
        email=user
        rdate=str(datetime.datetime(year,month, day, hour, minute, second))
        rid1=str(rid)
        query=('''INSERT into requests(rid,email,rdate,pickup,dropoff,amount) VALUES (?,?,?,?,?,?)''')
        if rdate and pickup and dropoff and cost:
            with conn:
                c.execute(query,[(rid1),(email),(rdate),(pickup),(dropoff),(cost)])
                tm.showinfo("SUCCESS","Request Made")
        else:
            tm.showerror("WRONG FORMAT", "Please Enter Correct Format")
        rid=1
        query2=('''SELECT * FROM requests''')
        with conn:
            c.execute(query2)
            qresults=c.fetchall()
            for row in qresults:
                if int(row[0])==rid:
                    rid+=1
                else:
                    break


class search_request(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        global user
        self.location1=tk.StringVar(self)
        self.rid=tk.StringVar(self)
        self.var1 = tk.StringVar(self)
        self.var1.set('Select Format')
        self.Lb = tk.Listbox(self, height = 8, width = 60,font=("arial", 12)) 
        self.Lb.grid(row=0,columnspan=1)
        scroll = tk.Scrollbar(self, orient = tk.HORIZONTAL) # set scrollbar to list box for when entries exceed size of list box
        scroll.config(command = self.Lb.xview)
        scroll.place(x=550,y=0)
        self.Lb.config(yscrollcommand = scroll.set)
        tk.Label(self, text="Enter rid of request you wish to delete").grid(row=1,column=0)
        self.rid = tk.Entry(self)
        self.rid.grid(row=1,column=1)
        tk.Label(self, text="Enter location to search for rides in that location  (city,lcode):").grid(row=2,column=0)
        self.location1 = tk.Entry(self)
        self.location1.grid(row=2,column=1)
        tk.Button(self,text="Go Back",command=lambda:master.switch_frame(LoginScreen)).grid(columnspan=2)
        tk.Button(self, text="Delete Request",
                  command=self.delete).grid(columnspan=2)
        tk.Button(self, text="Search",
                  command=self.search).grid(columnspan=2)
        self.Lb.insert(0,"Your Ride Requests:")
        greeting="|rid|             |email|                             |rdate|                    |pickup| |dropoff| |amount|"
        self.Lb.insert(1,greeting)
        self.index=1
        query=('''SELECT * FROM requests WHERE email= ?''')
        self.list=[]
        with conn:
            c.execute(query,[(user)])
            qresults=c.fetchall()
            for row in qresults:
                line=''
                self.index+=1
                self.list.append(row[0])
                for i in row:
                    line+=str(i)+' | '
                self.Lb.insert(2,line)
                line=''
        self.list.reverse()
    
    def delete(self):
        global user
        count=0
        check=0
        query=('''DELETE FROM requests WHERE rid like ? AND email like ?''')
        for i in self.list:
            if i==int(self.rid.get()):
                check=1
                with conn:
                    c.execute(query,[(self.rid.get()),(user)])
                    tm.showinfo("SUCCESS","Request Deleted")
        if check==0:
            tm.showerror("ERROR", "Please Enter Correct Request")
        for i in self.list :
            if i==int(self.rid.get()):
                self.Lb.delete(count+2)
                self.list.remove(int(self.rid.get()))
            else:
                count+=1        
    
    def search(self):
        self.Lb.insert(self.index+1,"Search Results:")
        self.Lb.delete(self.index+2, tk.END)
        location1=self.location1.get()
        qresults=''
        location=('''SELECT DISTINCT * FROM requests R, locations L WHERE R.pickup=L.lcode AND (L.lcode like ? OR L.city like ? ) GROUP BY (rid) LIMIT 0,5''')
        with conn:
            c.execute(location,[(location1),(location1)])
            qresults=c.fetchall()
        for row in qresults:
            line=''
            for i in row:
                line+=str(i)+' | '
            self.Lb.insert(self.index+2,line)
            line=''
        self.recipient= tk.StringVar(self)
        self.message=tk.StringVar(self)
        self.rno=tk.StringVar(self)
        tk.Label(self, text="Enter email of member requesting ride (email)").grid(row=6,column=0, sticky=tk.E)
        self.recipient=tk.Entry(self)
        self.recipient.grid(row=6,column=1)
        tk.Label(self, text="Enter your message (message)").grid(row=7,column=0, sticky=tk.E)
        self.message=tk.Entry(self)
        self.message.grid(row=7,column=1)
        tk.Button(self, text="Message User",
                command=self.send_email).grid(row=8,column=1)
    
    def send_email(self):
        global user
        recipient=self.recipient.get()
        timestamp=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        sender=user
        message=self.message.get()
        rno="NULL"
        seen="n"
        query=('''INSERT into inbox(email,msgTimestamp,sender,content,rno,seen) VALUES (?,?,?,?,?,?)''')
        if recipient and message and rno and user:
            with conn:
                c.execute(query,[(recipient),(timestamp),(sender),(message),(rno),(seen)])
                tm.showinfo("SUCCESS","Message Sent")
        else:
            tm.showerror("WRONG FORMAT", "Please Enter Correct Format")



if __name__ == "__main__":
    app = Database()
    app.title("Database")
    app.geometry("1280x720")
    app.title("Database")
    app.configure(background='black')
    app.resizable(width=True,height=False)
    fname="giphy.gif"
    bg=tk.PhotoImage(file=fname)
    cv = tk.Canvas(width="350", height="400",highlightthickness=0)
    cv.place(x=0,y=0,anchor="nw")
    cv.create_image(0, 0, image=bg, anchor='nw')
    app.mainloop()

