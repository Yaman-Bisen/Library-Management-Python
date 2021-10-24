import cx_Freeze
import sys
import os
base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

os.environ['TCL_LIBRARY'] = r"C:\Users\Administrator\AppData\Local\Programs\Python\Python38\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\Administrator\AppData\Local\Programs\Python\Python38\tcl\tk8.6"

executables = [cx_Freeze.Executable("login_page.py",base=base,icon="library.ico")]

cx_Freeze.setup(
    name = "Library App",
    options = {"build_exe" : {"packages":["tkinter","os","mysql","tkcalendar"], "include_files":["library.ico",'tcl86t.dll','tk86t.dll','images','sign_up.py','forgotPass.py','master_page.py']}},
    verson = "0.01",
    description = "Tkinter Application",
    executables = executables
)