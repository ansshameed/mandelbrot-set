from tkinter import *
import os
import editing_window_updated
import time
import RGBMandelbrotSliderUpdated
import webbrowser
import string
from random import choice
import JuliaSetNEAExtension 


#---------------------------------------------SETUP-------------------------------------------


#'main' is the main parent class for the overall login and registry system
#'object' is used as a standard parameter for the class to show Python that this class is the main object constructor for the child/subclasses (login and register)
#__init__ used to initialise attributes of the class when inherited from subclasses. self.mainScreen is the main root window the main menu 

class main(object):
    def __init__(self):
        self.mainScreen = Tk()

#----------------__pack__---------------------------
#__pack__ is the setting of the essential labels and titles needed within the main menu window (mainScreen)
#'pack()' is used in Tkinter to pack the widgets into rows and columns, .geometry used to fix the window size, .title uses for the main title of the window

    def __pack__(self):

        self.mainScreen.geometry("600x600")
        self.mainScreen.title("Main Menu")

#'Welcome' label at top of the screen. Pack used to place it in adjusted place
#'Click register' label to let user register. 'Login button used to call the subclass login when the button is pressed
#"" label is used to create a slight space between buttons to organise buttons for the user to show them clearly so they do not overlap
#Register button used to call the subclass register when the button is pressed. Guest button is used to call the 'access' function which will call the editing window
#RGB Slider used to call the RGB slider module. Help button used to access a notepad for the help menu 


        Label(text = "Welcome!", width ="300", height = "2", font = ("Calibri", 12)).pack()
        Label(text = "Click register if you do not have an account.", width="300", height="2", font = ("Calibri", 12)).pack()
        Button(text="Login", width="30", height ="2", font = ("Calibri", 15), command=login).pack() 
        Label(text="").pack()
        Button(text="Register", width = "30", height = "2", font = ("Calibri", 15), command = register).pack()
        Label(text="").pack()
        Button(text="Guest", width="30", height="2", font = ("Calibri", 15), command=self.access).pack()
        Label(text="").pack()
        Button(text="Julia Set Preview", width="30", height="2", font = ("Calibri", 15), command=self.juliaSet).pack()
        Label(text="").pack() 
        Button(text="RGB Slider", width="30", height = "2", font = ("Calibri", 15), command=self.__accessSlider).pack()
        Label(text="").pack()
        Button(text="Help", width="30", height="2", font = ("Calibri", 15), command=self.__helpMenu).pack()
        Label(text="").pack()


#---------------------helpMenu-------------------------------
#webbrowser is used to directly open the notepad text file of the help document for the user's benefit and knowledge behind how the program works

    def __helpMenu(self):
       webbrowser.open("NEAMandelbrotControls.txt") 
        

#----------------------accessSlider--------------------------
#accessSlider is used to access the RGB Slider which calls the RGBSliderMandelbrot module when the 'RGB Slider' button is clicked

    def __accessSlider(self):
        RGBMandelbrotSliderUpdated.main()

#----------------------juliaSet------------------------------
#juliaSet is used to access the Julia set preview 

    def juliaSet(self):
        JuliaSetNEAExtension.Julia() 


#---------------------access----------------------------------
#access is used to access the editing window from the module 'editing_window_updated' when clicked on 'Guest' button or when login is successful
#time.sleep(1) used to allow some delay in between editing window showing and when being accessed 

    def access(self):
        time.sleep(0.5) 
        editing_window_updated.call()

#-------------------run---------------------------------------
#run used as the main calling of the tkinter main menu
#.mainloop() allows for Python to run the tkinter event loop for events such as button clicking and any code after this loop will not run until the window is closed 

    def run(self):
        self.mainScreen.mainloop()

#--------------------------------------------DESTROY---------------------------------------
#Used to destroy the widget. Grouped into one class for the ease of access when destroying certain windows/widgets

class destroy(main):
    def delete(self):
        self.mainScreen.destroy()
    def delete1(self):
        self.loginScreen.destroy()
    def delete2(self):
        self.registerScreen.destroy() 


#--------------------------------------------REGISTER---------------------------------------    
#register class is inherited from the parent class of 'main'
#super().__init() is used to give acces to the methods and attributes of the parent class - 'main'. This will return the object representing the parent class
#super will be used to access attributes such as the 'mainScreen' Tk root - inheritance is used here between child class of register to parent class of 'main'

class register(main):
    def __init__(self):
        super().__init__()

