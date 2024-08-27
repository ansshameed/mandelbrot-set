from tkinter import *
from tkinter import ttk
import os
import mandelbrotNEAOOP
import re 

#editing class is initialised as an object as its the main constructor of variables, buttons etc. when being called upon by the loginlogin module
#editWindow is the main Tk() root widget with dimensions of 700x500 constructued by .geometry and has title of Fractal Editing Window
#reg is for the entry input validation to ensure only floating point numbers or decimals 

class editing(object):
     def __init__(self):

          self.editWindow = Tk()
          self.editWindow.geometry("700x500")
          self.editWindow.title("Fractal Editing Window")
          reg = self.editWindow.register(self.inputValidation)

#editLabelTitle tells the user to input the values which are needed to enter such as the maximum iterations

          self.editLabelTitle = ttk.Label(self.editWindow, text="Input the values required: ", font = ("Calibri", 20)).place(x=125, y = 10)

#value = 50 is the default value input - recommended maximum iterations value
#validate="key" and registration used for exception handling of entry box 

          self.maximumIterationsInput = IntVar(self.editWindow, value=50)
          self.labelMaxIt = Label(self.editWindow, text="Maximum Iterations: ", width="25").place(x=27, y=150)
          self.maximumItEntry = Entry(self.editWindow, textvariable = self.maximumIterationsInput)
          self.maximumItEntry.place(x=170, y=150)
          self.maximumItEntry.config(validate="key", validatecommand=(reg, '%P'))
          

#self.sizeSelect is to monitor the string variable selected (the element selected from imageSizes list)
#self.sizeSelect.set uses and index for the second element in the imageSizes list to show as the default window size as its the smallest and allows quickest processing
#self.imageSizesDrop is the dropbox used for the image dimensions used. Uses the list of self.imageSizes as the options from the dropbox 

          self.labelDimensions = Label(self.editWindow, text="Image Dimensions: ", width="25").place(x=27,y=200) 
          self.imageSizes = ["320x200", "512x512", "640x480", "800x600", "1280x1024"]
          self.sizeSelect = StringVar(self.editWindow)
          self.sizeSelect.set(self.imageSizes[1]) 
          self.imageSizeDrop = OptionMenu(self.editWindow, self.sizeSelect, *self.imageSizes).place(x=170, y=200)


#Default is the standard RGB values selected by me, fire is a red theme, emerald is a light blue/green theme, ocean is a blue theme and sunset is a yellow/orange theme
#self.themesSelect is to monitor the string variable selected from the self.themes list in the dropbox
#self.themesSelect.set is used to set 'Default' as the default theme selected, also known as the first element in the list 



          self.labelColourThemes = Label(self.editWindow, text="Colour Themes: ", width="25").place(x=27, y=250)
          self.themes = ["Default", "Fire", "Sunset", "Ocean", "Emerald"]
          self.themesSelect = StringVar(self.editWindow)
          self.themesSelect.set(self.themes[0])
          self.themesDrop = OptionMenu(self.editWindow, self.themesSelect, *self.themes).place(x=170, y=250)


#self.ssInput is to monitor the decimal value of the value entered in the entry box also known as being a 'Double' rather than integer as scaling speed value is small
#value = 0.01 shows the default value of scaling speed. self.ssEntry is the entry box for the ssInput DoubleVar (scaling speed)
#validate used for exception handling for floating point numbers 

          self.ssLabel = Label(self.editWindow, text="Scaling Speed: ", width="25").place(x=27, y=300)
          self.ssInput = DoubleVar(self.editWindow, value=0.001)
          self.ssEntry = Entry(self.editWindow, textvariable = self.ssInput)
          self.ssEntry.place(x=170, y=300)
          self.ssEntry.config(validate="key", validatecommand=(reg, '%P'))
          

          self.applyButton = Button(self.editWindow, text="Apply Values",
                                 command = self.__apply)
          self.applyButton.place(x=100, y=350)

          self.warningIterations= Label(self.editWindow, text="WARNING: Maximum Iteration values over 500 may take more processing time: O(2^n)...",
                                                fg="red",font=("calibri", 11)).place(x=10, y=70) 
          self.warningDimensions = Label(self.editWindow, text=" LARGER THE WINDOW SIZE = LARGER THE PROCESSING TIME!",
                                 fg="red", font=("calibri", 11)).place(x=10, y=90)

#-------------------inputValidation-------------------------------
#Regular expression and isdigit used with if statements for exception handling of integers and floating point numbers for SS and maximum iteration entries
#Blank space also returns True ("") 

     def inputValidation(self, inp):
          p = re.compile('^(\d+)?([.]?\d{0,10})?$')
          if inp.isdigit() or p.match(inp): 
               return True
          elif inp == "":
               return True 
          else:
               return False

#----------------------setImageDimensions--------------------------
#imageSize is a 'getter' function to return the value of the image dimension selected for the fractal size in the window

     def __setImageDimensions(self):
          imageSize = self.sizeSelect.get()

