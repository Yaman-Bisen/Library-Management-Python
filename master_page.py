from tkinter import *
from tkinter import ttk,messagebox
import mysql.connector
from tkinter import Menu
from tkcalendar import Calendar,DateEntry

#################################################### AutoComplete Textbox #############################################

class AutocompleteEntry(Entry):
    def __init__(self, xpos, ypos, *args, **kwargs):
        
        self.lista = []
        self.xpos = xpos
        self.ypos = ypos
        Entry.__init__(self, *args, **kwargs)
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.lb = Listbox()
        self.lb.config(bg = 'lightgrey')
        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        
        self.lb_up = False
        
    def get_list(self,list_param):
       self.lista = list_param
    #    messagebox.showerror("error",f"{self.lista} and {self}")     
        

    def changed(self, name, index, mode):  

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:            
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.config(bg = 'lightgrey')
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.xpos, y=self.ypos)
                    self.lb_up = True
                
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def empty_entry(self):
        self.delete(0,END)

    def lb_destroy(self):
        self.lb.destroy()
    
    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def comparison(self):
        # messagebox.showerror("error",f"{self.lista} and {self}")
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]

###################################################  End AutoComplete     ############################################
###################################################  MySQL Connection Function #######################################
mydb = "unknown"
def mysql_connect():
    global mydb
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "yaman",
        password = "yaman",
        database = "pythondatabase"
    )
##################################################   End MySQL Connection Function ##################################
win = Tk()
win.title("Library...")

width = win.winfo_screenwidth()
height = win.winfo_screenheight()
win.geometry("%dx%d+0+0" % (width,height))
win.wm_iconbitmap('library.ico')

main_menu = Menu(win)                                                                        # creating menu bar 

# customer datail menu
customer_details = Menu(main_menu,tearoff=False)                                             # creating menu