#Toplevel is used when closing the window so all children widgets are destroyed (register window) but the program will not shut down in case the user wants to just
#--> close the register window for the meantime.

        self.registerScreen = Toplevel()
        self.mainScreen.withdraw()
        self.registerScreen.geometry("500x600")
        self.registerScreen.title("Register")

#StringVar is used to directly accessing and interpreting the variables when the entry of the user is needed e.g. self.username will be used when helper functions
#--> in the class need to acccess the entry of the username entered by the user
#self.email is for the string variable of the email address, self.password is the password chosen and password2 is the confirmation (second entry) of the password

        self.username = StringVar()
        self.email = StringVar()
        self.password = StringVar()
        self.password2 = StringVar()

#Entry is the entry box for each required field for username, password, password2 and email

        self.createAccountLabel = Label(self.registerScreen, text = "Create an account", font = ("Calibri", 20)).place(x=50,y=3)
    
        self.detailsTitle = Label(self.registerScreen, text = "Please, fill in the details below in order to register").place(x=90, y=50)
        self.requiredTitle = Label(self.registerScreen, text = "* indicates a required field", fg = "red").place(x=140, y=73)

        self.labelUser = Label(self.registerScreen, text ="Username", width = "25").place(x=30, y=130)
        self.labelRequiredUser = Label(self.registerScreen, text="*", fg = "red").place(x=335, y=130)
        self.usernameEntry = Entry(self.registerScreen, textvariable = self.username)
        self.usernameEntry.place(x=170, y=130)

        self.labelEmail = Label(self.registerScreen, text ="Email address", width = "25").place(x=17, y=170)
        self.emailEntry = Entry(self.registerScreen, textvariable = self.email)
        self.emailEntry.place(x=170, y=170)
    
        self.labelPassword = Label(self.registerScreen, text ="Password", width = "25").place(x=31, y=210)
        self.labelRequiredPassword = Label(self.registerScreen, text="*", fg = "red").place(x=335, y=210)
        self.passwordEntry = Entry(self.registerScreen, textvariable = self.password, show = '*')
        self.passwordEntry.place(x=170, y=210)

        self.labelConfirm = Label(self.registerScreen, text ="Confirm", width = "25").place(x=35, y=250)
        self.labelRequriedConfirm = Label(self.registerScreen, text="*", fg = "red").place(x=335, y=250)
        self.confirmEntry = Entry(self.registerScreen, textvariable = self.password2, show = '*')
        self.confirmEntry.place(x=170, y=250)

        self.labelNameReq = Label(self.registerScreen, text="Username is maximum 20 characters").place(x=90, y=290)
        self.labelPassReq = Label(self.registerScreen, text="Password must be minimum 8 characters with numerical characters included").place(x=90, y=310)
        

#Register button is used to call upon the 'registrationComplete' function with .self as it is in the same class

        Button(self.registerScreen, text="Register", width=20, bg="brown", fg="white", command = self.__registrationComplete).place(x=160, y=490)

        
#--------------------registrationComplete------------------------------------
#This function is used to verify the user's details to make sure they match the username, email and password requirements and write to file if criteria met 

    def __registrationComplete(self):

#userName info is used as a 'getter' function to return the value entered by the user in the entry box which is a string variable (StringVar)
#These are private variables used only within this function 

        usernameInfo = self.username.get()
        passwordInfo = self.password.get()
        password2Info = self.password2.get()
        emailInfo = self.email.get()


#Used regular expression for precise detail of the criteria being met for the password, username and email (used for revision purpose within Comp Sci)
#The usernameInfo (username entry) must be equal to or below 20 characters and password regex criteria allows for upper and lower case letters with digits 0-9 and with
#--> selected symbols being: @#$%^&+= to maintain simplicity of login system when writing using direct access to write registry details to file
#boolean 'and' used within if statement as all criteria MUST be met before next if statement in nested structure - checks all entry boxes are not empty with != ''
#if statement validates the email entry with upper and lower case letters allowed with no unusual symbols in the emailInfo (StringVar). There must be an @
#--> symbol followed by form of '.' If email regex criteria not met, labelInvalidEmail shown to indicate email is invalid, red font and it is returned 
#Next if statememt validates whether or not the password2info (password confirmation) matches the initial password (passwordInfo) using == boolean operator and breaks

        while True:

            if len(usernameInfo)<=20 and re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', passwordInfo) and usernameInfo != '' and passwordInfo != '' and password2Info != '' and emailInfo != '':
                if re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+[a-zA-Z]*$',emailInfo):
                    if password2Info == passwordInfo:
                        break

                    else:
                        labelNoMatch = Label(self.registerScreen, text=" Passwords don't match  ", fg="red",font=("calibri", 11)).place(x=40, y=93)
                        return
                else:
                    labelInvalidEmail = Label(self.registerScreen, text="Please enter a valid email address", fg="red", font=("calibri", 11)).place(x=70, y=93)
                    return
            else:
                labelFillRequired = Label(self.registerScreen, text="           Please fill the required fields", fg="red", font=("calibri", 11)).place(x=70, y=93)
                return