#'if' statement is used to check is 'imageSize.txt' exists , if it does, then 'os' will remove it from directory
#It is removed so that whenever a new value is input then the file will be remade and the new value will be written rather than a file with lots of values
#'else' will print the file doesnt exist if the file does not exist in os 
          
          if os.path.exists("imageSize.txt"):
               os.remove("imageSize.txt")
          else:
               print("File doesn't exist!")

#imageDimensionsFile is to open the 'imageSizes.txt' in an append format to append the height and width of the dimensions needed
#if the imageSize is equal to (equal boolean operator) to the first element of the imageSizes list returned being 300x200.
          
          imageDimensionsFile = open("imageSize.txt", "a")
          if imageSize == self.imageSizes[0]:
               imageDimensionsFile.write(f"\n{320}")
               imageDimensionsFile.write(f"\n{200}")
               imageDimensionsFile.close()
          elif imageSize == self.imageSizes[1]:
               imageDimensionsFile.write(f"\n{512}")
               imageDimensionsFile.write(f"\n{512}")
               imageDimensionsFile.close()
          elif imageSize == self.imageSizes[2]:
               imageDimensionsFile.write(f"\n{640}")
               imageDimensionsFile.write(f"\n{480}")
               imageDimensionsFile.close()
          elif imageSize == self.imageSizes[3]:
               imageDimensionsFile.write(f"\n{800}")
               imageDimensionsFile.write(f"\n{600}")
               imageDimensionsFile.close()
          else:
               imageDimensionsFile.write(f"\n{1280}")
               imageDimensionsFile.write(f"\n{1024}")
               imageDimensionsFile.close()

#-------------------------setIterations----------------------------
#This function is used to set the maximum iterations value as entered by the user
#maximumIterations will return the maximum iterations value inputted in the main widget 

     def __setIterations(self):
         maximumIterations = self.maximumIterationsInput.get()
         
#'if' statement used to verify the maximum iterations value is only going to be processed and written to the file if the value is above 0
#The maximumIterations value returned from the entry box is written to the file using fractalFile.write

         while True:
               if maximumIterations > 0: 
                   if os.path.exists("maximumIterations.txt"):
                        os.remove("maximumIterations.txt")
                   else:
                         print("File doesn't exist!")
                   fractalFile = open("maximumIterations.txt", "a")
                   fractalFile.write(f"\n{maximumIterations}")
                   fractalFile.close()
                   return
                   self.maximumItEntry.delete(0, END)

#'else' used to show user that if the maximum iterations value is below 0 then it can not be processed, red font.
#return statement to show that while loop is now ended 
                   
               else:
                    labelTitle = Label(self.editWindow, text="Iterations can't 0 or below", fg="red",font=("calibri", 11))
                    labelTitle.place(x=40, y=93)
                    return

#--------------------------setThemes-----------------------------
#A 2D array is used for each set of RGB values for each theme
#2D array used as all sets of RGB values need to be stored in an array for access through file individually for colouring algorithm to loop through the rows 
#Default = Default theme chosen by me, Fire = Red theme, Ocean = Blue Theme, Emerald = Green/Turqoise theme, Sunset = yellow/orange theme 
#RGB values decided upon by the use of my RGB slider tool 

     def __setThemes(self):
          default = [[10, 5, 20],
                        [10, 10, 35],
                        [11, 20, 20],
                        [10, 7, 26],
                        [9, 1, 47],
                        [4, 4, 73],
                        [0, 7, 100],
                        [12, 44, 138],
                        [24, 82, 177],
                        [57, 125, 209],
                        [134, 181, 229],
                        [211, 236, 248],
                        [241, 233, 191],
                        [248, 201, 95],
                        [255, 170, 0],
                        [204, 128, 0],
                        [10, 5, 20]]
                        
          fire = [[230, 10, 20],
                        [250, 5, 5],
                        [240, 10, 10],
                        [235, 12, 12],
                        [220, 15, 15],
                        [216, 30, 40],
                        [200, 50, 90],
                        [195, 50, 90],
                        [200, 30, 20],
                        [57, 125, 209],
                        [134, 181, 229],
                        [211, 236, 248],
                        [241, 233, 191],
                        [248, 201, 95],
                        [255, 170, 0],
                        [204, 128, 0],
                        [230, 10, 20]]
                

          sunset = [[245, 117, 10],
                        [230, 110, 9],
                        [235, 104, 13],
                        [220, 100, 26],
                        [210, 90, 30],
                        [215, 95, 25],
                        [210, 85, 20],
                        [210, 44, 138],
                        [24, 82, 177],
                        [57, 125, 209],
                        [134, 181, 229],
                        [211, 236, 248],
                        [241, 233, 191],
                        [248, 201, 95],
                        [255, 170, 0],
                        [204, 128, 0],
                        [245, 117, 10]]

          ocean = [[17, 84, 174],
                        [10, 80, 170],
                        [15, 82, 175],
                        [20, 83, 162],
                        [27, 79, 172],
                        [30, 84, 163],
                        [57, 71, 167],
                        [80, 44, 138],
                        [70, 82, 177],
                        [57, 125, 209],
                        [134, 181, 229],
                        [211, 236, 248],
                        [241, 233, 191],
                        [248, 201, 95],
                        [255, 170, 0],
                        [204, 128, 0],
                        [20, 80, 190]]

          emerald = [[5, 150, 81],
                        [10, 160, 90],
                        [5, 170, 85],
                        [10, 160, 90],
                        [20, 175, 87],
                        [25, 190, 80],
                        [2, 160, 81],
                        [12, 44, 138],
                        [24, 82, 177],
                        [57, 125, 209],
                        [134, 181, 229],
                        [211, 236, 248],
                        [241, 233, 191],
                        [248, 201, 95],
                        [255, 170, 0],
                        [204, 128, 0],
                        [5, 150, 81]]
          