############################################# new customer registration Page ##################################################
newCustomer_count = 0
def new_customer(event=None):
    global newCustomer_count
    if newCustomer_count == 0:
        newCustomer_count = 1

        newCustomer = LabelFrame(win,text = 'Add Customer Details...')
        newCustomer.place(x = 500, y = 50,width = 500, height = 600)
        bg_color = Label(newCustomer,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        # newCustomer = Toplevel()            # it just like a main window
        # newCustomer.geometry('500x700+500+90')
        # newCustomer.title('Add Customer Details :')
        # newCustomer.focus_set()
        # newCustomer.resizable(0,0)

        # bg_color = Label(newCustomer,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl_id = Label(newCustomer,text="Customer id :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=10)

        cust_id = Entry(newCustomer,font=("times new roman",15),bg="lightgrey")
        cust_id.place(x=75,y=40,width=350,height=35)
        #############
        mysql_connect()

        mycursor = mydb.cursor()

        mycursor.execute("select * from customer_details")

        myresult = mycursor.fetchall()
        
        cust_id.insert(0,"D" + str(int(myresult[-1][0][1:])+1))
        #############
        cust_id['state'] = 'readonly'
        

        lbl_name = Label(newCustomer,text="Enter Customer Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=80)

        cust_name = Entry(newCustomer,font=("times new roman",15),bg="lightgrey")
        cust_name.place(x=75,y=110,width=350,height=35)
        cust_name.focus_set()

        lbl_address = Label(newCustomer,text="Enter Customer Address :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=150)

        cust_address = Entry(newCustomer,font=("times new roman",15),bg="lightgrey")
        cust_address.place(x=75,y=180,width=350,height=35)

        lbl_phone = Label(newCustomer,text="Enter Mobile Number :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=220)

        cust_phone = Entry(newCustomer,font=("times new roman",15),bg="lightgrey")
        cust_phone.place(x=75,y=250,width=350,height=35)

        lbl_prof = Label(newCustomer,text="Enter Customer Proffession :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=290)

        cust_prof = Entry(newCustomer,font=("times new roman",15),bg="lightgrey")
        cust_prof.place(x=75,y=320,width=350,height=35)

        lbl_dob = Label(newCustomer,text="Select Date of birth :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=360)

        # cust_dob = Calendar(newCustomer,font=("times new roman",15),bg="lightgrey",selectmode = 'day', year = 2021, month = 3, day = 12)
        cust_dob = DateEntry(newCustomer,date_pattern='mm/dd/yyyy',font=("times new roman",15),bg="lightgrey",fg="lightgrey")
        cust_dob.place(x=75,y=390,width=350,height=35)

        lbl_adhar = Label(newCustomer,text="Enter Aadhar number :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=430)

        cust_adhar = Entry(newCustomer,font=("times new roman",15),bg="lightgrey")
        cust_adhar.place(x=75,y=460,width=350,height=35)

        def register_customer():
            id = cust_id.get()
            name = cust_name.get()
            address = cust_address.get()
            phone = cust_phone.get()
            prof = cust_prof.get()
            dob = cust_dob.get_date()
            aadhar = cust_adhar.get()

            if id == "" and name == "" and address == "" and phone == "" and prof == "" and dob == "" and aadhar == "":
                messagebox.showwarning("Warning","Please fill all the fields...")
                cust_id.focus_set()
            elif id == "":
                messagebox.showwarning("Warning","something went wrong please try again later...")
                cust_id.focus_set()
            elif name == "":
                messagebox.showwarning("Warning","Please enter the name...")
                cust_name.focus_set()
            elif address == "":
                messagebox.showwarning("Warning","Please enter address...")
                cust_address.focus_set()
            elif phone == "":
                messagebox.showwarning("Warning","Please enter phone number...")
                cust_phone.focus_set()
            elif prof == "":
                messagebox.showwarning("Warning","Please enter proffession...")
                cust_prof.focus_set()
            elif dob == "":
                messagebox.showwarning("Warning","Please select dob...")
            elif aadhar == "":
                messagebox.showwarning("Warning","Please enter aadhar number...")
                cust_address.focus_set()
            else:
                mysql_connect()

                mycursor = mydb.cursor()

                sql_query = "insert into customer_details (cust_id,cust_name,cust_address,cust_mobile,cust_profession,cust_dob,cust_aadhar) values (%s,%s,%s,%s,%s,%s,%s)"

                values = (id,name,address,phone,prof,dob,aadhar)

                mycursor.execute(sql_query,values)

                mydb.commit()

                # print(mycursor.rowcount, "record inserted")
                messagebox.showinfo("Successfull","Customer registered successfully...")

                cust_id['state'] = 'normal'

                cust_id.delete(0,'end')
                cust_id.focus_set()
                cust_name.delete(0,'end')
                cust_address.delete(0,'end')
                cust_phone.delete(0,'end')
                cust_prof.delete(0,'end')
                cust_adhar.delete(0,'end')

                mysql_connect()

                mycursor = mydb.cursor()

                mycursor.execute("select * from customer_details")

                myresult = mycursor.fetchall()

                cust_id.insert(0,"D" + str(int(myresult[-1][0][1:])+1))

                cust_id['state'] = 'readonly'

        def close_func():
            global newCustomer_count
            newCustomer_count = 0
            newCustomer.destroy()

        btn_register = Button(newCustomer,text="Register",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=register_customer).place(x=110,y=520,width=120)

        btn_cancel = Button(newCustomer,text="Cancel",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_func).place(x=260,y=520,width=120)
    else:
        pass
        # messagebox.showwarning("Warning","Page is already opened...")

    # newCustomer.mainloop()


                ###############################################################################

customer_details.add_command(label='New Customer',compound=LEFT,accelerator='Ctrl + N',command=new_customer)        # sub menu

############################################# end new customer registration Page ##################################################

####################################################### Update Customer ##############################################################
update_customer_count = 0
entry = 0
def update_customer(event=None):
    global entry
    global update_customer_count
    if update_customer_count == 0:
        update_customer_count = 1

        updateCustomer = LabelFrame(win,text = 'Add Customer Details to update...')
        updateCustomer.place(x = 500, y = 50,width = 500, height = 600)
        bg_color = Label(updateCustomer,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        ######################## Radio Buttons #################################
        entry = AutocompleteEntry(575, 160, updateCustomer,font=("times new roman",15),bg = "lightgrey")
        entry.place(x=75,y=60,width=270,height=35)
        entry['state'] = 'readonly'

        lbl_update_name = Label(updateCustomer,text="Customer Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        lbl_update_name.place(x=75,y=100)

        cust_update_name = Entry(updateCustomer,font=("times new roman",15),bg="lightgrey")
        cust_update_name.place(x=75,y=130,width=350,height=35)
        cust_update_name.focus_set()

        lbl_update_address = Label(updateCustomer,text="Customer Address :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=170)

        cust_update_address = Entry(updateCustomer,font=("times new roman",15),bg="lightgrey")
        cust_update_address.place(x=75,y=200,width=350,height=35)

        lbl_update_phone = Label(updateCustomer,text="Mobile Number :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=240)

        cust_update_phone = Entry(updateCustomer,font=("times new roman",15),bg="lightgrey")
        cust_update_phone.place(x=75,y=270,width=350,height=35)

        lbl_update_prof = Label(updateCustomer,text="Customer Proffession :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=310)

        cust_update_prof = Entry(updateCustomer,font=("times new roman",15),bg="lightgrey")
        cust_update_prof.place(x=75,y=340,width=350,height=35)

        lbl_update_dob = Label(updateCustomer,text="Date of birth :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=380)

        # cust_dob = Calendar(newCustomer,font=("times new roman",15),bg="lightgrey",selectmode = 'day', year = 2021, month = 3, day = 12)
        cust_update_dob = DateEntry(updateCustomer,date_pattern='mm/dd/yyyy',font=("times new roman",15),bg="lightgrey",fg="lightgrey")
        cust_update_dob.place(x=75,y=410,width=350,height=35)

        lbl_update_adhar = Label(updateCustomer,text="Aadhar number :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=450)

        cust_update_adhar = Entry(updateCustomer,font=("times new roman",15),bg="lightgrey")
        cust_update_adhar.place(x=75,y=480,width=350,height=35)

        def option_selected():
            cust_update_name.delete(0,END)
            cust_update_address.delete(0,END)
            cust_update_phone.delete(0,END)
            cust_update_prof.delete(0,END)
            cust_update_dob.delete(0,END)
            cust_update_adhar.delete(0,END)
            
            global entry
            entry.focus_set()
            entry['state'] = "normal"
            entry.empty_entry()

            if var.get() == 1:
                lbl_update_name['text'] = "Customer Name :"
                
                mysql_connect()

                mycursor = mydb.cursor()
                
                sql = "select cust_id from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                
                # myresult = [('D1001',),('D1002',)]

                lista = []
                for x in myresult:          #   x = ('D1001',)  
                    lista.append(x[0])      #   x[0] = 'D1001'
                
                mycursor.close()

                entry.get_list(lista)       # ['D1001','D1002']
                # print(lista)
            else:
                lbl_update_name['text'] = "Customer Id :"
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select cust_name from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                listb = []
                for x in myresult:
                    listb.append(x[0])

                mycursor.close()
                
                entry.get_list(listb)
                # print(listb)
                
        var = IntVar()
        R1 = Radiobutton(updateCustomer, text="Search by ID", variable=var, value=1,bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=option_selected)
        R1.place(x = 60,y = 10)

        R2 = Radiobutton(updateCustomer, text="Search by Name",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red", variable=var, value=2,command=option_selected)
        R2.place(x = 250,y = 10)

        ############################### search button ###########################################
        def fetch_details():
            if entry.get() == "":           # id or name text box
                messagebox.showwarning("Warning","Please enter id or name for search...")
            else:
                if var.get() == 1:
                    update_id = entry.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from customer_details where cust_id = %s"
                    val = (update_id,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        cust_update_name.delete(0,END)
                        cust_update_address.delete(0,END)
                        cust_update_phone.delete(0,END)
                        cust_update_prof.delete(0,END)
                        cust_update_dob.delete(0,END)
                        cust_update_adhar.delete(0,END)

                        entry.lb_destroy()
                        cust_update_name.insert(0,myresult[0][1])
                        cust_update_address.insert(0,myresult[0][2])
                        cust_update_phone.insert(0,myresult[0][3])
                        cust_update_prof.insert(0,myresult[0][4])
                        cust_update_dob.insert(0,myresult[0][5])
                        cust_update_adhar.insert(0,myresult[0][6])
                    else:
                        messagebox.showerror("Error","Customer not found, Please enter valid Customer Id...")
                        entry.empty_entry()
                        cust_update_name.delete(0,END)
                        cust_update_address.delete(0,END)
                        cust_update_phone.delete(0,END)
                        cust_update_prof.delete(0,END)
                        cust_update_dob.delete(0,END)
                        cust_update_adhar.delete(0,END)
                    mycursor.close()
                else:
                    update_name = entry.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from customer_details where cust_name = %s"
                    val = (update_name,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        cust_update_name.delete(0,END)
                        cust_update_address.delete(0,END)
                        cust_update_phone.delete(0,END)
                        cust_update_prof.delete(0,END)
                        cust_update_dob.delete(0,END)
                        cust_update_adhar.delete(0,END)

                        entry.lb_destroy()
                        cust_update_name.insert(0,myresult[0][0])
                        cust_update_address.insert(0,myresult[0][2])
                        cust_update_phone.insert(0,myresult[0][3])
                        cust_update_prof.insert(0,myresult[0][4])
                        cust_update_dob.insert(0,myresult[0][5])
                        cust_update_adhar.insert(0,myresult[0][6])
                    else:
                        messagebox.showerror("Error","Customer not found, Please enter valid Customer Name...")
                        entry.empty_entry()
                        cust_update_name.delete(0,END)
                        cust_update_address.delete(0,END)
                        cust_update_phone.delete(0,END)
                        cust_update_prof.delete(0,END)
                        cust_update_dob.delete(0,END)
                        cust_update_adhar.delete(0,END)

        btn_update_search = Button(updateCustomer,text="Fetch",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=fetch_details).place(x=355,y=60,width=100)

        def update_customer_details():
            update_id = 0
            update_name = 0
            if var.get() == 1:
                update_id = entry.get()
                update_name = cust_update_name.get()
            else:
                update_id = cust_update_name.get()
                update_name = entry.get()
            update_address = cust_update_address.get()
            update_phone = cust_update_phone.get()
            update_prof = cust_update_prof.get()
            update_dob = cust_update_dob.get()
            update_aadhar = cust_update_adhar.get()
          
            if update_id == "" and update_name == "" and update_address == "" and update_phone == "" and update_prof == "" and update_dob == "" and update_aadhar == "":
                messagebox.showwarning("Warning","Please fill all the fields...")
                cust_update_name.focus_set()
            elif update_id == "":
                messagebox.showwarning("Warning","Please enter customer id...")
                cust_update_name.focus_set()
            elif update_name == "":
                messagebox.showwarning("Warning","Please enter the name...")
                cust_update_name.focus_set()
            elif update_address == "":
                messagebox.showwarning("Warning","Please enter address...")
                cust_update_address.focus_set()
            elif update_phone == "":
                messagebox.showwarning("Warning","Please enter phone number...")
                cust_update_phone.focus_set()
            elif update_prof == "":
                messagebox.showwarning("Warning","Please enter proffession...")
                cust_update_prof.focus_set()
            elif update_dob == "":
                messagebox.showwarning("Warning","Please select dob...")
            elif update_aadhar == "":
                messagebox.showwarning("Warning","Please enter aadhar number...")
                cust_update_adhar.focus_set()
            else:
                try:
                    mysql_connect()

                    mycursor = mydb.cursor()

                    sql_query = "update customer_details set cust_id = %s, cust_name = %s, cust_address = %s, cust_mobile = %s, cust_profession = %s, cust_dob = %s, cust_aadhar = %s where cust_id = %s"

                    values = (update_id,update_name,update_address,update_phone,update_prof,update_dob,update_aadhar,update_id)

                    # print(values)
                    mycursor.execute(sql_query,values)

                    mydb.commit()

                    # print(mycursor.rowcount, "record inserted")
                    messagebox.showinfo("Successfull","Customer information updated successfully...")
                    
                    entry.empty_entry()
                    entry.focus_set()
                    cust_update_name.delete(0,END)
                    cust_update_address.delete(0,END)
                    cust_update_phone.delete(0,END)
                    cust_update_prof.delete(0,END)
                    cust_update_dob.delete(0,END)
                    cust_update_adhar.delete(0,END)

                    mycursor.close()
                except Exception as e:
                    messagebox.showerror("Error",f"{e} on line 539")

        def close_update_func():
            global entry
            global update_customer_count
            update_customer_count = 0
            entry.empty_entry()
            updateCustomer.destroy()

        btn_update = Button(updateCustomer,text="Update",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=update_customer_details).place(x=110,y=530,width=120)

        btn_update_cancel = Button(updateCustomer,text="Cancel",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_update_func).place(x=260,y=530,width=120)
    else:
        pass
        # messagebox.showerror("Error",'Page is already opened...')

customer_details.add_command(label='Update Customer',compound=LEFT,accelerator='Ctrl + U',command=update_customer)        

####################################################### End Update Customer ##############################################################

####################################################### Delete Customer Page ##############################################################
delete_customer_count = 0
entry = 0
def delete_customer(event=None):
    global entry
    global delete_customer_count
    
    if delete_customer_count == 0:
        delete_customer_count = 1

        deleteCustomer = LabelFrame(win,text = 'Select customer by id or name to delete...')
        deleteCustomer.place(x = 500, y = 50,width = 500, height = 600)
        bg_color = Label(deleteCustomer,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        entry = AutocompleteEntry(575, 160, deleteCustomer,font=("times new roman",15),bg = "lightgrey")
        entry.place(x=75,y=60,width=270,height=35)
        entry['state'] = 'readonly'

        lbl_delete_name = Label(deleteCustomer,text="Customer Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        lbl_delete_name.place(x=75,y=100)

        cust_delete_name = Entry(deleteCustomer,font=("times new roman",15),bg="lightgrey")
        cust_delete_name.place(x=75,y=130,width=350,height=35)
        cust_delete_name.focus_set()

        lbl_delete_address = Label(deleteCustomer,text="Customer Address :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=170)

        cust_delete_address = Entry(deleteCustomer,font=("times new roman",15),bg="lightgrey")
        cust_delete_address.place(x=75,y=200,width=350,height=35)

        lbl_delete_phone = Label(deleteCustomer,text="Mobile Number :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=240)

        cust_delete_phone = Entry(deleteCustomer,font=("times new roman",15),bg="lightgrey")
        cust_delete_phone.place(x=75,y=270,width=350,height=35)

        lbl_delete_prof = Label(deleteCustomer,text="Customer Proffession :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=310)

        cust_delete_prof = Entry(deleteCustomer,font=("times new roman",15),bg="lightgrey")
        cust_delete_prof.place(x=75,y=340,width=350,height=35)

        lbl_delete_dob = Label(deleteCustomer,text="Date of birth :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=380)

        # cust_dob = Calendar(newCustomer,font=("times new roman",15),bg="lightgrey",selectmode = 'day', year = 2021, month = 3, day = 12)
        cust_delete_dob = DateEntry(deleteCustomer,date_pattern='mm/dd/yyyy',font=("times new roman",15),bg="lightgrey",fg="lightgrey")
        cust_delete_dob.place(x=75,y=410,width=350,height=35)

        lbl_delete_adhar = Label(deleteCustomer,text="Aadhar number :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=450)

        cust_delete_adhar = Entry(deleteCustomer,font=("times new roman",15),bg="lightgrey")
        cust_delete_adhar.place(x=75,y=480,width=350,height=35)

        def option_selected():
            cust_delete_name.delete(0,END)
            cust_delete_address.delete(0,END)
            cust_delete_prof.delete(0,END)
            cust_delete_phone.delete(0,END)
            cust_delete_dob.delete(0,END)
            cust_delete_adhar.delete(0,END)
            global entry
            entry.focus_set()
            entry['state'] = "normal"

            entry.empty_entry()
            if var.get() == 1:
                lbl_delete_name['text'] = "Customer Name :"
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select cust_id from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                lista = []
                for x in myresult:
                    lista.append(x[0])
                
                mycursor.close()

                entry.get_list(lista)
                # print(lista)
            else:
                lbl_delete_name['text'] = "Customer Id :"
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select cust_name from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                listb = []
                for x in myresult:
                    listb.append(x[0])

                mycursor.close()
                
                entry.get_list(listb)
                # print(listb)
                
        var = IntVar()
        R1 = Radiobutton(deleteCustomer, text="Search by ID", variable=var, value=1,bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=option_selected)
        R1.place(x = 60,y = 10)

        R2 = Radiobutton(deleteCustomer, text="Search by Name",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red", variable=var, value=2,command=option_selected)
        R2.place(x = 250,y = 10)

        ############################### search button ###########################################
        def fetch_details():
            if entry.get() == "":
                messagebox.showwarning("Warning","Please enter id or name for search...")
            else:
                if var.get() == 1:
                    delete_id = entry.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from customer_details where cust_id = %s"
                    val = (delete_id,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        cust_delete_name.delete(0,END)
                        cust_delete_address.delete(0,END)
                        cust_delete_prof.delete(0,END)
                        cust_delete_phone.delete(0,END)
                        cust_delete_dob.delete(0,END)
                        cust_delete_adhar.delete(0,END)

                        entry.lb_destroy()
                        cust_delete_name.insert(0,myresult[0][1])
                        cust_delete_address.insert(0,myresult[0][2])
                        cust_delete_phone.insert(0,myresult[0][3])
                        cust_delete_prof.insert(0,myresult[0][4])
                        cust_delete_dob.insert(0,myresult[0][5])
                        cust_delete_adhar.insert(0,myresult[0][6])
                    else:
                        messagebox.showerror("Error","Customer not found, Please enter valid Customer Id...")
                        entry.empty_entry()
                        cust_delete_name.delete(0,END)
                        cust_delete_address.delete(0,END)
                        cust_delete_phone.delete(0,END)
                        cust_delete_prof.delete(0,END)
                        cust_delete_dob.delete(0,END)
                        cust_delete_adhar.delete(0,END)
                    mycursor.close()
                else:
                    delete_name = entry.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from customer_details where cust_name = %s"
                    val = (delete_name,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        cust_delete_name.delete(0,END)
                        cust_delete_address.delete(0,END)
                        cust_delete_phone.delete(0,END)
                        cust_delete_prof.delete(0,END)
                        cust_delete_dob.delete(0,END)
                        cust_delete_adhar.delete(0,END)

                        entry.lb_destroy()
                        cust_delete_name.insert(0,myresult[0][0])
                        cust_delete_address.insert(0,myresult[0][2])
                        cust_delete_phone.insert(0,myresult[0][3])
                        cust_delete_prof.insert(0,myresult[0][4])
                        cust_delete_dob.insert(0,myresult[0][5])
                        cust_delete_adhar.insert(0,myresult[0][6])
                    else:
                        messagebox.showerror("Error","Customer not found, Please enter valid Customer Name...")
                        entry.empty_entry()
                        cust_delete_name.delete(0,END)
                        cust_delete_address.delete(0,END)
                        cust_delete_phone.delete(0,END)
                        cust_delete_prof.delete(0,END)
                        cust_delete_dob.delete(0,END)
                        cust_delete_adhar.delete(0,END)

        btn_update_search = Button(deleteCustomer,text="Fetch",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=fetch_details).place(x=355,y=60,width=100)

        def delete_customer_details():
            delete_id = 0
            delete_name = 0
            if var.get() == 1:
                delete_id = entry.get()
                delete_name = cust_delete_name.get()
            else:
                delete_id = cust_delete_name.get()
                delete_name = entry.get()
            
            if delete_id == "" and delete_name == "":
                messagebox.showerror("Error","Sorry !!! we didn't get your id or name...")
                cust_delete_name.focus_set()
            else:
                try:
                    mysql_connect()

                    mycursor = mydb.cursor()

                    sql_query = "delete from customer_details where cust_id = %s and cust_name = %s"

                    values = (delete_id,delete_name)

                    mycursor.execute(sql_query,values)

                    mydb.commit()

                    # print(mycursor.rowcount, "record inserted")
                    messagebox.showinfo("Successfull","Customer record deleted successfully...")

                    entry.empty_entry()
                    entry.focus_set()
                    cust_delete_name.delete(0,END)
                    cust_delete_address.delete(0,END)
                    cust_delete_phone.delete(0,END)
                    cust_delete_prof.delete(0,END)
                    cust_delete_dob.delete(0,END)
                    cust_delete_adhar.delete(0,END)
                except Exception as e:
                    messagebox.showerror("Error","something went wrong while transaction with database, kindly call developer...")

        def close_delete_func():
            global entry
            entry.empty_entry()
            entry.lb_destroy()
            global delete_customer_count
            delete_customer_count = 0
            deleteCustomer.destroy()

        btn_delete = Button(deleteCustomer,text="Delete",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=delete_customer_details).place(x=110,y=530,width=120)

        btn_delete_cancel = Button(deleteCustomer,text="Cancel",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_delete_func).place(x=260,y=530,width=120)
    else:
        pass

customer_details.add_command(label='Delete Customer',compound=LEFT,accelerator='Ctrl + D',command=delete_customer)  

####################################################### End Delete Customer page ##############################################################

####################################################### View All Customer page ##############################################################
view_all_count = 0
def view_all_customer(event=None):
    global view_all_count
    if view_all_count == 0:
        view_all_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "All Customers", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        cols = ('Customer Id','Name','Address','Mobile Number','Profession','Date of Birth','Aadhar Number')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center")
            my_tree.heading(col,text = col)

        for col in cols:
            my_tree.column(col,anchor = "center",width=140)
            my_tree.heading(col,text = col)
        
        try:

            mysql_connect()

            mycursor = mydb.cursor()

            sql = "Select * from customer_details where cust_id not in ('D1000')"

            mycursor.execute(sql)

            myresult = mycursor.fetchall()

            for id,name,address,mobile,profession,dob,aadhar in myresult:
                    # print(id, name, address,mobile,profession,dob,aadhar)
                my_tree.insert("","end",values=(id, name, address,mobile,profession,dob,aadhar))
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_view_all_page():
            global view_all_count
            view_all_count = 0
            tree_frame.destroy()
            # my_tree.destroy()
            # tree_scroll.destroy()
            # btn_close.destroy()
                  

        btn_close = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_view_all_page).place(x=450,y=555,width=120)
    else:
        pass

customer_details.add_separator()
customer_details.add_command(label='All Customer',compound=LEFT,accelerator='Ctrl+Alt+A',command=view_all_customer)        

####################################################### End View All Customer page ##############################################################

# allocate book menu
allocate_book = Menu(main_menu,tearoff=False)

####################################################### Allocate book page ##############################################################
customer_search = 0
book_search = 0
global entry_customer
global book_entry
allocate_book_count = 0
proceed_cust_id = 0
proceed_book_id = 0
def allocate_book_page(event=None):
    global proceed_cust_id
    global proceed_book_id
    global customer_search
    global book_search
    global book_entry
    global entry_customer
    global allocate_book_count
    if allocate_book_count == 0:
        allocate_book_count = 1

        main_frame = LabelFrame(win,text = 'Allocate Book...')
        main_frame.place(x = 18, y = 50,width = 1500, height = 600)
        bg_color = Label(main_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        #############################   customer frame ##################################

        customer_details_frame = LabelFrame(main_frame,text = 'Select customer by id or name...')
        customer_details_frame.place(x = 0, y = 0,width = 500, height = 550)
        bg_color = Label(customer_details_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        entry_customer = AutocompleteEntry(98, 178, customer_details_frame,font=("times new roman",15),bg = "lightgrey")
        entry_customer.place(x=75,y=60,width=240,height=35)
        entry_customer['state'] = 'readonly'

        lbl_name_cust = Label(customer_details_frame,text="Customer Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        lbl_name_cust.place(x=75,y=100)

        entry_cust_name = Entry(customer_details_frame,font=("times new roman",15),bg="lightgrey")
        entry_cust_name.place(x=75,y=130,width=350,height=35)

        lbl_address_cust = Label(customer_details_frame,text="Customer Address :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=170)

        entry_cust_address = Entry(customer_details_frame,font=("times new roman",15),bg="lightgrey")
        entry_cust_address.place(x=75,y=200,width=350,height=35)

        lbl_phone_cust = Label(customer_details_frame,text="Mobile Number :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=240)

        entry_cust_phone = Entry(customer_details_frame,font=("times new roman",15),bg="lightgrey")
        entry_cust_phone.place(x=75,y=270,width=350,height=35)

        lbl_prof_cust = Label(customer_details_frame,text="Customer Proffession :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=310)

        entry_cust_prof = Entry(customer_details_frame,font=("times new roman",15),bg="lightgrey")
        entry_cust_prof.place(x=75,y=340,width=350,height=35)

        lbl_dob_cust = Label(customer_details_frame,text="Date of birth :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=380)

        # cust_dob = Calendar(newCustomer,font=("times new roman",15),bg="lightgrey",selectmode = 'day', year = 2021, month = 3, day = 12)
        entry_cust_dob = DateEntry(customer_details_frame,date_pattern='mm/dd/yyyy',font=("times new roman",15),bg="lightgrey",fg="lightgrey")
        entry_cust_dob.place(x=75,y=410,width=350,height=35)

        lbl_aadhar_cust = Label(customer_details_frame,text="Aadhar number :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=450)

        entry_cust_aadhar = Entry(customer_details_frame,font=("times new roman",15),bg="lightgrey")
        entry_cust_aadhar.place(x=75,y=480,width=350,height=35)

        def option_customer_selected():
            global customer_search
            global entry_customer
            
            make_trans_entries_normal()
            make_trans_entries_empty()
            make_trans_entries_readonly()

            customer_search = 0

            make_cust_entries_normal()
            empty_cust_entries()
            make_cust_entries_readonly()

            entry_customer.focus_set()
            entry_customer['state'] = "normal"

            entry_customer.empty_entry()
            if var.get() == 1:
                lbl_name_cust['text'] = "Customer Name :"
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select cust_id from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                lista = []
                for x in myresult:
                    lista.append(x[0])
                
                mycursor.close()

                entry_customer.get_list(lista)
                # print(lista)
            else:
                lbl_name_cust['text'] = "Customer Id :"
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select cust_name from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                listb = []
                for x in myresult:
                    listb.append(x[0])

                mycursor.close()
                
                entry_customer.get_list(listb)
                # print(listb)
                
        var = IntVar()
        Radio_customer_id = Radiobutton(customer_details_frame, text="Search by ID", variable=var, value=1,bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=option_customer_selected)
        Radio_customer_id.place(x = 60,y = 10)

        Radio_customer_name = Radiobutton(customer_details_frame, text="Search by Name",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red", variable=var, value=2,command=option_customer_selected)
        Radio_customer_name.place(x = 250,y = 10)

        ############################### search button ###########################################
        def fetch_customer_details():
            global proceed_cust_id
            global customer_search
            if entry_customer.get() == "":
                messagebox.showwarning("Warning","Please enter id or name for search...")
            else:
                if var.get() == 1:
                    customer_id = entry_customer.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from customer_details where cust_id = %s"
                    val = (customer_id,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:

                        make_cust_entries_normal()

                        empty_cust_entries()

                        entry_customer.lb_destroy()
                        proceed_cust_id = entry_customer.get()
                        entry_cust_name.insert(0,myresult[0][1])
                        entry_cust_address.insert(0,myresult[0][2])
                        entry_cust_phone.insert(0,myresult[0][3])
                        entry_cust_prof.insert(0,myresult[0][4])
                        entry_cust_dob.insert(0,myresult[0][5])
                        entry_cust_aadhar.insert(0,myresult[0][6])
                        customer_search = 1

                        make_cust_entries_readonly()
                    else:
                        messagebox.showerror("Error","Customer not found, Please enter valid Customer Id...")
                        entry_customer.empty_entry()
                        empty_cust_entries()

                    mycursor.close()
                else:
                    customer_name = entry_customer.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from customer_details where cust_name = %s"
                    val = (customer_name,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        make_cust_entries_normal()
                        
                        empty_cust_entries()
                        
                        entry_customer.lb_destroy()
                        proceed_cust_id = myresult[0][0]
                        entry_cust_name.insert(0,myresult[0][0])
                        entry_cust_address.insert(0,myresult[0][2])
                        entry_cust_phone.insert(0,myresult[0][3])
                        entry_cust_prof.insert(0,myresult[0][4])
                        entry_cust_dob.insert(0,myresult[0][5])
                        entry_cust_aadhar.insert(0,myresult[0][6])
                        customer_search = 1

                        make_cust_entries_readonly()
                    else:
                        messagebox.showerror("Error","Customer not found, Please enter valid Customer Name...")
                        entry_customer.empty_entry()
                        empty_cust_entries()

        btn_customer_search = Button(customer_details_frame,text="Fetch",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=fetch_customer_details).place(x=325,y=60,width=100)

        #############################    book frame     ##################################333

        book_frame = LabelFrame(main_frame,text = 'Select book by id or name...')
        book_frame.place(x = 500, y = 0,width = 500, height = 550)
        bg_color = Label(book_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        book_entry = AutocompleteEntry(598, 178, book_frame,font=("times new roman",15),bg = "lightgrey")
        book_entry.place(x=75,y=60,width=240,height=35)
        book_entry['state'] = 'readonly'

        lbl_name_book = Label(book_frame,text="Book Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        lbl_name_book.place(x=75,y=100)

        entry_book_name = Entry(book_frame,font=("times new roman",15),bg="lightgrey")
        entry_book_name.place(x=75,y=130,width=350,height=35) 

        lbl_auth_name_book = Label(book_frame,text="Auther Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=170)

        entry_auth_name = Entry(book_frame,font=("times new roman",15),bg="lightgrey")
        entry_auth_name.place(x=75,y=200,width=350,height=35)

        lbl_paid_unpaid_book = Label(book_frame,text="Select Option :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=240)

        combo_paid_unpaid = ttk.Combobox(book_frame,font=("times new roman",15))
        combo_paid_unpaid['values'] = ('Select Option','Paid','Unpaid')
        combo_paid_unpaid.current(0)
        combo_paid_unpaid.place(x=75,y=270,width=350,height=35)
        combo_paid_unpaid['state'] = 'readonly'

        lbl_price_book = Label(book_frame,text="Custom Price :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=310)

        entry_price = Entry(book_frame,font=("times new roman",15),bg="lightgrey")
        entry_price.place(x=75,y=340,width=350,height=35)
        
        lbl_quantity_book = Label(book_frame,text="Quantity :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=380)

        entry_quantity = Entry(book_frame,font=("times new roman",15),bg="lightgrey")
        entry_quantity.place(x=75,y=410,width=350,height=35)

        def make_cust_entries_readonly():
            entry_customer['state'] = 'readonly'
            entry_cust_name['state'] = 'readonly'
            entry_cust_address['state'] = 'readonly'
            entry_cust_phone['state'] = 'readonly'
            entry_cust_prof['state'] = 'readonly'
            entry_cust_dob['state'] = 'readonly'
            entry_cust_aadhar['state'] = 'readonly'
        
        def make_book_entries_readonly():
            book_entry['state'] = 'readonly'
            entry_book_name['state'] = 'readonly'
            entry_auth_name['state'] = 'readonly'
            combo_paid_unpaid['state'] = 'readonly'
            entry_price['state'] = 'readonly'
            entry_quantity['state'] = 'readonly'

        def make_cust_entries_normal():
            entry_customer['state'] = 'normal'
            entry_cust_name['state'] = 'normal'
            entry_cust_address['state'] = 'normal'
            entry_cust_phone['state'] = 'normal'
            entry_cust_prof['state'] = 'normal'
            entry_cust_dob['state'] = 'normal'
            entry_cust_aadhar['state'] = 'normal'
        
        def make_book_entries_normal():
            book_entry['state'] = 'normal'
            entry_book_name['state'] = 'normal'
            entry_auth_name['state'] = 'normal'
            combo_paid_unpaid['state'] = 'normal'
            entry_price['state'] = 'normal'
            entry_quantity['state'] = 'normal'

        def empty_cust_entries():
            entry_cust_name.delete(0,END)
            entry_cust_address.delete(0,END)
            entry_cust_prof.delete(0,END)
            entry_cust_phone.delete(0,END)
            entry_cust_dob.delete(0,END)
            entry_cust_aadhar.delete(0,END)

        def empty_book_entries():
            entry_book_name.delete(0,END)
            entry_auth_name.delete(0,END)
            combo_paid_unpaid.current(0)
            entry_price.delete(0,END)
            entry_quantity.delete(0,END)
        
        def make_trans_entries_normal():
            trans_cust_entry_id['state'] = 'normal'
            trans_book_entry_id['state'] = 'normal'
            trans_rental_price['state'] = 'normal'
            trans_total_rent['state'] = 'normal'
            trans_rent_given['state'] = 'normal'

        def make_trans_entries_empty():
            trans_cust_entry_id.delete(0,END)
            trans_book_entry_id.delete(0,END)
            trans_rental_price.delete(0,END)
            trans_total_rent.delete(0,END)
            trans_rent_given.delete(0,END)
        
        def make_trans_entries_readonly():
            trans_cust_entry_id['state'] = 'readonly'
            trans_book_entry_id['state'] = 'readonly'
            trans_rental_price['state'] = 'readonly'
            trans_total_rent['state'] = 'readonly'
            trans_rent_given['state'] = 'readonly'
        
        make_book_entries_readonly()
        make_cust_entries_readonly()

        def option_book_selected():
            global book_search
            global book_entry

            make_trans_entries_normal()
            make_trans_entries_empty()
            make_trans_entries_readonly()

            book_search = 0

            make_book_entries_normal()
            empty_book_entries()            # for empty entry boxes of book_frame
            make_book_entries_readonly()
            
            book_entry.focus_set()
            book_entry['state'] = "normal"
            book_entry.empty_entry()

            if var1.get() == 1:
                lbl_name_book['text'] = "Book Name :"
                
                mysql_connect()

                mycursor = mydb.cursor()
                
                sql = "select book_id from book_details where book_id not in ('B1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                
                # myresult = [('D1001',),('D1002',)]

                lista = []
                for x in myresult:          #   x = ('B1001',)  
                    lista.append(x[0])      #   x[0] = 'B1001'
                
                mycursor.close()

                book_entry.get_list(lista)       # ['B1001','B1002']
                # print(lista)
            else:
                lbl_name_book['text'] = "Book Id :"
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select book_name from book_details where book_id not in ('B1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                listb = []
                for x in myresult:
                    listb.append(x[0])

                mycursor.close()
                
                book_entry.get_list(listb)
                # print(listb)
                
        var1 = IntVar()
        radio_book_id = Radiobutton(book_frame, text="Search by ID", variable=var1, value=1,bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=option_book_selected)
        radio_book_id.place(x = 60,y = 10)

        radio_book_name = Radiobutton(book_frame, text="Search by Name",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red", variable=var1, value=2,command=option_book_selected)
        radio_book_name.place(x = 250,y = 10)

        ############################### search button ###########################################
        def fetch_book_details():
            global proceed_book_id
            global book_search
            if book_entry.get() == "":           # id or name text box
                messagebox.showwarning("Warning","Please enter id or name for search...")
            else:
                if var1.get() == 1:
                    book_id = book_entry.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from book_details where book_id = %s"
                    val = (book_id,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:

                        make_book_entries_normal()

                        empty_book_entries()

                        book_entry.lb_destroy()
                        proceed_book_id = book_entry.get()
                        entry_book_name.insert(0,myresult[0][1])
                        entry_auth_name.insert(0,myresult[0][2])
                        if myresult[0][3] == "Paid":
                            combo_paid_unpaid.current(1)
                        else:
                            combo_paid_unpaid.current(2)
                        entry_price.insert(0,myresult[0][4])
                        entry_quantity.insert(0,myresult[0][6])
                        book_search = 1

                        make_book_entries_readonly()
                    else:
                        messagebox.showerror("Error","Book not found, Please enter valid book Id...")
                        book_entry.empty_entry()
                        empty_book_entries()
                    mycursor.close()
                else:
                    book_name = book_entry.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from book_details where book_name = %s"
                    val = (book_name,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:

                        make_book_entries_normal()

                        empty_book_entries()

                        book_entry.lb_destroy()
                        proceed_book_id = myresult[0][0]
                        entry_book_name.insert(0,myresult[0][0])
                        entry_auth_name.insert(0,myresult[0][2])
                        if myresult[0][3] == "Paid":
                            combo_paid_unpaid.current(1)
                        else:
                            combo_paid_unpaid.current(2)
                        entry_price.insert(0,myresult[0][4])
                        entry_quantity.insert(0,myresult[0][6])
                        book_search = 1

                        make_book_entries_readonly()
                    else:
                        messagebox.showerror("Error","Book not found, Please enter valid book Name...")
                        book_entry.empty_entry()
                        empty_book_entries()

        btn_book_search = Button(book_frame,text="Fetch",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=fetch_book_details).place(x=325,y=60,width=100)

        #############################   transaction frame   ##############################3

        transaction_frame = LabelFrame(main_frame,text = 'Transaction Details...')
        transaction_frame.place(x = 1000, y = 0,width = 495, height = 550)
        bg_color = Label(transaction_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        trans_cust_id = Label(transaction_frame,text="Customer Id :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        trans_cust_id.place(x=30,y=20)

        trans_cust_entry_id = Entry(transaction_frame,font=("times new roman",15),bg="lightgrey")
        trans_cust_entry_id.place(x=155,y=20,width=300,height=30)

        trans_book_id = Label(transaction_frame,text="Book Id :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        trans_book_id.place(x=30,y=70)

        trans_book_entry_id = Entry(transaction_frame,font=("times new roman",15),bg="lightgrey")
        trans_book_entry_id.place(x=155,y=70,width=300,height=30)

        trans_allocate_date_lbl = Label(transaction_frame,text="Select Date :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        trans_allocate_date_lbl.place(x=30,y=120)

        trans_allocate_date = DateEntry(transaction_frame,date_pattern='yyyy/mm/dd',font=("times new roman",15),background="lightgrey",foreground="lightgrey")
        trans_allocate_date.place(x=155,y=120,width=300,height=30)

        trans_lbl_rental_price = Label(transaction_frame,text="Rental Price :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        trans_lbl_rental_price.place(x=30,y=170)

        trans_rental_price = Entry(transaction_frame,font=("times new roman",15),bg="lightgrey")
        trans_rental_price.place(x=155,y=170,width=300,height=30)

        trans_lbl_quantity = Label(transaction_frame,text="Quantity :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        trans_lbl_quantity.place(x=30,y=220)

        trans_quantity_given = Entry(transaction_frame,font=("times new roman",15),bg="lightgrey")
        trans_quantity_given.place(x=155,y=220,width=185,height=30)

        def calculation_function():
            trans_total_rent['state'] = 'normal'
            trans_total_rent.delete(0,END)
            trans_rent_given.delete(0,END)
            if trans_quantity_given.get() == "":
                messagebox.showerror("Error","Please enter quantity to calculate...")
                trans_quantity_given.focus_set()
            else:
                total = int(trans_rental_price.get()) * int(trans_quantity_given.get())
                trans_total_rent.insert(0,total)
                if total == 0:
                    trans_rent_given.insert(0,0)
                trans_rent_given.focus_set()
                trans_total_rent['state'] = 'readonly'

        btn_calc = Button(transaction_frame,text="Calc",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=calculation_function).place(x=355,y=220,width=100,height=30)

        trans_total_rent_lbl = Label(transaction_frame,text="Total Rent :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        trans_total_rent_lbl.place(x=30,y=270)

        trans_total_rent = Entry(transaction_frame,font=("times new roman",15),bg="lightgrey")
        trans_total_rent.place(x=155,y=270,width=300,height=30)


        trans_lbl_rent_given = Label(transaction_frame,text="Rent paid :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        trans_lbl_rent_given.place(x=30,y=320)

        trans_rent_given = Entry(transaction_frame,font=("times new roman",15),bg="lightgrey")
        trans_rent_given.place(x=155,y=320,width=300,height=30)

        trans_lbl_returned_status = Label(transaction_frame,text="Status :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        trans_lbl_returned_status.place(x=30,y=370)

        trans_returned_status = Entry(transaction_frame,font=("times new roman",15),bg="lightgrey")
        trans_returned_status.place(x=155,y=370,width=300,height=30)
        trans_returned_status.insert(0,"Not Returned")
        trans_returned_status['state'] = 'readonly'

        make_trans_entries_readonly()

        def procced_request():
            global proceed_book_id
            global proceed_cust_id
            global customer_search
            global book_search
            make_trans_entries_normal()
            if customer_search == 1 and book_search == 1:
                trans_total_rent.delete(0,END)
                trans_rent_given.delete(0,END)
                trans_cust_entry_id.insert(0,proceed_cust_id)
                trans_book_entry_id.insert(0,proceed_book_id)
                trans_rental_price.insert(0,entry_price.get())
                if (entry_price.get() == '0'):
                    trans_total_rent.insert(0,0)
                    trans_rent_given.insert(0,0)
                    trans_total_rent['state'] = 'readonly'
                    trans_rent_given['state'] = 'readonly'


                trans_cust_entry_id['state'] = 'readonly'
                trans_book_entry_id['state'] = 'readonly'
                trans_rental_price['state'] = 'readonly'
                trans_total_rent['state'] = 'readonly'

            elif customer_search == 0 and book_search == 0:
                messagebox.showerror("Error","Both Customer and book details are not searched yet...")
            elif customer_search == 0:
                messagebox.showerror("Error","Customer details are not searched yet...")
            elif book_search == 0:
                messagebox.showerror("Error","Book details are not searched yet...")

        btn_proceed = Button(book_frame,text="Proceed",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=procced_request).place(x=180,y=470,width=120)

        def book_allocation():
            global entry_customer
            global book_entry
            global customer_search
            global book_search

            if customer_search == 1 and book_search == 1:
                trans_total_rent['state'] = 'normal'
                total_rent = trans_total_rent.get()
                trans_total_rent['state'] = 'readonly'
                if entry_quantity.get() == '0':
                    messagebox.showerror("Error",'Book is out of stock, please select another book...')
                elif trans_quantity_given.get() == "":
                    messagebox.showerror("Error","Please enter quantity to be given...")
                elif int(entry_quantity.get()) < int(trans_quantity_given.get()):
                    messagebox.showerror("Error","Allocating quantity is greater than the stock we have...please check...")
                elif total_rent == "":
                    messagebox.showerror("Error",'Please calculate the total...')
                elif trans_rent_given.get() == "":
                    messagebox.showerror("Error",'Please enter the amount paid by customer...')
                else:
                    cust_trans_id = trans_cust_entry_id.get()
                    book_trans_id = trans_book_entry_id.get()
                    allocate_trans_date = trans_allocate_date.get()
                    rental_trans_price = trans_rental_price.get()
                    quantity_trans_given = trans_quantity_given.get()
                    rent_trans_paid = trans_rent_given.get()
                    status_trans = 'Not Returned'

                    try:
                        mysql_connect()

                        mycursor = mydb.cursor()

                        sql = "Select * from transactions where cust_id = %s and book_id = %s and return_status = %s"

                        val = (cust_trans_id,book_trans_id,status_trans)

                        mycursor.execute(sql,val)
                
                        myresult = mycursor.fetchall()

                        if len(myresult)>0:
                            messagebox.showwarning("Error",f"Same customer have a same book which is not returned yet, Allocated Date = {myresult[0][2]}...")
                        else:
                            quantity_update = int(entry_quantity.get()) - int(trans_quantity_given.get())
                            sql_update = "update book_details set book_quantity = %s where book_id = %s"

                            values = (quantity_update,book_trans_id)

                            # print(values)

                            mycursor.execute(sql_update,values)

                            mydb.commit()

                            # print(mycursor.rowcount, "record inserted")
                            # messagebox.showinfo("Successfull","quantity updated...")


                            sql_query = "insert into transactions (cust_id,book_id,allocate_date,rental_price,quantity_given,total_rent,rent_given,return_status,day_diff,due_amount,return_date) values (%s,%s,%s,%s,%s,%s,%s,%s,'0','0','0')"

                            values = (cust_trans_id,book_trans_id,allocate_trans_date,rental_trans_price,quantity_trans_given,total_rent,rent_trans_paid,status_trans)

                            mycursor.execute(sql_query,values)

                            mydb.commit()

                            # print(mycursor.rowcount, "record inserted")
                            messagebox.showinfo("Successfull","Book allocated successfully...")

                            
                            make_cust_entries_normal()
                            make_book_entries_normal()
                            make_trans_entries_normal()
                            
                            entry_customer.empty_entry()
                            book_entry.empty_entry()
                            
                            make_trans_entries_empty()
                            empty_cust_entries()
                            empty_book_entries()

                            
                            trans_quantity_given.delete(0,END)
                    except Exception as e:
                        messagebox.showerror("Error",f"Error in transaction frame line 1507 {e}")
            else:
                messagebox.showerror("Error","Customer or book details are not searched yet...")
            
        def close_allocation():
            global allocate_book_count
            allocate_book_count = 0
            customer_details_frame.destroy()
            book_frame.destroy()
            transaction_frame.destroy()
            main_frame.destroy()
        
        btn_close_allocation = Button(transaction_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_allocation).place(x=270,y=470,width=120)

        btn_allocate = Button(transaction_frame,text="Allocate",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=book_allocation).place(x=120,y=470,width=120)
    else:
        pass

allocate_book.add_command(label='Allocate Book',compound= LEFT,accelerator='Ctrl + A',command=allocate_book_page)
####################################################### Allocate book page ##############################################################

####################################################### Return book page ##############################################################
due_days = 0
due_amount_calc = 0
return_customer_search = 0
return_book_search = 0
global entry_customer_return
return_book_count = 0
proceed_cust_return_id = 0
proceed_book_return_id = 0
def return_book_page(event=None):
    global due_days
    global due_amount_calc
    global proceed_cust_return_id
    global proceed_book_return_id
    global return_customer_search
    global return_book_search
    global entry_customer_return
    global return_book_count
    if return_book_count == 0:
        return_book_count = 1

        main_frame = LabelFrame(win,text = 'Return Book...')
        main_frame.place(x = 250, y = 30,width = 1000, height = 650)
        bg_color = Label(main_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        #############################   customer frame ##################################

        customer_details_frame = LabelFrame(main_frame,text = 'Select customer by id or name...')
        customer_details_frame.place(x = 0, y = 0,width = 500, height = 620)
        bg_color = Label(customer_details_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        entry_customer_return = AutocompleteEntry(327, 158, customer_details_frame,font=("times new roman",15),bg = "lightgrey")
        entry_customer_return.place(x=75,y=60,width=240,height=35)
        entry_customer_return['state'] = 'readonly'

        lbl_name_cust = Label(customer_details_frame,text="Customer Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        lbl_name_cust.place(x=75,y=100)

        entry_cust_name = Entry(customer_details_frame,font=("times new roman",15),bg="lightgrey")
        entry_cust_name.place(x=75,y=130,width=350,height=35)

        lbl_address_cust = Label(customer_details_frame,text="Customer Address :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=170)

        entry_cust_address = Entry(customer_details_frame,font=("times new roman",15),bg="lightgrey")
        entry_cust_address.place(x=75,y=200,width=350,height=35)

        lbl_phone_cust = Label(customer_details_frame,text="Mobile Number :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=240)

        entry_cust_phone = Entry(customer_details_frame,font=("times new roman",15),bg="lightgrey")
        entry_cust_phone.place(x=75,y=270,width=350,height=35)

        lbl_prof_cust = Label(customer_details_frame,text="Customer Proffession :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=310)

        entry_cust_prof = Entry(customer_details_frame,font=("times new roman",15),bg="lightgrey")
        entry_cust_prof.place(x=75,y=340,width=350,height=35)

        lbl_aadhar_cust = Label(customer_details_frame,text="Aadhar number :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=380)

        entry_cust_aadhar = Entry(customer_details_frame,font=("times new roman",15),bg="lightgrey")
        entry_cust_aadhar.place(x=75,y=410,width=350,height=35)

        lbl_book_allocated = Label(customer_details_frame,text="Allocated books :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=450)

        book_allocated = ttk.Combobox(customer_details_frame,font=("times new roman",15))
        book_allocated['values'] = ('Select Book',)
        book_allocated.current(0)
        book_allocated.place(x=75,y=480,width=350,height=35)
        book_allocated['state'] = 'readonly'

        lbl_select_option = Label(customer_details_frame,text="Select Option :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=520)

        combo_select_option = ttk.Combobox(customer_details_frame,font=("times new roman",15))
        combo_select_option['values'] = ('Select Option','Return','Re-allocate')
        combo_select_option.current(0)
        combo_select_option.place(x=75,y=550,width=220,height=35)
        combo_select_option['state'] = 'readonly'

        def option_customer_selected():
            global return_customer_search
            global entry_customer_return

            make_return_entry_normal()
            quantity_returned['state'] = 'normal'
            empty_return_boxes()
            quantity_returned['state'] = 'readonly'
            make_return_entry_readonly()
            
            # make_trans_entries_normal()
            # make_trans_entries_empty()
            # make_trans_entries_readonly()

            return_customer_search = 0

            make_cust_entries_normal()

            empty_cust_entries()
            make_cust_entries_readonly()

            entry_customer_return.focus_set()
            entry_customer_return['state'] = "normal"

            entry_customer_return.empty_entry()
            if var.get() == 1:
                lbl_name_cust['text'] = "Customer Name :"
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select cust_id from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                lista = []
                for x in myresult:
                    lista.append(x[0])
                
                mycursor.close()

                entry_customer_return.get_list(lista)
                # print(lista)
            else:
                lbl_name_cust['text'] = "Customer Id :"
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select cust_name from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                listb = []
                for x in myresult:
                    listb.append(x[0])

                mycursor.close()
                
                entry_customer_return.get_list(listb)
                # print(listb)
                
        var = IntVar()
        Radio_customer_id = Radiobutton(customer_details_frame, text="Search by ID", variable=var, value=1,bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=option_customer_selected)
        Radio_customer_id.place(x = 60,y = 10)

        Radio_customer_name = Radiobutton(customer_details_frame, text="Search by Name",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red", variable=var, value=2,command=option_customer_selected)
        Radio_customer_name.place(x = 250,y = 10)

        ############################### search button ###########################################
        def fetch_customer_details():
            global proceed_cust_return_id
            global return_customer_search
            if entry_customer_return.get() == "":
                messagebox.showwarning("Warning","Please enter id or name for search...")
            else:
                if var.get() == 1:
                    customer_id = entry_customer_return.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select c.cust_id,c.cust_name,c.cust_address,c.cust_mobile,c.cust_profession,c.cust_aadhar,b.book_name from customer_details c inner join transactions t on c.cust_id = t.cust_id inner join book_details b on b.book_id = t.book_id where c.cust_id = %s and t.return_status='Not Returned';"
                    val = (customer_id,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        
                        make_return_entry_normal()
                        quantity_returned['state'] = 'normal'
                        empty_return_boxes()
                        quantity_returned['state'] = 'readonly'
                        make_return_entry_readonly()

                        make_cust_entries_normal()

                        empty_cust_entries()

                        entry_customer_return.lb_destroy()
                        proceed_cust_return_id = entry_customer_return.get()

                        entry_cust_name.insert(0,myresult[0][1])
                        entry_cust_address.insert(0,myresult[0][2])
                        entry_cust_phone.insert(0,myresult[0][3])
                        entry_cust_prof.insert(0,myresult[0][4])
                        entry_cust_aadhar.insert(0,myresult[0][5])

                        l = ['Select Book']
                        for i in myresult:
                            l.append(i[-1])
                        
                        book_allocated['values'] = tuple(l)
                        book_allocated.current(0)

                        return_customer_search = 1

                        make_cust_entries_readonly()
                    else:
                        messagebox.showerror("Error","Customer not have any book...")
                        entry_customer_return.empty_entry()
                        empty_cust_entries()

                    mycursor.close()
                else:
                    customer_name = entry_customer_return.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select c.cust_id,c.cust_name,c.cust_address,c.cust_mobile,c.cust_profession,c.cust_aadhar,b.book_name from customer_details c inner join transactions t on c.cust_id = t.cust_id inner join book_details b on b.book_id = t.book_id where c.cust_name = %s and t.return_status='Not Returned';"
                    val = (customer_name,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        make_cust_entries_normal()
                        
                        empty_cust_entries()
                        
                        entry_customer_return.lb_destroy()

                        proceed_cust_return_id = myresult[0][0]

                        entry_cust_name.insert(0,myresult[0][0])
                        entry_cust_address.insert(0,myresult[0][2])
                        entry_cust_phone.insert(0,myresult[0][3])
                        entry_cust_prof.insert(0,myresult[0][4])
                        entry_cust_aadhar.insert(0,myresult[0][5])
                        return_customer_search = 1

                        l = ['Select Book']
                        for i in myresult:
                            l.append(i[-1])
                        
                        book_allocated['values'] = tuple(l)
                        book_allocated.current(0)

                        return_customer_search = 1

                        make_cust_entries_readonly()
                    else:
                        messagebox.showerror("Error","Customer not found, Please enter valid Customer Name...")
                        entry_customer_return.empty_entry()
                        empty_cust_entries()

        btn_customer_search = Button(customer_details_frame,text="Fetch",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=fetch_customer_details).place(x=325,y=60,width=100)

        def make_cust_entries_readonly():
            entry_customer_return['state'] = 'readonly'
            entry_cust_name['state'] = 'readonly'
            entry_cust_address['state'] = 'readonly'
            entry_cust_phone['state'] = 'readonly'
            entry_cust_prof['state'] = 'readonly'
            entry_cust_aadhar['state'] = 'readonly'
            book_allocated['state'] = 'readonly'
            combo_select_option['state'] = 'readonly'

        def make_cust_entries_normal():
            entry_customer_return['state'] = 'normal'
            entry_cust_name['state'] = 'normal'
            entry_cust_address['state'] = 'normal'
            entry_cust_phone['state'] = 'normal'
            entry_cust_prof['state'] = 'normal'
            entry_cust_aadhar['state'] = 'normal'
            book_allocated['state'] = 'normal'
            combo_select_option['state'] = 'normal'

        def empty_cust_entries():
            entry_cust_name.delete(0,END)
            entry_cust_address.delete(0,END)
            entry_cust_prof.delete(0,END)
            entry_cust_phone.delete(0,END)
            entry_cust_aadhar.delete(0,END)
            book_allocated.delete(0,END)
            book_allocated['values'] = ('Select Book',)
            book_allocated.current(0)
            combo_select_option.current(0)

        make_cust_entries_readonly()
    
        return_frame = LabelFrame(main_frame,text = 'Return Dtails...')
        return_frame.place(x = 500, y = 0,width = 495, height = 620)
        bg_color = Label(return_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        return_cust_id = Label(return_frame,text="Customer Id :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        return_cust_id.place(x=30,y=20)

        return_cust_entry_id = Entry(return_frame,font=("times new roman",15),bg="lightgrey")
        return_cust_entry_id.place(x=175,y=20,width=280,height=30)

        return_book_id = Label(return_frame,text="Book Id :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        return_book_id.place(x=30,y=60)

        return_book_entry_id = Entry(return_frame,font=("times new roman",15),bg="lightgrey")
        return_book_entry_id.place(x=175,y=60,width=280,height=30)

        return_allocate_date_lbl = Label(return_frame,text="Allocated on :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        return_allocate_date_lbl.place(x=30,y=100)

        return_allocate_date = Entry(return_frame,font=("times new roman",15),bg="lightgrey")
        return_allocate_date.place(x=175,y=100,width=280,height=30)

        return_lbl_retnal_price = Label(return_frame,text="Rental Price :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        return_lbl_retnal_price.place(x=30,y=140)

        return_rental_price = Entry(return_frame,font=("times new roman",15),bg="lightgrey")
        return_rental_price.place(x=175,y=140,width=280,height=30)

        return_lbl_quantity = Label(return_frame,text="Quantity :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        return_lbl_quantity.place(x=30,y=180)

        return_quantity_given = Entry(return_frame,font=("times new roman",15),bg="lightgrey")
        return_quantity_given.place(x=175,y=180,width=280,height=30)

        return_lbl_total_rent = Label(return_frame,text="Total rent :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        return_lbl_total_rent.place(x=30,y=220)

        return_total_rent = Entry(return_frame,font=("times new roman",15),bg="lightgrey")
        return_total_rent.place(x=175,y=220,width=280,height=30)

        return_lbl_rent_given = Label(return_frame,text="Rent given :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        return_lbl_rent_given.place(x=30,y=260)

        return_rent_given = Entry(return_frame,font=("times new roman",15),bg="lightgrey")
        return_rent_given.place(x=175,y=260,width=280,height=30)

        return_lbl_balance = Label(return_frame,text="Balance :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        return_lbl_balance.place(x=30,y=300)

        return_balance = Entry(return_frame,font=("times new roman",15),bg="lightgrey")
        return_balance.place(x=175,y=300,width=280,height=30)

        return_lbl_day_due = Label(return_frame,text="Due days :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        return_lbl_day_due.place(x=30,y=340)

        return_day_due = Entry(return_frame,font=("times new roman",15),bg="lightgrey")
        return_day_due.place(x=175,y=340,width=280,height=30)

        return_lbl_total_amount = Label(return_frame,text="Total Amount :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        return_lbl_total_amount.place(x=30,y=380)

        return_total_amount = Entry(return_frame,font=("times new roman",15),bg="lightgrey")
        return_total_amount.place(x=175,y=380,width=280,height=30)

        return_amount_paying_lbl = Label(return_frame,text="Pay amount :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        return_amount_paying_lbl.place(x=30,y=420)

        return_amount_paying = Entry(return_frame,font=("times new roman",15),bg="lightgrey")
        return_amount_paying.place(x=175,y=420,width=280,height=30)

        return_lbl_quantity = Label(return_frame,text="Return Quantity:",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        return_lbl_quantity.place(x=30,y=460)

        quantity_returned = Entry(return_frame,font=("times new roman",15),bg="lightgrey")
        quantity_returned.place(x=175,y=460,width=280,height=30)

        date_returned = Label(return_frame,text="Select Date :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        date_returned.place(x=30,y=500)
        
        return_date = DateEntry(return_frame,date_pattern='yyyy/mm/dd',font=("times new roman",15))
        return_date.place(x=175,y=500,width=280,height=30)

        def get_details():
            global due_amount_calc
            global return_customer_search
            global proceed_cust_return_id
            global due_days
            if return_customer_search == 1:
            
                book_selected = book_allocated.get()
                
                if book_selected == 'Select Book':
                    messagebox.showerror("Error",'please select book...')
                elif combo_select_option.get() == 'Select Option':
                    messagebox.showerror("Error",'Please select option to perform...')
                else:
                    mysql_connect()

                    mycursor = mydb.cursor()

                    sql = "select b.book_id,t.allocate_date,t.rental_price,t.quantity_given, t.total_rent,t.rent_given,t.total_rent-t.rent_given as balance, datediff(curdate(),t.allocate_date) as due_date from book_details b inner join transactions t on b.book_id = t.book_id where b.book_name = %s and t.cust_id = %s and t.return_status = 'Not Returned';"

                    val = (book_selected,proceed_cust_return_id)

                    mycursor.execute(sql,val)

                    myresult = mycursor.fetchall()

                    if len(myresult)>0:
                        
                        make_return_entry_normal()
                        quantity_returned['state'] = 'normal'
                        empty_return_boxes()

                        due_days = int(myresult[0][7])

                        if due_days >= 10 and combo_select_option.get() == "Re-allocate":
                            messagebox.showerror("Error","These books have due amount, you have to return these books...")
                        else:
                            return_cust_entry_id.insert(0,proceed_cust_return_id)
                            return_book_entry_id.insert(0,myresult[0][0])    
                            return_allocate_date.insert(0,myresult[0][1])
                            return_rental_price.insert(0,myresult[0][2])
                            return_quantity_given.insert(0,myresult[0][3])
                            return_total_rent.insert(0,myresult[0][4])
                            return_rent_given.insert(0,myresult[0][5])
                            return_balance.insert(0,myresult[0][6])
                            return_day_due.insert(0,myresult[0][7])

                            
                            more_days = due_days - 10
                            due_amount_calc = more_days * 10

                            if myresult[0][7] >=10:
                                
                                balance_amount = int(myresult[0][6])
                                
                                total_amount = due_amount_calc + balance_amount

                                return_total_amount.insert(0,total_amount)
                            else:
                                return_total_amount.insert(0,myresult[0][6])

                                # print(due_amount_calc)
                                # print(myresult[0][6])
                            
                            if myresult[0][3] == 1:
                                quantity_returned.insert(0,1)
                                quantity_returned['state'] = 'readonly'
                            else:
                                quantity_returned['state'] = 'normal'
                            
                            make_return_entry_readonly()  
                            quantity_returned['state'] = 'readonly'        
                    else:
                        messagebox.showerror("Error","Book details not found...")
            else:
                messagebox.showerror("Error",'Please search customer details first...')

        def make_return_entry_readonly():
            return_cust_entry_id['state'] = 'readonly'
            return_book_entry_id['state'] = 'readonly'
            return_allocate_date['state'] = 'readonly'
            return_rental_price['state'] = 'readonly'
            return_quantity_given['state'] = 'readonly'
            return_total_rent['state'] = 'readonly'
            return_rent_given['state'] = 'readonly'
            return_balance['state'] = 'readonly'
            return_day_due['state'] = 'readonly'
            return_total_amount['state'] = 'readonly'
        
        def make_return_entry_normal():
            return_cust_entry_id['state'] = 'normal'
            return_book_entry_id['state'] = 'normal'
            return_allocate_date['state'] = 'normal'
            return_rental_price['state'] = 'normal'
            return_quantity_given['state'] = 'normal'
            return_total_rent['state'] = 'normal'
            return_rent_given['state'] = 'normal'
            return_balance['state'] = 'normal'
            return_day_due['state'] = 'normal'
            return_total_amount['state'] = 'normal'


        def empty_return_boxes():
            return_cust_entry_id.delete(0,END)
            return_book_entry_id.delete(0,END)
            return_allocate_date.delete(0,END)
            return_rental_price.delete(0,END)
            return_quantity_given.delete(0,END)
            return_total_rent.delete(0,END)
            return_rent_given.delete(0,END)
            return_balance.delete(0,END)
            return_day_due.delete(0,END)
            return_total_amount.delete(0,END)
            quantity_returned.delete(0,END)
            return_amount_paying.delete(0,END)
            quantity_returned.delete(0,END)

        def return_procedure():
            global return_customer_search
            global due_days
            global due_amount_calc
            global proceed_cust_return_id

            if return_customer_search == 1:
                if return_amount_paying.get() == "":
                    messagebox.showerror("Error","Please Enter amount to pay...")
                elif quantity_returned.get() == "":
                    messagebox.showerror("Error",f"Please enter quantity for {combo_select_option.get()}")
                else:
                    if combo_select_option.get() == 'Return':
                        if int(return_amount_paying.get()) > int(return_total_amount.get()):
                            messagebox.showerror("Error","Please enter appropriate price...")
                        elif int(return_quantity_given.get()) == int(quantity_returned.get()) and (int(return_total_amount.get()) > int(return_amount_paying.get())):
                            messagebox.showerror('Error','You have to pay full amount...')
                        elif int(return_quantity_given.get()) == int(quantity_returned.get()) and (int(return_total_amount.get()) == int(return_amount_paying.get())):
                            if return_amount_paying.get() < return_total_amount.get():
                                messagebox.showerror("Error","You must have to pay full amount...")
                            else:
                                book_id = return_book_entry_id.get()
                                if due_days >=10:
                                    update_total_rent = int(return_total_rent.get()) + due_amount_calc
                                else:
                                    due_amount_calc = 0
                                    update_total_rent = int(return_total_rent.get())

                                update_rent_given = int(return_rent_given.get()) + int(return_total_amount.get())
                                update_return_date = return_date.get()

                                try:
                                    mysql_connect()

                                    mycursor = mydb.cursor()

                                    sql_query = "update transactions set total_rent = %s, rent_given = %s, return_status = %s, day_diff = %s , due_amount = %s, return_date = %s where cust_id = %s and book_id = %s and return_status = %s"

                                    values = (update_total_rent,update_rent_given,'Returned',due_days,due_amount_calc,update_return_date,proceed_cust_return_id,book_id,'Not Returned')
                                    # print(values)

                                    mycursor.execute(sql_query,values)

                                    mydb.commit()

                                    # print(mycursor.rowcount, "record inserted")
                                    messagebox.showinfo("Successfull","Book Returned successfully...")

                                    make_return_entry_normal()
                                    quantity_returned['state'] = 'normal'
                                    empty_return_boxes()
                                    quantity_returned['state'] = 'readonly'
                                    make_return_entry_readonly()

                                    mycursor.close()
                                except Exception as e:
                                    messagebox.showerror("Error",f"line 2053 {e}")

                        elif int(return_quantity_given.get()) > int(quantity_returned.get()):       # taken 2 books Returning 1 book
                            if due_days <=10:
                                min_amount = int(quantity_returned.get()) * int(return_rental_price.get())

                                if min_amount > (int(return_rent_given.get()) + int(return_amount_paying.get())):
                                    messagebox.showwarning("Warning",f'You must have to pay minimum {min_amount - int(return_rent_given.get())} Rs.')
                                elif min_amount == (int(return_rent_given.get()) + int(return_amount_paying.get())):
                                    if due_amount_calc < 0:
                                        due_amount_calc = 0
                                    total_rent_equal = int(quantity_returned.get()) * int(return_rental_price.get())
                                    rent_given_equal = total_rent_equal
                                    return_date_equal = return_date.get()
                                    book_id_equal = return_book_entry_id.get()

                                    new_quantity = int(return_quantity_given.get()) - int(quantity_returned.get())
                                    new_total_rent_equal = new_quantity * int(return_rental_price.get())

                                    try:
                                        mysql_connect()

                                        mycursor = mydb.cursor()

                                        sql_query = "update transactions set total_rent = %s,quantity_given = %s, rent_given = %s, return_status = %s, day_diff = %s , due_amount = %s, return_date = %s where cust_id = %s and book_id = %s and return_status = %s"

                                        values = (total_rent_equal,quantity_returned.get(),rent_given_equal,'Returned',due_days,due_amount_calc,return_date_equal,proceed_cust_return_id,book_id_equal,'Not Returned')
                                        # print(values)

                                        mycursor.execute(sql_query,values)

                                        mydb.commit()

                                        # print(mycursor.rowcount, "record inserted")

                                        

                                        insert_sql_query = "insert into transactions (cust_id,book_id,allocate_date,rental_price,quantity_given,total_rent,rent_given,return_status,day_diff,due_amount,return_date) values (%s,%s,%s,%s,%s,%s,%s,%s,'0','0','0')"

                                        val = (proceed_cust_return_id,book_id_equal,return_allocate_date.get(),return_rental_price.get(),new_quantity,new_total_rent_equal,0,'Not Returned')

                                        mycursor.execute(insert_sql_query,val)

                                        mydb.commit()

                                        messagebox.showinfo("Successfull","Book Returned successfully...")

                                        make_return_entry_normal()
                                        quantity_returned['state'] = 'normal'
                                        empty_return_boxes()
                                        quantity_returned['state'] = 'readonly'
                                        make_return_entry_readonly()

                                        mycursor.close()


                                        ### test the code first then go forward
                                    except Exception as e:
                                        messagebox.showerror("Error",f"line 2111 {e}")

                                    # equal then complete 1st recodrd and balance one book fees in second record
                                
                                elif min_amount < (int(return_rent_given.get()) + int(return_amount_paying.get())):
                                    # messagebox.showwarning("warn",'less')
                                    if due_amount_calc < 0:
                                        due_amount_calc = 0

                                    total_rent_less = int(quantity_returned.get()) * int(return_rental_price.get()) # 1 * 300 = 300

                                    rent_given_less = total_rent_less                                               # 300 bec. 1st book payment complete
                                    return_date_less = return_date.get()
                                    book_id_less = return_book_entry_id.get()                                       # B1001

                                    new_quantity = int(return_quantity_given.get()) - int(quantity_returned.get())  # 3 - 1 = 2
                                    new_total_rent_less = new_quantity * int(return_rental_price.get())             # 1 * 300 = 300

                                    try:
                                        mysql_connect()

                                        mycursor = mydb.cursor()

                                        sql_query = "update transactions set total_rent = %s,quantity_given = %s, rent_given = %s, return_status = %s, day_diff = %s , due_amount = %s, return_date = %s where cust_id = %s and book_id = %s and return_status = %s"

                                        values = (total_rent_less,quantity_returned.get(),rent_given_less,'Returned',due_days,due_amount_calc,return_date_less,proceed_cust_return_id,book_id_less,'Not Returned')
                                        # print(values)

                                        mycursor.execute(sql_query,values)

                                        mydb.commit()

                                        # print(mycursor.rowcount, "record inserted")

                                        balance_payment_allocation = (int(return_rent_given.get()) + int(return_amount_paying.get())) - total_rent_less   #  300 + 200 - 300 (200)                                        # = 

                                        insert_sql_query = "insert into transactions (cust_id,book_id,allocate_date,rental_price,quantity_given,total_rent,rent_given,return_status,day_diff,due_amount,return_date) values (%s,%s,%s,%s,%s,%s,%s,%s,'0','0','0')"

                                        val = (proceed_cust_return_id,book_id_less,return_allocate_date.get(),return_rental_price.get(),new_quantity,new_total_rent_less,balance_payment_allocation,'Not Returned')

                                        mycursor.execute(insert_sql_query,val)

                                        mydb.commit()

                                        messagebox.showinfo("Successfull","Book Returned successfully...")

                                        make_return_entry_normal()
                                        quantity_returned['state'] = 'normal'
                                        empty_return_boxes()
                                        quantity_returned['state'] = 'readonly'
                                        make_return_entry_readonly()
                                        

                                        mycursor.close()


                                        ### test the code first then go forward
                                    except Exception as e:
                                        messagebox.showerror("Error",f"line 2169 {e}")
                                    # 500 dile -- 300 price ahe --> 300 1st return complete and 200 amount add to 2nd record
                            else:
                                messagebox.showerror("Error","You have to return all the books as due days exceeds...")
                        else:
                            messagebox.showerror("Error","Something went wrong...")
                    elif combo_select_option.get() == 'Re-allocate':
                        if due_days >= 10:
                            messagebox.showerror("Error","You have to simply return this books because these books are having due amount...")
                        elif int(return_quantity_given.get()) > int(quantity_returned.get()):
                            messagebox.showerror("Error",'You can Re-allocate all the books, or return unwanted no. of books and then Re-allocate...')
                        elif int(return_quantity_given.get()) < int(quantity_returned.get()):
                            messagebox.showerror("Error",'Please enter the appropriate quantity...')
                        elif int(return_total_amount.get()) ==  int(return_amount_paying.get()):
                            if due_amount_calc < 0:
                                due_amount_calc = 0

                            total_rent_equal = int(return_total_rent.get())
                            rent_given_equal = total_rent_equal
                            return_date_equal = return_date.get()
                            book_id_equal = return_book_entry_id.get()

                            new_quantity = int(quantity_returned.get())
                            new_total_rent_equal = new_quantity * int(return_rental_price.get())

                            try:
                                mysql_connect()

                                mycursor = mydb.cursor()

                                sql_query = "update transactions set total_rent = %s,quantity_given = %s, rent_given = %s, return_status = %s, day_diff = %s , due_amount = %s, return_date = %s where cust_id = %s and book_id = %s and return_status = %s"

                                values = (total_rent_equal,quantity_returned.get(),rent_given_equal,'Returned',due_days,due_amount_calc,return_date_equal,proceed_cust_return_id,book_id_equal,'Not Returned')
                                # print(values)

                                mycursor.execute(sql_query,values)

                                mydb.commit()

                                # print(mycursor.rowcount, "record inserted")

                                

                                insert_sql_query = "insert into transactions (cust_id,book_id,allocate_date,rental_price,quantity_given,total_rent,rent_given,return_status,day_diff,due_amount,return_date) values (%s,%s,%s,%s,%s,%s,%s,%s,'0','0','0')"

                                val = (proceed_cust_return_id,book_id_equal,return_date.get(),return_rental_price.get(),new_quantity,new_total_rent_equal,0,'Not Returned')

                                mycursor.execute(insert_sql_query,val)

                                mydb.commit()

                                messagebox.showinfo("Successfull","Book Re-allocated successfully...")

                                make_return_entry_normal()
                                quantity_returned['state'] = 'normal'
                                empty_return_boxes()
                                quantity_returned['state'] = 'readonly'
                                make_return_entry_readonly()

                                mycursor.close()

                            except Exception as e:
                                messagebox.showerror("Error",f"line 2231 {e}")

                        elif int(return_total_amount.get()) < int(return_amount_paying.get()):
                            if due_amount_calc < 0:
                                due_amount_calc = 0

                            total_rent_equal = int(return_total_rent.get())
                            rent_given_equal = total_rent_equal
                            return_date_equal = return_date.get()
                            book_id_equal = return_book_entry_id.get()

                            new_quantity = int(quantity_returned.get())
                            new_total_rent_equal = new_quantity * int(return_rental_price.get())

                            rent_given_less = (int(return_rent_given.get()) + int(return_amount_paying.get())) - int(return_total_rent.get())

                            try:
                                mysql_connect()

                                mycursor = mydb.cursor()

                                sql_query = "update transactions set total_rent = %s,quantity_given = %s, rent_given = %s, return_status = %s, day_diff = %s , due_amount = %s, return_date = %s where cust_id = %s and book_id = %s and return_status = %s"

                                values = (total_rent_equal,quantity_returned.get(),rent_given_equal,'Returned',due_days,due_amount_calc,return_date_equal,proceed_cust_return_id,book_id_equal,'Not Returned')
                                # print(values)

                                mycursor.execute(sql_query,values)

                                mydb.commit()

                                # print(mycursor.rowcount, "record inserted")

                                

                                insert_sql_query = "insert into transactions (cust_id,book_id,allocate_date,rental_price,quantity_given,total_rent,rent_given,return_status,day_diff,due_amount,return_date) values (%s,%s,%s,%s,%s,%s,%s,%s,'0','0','0')"

                                val = (proceed_cust_return_id,book_id_equal,return_date.get(),return_rental_price.get(),new_quantity,new_total_rent_equal,rent_given_less,'Not Returned')

                                mycursor.execute(insert_sql_query,val)

                                mydb.commit()

                                messagebox.showinfo("Successfull","Book Re-allocated successfully...")

                                make_return_entry_normal()
                                quantity_returned['state'] = 'normal'
                                empty_return_boxes()
                                quantity_returned['state'] = 'readonly'
                                make_return_entry_readonly()

                                mycursor.close()

                            except Exception as e:
                                messagebox.showerror("Error",f"line 2284 {e}")

                        elif int(return_total_amount.get()) > int(return_amount_paying.get()):
                            messagebox.showerror("Error","You have to pay full amount...")
            else:
                messagebox.showerror("Error","Please get customer details first")

        def close_return_page():
            global return_book_count
            return_book_count = 0
            customer_details_frame.destroy()
            return_frame.destroy()
            main_frame.destroy()
            

        make_return_entry_readonly()

        btn_book_proceed = Button(customer_details_frame,text="Get Details",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=get_details).place(x=305,y=550,width=120)

        btn_close_return = Button(return_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_return_page).place(x=270,y=550,width=120)

        btn_return_book = Button(return_frame,text="Return",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=return_procedure).place(x=120,y=550,width=120)

allocate_book.add_command(label='Return Book',compound= LEFT,accelerator='Ctrl + R',command= return_book_page)                          

######################################### book details #######################################

book_details = Menu(main_menu,tearoff=False)                                             # creating menu

####################################################### New Book Page ##############################################################

newBook_count = 0
def new_book(event=None):
    global newBook_count
    if newBook_count == 0:
        newBook_count = 1

        newBook = LabelFrame(win,text = 'Add Book Details...')
        newBook.place(x = 500, y = 50,width = 500, height = 600)
        bg_color = Label(newBook,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl_book_id = Label(newBook,text="Book id :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=10)

        book_id = Entry(newBook,font=("times new roman",15),bg="lightgrey")
        book_id.place(x=75,y=40,width=350,height=35)
        #############
        mysql_connect()

        mycursor = mydb.cursor()

        mycursor.execute("select * from book_details")

        myresult = mycursor.fetchall()

        book_id.insert(0, "B" + str(int(myresult[-1][0][1:])+1))
        #############
        book_id['state'] = 'readonly'
        

        lbl_book_name = Label(newBook,text="Enter Book Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=80)

        book_name = Entry(newBook,font=("times new roman",15),bg="lightgrey")
        book_name.place(x=75,y=110,width=350,height=35)
        book_name.focus_set()

        lbl_auth_name = Label(newBook,text="Enter Auther Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=150)

        auth_name = Entry(newBook,font=("times new roman",15),bg="lightgrey")
        auth_name.place(x=75,y=180,width=350,height=35)

        lbl_paid_unpaid = Label(newBook,text="Select option :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=220)

        paid_unpaid = ttk.Combobox(newBook,font=("times new roman",15))
        paid_unpaid['values'] = ('Select Option','Paid','Unpaid')
        paid_unpaid.current(0)
        paid_unpaid.place(x=75,y=250,width=350,height=35)
        paid_unpaid['state'] = 'readonly'

        lbl_price = Label(newBook,text="Enter Custom price :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=290)

        book_price = Entry(newBook,font=("times new roman",15),bg="lightgrey")
        book_price.place(x=75,y=320,width=350,height=35)

        lbl_book_entry = Label(newBook,text="Select Date of entry :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=360)

        # cust_dob = Calendar(newCustomer,font=("times new roman",15),bg="lightgrey",selectmode = 'day', year = 2021, month = 3, day = 12)
        book_entry_date = DateEntry(newBook,date_pattern='mm/dd/yyyy',font=("times new roman",15),bg="lightgrey",fg="lightgrey")
        book_entry_date.place(x=75,y=390,width=350,height=35)

        lbl_quantity = Label(newBook,text="Enter quantity of books :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=430)

        book_quantity = Entry(newBook,font=("times new roman",15),bg="lightgrey")
        book_quantity.place(x=75,y=460,width=350,height=35)

        def book_entry():
            id = book_id.get()
            name = book_name.get()
            author = auth_name.get()
            pdud = paid_unpaid.get()
            price = book_price.get()
            doe = book_entry_date.get_date()
            quan = book_quantity.get()

            if id == "" and name == "" and author == "" and pdud == "Select Option" and price == "" and doe == "" and quan == "":
                messagebox.showwarning("Warning","Please fill all the fields...")
                book_id.focus_set()
            elif id == "":
                messagebox.showwarning("Warning","something went wrong please try again later...")
                book_id.focus_set()
            elif name == "":
                messagebox.showwarning("Warning","Please enter the name...")
                book_name.focus_set()
            elif author == "":
                messagebox.showwarning("Warning","Please enter author name...")
                auth_name.focus_set()
            elif pdud == "Select Option":
                messagebox.showwarning("Warning","Please select any one option...")
                cust_phone.focus_set()
            elif price == "":
                messagebox.showwarning("Warning","Please enter price...")
                book_price.focus_set()
            elif doe == "":
                messagebox.showwarning("Warning","Please select doe...")
            elif quan == "":
                messagebox.showwarning("Warning","Please enter quantity of books...")
                book_quantity.focus_set()
            elif pdud == "Paid" and int(price) < 1:
                messagebox.showwarning("Warning","please enter appropriate price...")
            elif pdud == "Unpaid" and int(price) > 0:
                    messagebox.showwarning("Warning","Please enter zero as your selected book as UnPaid...")
            else:
                mysql_connect()

                mycursor = mydb.cursor()

                sql_query = "insert into book_details (book_id,book_name,auther_name,paid_unpaid,custom_price,book_doe,book_quantity) values (%s,%s,%s,%s,%s,%s,%s)"

                values = (id,name,author,pdud,price,doe,quan)

                mycursor.execute(sql_query,values)

                mydb.commit()

                # print(mycursor.rowcount, "record inserted")
                messagebox.showinfo("Successfull","Book registered successfully...")

                book_id['state'] = 'normal'

                book_id.delete(0,'end')
                book_name.delete(0,'end')
                book_name.focus_set()
                auth_name.delete(0,'end')
                paid_unpaid.current(0)
                book_price.delete(0,'end')
                book_quantity.delete(0,'end')

                mysql_connect()

                mycursor = mydb.cursor()

                mycursor.execute("select * from book_details")

                myresult = mycursor.fetchall()

                book_id.insert(0,"B" + str(int(myresult[-1][0][1:])+1))

                book_id['state'] = 'readonly'


        def close_book_func():
            global newBook_count
            newBook_count = 0
            newBook.destroy()

        btn_book_entry = Button(newBook,text="Register",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=book_entry).place(x=110,y=520,width=120)

        btn_book_cancel = Button(newBook,text="Cancel",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_book_func).place(x=260,y=520,width=120)
    else:
        pass

book_details.add_command(label='New book',compound=LEFT,accelerator='Alt + N',command=new_book)

####################################################### End New Book Page ##############################################################

####################################################### Update book Page ##############################################################

update_book_count = 0
entry_book = 0
def update_book(event=None):
    global entry_book
    global update_book_count
    if update_book_count == 0:
        update_book_count = 1

        updatebook = LabelFrame(win,text = 'Add Book Details to update...')
        updatebook.place(x = 500, y = 50,width = 500, height = 600)
        bg_color = Label(updatebook,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        entry_book = AutocompleteEntry(575, 160, updatebook,font=("times new roman",15),bg = "lightgrey")
        entry_book.place(x=75,y=60,width=270,height=35)
        entry_book['state'] = 'readonly'

        lbl_update_name = Label(updatebook,text="Book Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        lbl_update_name.place(x=75,y=100)

        book_update_name = Entry(updatebook,font=("times new roman",15),bg="lightgrey")
        book_update_name.place(x=75,y=130,width=350,height=35) 
        book_update_name.focus_set()

        lbl_update_auth_name = Label(updatebook,text="Auther Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=170)

        book_update_auth_name = Entry(updatebook,font=("times new roman",15),bg="lightgrey")
        book_update_auth_name.place(x=75,y=200,width=350,height=35)

        lbl_update_paid_unpaid = Label(updatebook,text="Select Option :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=240)

        paid_unpaid = ttk.Combobox(updatebook,font=("times new roman",15))
        paid_unpaid['values'] = ('Select Option','Paid','Unpaid')
        paid_unpaid.current(0)
        paid_unpaid.place(x=75,y=270,width=350,height=35)
        paid_unpaid['state'] = 'readonly'

        lbl_update_price = Label(updatebook,text="Custom Price :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=310)

        book_update_price = Entry(updatebook,font=("times new roman",15),bg="lightgrey")
        book_update_price.place(x=75,y=340,width=350,height=35)

        lbl_update_dob = Label(updatebook,text="Date of entry :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=380)

        # cust_dob = Calendar(newCustomer,font=("times new roman",15),bg="lightgrey",selectmode = 'day', year = 2021, month = 3, day = 12)
        book_update_doe = DateEntry(updatebook,date_pattern='mm/dd/yyyy',font=("times new roman",15),bg="lightgrey",fg="lightgrey")
        book_update_doe.place(x=75,y=410,width=350,height=35)

        lbl_update_quantity = Label(updatebook,text="Quantity :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=450)

        book_update_quantity = Entry(updatebook,font=("times new roman",15),bg="lightgrey")
        book_update_quantity.place(x=75,y=480,width=350,height=35)

        def option_selected():
            book_update_name.delete(0,END)
            book_update_auth_name.delete(0,END)
            paid_unpaid.current(0)
            book_update_price.delete(0,END)
            book_update_doe.delete(0,END)
            book_update_quantity.delete(0,END)
            
            global entry_book
            entry_book.focus_set()
            entry_book['state'] = "normal"
            entry_book.empty_entry()

            if var.get() == 1:
                lbl_update_name['text'] = "Book Name :"
                
                mysql_connect()

                mycursor = mydb.cursor()
                
                sql = "select book_id from book_details where book_id not in ('B1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                
                # myresult = [('D1001',),('D1002',)]

                lista = []
                for x in myresult:          #   x = ('B1001',)  
                    lista.append(x[0])      #   x[0] = 'B1001'
                
                mycursor.close()

                entry_book.get_list(lista)       # ['B1001','B1002']
                # print(lista)
            else:
                lbl_update_name['text'] = "Book Id :"
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select book_name from book_details where book_id not in ('B1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                listb = []
                for x in myresult:
                    listb.append(x[0])

                mycursor.close()
                
                entry_book.get_list(listb)
                # print(listb)
                
        var = IntVar()
        R1 = Radiobutton(updatebook, text="Search by ID", variable=var, value=1,bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=option_selected)
        R1.place(x = 60,y = 10)

        R2 = Radiobutton(updatebook, text="Search by Name",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red", variable=var, value=2,command=option_selected)
        R2.place(x = 250,y = 10)

        ############################### search button ###########################################
        def fetch_details():
            if entry_book.get() == "":           # id or name text box
                messagebox.showwarning("Warning","Please enter id or name for search...")
            else:
                if var.get() == 1:
                    update_id = entry_book.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from book_details where book_id = %s"
                    val = (update_id,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        book_update_name.delete(0,END)
                        book_update_auth_name.delete(0,END)
                        paid_unpaid.current(0)
                        book_update_price.delete(0,END)
                        book_update_doe.delete(0,END)
                        book_update_quantity.delete(0,END)

                        entry_book.lb_destroy()
                        book_update_name.insert(0,myresult[0][1])
                        book_update_auth_name.insert(0,myresult[0][2])
                        if myresult[0][3] == "Paid":
                            paid_unpaid.current(1)
                        else:
                            paid_unpaid.current(2)
                        book_update_price.insert(0,myresult[0][4])
                        book_update_doe.insert(0,myresult[0][5])
                        book_update_quantity.insert(0,myresult[0][6])
                    else:
                        messagebox.showerror("Error","Book not found, Please enter valid book Id...")
                        entry_book.empty_entry()
                        book_update_name.delete(0,END)
                        book_update_auth_name.delete(0,END)
                        paid_unpaid.current(0)
                        book_update_price.delete(0,END)
                        book_update_doe.delete(0,END)
                        book_update_quantity.delete(0,END)
                    mycursor.close()
                else:
                    update_name = entry_book.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from book_details where book_name = %s"
                    val = (update_name,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        book_update_name.delete(0,END)
                        book_update_auth_name.delete(0,END)
                        paid_unpaid.current(0)
                        book_update_price.delete(0,END)
                        book_update_doe.delete(0,END)
                        book_update_quantity.delete(0,END)

                        entry_book.lb_destroy()
                        book_update_name.insert(0,myresult[0][0])
                        book_update_auth_name.insert(0,myresult[0][2])
                        if myresult[0][3] == "Paid":
                            paid_unpaid.current(1)
                        else:
                            paid_unpaid.current(2)
                        book_update_price.insert(0,myresult[0][4])
                        book_update_doe.insert(0,myresult[0][5])
                        book_update_quantity.insert(0,myresult[0][6])
                    else:
                        messagebox.showerror("Error","Book not found, Please enter valid book Name...")
                        entry_book.empty_entry()
                        book_update_name.delete(0,END)
                        book_update_auth_name.delete(0,END)
                        paid_unpaid.current(0)
                        book_update_price.delete(0,END)
                        book_update_doe.delete(0,END)
                        book_update_quantity.delete(0,END)

        btn_update_search = Button(updatebook,text="Fetch",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=fetch_details).place(x=355,y=60,width=100)

        def update_book_details():
            update_id = 0
            update_name = 0
            if var.get() == 1:
                update_id = entry_book.get()
                update_name = book_update_name.get()
            else:
                update_id = book_update_name.get()
                update_name = entry_book.get()
            update_auth_name = book_update_auth_name.get()
            pdud = paid_unpaid.get()
            update_price = book_update_price.get()
            update_doe = book_update_doe.get()
            update_quantity = book_update_quantity.get()
          
            if update_id == "" and update_name == "" and update_auth_name == "" and pdud == "Select Option" and update_price == "" and update_doe == "" and update_quantity == "":
                messagebox.showwarning("Warning","Please fill all the fields...")
                entry_book.focus_set()
            elif update_id == "":
                messagebox.showwarning("Warning","Please enter book id...")
                book_update_name.focus_set()
            elif update_name == "":
                messagebox.showwarning("Warning","Please enter the name...")
                book_update_name.focus_set()
            elif update_auth_name == "":
                messagebox.showwarning("Warning","Please enter auther name...")
                book_update_auth_name.focus_set()
            elif pdud == "Select Option":
                messagebox.showwarning("Warning","Please selece any one option...")
                paid_unpaid.focus_set()
            elif update_price == "":
                messagebox.showwarning("Warning","Please enter price...")
                book_update_price.focus_set()
            elif update_doe == "":
                messagebox.showwarning("Warning","Please select doe...")
            elif update_quantity == "":
                messagebox.showwarning("Warning","Please enter quantity...")
                book_update_quantity.focus_set()
            elif pdud == "Paid" and int(update_price) < 1:
                messagebox.showwarning("Warning","please enter appropriate price...")
            elif pdud == "Unpaid" and int(update_price) > 0:
                    messagebox.showwarning("Warning","Please enter zero as your selected book is UnPaid...")
            else:
                try:
                    mysql_connect()

                    mycursor = mydb.cursor()

                    sql_query = "update book_details set book_id = %s, book_name = %s, auther_name = %s, paid_unpaid = %s, custom_price = %s, book_doe = %s, book_quantity = %s where book_id = %s"

                    values = (update_id,update_name,update_auth_name,pdud,update_price,update_doe,update_quantity,update_id)

                    # print(values)
                    mycursor.execute(sql_query,values)

                    mydb.commit()

                    # print(mycursor.rowcount, "record inserted")
                    messagebox.showinfo("Successfull","Book information updated successfully...")
                    
                    entry_book.empty_entry()
                    entry_book.focus_set()
                    book_update_name.delete(0,END)
                    book_update_auth_name.delete(0,END)
                    paid_unpaid.current(0)
                    book_update_price.delete(0,END)
                    book_update_doe.delete(0,END)
                    book_update_quantity.delete(0,END)

                    mycursor.close()
                except Exception as e:
                    messagebox.showerror("Error",e)

        def close_update_func():
            global entry_book
            global update_book_count
            update_book_count = 0
            entry_book.empty_entry()
            updatebook.destroy()

        btn_update = Button(updatebook,text="Update",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=update_book_details).place(x=110,y=530,width=120)

        btn_update_cancel = Button(updatebook,text="Cancel",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_update_func).place(x=260,y=530,width=120)
    else:
        pass

book_details.add_command(label='Update book',compound=LEFT,accelerator='Alt + U',command=update_book)    

######################################## End Update Book ####################################

####################################################### Delete book Page ##############################################################

delete_book_count = 0
entry_delete_book = 0
def delete_book(event=None):
    global entry_delete_book
    global delete_book_count
    
    if delete_book_count == 0:
        delete_book_count = 1

        deletebook = LabelFrame(win,text = 'Select customer by id or name to delete...')
        deletebook.place(x = 500, y = 50,width = 500, height = 600)
        bg_color = Label(deletebook,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        entry_delete_book = AutocompleteEntry(575, 160, deletebook,font=("times new roman",15),bg = "lightgrey")
        entry_delete_book.place(x=75,y=60,width=270,height=35)
        entry_delete_book['state'] = 'readonly'

        lbl_delete_name = Label(deletebook,text="Book Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        lbl_delete_name.place(x=75,y=100)

        book_delete_name = Entry(deletebook,font=("times new roman",15),bg="lightgrey")
        book_delete_name.place(x=75,y=130,width=350,height=35)
        book_delete_name.focus_set()

        lbl_delete_auth_name = Label(deletebook,text="Auther Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=170)

        book_delete_auth_name = Entry(deletebook,font=("times new roman",15),bg="lightgrey")
        book_delete_auth_name.place(x=75,y=200,width=350,height=35)

        lbl_delete_pdud = Label(deletebook,text="Select option :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=240)

        paid_unpaid = ttk.Combobox(deletebook,font=("times new roman",15))
        paid_unpaid['values'] = ('Select Option','Paid','Unpaid')
        paid_unpaid.current(0)
        paid_unpaid.place(x=75,y=270,width=350,height=35)
        paid_unpaid['state'] = 'readonly'

        lbl_delete_price = Label(deletebook,text="Custom Price :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=310)

        book_delete_price = Entry(deletebook,font=("times new roman",15),bg="lightgrey")
        book_delete_price.place(x=75,y=340,width=350,height=35)

        lbl_delete_dob = Label(deletebook,text="Date of entry :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=380)

        # cust_dob = Calendar(newCustomer,font=("times new roman",15),bg="lightgrey",selectmode = 'day', year = 2021, month = 3, day = 12)
        book_delete_doe = DateEntry(deletebook,date_pattern='mm/dd/yyyy',font=("times new roman",15),bg="lightgrey",fg="lightgrey")
        book_delete_doe.place(x=75,y=410,width=350,height=35)

        lbl_update_quantity = Label(deletebook,text="Quantity :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=450)

        book_delete_quantity = Entry(deletebook,font=("times new roman",15),bg="lightgrey")
        book_delete_quantity.place(x=75,y=480,width=350,height=35)

        def option_selected():
            book_delete_name.delete(0,END)
            book_delete_auth_name.delete(0,END)
            paid_unpaid.current(0)
            book_delete_price.delete(0,END)
            book_delete_price.delete(0,END)
            book_delete_quantity.delete(0,END)
            
            global entry_delete_book
            entry_delete_book.focus_set()
            entry_delete_book['state'] = "normal"
            entry_delete_book.empty_entry()

            if var.get() == 1:
                lbl_delete_name['text'] = "Book Name :"
                
                mysql_connect()

                mycursor = mydb.cursor()
                
                sql = "select book_id from book_details where book_id not in ('B1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                
                # myresult = [('D1001',),('D1002',)]

                lista = []
                for x in myresult:          #   x = ('B1001',)  
                    lista.append(x[0])      #   x[0] = 'B1001'
                
                mycursor.close()

                entry_delete_book.get_list(lista)       # ['B1001','B1002']
                # print(lista)
            else:
                lbl_delete_name['text'] = "Book Id :"
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select book_name from book_details where book_id not in ('B1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                listb = []
                for x in myresult:
                    listb.append(x[0])

                mycursor.close()
                
                entry_delete_book.get_list(listb)
                # print(listb)
                
        var = IntVar()
        R1 = Radiobutton(deletebook, text="Search by ID", variable=var, value=1,bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=option_selected)
        R1.place(x = 60,y = 10)

        R2 = Radiobutton(deletebook, text="Search by Name",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red", variable=var, value=2,command=option_selected)
        R2.place(x = 250,y = 10)

        ############################### search button ###########################################
        def fetch_details():
            if entry_delete_book.get() == "":           # id or name text box
                messagebox.showwarning("Warning","Please enter id or name for search...")
            else:
                if var.get() == 1:
                    update_id = entry_delete_book.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from book_details where book_id = %s"
                    val = (update_id,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        book_delete_name.delete(0,END)
                        book_delete_auth_name.delete(0,END)
                        paid_unpaid.current(0)
                        book_delete_price.delete(0,END)
                        book_delete_doe.delete(0,END)
                        book_delete_quantity.delete(0,END)

                        entry_delete_book.lb_destroy()
                        book_delete_name.insert(0,myresult[0][1])
                        book_delete_auth_name.insert(0,myresult[0][2])
                        if myresult[0][3] == "Paid":
                            paid_unpaid.current(1)
                        else:
                            paid_unpaid.current(2)
                        book_delete_price.insert(0,myresult[0][4])
                        book_delete_doe.insert(0,myresult[0][5])
                        book_delete_quantity.insert(0,myresult[0][6])
                    else:
                        messagebox.showerror("Error","Book not found, Please enter valid Book Id...")
                        entry_delete_book.empty_entry()
                        book_delete_name.delete(0,END)
                        book_delete_auth_name.delete(0,END)
                        paid_unpaid.current(0)
                        book_delete_price.delete(0,END)
                        book_delete_doe.delete(0,END)
                        book_delete_quantity.delete(0,END)
                    mycursor.close()
                else:
                    update_name = entry_delete_book.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from book_details where book_name = %s"
                    val = (update_name,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        book_delete_name.delete(0,END)
                        book_delete_auth_name.delete(0,END)
                        paid_unpaid.current(0)
                        book_delete_price.delete(0,END)
                        book_delete_doe.delete(0,END)
                        book_delete_quantity.delete(0,END)

                        entry_delete_book.lb_destroy()
                        book_delete_name.insert(0,myresult[0][0])
                        book_delete_auth_name.insert(0,myresult[0][2])
                        if myresult[0][3] == "Paid":
                            paid_unpaid.current(1)
                        else:
                            paid_unpaid.current(2)
                        book_delete_price.insert(0,myresult[0][4])
                        book_delete_doe.insert(0,myresult[0][5])
                        book_delete_quantity.insert(0,myresult[0][6])
                    else:
                        messagebox.showerror("Error","Book not found, Please enter valid Book Name...")
                        entry_delete_book.empty_entry()
                        book_delete_name.delete(0,END)
                        book_delete_auth_name.delete(0,END)
                        paid_unpaid.current(0)
                        book_delete_price.delete(0,END)
                        book_delete_doe.delete(0,END)
                        book_delete_quantity.delete(0,END)

        btn_delete_search = Button(deletebook,text="Fetch",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=fetch_details).place(x=355,y=60,width=100)

        def delete_book_details():
            delete_id = 0
            delete_name = 0
            if var.get() == 1:
                delete_id = entry_delete_book.get()
                delete_name = book_delete_name.get()
            else:
                delete_id = book_delete_name.get()
                delete_name = entry_delete_book.get()
            
            if delete_id == "" and delete_name == "":
                messagebox.showerror("Error","Sorry !!! we didn't get your id or name...")
                entry_delete_book.focus_set()
            else:
                try:
                    mysql_connect()

                    mycursor = mydb.cursor()

                    sql_query = "delete from book_details where book_id = %s and book_name = %s"

                    values = (delete_id,delete_name)

                    mycursor.execute(sql_query,values)

                    mydb.commit()

                    # print(mycursor.rowcount, "record inserted")
                    messagebox.showinfo("Successfull","Book record deleted successfully...")

                    entry_delete_book.empty_entry()
                    entry_delete_book.focus_set()
                    book_delete_name.delete(0,END)
                    book_delete_auth_name.delete(0,END)
                    paid_unpaid.current(0)
                    book_delete_price.delete(0,END)
                    book_delete_doe.delete(0,END)
                    book_delete_quantity.delete(0,END)
                except Exception as e:
                    messagebox.showerror("Error","something went wrong while transaction with database, kindly call developer...")

        def close_delete_func():
            global entry_delete_book
            entry_delete_book.empty_entry()
            global delete_book_count
            delete_book_count = 0
            deletebook.destroy()

        btn_delete_book = Button(deletebook,text="Delete",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=delete_book_details).place(x=110,y=530,width=120)

        btn_delete_book_cancel = Button(deletebook,text="Cancel",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_delete_func).place(x=260,y=530,width=120)
    else:
        pass


book_details.add_command(label='Delete book',compound=LEFT,accelerator='Alt + D',command=delete_book)      

####################################################### Delete book Page ##############################################################

####################################################### In stock book Page ##############################################################

in_stock_count = 0
def in_stock_page():
    global in_stock_count
    if in_stock_count == 0:
        in_stock_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "In Stock Books", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Book Id','Book Name','Auther Name','Paid / Unpaid','Price','Date of Entry','Stock Quantity')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center")
            my_tree.heading(col,text = col)

        for col in cols:
            my_tree.column(col,anchor = "center",width=140)
            my_tree.heading(col,text = col)
        
        try:

            mysql_connect()

            mycursor = mydb.cursor()

            sql = "Select * from book_details where book_quantity > 0 and book_id not in ('B1000')"

            mycursor.execute(sql)

            myresult = mycursor.fetchall()

            for id,name,auther_name,pdud,price,doe,quantity in myresult:
                    # print(id, name, address,mobile,profession,dob,aadhar)
                my_tree.insert("","end",values=(id, name, auther_name,pdud,price,doe,quantity))
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_in_stock_page():
            global in_stock_count
            in_stock_count = 0
            tree_frame.destroy()
            # my_tree.destroy()
            # tree_scroll.destroy()
            # btn_close.destroy()
                  

        btn_close_in_stock = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_in_stock_page).place(x=450,y=555,width=120)
    else:
        pass

book_details.add_separator()
book_details.add_command(label='In Stock books',compound=LEFT,command=in_stock_page)  

####################################################### End IN stock book Page ##############################################################

####################################################### Out of stock book Page ##############################################################

out_of_stock_count = 0
def out_of_stock_page():
    global out_of_stock_count
    if out_of_stock_count == 0:
        out_of_stock_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "Out of Stock Books", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Book Id','Book Name','Auther Name','Paid / Unpaid','Price','Date of Entry','Stock Quantity')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center")
            my_tree.heading(col,text = col)

        for col in cols:
            my_tree.column(col,anchor = "center",width=140)
            my_tree.heading(col,text = col)
        
        try:

            mysql_connect()

            mycursor = mydb.cursor()

            sql = "Select * from book_details where book_quantity < 1 and book_id not in ('B1000')"

            mycursor.execute(sql)

            myresult = mycursor.fetchall()

            for id,name,auther_name,pdud,price,doe,quantity in myresult:
                    # print(id, name, address,mobile,profession,dob,aadhar)
                my_tree.insert("","end",values=(id, name, auther_name,pdud,price,doe,quantity))
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_out_of_stock_page():
            global out_of_stock_count
            out_of_stock_count = 0
            tree_frame.destroy()
            # my_tree.destroy()
            # tree_scroll.destroy()
            # btn_close.destroy()
                  

        btn_close_out_of_stock = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_out_of_stock_page).place(x=450,y=555,width=120)
    else:
        pass

book_details.add_command(label='Out of Stock books',compound=LEFT,command=out_of_stock_page)       

####################################################### End out of stock book Page ##############################################################

####################################################### paid book stock Page ##############################################################

paid_book_stock_count = 0
def paid_book_stock_page():
    global paid_book_stock_count
    if paid_book_stock_count == 0:
        paid_book_stock_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "In Stock Paid Books", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Book Id','Book Name','Auther Name','Paid / Unpaid','Price','Date of Entry','Stock Quantity')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center")
            my_tree.heading(col,text = col)

        for col in cols:
            my_tree.column(col,anchor = "center",width=140)
            my_tree.heading(col,text = col)
        
        try:

            mysql_connect()

            mycursor = mydb.cursor()

            sql = "Select * from book_details where book_quantity > 0 and book_id not in ('B1000') and paid_unpaid = 'paid'"

            mycursor.execute(sql)

            myresult = mycursor.fetchall()

            for id,name,auther_name,pdud,price,doe,quantity in myresult:
                    # print(id, name, address,mobile,profession,dob,aadhar)
                my_tree.insert("","end",values=(id, name, auther_name,pdud,price,doe,quantity))
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_paid_book_stock_page():
            global paid_book_stock_count
            paid_book_stock_count = 0
            tree_frame.destroy()                  

        btn_close_paid_stock = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_paid_book_stock_page).place(x=450,y=555,width=120)
    else:
        pass


book_details.add_separator()
book_details.add_command(label='In stock paid books',compound=LEFT,command=paid_book_stock_page)     

####################################################### End paid book stock Page ##############################################################

####################################################### paid book out of stock Page ##############################################################

paid_book_out_of_stock_count = 0
def paid_book_out_of_stock_page():
    global paid_book_out_of_stock_count
    if paid_book_out_of_stock_count == 0:
        paid_book_out_of_stock_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "Out of Stock Paid Books", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Book Id','Book Name','Auther Name','Paid / Unpaid','Price','Date of Entry','Stock Quantity')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center")
            my_tree.heading(col,text = col)

        for col in cols:
            my_tree.column(col,anchor = "center",width=140)
            my_tree.heading(col,text = col)
        
        try:

            mysql_connect()

            mycursor = mydb.cursor()

            sql = "Select * from book_details where book_quantity < 1 and book_id not in ('B1000') and paid_unpaid = 'paid'"

            mycursor.execute(sql)

            myresult = mycursor.fetchall()

            for id,name,auther_name,pdud,price,doe,quantity in myresult:
                    # print(id, name, address,mobile,profession,dob,aadhar)
                my_tree.insert("","end",values=(id, name, auther_name,pdud,price,doe,quantity))
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_paid_book_out_of_stock_page():
            global paid_book_out_of_stock_count
            paid_book_out_of_stock_count = 0
            tree_frame.destroy()                  

        btn_close_paid_stock = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_paid_book_out_of_stock_page).place(x=450,y=555,width=120)
    else:
        pass

book_details.add_command(label='Out of stock paid books',compound=LEFT,command=paid_book_out_of_stock_page)

####################################################### End paid book stock Page ##############################################################

####################################################### in stock unpaid Page ##############################################################

in_stock_unpaid_count = 0
def in_stock_unpaid_page():
    global in_stock_unpaid_count
    if in_stock_unpaid_count == 0:
        in_stock_unpaid_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "In stock unpaid books", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Book Id','Book Name','Auther Name','Paid / Unpaid','Price','Date of Entry','Stock Quantity')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center")
            my_tree.heading(col,text = col)

        for col in cols:
            my_tree.column(col,anchor = "center",width=140)
            my_tree.heading(col,text = col)
        
        try:

            mysql_connect()

            mycursor = mydb.cursor()

            sql = "Select * from book_details where book_quantity > 0 and book_id not in ('B1000') and paid_unpaid = 'Unpaid'"

            mycursor.execute(sql)

            myresult = mycursor.fetchall()

            for id,name,auther_name,pdud,price,doe,quantity in myresult:
                    # print(id, name, address,mobile,profession,dob,aadhar)
                my_tree.insert("","end",values=(id, name, auther_name,pdud,price,doe,quantity))
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_in_stock_unpaid():
            global in_stock_unpaid_count
            in_stock_unpaid_count = 0
            tree_frame.destroy()                  

        btn_close_unpaid = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_in_stock_unpaid).place(x=450,y=555,width=120)
    else:
        pass


book_details.add_separator()
book_details.add_command(label='In stock Unpaid books',compound=LEFT,command=in_stock_unpaid_page)       

####################################################### out of stock unpaid books ##############################################################

out_stock_unpaid_count = 0
def out_stock_unpaid_page():
    global out_stock_unpaid_count
    if out_stock_unpaid_count == 0:
        out_stock_unpaid_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "Out of stock unpaid books", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Book Id','Book Name','Auther Name','Paid / Unpaid','Price','Date of Entry','Stock Quantity')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center")
            my_tree.heading(col,text = col)

        for col in cols:
            my_tree.column(col,anchor = "center",width=140)
            my_tree.heading(col,text = col)
        
        try:

            mysql_connect()

            mycursor = mydb.cursor()

            sql = "Select * from book_details where book_quantity < 1 and book_id not in ('B1000') and paid_unpaid = 'Unpaid'"

            mycursor.execute(sql)

            myresult = mycursor.fetchall()

            for id,name,auther_name,pdud,price,doe,quantity in myresult:
                    # print(id, name, address,mobile,profession,dob,aadhar)
                my_tree.insert("","end",values=(id, name, auther_name,pdud,price,doe,quantity))
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_out_stock_unpaid():
            global out_stock_unpaid_count
            out_stock_unpaid_count = 0
            tree_frame.destroy()                  

        btn_close_out_unpaid = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_out_stock_unpaid).place(x=450,y=555,width=120)
    else:
        pass

book_details.add_command(label='Out of stock Unpaid books',compound=LEFT,command=out_stock_unpaid_page)       
####################################################### End out of stock unpaid books ##############################################################

####################################################### All books ##############################################################

view_all_book_count = 0
def view_all_book_page(event=None):
    global view_all_book_count
    if view_all_book_count == 0:
        view_all_book_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "All Books", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Book Id','Book Name','Auther Name','Paid / Unpaid','Price','Date of Entry','Stock Quantity')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center")
            my_tree.heading(col,text = col)

        try:

            mysql_connect()

            mycursor = mydb.cursor()

            sql = "Select * from book_details where book_id not in ('B1000')"

            mycursor.execute(sql)

            myresult = mycursor.fetchall()

            for id,name,auther_name,pdud,price,doe,quantity in myresult:
                    # print(id, name, address,mobile,profession,dob,aadhar)
                my_tree.insert("","end",values=(id, name, auther_name,pdud,price,doe,quantity))
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_view_all_book_page():
            global view_all_book_count
            view_all_book_count = 0
            tree_frame.destroy()                  

        btn_close_all_book = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_view_all_book_page).place(x=450,y=555,width=120)
    else:
        pass


book_details.add_separator()
book_details.add_command(label='All books',compound=LEFT,accelerator='Ctrl+Alt+B',command=view_all_book_page)  

####################################################### End All books ##############################################################

######################################## End Book Details ####################################
# Allocate Details

allocate_details = Menu(main_menu,tearoff=False)

####################################################### Between Date Allocated ##############################################################

bet_date_alloc_count = 0
def bet_date_alloc_page(event=None):
    global bet_date_alloc_count
    if bet_date_alloc_count == 0:
        bet_date_alloc_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        # lbl = Label(tree_frame,text = "Between Selected dates", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        lbl = Label(tree_frame,text="Select dates :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        lbl.place(x=100,y=10,width=130,height=35)

        date_entry1 = DateEntry(tree_frame,date_pattern='yyyy/mm/dd',font=("times new roman",15),bg="lightgrey",fg="lightgrey")
        date_entry1.place(x=250,y=10,width=250,height=35)

        date_entry2 = DateEntry(tree_frame,date_pattern='yyyy/mm/dd',font=("times new roman",15),bg="lightgrey",fg="lightgrey")
        date_entry2.place(x=510,y=10,width=250,height=35)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Cust Id','Cust Name','Book Id','Book Name','Quantity Given','Total Rent','Date Allocated')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        def get_details():
            # print(*my_tree.get_children())
            my_tree.delete(*my_tree.get_children())     # clear treeview

            date1 = date_entry1.get()
            date2 = date_entry2.get()

            if date1 == "" and date2 =="":
                messagebox.showerror("Error","Please select dates...")
            else:
                for col in cols:
                    my_tree.column(col,anchor = "center",width=140)
                    my_tree.heading(col,text = col)
                
                try:
                    mysql_connect()

                    mycursor = mydb.cursor()

                    sql = "select t.cust_id,c.cust_name,t.book_id,b.book_name,t.quantity_given,t.total_rent,t.allocate_date from transactions t inner join customer_details c on t.cust_id = c.cust_id inner join book_details b on t.book_id = b.book_id where allocate_date between %s and %s and return_status = 'Not Returned';"

                    values = (date1,date2)

                    mycursor.execute(sql,values)

                    myresult = mycursor.fetchall()
                    
                    if len(myresult) > 0:
                        for cust_id,cust_name,book_id,book_name,quantity,total_rent,allocate_date in myresult:
                                # print(id, name, address,mobile,profession,dob,aadhar)
                            my_tree.insert("","end",values=(cust_id,cust_name, book_id, book_name, quantity, total_rent,allocate_date))
                    else:
                        messagebox.showerror("Error","No Records found...")
                
                    mycursor.close()
                except Exception as e:
                    messagebox.showerror("Error",e)

        btn_get_data = Button(tree_frame,text="View Records",bg="lightblue",font=("Goudy old style",12,"bold"),fg="red",command=get_details).place(x=790,y=12,width=120,height=32)

        def close_bet_date_page():
            global bet_date_alloc_count
            bet_date_alloc_count = 0
            tree_frame.destroy()                  

        btn_close_all_book = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_bet_date_page).place(x=450,y=555,width=120)
    else:
        pass


allocate_details.add_command(label='Between Date',compound=LEFT,command=bet_date_alloc_page)

####################################################### End Between Date Allocated ##############################################################

####################################################### Date Due page ##############################################################

date_due_count = 0
def date_due_page(event=None):
    global date_due_count
    if date_due_count == 0:
        date_due_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "Date Due", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Cust Name','Book Id','Book Name','Quantity Given','Mobile Number','Date Allocated','Due Days')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center",width=140)
            my_tree.heading(col,text = col)

        try:
            mysql_connect()

            mycursor = mydb.cursor()

            sql = "select c.cust_name,t.book_id,b.book_name,t.quantity_given,c.cust_mobile,t.allocate_date, datediff(curdate(),t.allocate_date) from transactions t inner join customer_details c on t.cust_id = c.cust_id inner join book_details b on t.book_id = b.book_id where datediff(curdate(),t.allocate_date) >= 10 and t.return_status = 'Not Returned';"

            mycursor.execute(sql)

            myresult = mycursor.fetchall()
            
            if len(myresult)>0:
                for cust_name,book_id,book_name,quantity,total_rent,allocate_date,due_days in myresult:
                    my_tree.insert("","end",values=(cust_name, book_id, book_name, quantity, total_rent,allocate_date,due_days))
            else:
                messagebox.showerror("Error","No records found...")
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_due_date_page():
            global date_due_count
            date_due_count = 0
            tree_frame.destroy()                  

        btn_close_all_book = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_due_date_page).place(x=450,y=555,width=120)
    else:
        pass

allocate_details.add_command(label='Date Due',compound=LEFT,command=date_due_page)

############################################# End Date Due page #######################################################################

################################################ Allocated Paid books #################################################################

allocated_paid_book_count = 0
def allocated_paid_book_page(event=None):
    global allocated_paid_book_count
    if allocated_paid_book_count == 0:
        allocated_paid_book_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "Allocated Paid Books", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Cust Name','Book Name','Quantity Given','Rental Price','Rent Given','Date Allocated','Due Days')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center",width=140)
            my_tree.heading(col,text = col)

        try:
            mysql_connect()

            mycursor = mydb.cursor()

            sql = "select c.cust_name,b.book_name,t.quantity_given,t.rental_price,t.rent_given,t.allocate_date, datediff(curdate(),t.allocate_date) from transactions t inner join customer_details c on t.cust_id = c.cust_id inner join book_details b on t.book_id = b.book_id where t.rental_price > 0 and t.return_status = 'Not Returned';" 

            mycursor.execute(sql)

            myresult = mycursor.fetchall()
            
            if len(myresult)>0:
                for cust_name,book_name,quantity,total_rent,rent_given,allocate_date,due_days in myresult:
                    my_tree.insert("","end",values=(cust_name, book_name, quantity, total_rent, rent_given, allocate_date,due_days))
            else:
                messagebox.showerror("Error","No records found...")
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_paid_book_allocated():
            global allocated_paid_book_count
            allocated_paid_book_count = 0
            tree_frame.destroy()                  

        btn_close_all_book = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_paid_book_allocated).place(x=450,y=555,width=120)
    else:
        pass

allocate_details.add_separator()
allocate_details.add_command(label='Paid books',compound=LEFT,command=allocated_paid_book_page)

################################################# End allocated paid books ########################################################

################################################# End allocated unpaid books ########################################################
allocated_unpaid_book_count = 0
def allocated_unpaid_book_page(event=None):
    global allocated_unpaid_book_count
    if allocated_unpaid_book_count == 0:
        allocated_unpaid_book_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "Allocated UnPaid Books", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Cust Name','Book Name','Quantity Given','Rental Price','Rent Given','Date Allocated','Due Days')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center",width=140)
            my_tree.heading(col,text = col)

        try:
            mysql_connect()

            mycursor = mydb.cursor()

            sql = "select c.cust_name,b.book_name,t.quantity_given,t.rental_price,t.rent_given,t.allocate_date, datediff(curdate(),t.allocate_date) from transactions t inner join customer_details c on t.cust_id = c.cust_id inner join book_details b on t.book_id = b.book_id where t.rental_price = 0 and t.return_status = 'Not Returned';" 

            mycursor.execute(sql)

            myresult = mycursor.fetchall()
            
            if len(myresult)>0:
                for cust_name,book_name,quantity,total_rent,rent_given,allocate_date,due_days in myresult:
                    my_tree.insert("","end",values=(cust_name, book_name, quantity, total_rent, rent_given, allocate_date,due_days))
            else:
                messagebox.showerror("Error","No records found...")
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_unpaid_book_allocated():
            global allocated_unpaid_book_count
            allocated_unpaid_book_count = 0
            tree_frame.destroy()                  

        btn_close_all_book = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_unpaid_book_allocated).place(x=450,y=555,width=120)
    else:
        pass

allocate_details.add_command(label='UnPaid books',compound=LEFT,command=allocated_unpaid_book_page)

################################################### End unpaid books ####################################################################

################################################### To Customer page ####################################################################

to_customer_count = 0
entry_to_customer = 0
def to_customer_page(event=None):
    global entry_to_customer
    global to_customer_count
    if to_customer_count == 0:
        to_customer_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        # lbl = Label(tree_frame,text = "Between Selected dates", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        entry_to_customer = AutocompleteEntry(700, 95, tree_frame,font=("times new roman",15),bg = "lightgrey")
        entry_to_customer.place(x=450,y=10,width=270,height=35)
        entry_to_customer['state'] = 'readonly'

        def option_to_customer_selected():
            global entry_to_customer
            entry_to_customer.focus_set()
            entry_to_customer['state'] = "normal"
            entry_to_customer.empty_entry()

            if var.get() == 1:
                mysql_connect()

                mycursor = mydb.cursor()
                
                sql = "select cust_id from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                
                # myresult = [('D1001',),('D1002',)]

                lista = []
                for x in myresult:          #   x = ('B1001',)  
                    lista.append(x[0])      #   x[0] = 'B1001'
                
                mycursor.close()

                entry_to_customer.get_list(lista)       # ['B1001','B1002']
                # print(lista)
            else:
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select cust_name from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                listb = []
                for x in myresult:
                    listb.append(x[0])

                mycursor.close()
                
                entry_to_customer.get_list(listb)

        var = IntVar()
        R1 = Radiobutton(tree_frame, text="Search by ID", variable=var, value=1,bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=option_to_customer_selected)
        R1.place(x = 75,y = 10)

        R2 = Radiobutton(tree_frame, text="Search by Name",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red", variable=var, value=2,command=option_to_customer_selected)
        R2.place(x = 250,y = 10)


        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Cust Name','Book Name','Quantity Given','Rental Price','Mobile No','Allocate Date','Due Days')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        def get_ot_cust_details():
            global entry_to_customer
            # print(*my_tree.get_children())
            my_tree.delete(*my_tree.get_children())     # clear treeview

            for col in cols:
                my_tree.column(col,anchor = "center",width=140)
                my_tree.heading(col,text = col)
                
            customer_name_id = entry_to_customer.get()

            if var.get() == 1: 
                try:
                    mysql_connect()

                    mycursor = mydb.cursor()

                    sql = "select c.cust_name,b.book_name,t.quantity_given,t.rental_price,c.cust_mobile,t.allocate_date, datediff(curdate(),t.allocate_date) from transactions t inner join customer_details c on t.cust_id = c.cust_id inner join book_details b on t.book_id = b.book_id where t.return_status = 'Not Returned' and c.cust_id = %s;"

                    values = (customer_name_id,)

                    mycursor.execute(sql,values)

                    myresult = mycursor.fetchall()
                    
                    if len(myresult) > 0:
                        for cust_name,book_name,quantity,rental_price,mobile_no,allocate_date,due_days in myresult:
                            my_tree.insert("","end",values=(cust_name,book_name,quantity,rental_price,mobile_no,allocate_date,due_days))
                    else:
                        messagebox.showerror("Error","No Records found...")
                
                    mycursor.close()
                except Exception as e:
                    messagebox.showerror("Error",e)
            else:
                try:
                    mysql_connect()

                    mycursor = mydb.cursor()

                    sql = "select c.cust_name,b.book_name,t.quantity_given,t.rental_price,c.cust_mobile,t.allocate_date, datediff(curdate(),t.allocate_date) from transactions t inner join customer_details c on t.cust_id = c.cust_id inner join book_details b on t.book_id = b.book_id where t.return_status = 'Not Returned' and c.cust_name = %s;"

                    values = (customer_name_id,)

                    mycursor.execute(sql,values)

                    myresult = mycursor.fetchall()
                    
                    if len(myresult) > 0:
                        for cust_name,book_name,quantity,rental_price,mobile_no,allocate_date,due_days in myresult:
                            my_tree.insert("","end",values=(cust_name,book_name,quantity,rental_price,mobile_no,allocate_date,due_days))
                    else:
                        messagebox.showerror("Error","No Records found...")
                
                    mycursor.close()
                except Exception as e:
                    messagebox.showerror("Error",e)

        btn_get_data = Button(tree_frame,text="View Records",bg="lightblue",font=("Goudy old style",12,"bold"),fg="red",command=get_ot_cust_details).place(x=760,y=12,width=120,height=32)

        def close_bet_date_page():
            global entry_to_customer
            global to_customer_count
            to_customer_count = 0
            entry_to_customer.lb_destroy()
            tree_frame.destroy()                  

        btn_close_all_book = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_bet_date_page).place(x=450,y=555,width=120)
    else:
        pass


allocate_details.add_separator()
allocate_details.add_command(label='To Customer',compound=LEFT,command=to_customer_page)

################################################### End To customer page ###############################################################

##################################################### View all allocated book ######################################################

view_all_allocated_count = 0
def view_all_allocated_page(event=None):
    global view_all_allocated_count
    if view_all_allocated_count == 0:
        view_all_allocated_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "All Allocated Books", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Cust Name','Book Name','Quantity Given','Rental Price','Mobile No','Date Allocated','Due Days')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center",width=140)
            my_tree.heading(col,text = col)

        try:
            mysql_connect()

            mycursor = mydb.cursor()

            sql = "select c.cust_name,b.book_name,t.quantity_given,t.rental_price,c.cust_mobile,t.allocate_date, datediff(curdate(),t.allocate_date) from transactions t inner join customer_details c on t.cust_id = c.cust_id inner join book_details b on t.book_id = b.book_id where t.return_status = 'Not Returned';" 

            mycursor.execute(sql)

            myresult = mycursor.fetchall()
            
            if len(myresult)>0:
                for cust_name,book_name,quantity,total_rent,mobile_no,allocate_date,due_days in myresult:
                    my_tree.insert("","end",values=(cust_name, book_name, quantity, total_rent, mobile_no, allocate_date,due_days))
            else:
                messagebox.showerror("Error","No records found...")
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_view_all_allocated():
            global view_all_allocated_count
            view_all_allocated_count = 0
            tree_frame.destroy()                  

        btn_close_all_book = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_view_all_allocated).place(x=450,y=555,width=120)
    else:
        pass


allocate_details.add_command(label='View all',compound=LEFT,accelerator='Ctrl + V',command=view_all_allocated_page)

##################################################### End View all allocated book ######################################################

# Return Details
return_details = Menu(main_menu,tearoff=False)
##################################################### Returned between date books ######################################################

bet_date_return_count = 0
def bet_date_return_page(event=None):
    global bet_date_return_count
    if bet_date_return_count == 0:
        bet_date_return_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        # lbl = Label(tree_frame,text = "Between Selected dates", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        lbl = Label(tree_frame,text="Select dates :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        lbl.place(x=100,y=10,width=130,height=35)

        date_entry1 = DateEntry(tree_frame,date_pattern='yyyy/mm/dd',font=("times new roman",15),bg="lightgrey",fg="lightgrey")
        date_entry1.place(x=250,y=10,width=250,height=35)

        date_entry2 = DateEntry(tree_frame,date_pattern='yyyy/mm/dd',font=("times new roman",15),bg="lightgrey",fg="lightgrey")
        date_entry2.place(x=510,y=10,width=250,height=35)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Cust Id','Cust Name','Book Id','Book Name','Quantity Given','Total Rent','Date Allocated')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        def get_details():
            # print(*my_tree.get_children())
            my_tree.delete(*my_tree.get_children())     # clear treeview

            date1 = date_entry1.get()
            date2 = date_entry2.get()

            if date1 == "" and date2 =="":
                messagebox.showerror("Error","Please select dates...")
            else:
                for col in cols:
                    my_tree.column(col,anchor = "center",width=140)
                    my_tree.heading(col,text = col)
                
                try:
                    mysql_connect()

                    mycursor = mydb.cursor()

                    sql = "select t.cust_id,c.cust_name,t.book_id,b.book_name,t.quantity_given,t.total_rent,t.allocate_date from transactions t inner join customer_details c on t.cust_id = c.cust_id inner join book_details b on t.book_id = b.book_id where allocate_date between %s and %s and return_status = 'Returned';"

                    values = (date1,date2)

                    mycursor.execute(sql,values)

                    myresult = mycursor.fetchall()
                    
                    if len(myresult) > 0:
                        for cust_id,cust_name,book_id,book_name,quantity,total_rent,allocate_date in myresult:
                                # print(id, name, address,mobile,profession,dob,aadhar)
                            my_tree.insert("","end",values=(cust_id,cust_name, book_id, book_name, quantity, total_rent,allocate_date))
                    else:
                        messagebox.showerror("Error","No Records found...")
                
                    mycursor.close()
                except Exception as e:
                    messagebox.showerror("Error",e)

        btn_get_data = Button(tree_frame,text="View Records",bg="lightblue",font=("Goudy old style",12,"bold"),fg="red",command=get_details).place(x=790,y=12,width=120,height=32)

        def close_bet_date_return_page():
            global bet_date_return_count
            bet_date_return_count = 0
            tree_frame.destroy()                  

        btn_close_all_book = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_bet_date_return_page).place(x=450,y=555,width=120)
    else:
        pass


return_details.add_command(label='Between Date',compound=LEFT,command=bet_date_return_page)

##################################################### End Returned between date books ######################################################

####################################################### Returned after due date ##############################################################
date_due_return_count = 0
def date_due_return_page(event=None):
    global date_due_return_count
    if date_due_return_count == 0:
        date_due_return_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "Date Due", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Cust Name','Book Id','Book Name','Quantity Given','Mobile Number','Date Allocated','Due Days')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center",width=140)
            my_tree.heading(col,text = col)

        try:
            mysql_connect()

            mycursor = mydb.cursor()

            sql = "select c.cust_name,t.book_id,b.book_name,t.quantity_given,c.cust_mobile,t.allocate_date, datediff(curdate(),t.allocate_date) from transactions t inner join customer_details c on t.cust_id = c.cust_id inner join book_details b on t.book_id = b.book_id where datediff(curdate(),t.allocate_date) >= 10 and t.return_status = 'Returned';"

            mycursor.execute(sql)

            myresult = mycursor.fetchall()
            
            if len(myresult)>0:
                for cust_name,book_id,book_name,quantity,total_rent,allocate_date,due_days in myresult:
                    my_tree.insert("","end",values=(cust_name, book_id, book_name, quantity, total_rent,allocate_date,due_days))
            else:
                messagebox.showerror("Error","No records found...")
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_due_return_date_page():
            global date_due_return_count
            date_due_return_count = 0
            tree_frame.destroy()                  

        btn_close_all_book = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_due_return_date_page).place(x=450,y=555,width=120)
    else:
        pass

return_details.add_command(label='After Due Date',compound=LEFT,command=date_due_return_page)

####################################################### End after due date returned ##############################################################

####################################################### customer returned books ##############################################################

customer_returned_count = 0
entry_customer_returned = 0
def customer_returned_page(event=None):
    global customer_returned_count
    global entry_customer_returned
    if customer_returned_count == 0:
        customer_returned_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        # lbl = Label(tree_frame,text = "Between Selected dates", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        entry_customer_returned = AutocompleteEntry(700, 95, tree_frame,font=("times new roman",15),bg = "lightgrey")
        entry_customer_returned.place(x=450,y=10,width=270,height=35)
        entry_customer_returned['state'] = 'readonly'

        def option_customer_return_selected():
            global entry_customer_returned
            entry_customer_returned.focus_set()
            entry_customer_returned['state'] = "normal"
            entry_customer_returned.empty_entry()

            if var.get() == 1:
                mysql_connect()

                mycursor = mydb.cursor()
                
                sql = "select cust_id from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                
                # myresult = [('D1001',),('D1002',)]

                lista = []
                for x in myresult:          #   x = ('B1001',)  
                    lista.append(x[0])      #   x[0] = 'B1001'
                
                mycursor.close()

                entry_customer_returned.get_list(lista)       # ['B1001','B1002']
                # print(lista)
            else:
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select cust_name from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                listb = []
                for x in myresult:
                    listb.append(x[0])

                mycursor.close()
                
                entry_customer_returned.get_list(listb)

        var = IntVar()
        R1 = Radiobutton(tree_frame, text="Search by ID", variable=var, value=1,bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=option_customer_return_selected)
        R1.place(x = 75,y = 10)

        R2 = Radiobutton(tree_frame, text="Search by Name",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red", variable=var, value=2,command=option_customer_return_selected)
        R2.place(x = 250,y = 10)


        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Cust Name','Book Name','Quantity Given','Rental Price','Mobile No','Allocate Date','Due Days')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        def get_returned_cust_details():
            global entry_customer_returned
            # print(*my_tree.get_children())
            my_tree.delete(*my_tree.get_children())     # clear treeview

            for col in cols:
                my_tree.column(col,anchor = "center",width=140)
                my_tree.heading(col,text = col)
                
            customer_name_id = entry_customer_returned.get()

            if var.get() == 1: 
                try:
                    mysql_connect()

                    mycursor = mydb.cursor()

                    sql = "select c.cust_name,b.book_name,t.quantity_given,t.rental_price,c.cust_mobile,t.allocate_date, datediff(curdate(),t.allocate_date) from transactions t inner join customer_details c on t.cust_id = c.cust_id inner join book_details b on t.book_id = b.book_id where t.return_status = 'Returned' and c.cust_id = %s;"

                    values = (customer_name_id,)

                    mycursor.execute(sql,values)

                    myresult = mycursor.fetchall()
                    
                    if len(myresult) > 0:
                        for cust_name,book_name,quantity,rental_price,mobile_no,allocate_date,due_days in myresult:
                            my_tree.insert("","end",values=(cust_name,book_name,quantity,rental_price,mobile_no,allocate_date,due_days))
                    else:
                        messagebox.showerror("Error","No Records found...")
                
                    mycursor.close()
                except Exception as e:
                    messagebox.showerror("Error",e)
            else:
                try:
                    mysql_connect()

                    mycursor = mydb.cursor()

                    sql = "select c.cust_name,b.book_name,t.quantity_given,t.rental_price,c.cust_mobile,t.allocate_date, datediff(curdate(),t.allocate_date) from transactions t inner join customer_details c on t.cust_id = c.cust_id inner join book_details b on t.book_id = b.book_id where t.return_status = 'Returned' and c.cust_name = %s;"

                    values = (customer_name_id,)

                    mycursor.execute(sql,values)

                    myresult = mycursor.fetchall()
                    
                    if len(myresult) > 0:
                        for cust_name,book_name,quantity,rental_price,mobile_no,allocate_date,due_days in myresult:
                            my_tree.insert("","end",values=(cust_name,book_name,quantity,rental_price,mobile_no,allocate_date,due_days))
                    else:
                        messagebox.showerror("Error","No Records found...")
                
                    mycursor.close()
                except Exception as e:
                    messagebox.showerror("Error",e)

        btn_get_data = Button(tree_frame,text="View Records",bg="lightblue",font=("Goudy old style",12,"bold"),fg="red",command=get_returned_cust_details).place(x=760,y=12,width=120,height=32)

        def close_return_date_page():
            global entry_customer_returned
            global customer_returned_count
            customer_returned_count = 0
            entry_customer_returned.lb_destroy()
            tree_frame.destroy()                  

        btn_close_all_book = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_return_date_page).place(x=450,y=555,width=120)
    else:
        pass


return_details.add_separator()
return_details.add_command(label='Customer Returned books',compound=LEFT,command=customer_returned_page)

######################################################## End customer returned books #################################################

######################################################## All returned books #################################################

view_all_returned_count = 0
def view_all_returned_page(event=None):
    global view_all_returned_count
    if view_all_returned_count == 0:
        view_all_returned_count = 1

        tree_frame = Frame(win)
        tree_frame.place(x = 250, y = 50,width = 1050, height = 600)
        bg_color = Label(tree_frame,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        lbl = Label(tree_frame,text = "All Returned Books", font=("Arial",30),bg="lightblue",fg="green").place(x=0,y=0,height=50,relwidth=1)

        style = ttk.Style()
        style.configure(".",font=('Helvetica',9),foreground="red")
        style.configure("Treeview.Heading",foreground='Red',font=('Goudy old style',14))

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side= RIGHT,fill=Y)

        cols = ('Cust Name','Book Name','Quantity Given','Rental Price','Mobile No','Date Allocated','Due Days')

        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,columns = cols, show = 'headings')
        my_tree.place(x=0,y=50,width=1032,height=500)

        tree_scroll.config(command=my_tree.yview)

        for col in cols:
            my_tree.column(col,anchor = "center",width=140)
            my_tree.heading(col,text = col)

        try:
            mysql_connect()

            mycursor = mydb.cursor()

            sql = "select c.cust_name,b.book_name,t.quantity_given,t.rental_price,c.cust_mobile,t.allocate_date, datediff(curdate(),t.allocate_date) from transactions t inner join customer_details c on t.cust_id = c.cust_id inner join book_details b on t.book_id = b.book_id where t.return_status = 'Returned';" 

            mycursor.execute(sql)

            myresult = mycursor.fetchall()
            
            if len(myresult)>0:
                for cust_name,book_name,quantity,total_rent,mobile_no,allocate_date,due_days in myresult:
                    my_tree.insert("","end",values=(cust_name, book_name, quantity, total_rent, mobile_no, allocate_date,due_days))
            else:
                messagebox.showerror("Error","No records found...")
        
            mycursor.close()
        except Exception as e:
            messagebox.showerror("Error",e)

        def close_view_all_returned():
            global view_all_returned_count
            view_all_returned_count = 0
            tree_frame.destroy()                  

        btn_close_all_book = Button(tree_frame,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_view_all_returned).place(x=450,y=555,width=120)
    else:
        pass

return_details.add_separator()
return_details.add_command(label='All Returned books',compound=LEFT,accelerator='Ctrl + Alt + R',command=view_all_returned_page)

######################################################## All returned books #################################################

####################################################### Search Menu ##############################################################
# Search menu

search_menu = Menu(main_menu,tearoff=False)

####################################################### Search books ##############################################################

search_book_count = 0
entry_search_book = 0
def search_book(event=None):
    global entry_search_book
    global search_book_count
    
    if search_book_count == 0:
        search_book_count = 1

        searchbook = LabelFrame(win,text = 'Search book by id or name...')
        searchbook.place(x = 500, y = 50,width = 500, height = 600)
        bg_color = Label(searchbook,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        entry_search_book = AutocompleteEntry(575, 160, searchbook,font=("times new roman",15),bg = "lightgrey")
        entry_search_book.place(x=75,y=60,width=270,height=35)
        entry_search_book['state'] = 'readonly'

        lbl_search_name = Label(searchbook,text="Book Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        lbl_search_name.place(x=75,y=100)

        book_search_name = Entry(searchbook,font=("times new roman",15),bg="lightgrey")
        book_search_name.place(x=75,y=130,width=350,height=35)
        book_search_name.focus_set()

        lbl_search_auth_name = Label(searchbook,text="Auther Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=170)

        book_search_auth_name = Entry(searchbook,font=("times new roman",15),bg="lightgrey")
        book_search_auth_name.place(x=75,y=200,width=350,height=35)

        lbl_search_pdud = Label(searchbook,text="Paid Unpaid :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=240)

        paid_unpaid = Entry(searchbook,font=("times new roman",15),bg="lightgrey")
        paid_unpaid.place(x=75,y=270,width=350,height=35)

        lbl_search_price = Label(searchbook,text="Custom Price :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=310)

        book_search_price = Entry(searchbook,font=("times new roman",15),bg="lightgrey")
        book_search_price.place(x=75,y=340,width=350,height=35)

        lbl_search_dob = Label(searchbook,text="Date of entry :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=380)

        # cust_dob = Calendar(newCustomer,font=("times new roman",15),bg="lightgrey",selectmode = 'day', year = 2021, month = 3, day = 12)
        book_search_doe = Entry(searchbook,font=("times new roman",15),bg="lightgrey")
        book_search_doe.place(x=75,y=410,width=350,height=35)

        lbl_search_quantity = Label(searchbook,text="Quantity :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=450)

        book_search_quantity = Entry(searchbook,font=("times new roman",15),bg="lightgrey")
        book_search_quantity.place(x=75,y=480,width=350,height=35)

        def option_selected():
            make_search_empty_normal()
            empty_serach_entry()
            make_search_empty_readonly()
            
            global entry_search_book
            entry_search_book.focus_set()
            entry_search_book['state'] = "normal"
            entry_search_book.empty_entry()

            if var.get() == 1:
                lbl_search_name['text'] = "Book Name :"
                
                mysql_connect()

                mycursor = mydb.cursor()
                
                sql = "select book_id from book_details where book_id not in ('B1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                
                # myresult = [('D1001',),('D1002',)]

                lista = []
                for x in myresult:          #   x = ('B1001',)  
                    lista.append(x[0])      #   x[0] = 'B1001'
                
                mycursor.close()

                entry_search_book.get_list(lista)       # ['B1001','B1002']
                # print(lista)
            else:
                lbl_search_name['text'] = "Book Id :"
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select book_name from book_details where book_id not in ('B1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                listb = []
                for x in myresult:
                    listb.append(x[0])

                mycursor.close()
                
                entry_search_book.get_list(listb)
                # print(listb)
                
        var = IntVar()
        R1 = Radiobutton(searchbook, text="Search by ID", variable=var, value=1,bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=option_selected)
        R1.place(x = 60,y = 10)

        R2 = Radiobutton(searchbook, text="Search by Name",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red", variable=var, value=2,command=option_selected)
        R2.place(x = 250,y = 10)

        def empty_serach_entry():
            book_search_name.delete(0,END)
            book_search_auth_name.delete(0,END)
            paid_unpaid.delete(0,END)
            book_search_price.delete(0,END)
            book_search_doe.delete(0,END)
            book_search_quantity.delete(0,END)
        
        def make_search_empty_readonly():
            book_search_name['state'] = 'readonly'
            book_search_auth_name['state'] = 'readonly'
            paid_unpaid['state'] = 'readonly'
            book_search_price['state'] = 'readonly'
            book_search_doe['state'] = 'readonly'
            book_search_quantity['state'] = 'readonly'

        def make_search_empty_normal():
            book_search_name['state'] = 'normal'
            book_search_auth_name['state'] = 'normal'
            paid_unpaid['state'] = 'normal'
            book_search_price['state'] = 'normal'
            book_search_doe['state'] = 'normal'
            book_search_quantity['state'] = 'normal'

        make_search_empty_readonly()
        ############################### search button ###########################################
        def fetch_details():
            if entry_search_book.get() == "":           # id or name text box
                messagebox.showwarning("Warning","Please enter id or name for search...")
            else:
                if var.get() == 1:
                    update_id = entry_search_book.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from book_details where book_id = %s"
                    val = (update_id,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        make_search_empty_normal()
                        empty_serach_entry()

                        entry_search_book.lb_destroy()
                        book_search_name.insert(0,myresult[0][1])
                        book_search_auth_name.insert(0,myresult[0][2])
                        paid_unpaid.insert(0,myresult[0][3])
                        book_search_price.insert(0,myresult[0][4])
                        book_search_doe.insert(0,myresult[0][5])
                        book_search_quantity.insert(0,myresult[0][6])

                        make_search_empty_readonly()
                    else:
                        messagebox.showerror("Error","Book not found, Please enter valid Book Id...")
                        entry_search_book.empty_entry()
                        make_search_empty_normal()
                        empty_serach_entry()
                        make_search_empty_readonly()
                    mycursor.close()
                else:
                    update_name = entry_search_book.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from book_details where book_name = %s"
                    val = (update_name,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        make_search_empty_normal()
                        empty_serach_entry()

                        entry_search_book.lb_destroy()
                        book_search_name.insert(0,myresult[0][0])
                        book_search_auth_name.insert(0,myresult[0][2])
                        paid_unpaid.insert(0,myresult[0][3])
                        book_search_price.insert(0,myresult[0][4])
                        book_search_doe.insert(0,myresult[0][5])
                        book_search_quantity.insert(0,myresult[0][6])

                        make_search_empty_readonly()
                    else:
                        messagebox.showerror("Error","Book not found, Please enter valid Book Name...")
                        entry_search_book.empty_entry()
                        make_search_empty_normal()
                        empty_serach_entry()
                        make_search_empty_readonly()
        
        def close_search_book():
            global search_book_count
            search_book_count = 0
            searchbook.destroy()                  

        btn_close_all_book = Button(searchbook,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_search_book).place(x=180,y=530,width=120)

        btn_search_book = Button(searchbook,text="Fetch",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=fetch_details).place(x=355,y=60,width=100)


search_menu.add_command(label='Search book',compound=LEFT,accelerator='Ctrl + B',command=search_book)

####################################################### End Search Books ##############################################################

search_customer_count = 0
entry_search_customer = 0
def search_customer(event=None):
    global entry_search_customer
    global search_customer_count
    
    if search_customer_count == 0:
        search_customer_count = 1

        searchcustomer = LabelFrame(win,text = 'Search book by id or name...')
        searchcustomer.place(x = 500, y = 50,width = 500, height = 600)
        bg_color = Label(searchcustomer,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

        entry_search_customer = AutocompleteEntry(575, 160, searchcustomer,font=("times new roman",15),bg = "lightgrey")
        entry_search_customer.place(x=75,y=60,width=270,height=35)
        entry_search_customer['state'] = 'readonly'

        lbl_search_name = Label(searchcustomer,text="Customer Name :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red")
        lbl_search_name.place(x=75,y=100)

        customer_search_name = Entry(searchcustomer,font=("times new roman",15),bg="lightgrey")
        customer_search_name.place(x=75,y=130,width=350,height=35)
        customer_search_name.focus_set()

        lbl_serach_address = Label(searchcustomer,text="Address :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=170)

        cust_search_address = Entry(searchcustomer,font=("times new roman",15),bg="lightgrey")
        cust_search_address.place(x=75,y=200,width=350,height=35)

        lbl_search_mobile = Label(searchcustomer,text="Mobile No :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=240)

        cust_search_mobile = Entry(searchcustomer,font=("times new roman",15),bg="lightgrey")
        cust_search_mobile.place(x=75,y=270,width=350,height=35)

        lbl_search_prof = Label(searchcustomer,text="Proffession :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=310)

        cust_search_prof = Entry(searchcustomer,font=("times new roman",15),bg="lightgrey")
        cust_search_prof.place(x=75,y=340,width=350,height=35)

        lbl_search_dob = Label(searchcustomer,text="Date of birth :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=380)

        # cust_dob = Calendar(newCustomer,font=("times new roman",15),bg="lightgrey",selectmode = 'day', year = 2021, month = 3, day = 12)
        cust_search_dob = Entry(searchcustomer,font=("times new roman",15),bg="lightgrey")
        cust_search_dob.place(x=75,y=410,width=350,height=35)

        lbl_search_aadhar = Label(searchcustomer,text="Aadhar No :",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red").place(x=75,y=450)

        cust_search_aadhar = Entry(searchcustomer,font=("times new roman",15),bg="lightgrey")
        cust_search_aadhar.place(x=75,y=480,width=350,height=35)

        def option_selected():
            make_search_empty_normal()
            empty_serach_entry()
            make_search_empty_readonly()
            
            global entry_search_customer
            entry_search_customer.focus_set()
            entry_search_customer['state'] = "normal"
            entry_search_customer.empty_entry()

            if var.get() == 1:
                lbl_search_name['text'] = "Book Name :"
                
                mysql_connect()

                mycursor = mydb.cursor()
                
                sql = "select cust_id from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                
                # myresult = [('D1001',),('D1002',)]

                lista = []
                for x in myresult:          #   x = ('B1001',)  
                    lista.append(x[0])      #   x[0] = 'B1001'
                
                mycursor.close()

                entry_search_customer.get_list(lista)       # ['B1001','B1002']
                # print(lista)
            else:
                lbl_search_name['text'] = "Book Id :"
                mysql_connect()

                mycursor = mydb.cursor()
                sql = "select cust_name from customer_details where cust_id not in ('D1000')"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                listb = []
                for x in myresult:
                    listb.append(x[0])

                mycursor.close()
                
                entry_search_customer.get_list(listb)
                # print(listb)
                
        var = IntVar()
        R1 = Radiobutton(searchcustomer, text="Search by ID", variable=var, value=1,bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=option_selected)
        R1.place(x = 60,y = 10)

        R2 = Radiobutton(searchcustomer, text="Search by Name",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red", variable=var, value=2,command=option_selected)
        R2.place(x = 250,y = 10)

        def empty_serach_entry():
            customer_search_name.delete(0,END)
            cust_search_address.delete(0,END)
            cust_search_mobile.delete(0,END)
            cust_search_prof.delete(0,END)
            cust_search_dob.delete(0,END)
            cust_search_aadhar.delete(0,END)
        
        def make_search_empty_readonly():
            customer_search_name['state'] = 'readonly'
            cust_search_address['state'] = 'readonly'
            cust_search_mobile['state'] = 'readonly'
            cust_search_prof['state'] = 'readonly'
            cust_search_dob['state'] = 'readonly'
            cust_search_aadhar['state'] = 'readonly'

        def make_search_empty_normal():
            customer_search_name['state'] = 'normal'
            cust_search_address['state'] = 'normal'
            cust_search_mobile['state'] = 'normal'
            cust_search_prof['state'] = 'normal'
            cust_search_dob['state'] = 'normal'
            cust_search_aadhar['state'] = 'normal'

        make_search_empty_readonly()
        ############################### search button ###########################################
        def fetch_details():
            if entry_search_customer.get() == "":           # id or name text box
                messagebox.showwarning("Warning","Please enter id or name for search...")
            else:
                if var.get() == 1:
                    search_id = entry_search_customer.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from customer_details where cust_id = %s"
                    val = (search_id,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        make_search_empty_normal()
                        empty_serach_entry()

                        entry_search_customer.lb_destroy()
                        customer_search_name.insert(0,myresult[0][1])
                        cust_search_address.insert(0,myresult[0][2])
                        cust_search_mobile.insert(0,myresult[0][3])
                        cust_search_prof.insert(0,myresult[0][4])
                        cust_search_dob.insert(0,myresult[0][5])
                        cust_search_aadhar.insert(0,myresult[0][6])

                        make_search_empty_readonly()
                    else:
                        messagebox.showerror("Error","Customer not found, Please enter valid Customer Id...")
                        entry_search_book.empty_entry()
                        make_search_empty_normal()
                        empty_serach_entry()
                        make_search_empty_readonly()
                    mycursor.close()
                else:
                    search_name = entry_search_customer.get()
                    mysql_connect()
                    mycursor = mydb.cursor()
                    sql = "select * from customer_details where cust_name = %s"
                    val = (search_name,)
                    mycursor.execute(sql,val)
                    myresult = mycursor.fetchall()
                    
                    if len(myresult)>0:
                        make_search_empty_normal()
                        empty_serach_entry()

                        entry_search_customer.lb_destroy()
                        customer_search_name.insert(0,myresult[0][0])
                        cust_search_address.insert(0,myresult[0][2])
                        cust_search_mobile.insert(0,myresult[0][3])
                        cust_search_prof.insert(0,myresult[0][4])
                        cust_search_dob.insert(0,myresult[0][5])
                        cust_search_aadhar.insert(0,myresult[0][6])

                        make_search_empty_readonly()
                    else:
                        messagebox.showerror("Error","Customer not found, Please enter valid Customer Name...")
                        entry_search_book.empty_entry()
                        make_search_empty_normal()
                        empty_serach_entry()
                        make_search_empty_readonly()
        
        def close_search_customer():
            global search_customer_count
            search_customer_count = 0
            searchcustomer.destroy()                  

        btn_close_all_cust = Button(searchcustomer,text="Close",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=close_search_customer).place(x=180,y=530,width=120)

        btn_search_book = Button(searchcustomer,text="Fetch",bg="lightblue",font=("Goudy old style",15,"bold"),fg="red",command=fetch_details).place(x=355,y=60,width=100)

search_menu.add_command(label='Search customer',compound=LEFT,accelerator='Ctrl + C',command=search_customer)

####################################################### End Search Menu ##############################################################
# exit menu
####################################################### Exit menu ##############################################################
exit_menu = Menu(main_menu,tearoff=False)

def exit_application(event=None):
    win.destroy()

exit_menu.add_command(label='Quit',compound=LEFT,accelerator='Ctrl + Q',command=exit_application)

####################################################### End Exit menu ##############################################################


main_menu.add_cascade(label='Allocate & Return Book',menu=allocate_book)
main_menu.add_cascade(label='Customer Details',menu=customer_details)                           # adding menu to main menu
main_menu.add_cascade(label='Book Details',menu=book_details)
main_menu.add_cascade(label='Allocate Details',menu=allocate_details)
main_menu.add_cascade(label='Return Details',menu=return_details)
main_menu.add_cascade(label='Search',menu=search_menu)
main_menu.add_cascade(label='Exit',menu=exit_menu)

win.config(menu = main_menu)

################################################ binding shortcut keys #####################################################

win.bind('<Control-N>',new_customer)
win.bind('<Control-n>',new_customer)
win.bind('<Control-D>',delete_customer)
win.bind('<Control-d>',delete_customer)
win.bind('<Control-U>',update_customer)
win.bind('<Control-u>',update_customer)
win.bind('<Control-Alt-A>',view_all_customer)
win.bind('<Control-Alt-a>',view_all_customer)

win.bind('<Alt-N>',new_book)
win.bind('<Alt-n>',new_book)
win.bind('<Alt-D>',delete_book)
win.bind('<Alt-d>',delete_book)
win.bind('<Alt-U>',update_book)
win.bind('<Alt-u>',update_book)
win.bind('<Control-Alt-B>',view_all_book_page)
win.bind('<Control-Alt-b>',view_all_book_page)

win.bind('<Control-A>',allocate_book_page)
win.bind('<Control-a>',allocate_book_page)
win.bind('<Control-R>',return_book_page)
win.bind('<Control-r>',return_book_page)

win.bind('<Control-B>',search_book)
win.bind('<Control-b>',search_book)
win.bind('<Control-C>',search_customer)
win.bind('<Control-c>',search_customer)

win.bind('<Control-Alt-R>',view_all_returned_page)
win.bind('<Control-Alt-r>',view_all_returned_page)


############################################################################################################################
win.mainloop()