#file is used to open the 'usernameInfo.txt' file
#file.write is used with direct access to write to the file the usernameInfo, passwordInfo and emailInfo once the regex criteria has been met
#\n is used to separate the information out for convenience of reading from the file when writing to a new file each time
#file is closed once written correct information
 
        file = open(usernameInfo+".txt", "w")
        file.write(usernameInfo+"\n")
        file.write(passwordInfo+"\n")
        file.write(emailInfo+"\n")
        file.close()

#Entry values within the entry boxes are deleted with (0,END) used as index to delete very first value to last to show the user it is now complete and if they wish
#---> to make another account they do not have to delete previous details in the entry boxes themself 

        self.usernameEntry.delete(0, END)
        self.passwordEntry.delete(0, END)
        self.emailEntry.delete(0, END)
        self.confirmEntry.delete(0, END)

#labelSuccess is a label on register window to show registration is a success in a green font 

        labelSuccess = Label(self.registerScreen, text="Registration success, you can now log in with your user", fg="green", font=("calibri", 11)).place(x=50, y=93)

#if statement via OS to remove previous password file for Vernam cipher (plaintext)
#open file statements used to open the files used for the paramaters of the Vernam encryption
#Vernam cipher function called with necessary files for encryption; plaintext (password), ciphertext, one time pad 
        if os.path.exists("vernamPass.txt"):
            os.remove("vernamPass.txt")
        else:
            print("File doesn't exist") 
        mPass = open("vernamPass.txt", "w")
        mPass.write(passwordInfo)
        mPass.close() 
        cText = open("ciphertext.txt", "w")
        cText.close() 
        accessOTP = open("oneTimePad.txt", "w")
        accessOTP.close() 
        self.vernamCipher("vernamPass.txt", "ciphertext.txt", "oneTimePad.txt")

#---------------------------vernamCipher--------------------------------
#randomised one time pad created using the 'string' library to randomise a character from ASCII table
#The plaintext file is read (password). OTP, plaintext and ciphertext files are opened.
#for loop used to read through all lines of the plaintext file and OTP written in same length of plaintext as one of the Vernam criterias to meet
#Encrypted ciphertext is written using algorithm of using 'chr' to generate the character format and 'ord' is used to generate the integer ASCII format for
#--> decryption of ciphertext 

    def vernamCipher(self, plaintext, ciphertext, OTP):
        randomOTP = (string.ascii_lowercase + string.ascii_uppercase
                     + string.digits)

        accessRegPass = open("vernamPass.txt", "r")
        passwordEncrypt = accessRegPass.read()
        #test: print("pass: ", passwordEncrypt) 

        with open(plaintext) as original:
            with open(OTP, "w") as oneTimePad:
                with open(ciphertext, "w") as encrypted:
                    for line in original.readlines():
                        for i in range(len(line)): 
                            calculatedOTP = choice(randomOTP)
                            oneTimePad.write(calculatedOTP)
                            encrypted.write(chr(ord(line[i])^ord(calculatedOTP)))
 
#-----------------------------------------LOGIN---------------------------------------------
#super().__init__() used to inherit the attributes of the main window from the main parent class
#TopLevel used with self.mainScreen used as a paramater to indicate that this screen should still show when closed to allow the user to still access the main menu
#Standard labels and titles used for similar purposes as the __init__ in register class as a constructor for private attributes
#withdraw to prevent extra widget being opened

class login(main):
    def __init__(self):
        super().__init__()

        self.loginScreen = Toplevel(self.mainScreen)
        self.loginScreen.title("Login")
        self.mainScreen.withdraw()
        self.loginScreen.geometry("500x300")

        Label(self.loginScreen, text="Please enter details below to login").pack()
        Label(self.loginScreen, text="").pack()

        self.usernameVerify = StringVar()
        self.passwordVerify = StringVar()

        Label(self.loginScreen, text="Username * ").pack()
        self.usernameEntry1 = Entry(self.loginScreen, textvariable = self.usernameVerify)
        self.usernameEntry1.pack()
        Label(self.loginScreen, text="").pack()

        Label(self.loginScreen, text="Password * ").pack()
        self.passwordEntry1 = Entry(self.loginScreen, textvariable = self.passwordVerify, show = '*')
        self.passwordEntry1.pack()
        Label(self.loginScreen, text="").pack()

