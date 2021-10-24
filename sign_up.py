from tkinter import *
import mysql.connector
from tkinter import messagebox
from PIL import ImageTk
from tkinter import ttk

win = Tk()
win.title("Sign Up...")
win.geometry("738x416+400+150")
win.resizable(False,False)
# win.overrideredirect(1)


bg = ImageTk.PhotoImage(file="images/signup.jpg")
bg_image = Label(win,image=bg,bg="grey").place(x=0,y=0,relwidth=1,relheight=1)

Frame_login = Frame(win,bg = "white")
Frame_login.place(x=120,y=10,height=380,width=500)

lbl_user = Label(Frame_login,text="Username :",font=("Goudy old style",15,"bold"),fg="grey",bg="white").place(x=75,y=10)

txt_user = Entry(Frame_login,font=("times new roman",15),bg="lightblue")
txt_user.place(x=75,y=40,width=350,height=35)
txt_user.focus_set()

lbl_pass = Label(Frame_login,text="Password :",font=("Goudy old style",15,"bold"),fg="grey",bg="white").place(x=75,y=80)

txt_pass = Entry(Frame_login,font=("times new roman",15),bg="lightblue",show="*")
txt_pass.place(x=75,y=110,width=350,height=35)

lbl_repass = Label(Frame_login,text="Re-Enter Password :",font=("Goudy old style",15,"bold"),fg="grey",bg="white").place(x=75,y=150)

txt_repass = Entry(Frame_login,font=("times new roman",15),bg="lightblue",show="*")
txt_repass.place(x=75,y=180,width=350,height=35)

lbl_question = Label(Frame_login,text="Select question :",font=("Goudy old style",15,"bold"),fg="grey",bg="white").place(x=75,y=220)

combo_question = ttk.Combobox(Frame_login,font=("times new roman",15))
combo_question.place(x=75,y=250,width=350,height=35)
combo_question["values"] = [('Select a question...'),('What is your pet name ?'),('What is your age ?'),('What is your school name ?'),('What is your mother name ?')]
combo_question.current(0)
combo_question['state'] = 'readonly'

lbl_answer = Label(Frame_login,text="Answer :",font=("Goudy old style",15,"bold"),fg="grey",bg="white").place(x=75,y=290)

txt_answer = Entry(Frame_login,font=("times new roman",15),bg="lightblue")
txt_answer.place(x=75,y=320,width=350,height=35)

def sign_up():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "yaman",
        password = "yaman",
        database = "pythondatabase"
    )

    mycursor = mydb.cursor()

    user_name = txt_user.get()
    pwd = txt_pass.get()
    re_pwd = txt_repass.get()
    question = combo_question.get()
    ans = txt_answer.get()

    if user_name == "" and pwd == "" and re_pwd == "" and question == "Select a question..." and ans == "":
        messagebox.showerror("Error","Please fill all the values and then sign up...")
        txt_user.focus_set()
    elif user_name == "":
        messagebox.showerror("Error","Please enter username...")
        txt_user.focus_set()
    elif pwd == "":
        messagebox.showerror("Error","Please enter password...")
        txt_pass.focus_set()
    elif re_pwd == "":
        messagebox.showerror("Error","Please Re-Enter the password...")
        txt_repass.focus_set()
    elif question == "Select a question...":
        messagebox.showerror("Error","Please select a question...")
        combo_question.focus_set()
    elif ans == "":
        messagebox.showerror("Error","Please enter the answer...")
        txt_answer.focus_set()
    elif pwd != re_pwd:
        messagebox.showerror("Error","Password and Re-Entered password must be matched...")
        txt_repass.focus_set()
    else:
        sql = "Select * from login where username = %s"

        val = (user_name,)

        mycursor.execute(sql,val)

        myresult = mycursor.fetchall()

        if len(myresult)>0:
            messagebox.showwarning("Error","Username already allocated please enter another one...")
            txt_user.focus_set()
        else:
            sql_query = "insert into login (username,password,question,answer) values (%s,%s,%s,%s)"

            values = (user_name,pwd,question,ans)

            mycursor.execute(sql_query,values)

            mydb.commit()

            # print(mycursor.rowcount, "record inserted")
            messagebox.showinfo("Successfull","Signed up successfully...")

            txt_user.delete(0,'end')
            txt_pass.delete(0,'end')
            txt_repass.delete(0,'end')
            combo_question.current(0)
            txt_answer.delete(0,'end')
            txt_user.focus_set()

            
           

def move_login():
    win.destroy()
    import login_page

def close_function():
    win.destroy()

sign_up_btn=Button(win,text="Sign Up",cursor="hand2",fg="grey",bg="skyblue",font=("times new roman",20),command=sign_up).place(x=135,y=370,width=150,height=40)

go_to_login_btn=Button(win,text="Login",cursor="hand2",fg="grey",bg="skyblue",font=("times new roman",20),command=move_login).place(x=295,y=370,width=150,height=40)

close_btn=Button(win,text="Close",cursor="hand2",fg="grey",bg="skyblue",font=("times new roman",20),command=close_function).place(x=455,y=370,width=150,height=40)

# sign_up_label = Label(win,text="Sign up here...")
# sign_up_label.place(x=10,y=10,width=180,height=40)

# win.wm_attributes('-transparentcolor','grey')


win.mainloop()