#'while True' loop used to check if 'mandelbrotThemes.'txt' exists in director. If it does exist in directory, it is in order to write the new RGB values from the
#--> 2D array according to what the user has chosen from drop down menu
#themesFile is the assignment for opening the 'mandelbrotThemes' file in append mode to append the RGB values into the text file

          colourTheme = self.themesSelect.get()
          while True: 
               if os.path.exists("mandelbrotThemes.txt"):
                    os.remove("mandelbrotThemes.txt")
               else:
                    print("File doesn't exist!")

               themesFile = open("mandelbrotThemes.txt", "a")


#The 'for row' loop is used to loop through every set of RGB values and the 'for item' loop is used to loop through every integer value within the RGB sets within
#--> the 2D array. 2 For loops used to loop through each set and then each value within the sets as its a 2D array
#For every item in the rows the value is written in string format with a space between them. For every row in text file it is written on a new file using "\n". 

               if colourTheme == self.themes[0]:
                    with open("mandelbrotThemes.txt", "wt"):
                       for row in default:
                           for item in row:
                               themesFile.write(str(item) + " ")
                           themesFile.write("\n")
                    return 
               
               elif colourTheme == self.themes[1]:
                    with open("mandelbrotThemes.txt", "wt"):
                       for row in fire:
                           for item in row:
                               themesFile.write(str(item) + " ")
                           themesFile.write("\n")
                    return 
               elif colourTheme == self.themes[2]:
                    with open("mandelbrotThemes.txt", "wt"):
                       for row in sunset:
                           for item in row:
                               themesFile.write(str(item) + " ")
                           themesFile.write("\n")
                    return 
               
               elif colourTheme == self.themes[3]:
                     with open("mandelbrotThemes.txt", "wt"):
                       for row in ocean:
                           for item in row:
                               themesFile.write(str(item) + " ")
                           themesFile.write("\n")
                     return
               else:
                    with open("mandelbrotThemes.txt", "wt"):
                       for row in emerald:
                           for item in row:
                               themesFile.write(str(item) + " ")
                           themesFile.write("\n")
                    return
                    

#------------------------------setSS---------------------------------------
#setSS is a function used to retrieve, return and write the scaling speed value. scalingSpeed returns the ssInput which is input into the entry box


     def __setSS(self):
          scalingSpeed = self.ssInput.get()

#'if' statements used to only process if the scaling speed is above float value of 0.0. ssFile is used open the 'scalingSpeed.txt' text file in notepad
#ssFile.write is used to write the scalingSpeed value on a new line using \n for direct access and then file is closed
#Once all the values have been input, mandelbrotNEAOOP.run() is used to call the main run() subroutine in the mandelbrotNEAOOP module

          while True:
               if scalingSpeed > 0.0:
                    if os.path.exists("scalingSpeed.txt"):
                         os.remove("scalingSpeed.txt")
                    else:
                         print("File doesn't exist!")
                    ssFile = open("scalingSpeed.txt", "a")
                    ssFile.write(f"\n{scalingSpeed}")
                    ssFile.close()
                    mandelbrotNEAOOP.run() 
                    return
               else:
                    labelTitle = Label(self.editWindow, text="Zooming/Scaling speed can not be 0 or below. Value above 1 is not not useful. Recommended: 0.1",  
                                       fg="red",font=("calibri", 11))
                    labelTitle.place(x=40, y=113)
                    return

     
#-----------------------apply----------------------
#This subroutine calls all the 'setter' functions used to write the values for mandelbrotNEAOOP module to read and use in calculations
     
                    
     def __apply(self): 
          self.__setImageDimensions() 
          self.__setIterations()
          self.__setThemes() 
          self.__setSS()

#--------------------editRun------------------------
#editRun() is used as a mainloop for the standard editWindow to enable all the buttons and labels to be called and run 
          
     def editRun(self):
          self.editWindow.mainloop()
          
#-------------------call----------------------------
#call function is outside the class to call class as an object of editCall with .editRun to call overall main editing window widget 
def call():
     editCall = editing()
     editCall.editRun()

#'if' statement is used to call this module and to not run straight away when it is called through loginlogin.py module 

if __name__ == "__main__":
     call() 