#Login button used to call the function of loginVerify to verify the login details entered to check if criteria is matched

        Button(self.loginScreen, text = "Login", width = 10, height = 1, command = self.__loginVerify).pack()

#---------------------------------loginVerify-----------------------------------------

    def __loginVerify(self):

#username1 is used as a 'getter' function for the username entry in the login window to return the StringVar entry, same purpose for password1
#.delete(0,END) is used to delete the entry details once the user clicks login so if the details are needed to be retyped they do not have to backspace it all or
#--> if they need to make another account it is already deleted from entry box from index 0 to END (last character of entry box) 

        username1 = self.usernameEntry1.get()
        password1 = self.passwordEntry1.get()
        self.usernameEntry1.delete(0, END)
        self.passwordEntry1.delete(0, END)

#This is an internal private class within the loginVerify function which prints a label showing the username or password are invalid, with red font
#__invalid__prompt is called when the username or password are not recognised. _empty__prompt is called when the username and/or password entry fields are empty 

        def __invalid_prompt():
            labelInvalid = Label(self.loginScreen, text="Invalid username or password", fg="red", font=("calibri", 11)).place(x=135, y=19)

        def __empty_prompt():
            labelEmpty = Label(self.loginScreen, text="Empty fields --> Enter Details", fg="red", font=("calibri", 11)).place(x=135, y=25)

#if statement for boolean OR to check empty fields of password/username             

        if (len(self.usernameEntry1.get()) or len(self.passwordEntry1.get())) == 0:
            __empty_prompt()
            
            
#try and except statement is used to catch and handle exceptions, in this case, reading the details of 'username1' file
#Opens the file according to the username which is entered, if it is not found in the text format when reading it ("r"), then the except state shows a
#--> FileNotFoundError to indicate the file is not found and therefore the username entered is not registered to the system
#If the except statement is met with invalid input, __invalid_prompt() is called to show the username or password is invalid and return statement is used 
            
        try: 
            userInfoFile = open(username1+".txt", "r")
        except FileNotFoundError: 
            __invalid_prompt()
            return

#within the file, the userData is read line by line as it is split using \n. print statement used for testing purpose with tuple 

        userData = userInfoFile.read().split("\n")
    
#Standard 'if' statement used with boolean 'and' to check whether the password entry matches the password in the file if username complementing the password is also
#--> matched to the username entered
#'else' used to call __invalid_prompt() to show username and password are invalid, return statement. Direct OS access used to remove previous decrypted login
#Decryption file is created using open stateent and decrypter is called with parameters of appropriate files
                                            
                                                    
        if password1 == password and username1 == username:
            if os.path.exists("decryptionRev.txt"):
                os.remove("decryptionRev.txt")
            else:
                print("File doesn't exist!")
            decryptPass = open("decryptionRev.txt", "w") 
            decryptPass.close() 
            self.vernamDecrypter("ciphertext.txt", "decryptionRev.txt", "oneTimePad.txt")
            self.access()
            return
        else:
            __invalid_prompt()
            return

#----------------------vernamDecrypter----------------------
#All necessary files are opened and try, except statement used to decrypt if the file exsits using the decryption algorithm designed
    
    def vernamDecrypter(self, ciphertext, reverse, OTP):
        with open(ciphertext) as encrypted:
            with open(OTP) as accessOTP:
                with open(reverse, "w") as decryption:
                    try: 
                        while True:
                            decryption.write(chr(ord(encrypted.read(1))^ord(accessOTP.read(1))))
                    except:
                        pass
        

#-------------------------------------------------MAIN---------------------------------------
#mainRunning function used to call the parent class main() which therefore is called upon by register and login sub/child classes with inheritance
#__pack__() is called for the private attributes in the main widget
#.run() used for mainloop of main widget 

def mainRunning():
    mainCall = main()
    mainCall.__pack__()
    mainCall.run()

#if statement used in case another module is used to access loginlogin.py which won't be run as soon as it is imported
#mainRunning() subroutine is called 

if __name__ == "__main__":
    mainRunning()
