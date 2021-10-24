from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector

win = Tk()
win.title("Forgot password...")
win.geometry("738x416+400+150")
win.resizable(False,False)

bg_color = Label(win,bg="lightblue").place(x=0,y=0,relwidth=1,relheight=1)

def create_frame_check():
    Frame_check = Frame(win,bg = "white")
    Frame_check.place(x=120,y=15,height=380,width=500)

    lbl_user = Label(Frame_check,text="Username :",font=("Goudy old style",15,"bold"),fg="grey",bg="white").place(x=75,y=50)

    txt_user = Entry(Frame_check,font=("times new roman",15),bg="lightblue")
    txt_user.place(x=75,y=90,width=350,height=35)
    txt_user.focus_set()


    lbl_question = Label(Frame_check,text="Select question :",font=("Goudy old style",15,"bold"),fg="grey",bg="white").place(x=75,y=130)

    combo_question = ttk.Combobox(Frame_check,font=("times new roman",15))
    combo_question.place(x=75,y=170,width=350,height=35)
    combo_question["values"] = [('Select a question...'),('What is your pet name ?'),('What is your age ?'),('What is your school name ?'),('What is your mother name ?')]
    combo_question.current(0)
    combo_question['state'] = 'readonly'

    lbl_answer = Label(Frame_check,text="Answer :",font=("Goudy old style",15,"bold"),fg="grey",bg="white").place(x=75,y=210)

    txt_answer = Entry(Frame_check,font=("times new roman",15),bg="lightblue")
    txt_answer.place(x=75,y=250,width=350,height=35)

    def check_func():
        user_name = txt_user.get()
        question = combo_question.get()
        ans = txt_answer.get()

        if user_name == "" and question == "Select a question..." and ans == "":
            messagebox.showwarning("Warning","Please fill all the values...")
            txt_user.focus_set()
        elif user_name == "":
            messagebox.showwarning("Warning","Please enter your username...")
            txt_user.focus_set()
        elif question == "Select a question...":
            messagebox.showwarning("Warning","Please select the question...")
            combo_question.focus_set()
        elif ans == "":
            messagebox.showwarning("Warning","Please enter your answer...")
            txt_answer.focus_set()
        else:
            mydb = mysql.connector.connect(
                host = "localhost",
                user = "yaman",
                password = "yaman",
                database = "pythondatabase"
            )

            mycursor = mydb.cursor()

            sql = "Select * from login where username = %s and question = %s and answer = %s"

            val = (user_name,question,ans)

            mycursor.execute(sql,val)

            myresult = mycursor.fetchall()

            if len(myresult)>0:

                Frame_check.destroy()

                Frame_reset_pass = Frame(win,bg = "white")
                Frame_reset_pass.place(x=120,y=15,height=380,width=500)
                
                create_button()

                lbl_pass = Label(Frame_reset_pass,text="New Password :",font=("Goudy old style",15,"bold"),fg="grey",bg="white").place(x=75,y=80)

                txt_pass = Entry(Frame_reset_pass,font=("times new roman",15),bg="lightblue",show="*")
                txt_pass.place(x=75,y=120,width=350,height=35)

                lbl_repass = Label(Frame_reset_pass,text="Re-Enter New Password :",font=("Goudy old style",15,"bold"),fg="grey",bg="white").place(x=75,y=160)

                txt_repass = Entry(Frame_reset_pass,font=("times new roman",15),bg="lightblue",show="*")
                txt_repass.place(x=75,y=200,width=350,height=35)

                def change_pass():
                    pwd = txt_pass.get()
                    repass = txt_repass.get()
                    
                    if pwd == "" and repass == "":
                        messagebox.showwarning("Warning","Please fill all the fields...")
                        txt_pass.focus_set()
                    elif pwd == "":
                        messagebox.showwarning("Warning","Please enter new password...")
                        txt_pass.focus_set()
                    elif repass == "":
                        messagebox.showwarning("Warning","Please RE-enter new password...")
                        txt_repass.focus_set()
                    elif pwd != repass:
                        messagebox.showerror("Erro","password and re-entered password must be matched...")
                    else:

                        ###############################################################
                        sql_query = "update login set password = %s where username = %s"

                        values = (pwd,user_name)

                        # print(values)

                        mycursor.execute(sql_query,values)

                        mydb.commit()

                        # print(mycursor.rowcount, "record inserted")
                        messagebox.showinfo("Successfull","password changed successfully...")


                change_button =Button(Frame_reset_pass,text="Change",cursor="hand2",fg="grey",bg="skyblue",font=("times new roman",20),command=change_pass).place(x=175,y=280,width=150,height=40)
            else:
                messagebox.showerror("Error","Invalid info...")

    submit_button =Button(Frame_check,text="Submit",cursor="hand2",fg="grey",bg="skyblue",font=("times new roman",20),command=check_func).place(x=175,y=300,width=150,height=40)

def create_button():
    go_to_login_btn=Button(win,text="Login",cursor="hand2",fg="grey",bg="skyblue",font=("times new roman",20),command=move_login).place(x=135,y=370,width=150,height=40)

    close_btn = Button(win,text="Close",cursor="hand2",fg="grey",bg="skyblue",font=("times new roman",20),command=close_function).place(x=455,y=370,width=150,height=40)

def move_login():
    win.destroy()
    import login_page

def close_function():
        win.destroy()


create_frame_check()
create_button()

win.mainloop()