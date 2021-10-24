from tkinter import *
import mysql.connector
from PIL import ImageTk     # for using .jpg file with PhotoImage class on line 11
from tkinter import messagebox

class login:
    # def mysql_connection(self):
    #     mydb = mysql.connector.connect(
    #         host = "localhost",
    #         user = "yaman",
    #         password = "yaman",
    #         database = "pythondatabse"
    #     )
    def __init__(self,root):
        self.root = root
        self.root.title("login system")
        root.overrideredirect(1)                    # border , minimize , maximize close remove
        self.root.geometry("1199x600+160+100")      # starts from x = 100 and y = 50
        self.root.resizable(False,False)

        ######## BG Image #######
        
        self.bg = ImageTk.PhotoImage(file="images/login.jpg")
        
        self.bg_image = Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
        # setting image on label using .place x = 0 y = 0 lable starts from cornor and relwidth and relheight = 1 to occupy full space as main window

        ######### Login Frame ######

        Frame_login = Frame(self.root,bg = "white")
        Frame_login.place(x=250,y=150,height=340,width=500)

        title = Label(Frame_login,text="Login Here...",font=("Impact",35,"bold"),fg="skyblue",bg="white").place(x=90,y=30)
        
        desc = Label(Frame_login,text="Welcome to our library...",font=("Goudy old style",15,"bold"),fg="skyblue",bg="white").place(x=90,y=100)
    
        lbl_user = Label(Frame_login,text="Username",font=("Goudy old style",15,"bold"),fg="grey",bg="white").place(x=90,y=140)

        self.txt_user = Entry(Frame_login,font=("times new roman",15),bg="lightgrey")
        self.txt_user.place(x=90,y=170,width=350,height=35)
        
        lbl_pass = Label(Frame_login,text="Password",font=("Goudy old style",15,"bold"),fg="grey",bg="white").place(x=90,y=210)

        self.txt_pass = Entry(Frame_login,font=("times new roman",15),bg="lightgrey",show="*")
        self.txt_pass.place(x=90,y=240,width=350,height=35)

        forget_btn=Button(Frame_login,text="Forgot password...?",cursor="hand2",bg="white",fg="blue",bd=0,font=("times new roman",12),command=self.move_forgot).place(x=90,y=280)

        sign_up_btn=Button(Frame_login,text="Register here...",cursor="hand2",bg="white",fg="blue",bd=0,font=("times new roman",12),command=self.move_sign_up).place(x=330,y=280)
        
        login_btn=Button(self.root,text="Login",cursor="hand2",fg="grey",bg="skyblue",font=("times new roman",20),command=self.login_function).place(x=310,y=470,width=180,height=40)

        close_btn=Button(self.root,text="Close",cursor="hand2",fg="grey",bg="skyblue",font=("times new roman",20),command=self.close_function).place(x=510,y=470,width=180,height=40)
    
    def move_sign_up(self):
        self.root.destroy()
        import sign_up

    def move_forgot(self):
        self.root.destroy()             # main page delete # closed
        import forgotPass

    def close_function(self):
        self.root.destroy()

    def move_login(self):
        self.root.destroy()
        import master_page


    def login_function(self):
        user_name = self.txt_user.get()
        pwd = self.txt_pass.get()
        if user_name == "" and pwd == "":
            messagebox.showerror("Error","Please enter username and password...",parent=self.root)
            self.txt_user.focus_set()
        elif user_name == "":
            messagebox.showerror("Error","Please enter username...")
            self.txt_user.focus_set()
        elif pwd == "":
            messagebox.showerror("Error","Please enter password...")
            self.txt_pass.focus_set()
        else:
            mydb = mysql.connector.connect(
            host = "localhost",
            user = "yaman",
            password = "yaman",
            database = "pythondatabase"
            )

            mycursor = mydb.cursor()

            sql = "Select * from login where username = %s and password = %s"

            val = (user_name,pwd)

            mycursor.execute(sql,val)

            myresult = mycursor.fetchall()

            if len(myresult)>0:
                messagebox.showinfo("Successfull","Login successfull...")
                self.move_login()
                mydb.close()
            else:
                messagebox.showerror("Error","Invalid username or password...")


win = Tk()

obj = login(win)

win.mainloop()