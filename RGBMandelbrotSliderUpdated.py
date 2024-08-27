from tkinter import *
#------------------------RGB-FUNCTIONS-----------------------------------

class mandelSlider:
    def __init__(self, *args):
#-------------------------MAIN-WIND0W-------------------------------------
#__init__ is used with *args and *kwargs to allow multiple keywords and arguments to be passed to functions later in the program
#The root window is constructed with the title, size (geometry) and resizeable disallows the user from changing the size of the window with boolean False value
#TopLevel must be used to be compatible with the main loginlogin window


        root = Tk()
        root.withdraw()
        self.RGBWindow  = Toplevel()
        self.RGBWindow.title("RGB Slider Mandelbrot") 
        self.RGBWindow.geometry("800x300")
        self.RGBWindow.resizable(False, False) 

#--------------------------SLIDER-LABELS----------------------------------
#Using .place for the placement of the RGB sliders to show user which colour the slider is interacting with 

        self.redLabel = Label(self.RGBWindow, text="R").place(x=100, y=65) 
        self.greenLabel = Label(self.RGBWindow, text="G").place(x=100, y=115)
        self.blueLabel = Label(self.RGBWindow, text="B").place(x=100, y=165) 

#-----------------------------SLIDER-VALUES-------------------------------
#These are the slider value for red, green and blue. IntVar is used because integer values are being used to set the RGB values as integers from 1 to 255

        self.redSliderValue= IntVar(name = 'redSliderValue')
        self.greenSliderValue= IntVar(name = 'greenSliderValue')
        self.blueSliderValue= IntVar(name = 'blueSliderValue')

#-----------------------------COLOUR-EXCEPTION-------------------------
#This is used to only allow the user to input the suitable values from 1 to 255 and only integers as an exception handling algorithm for the entry box 

        self.colouringCodes = StringVar()
        checkerReg = self.RGBWindow.register(self.__RGBLimits) 

#------------------------------------SLIDER-ENTRIES----------------------
#These are entry values for each slider. The entries must be within the given range of 1 to 255 for the standard RGB values. Used to prevent range and type errors 
#%P is the standard regex used for the validation of the exception handling in the entry box. 

        self.redEntry = Entry(self.RGBWindow, textvariable = self.redSliderValue)
        self.redEntry.config(validate = "key", validatecommand = (checkerReg, "%P"))

        self.greenEntry = Entry(self.RGBWindow, textvariable = self.greenSliderValue)
        self.greenEntry.config(validate = "key", validatecommand = (checkerReg, "%P"))
        

        self.blueEntry = Entry(self.RGBWindow, textvariable = self.blueSliderValue)
        self.blueEntry.config(validate = "key", validatecommand = (checkerReg, "%P"))
        
#-----------------------------------COLOUR-BINDING-------------------------
#.bind allows the slider to be adjusted to where the user inputs the valid of the RGB value manually
#For example, if the redEntry is the 255 the slider will bind up and adjust itself to the end of the slider where 255 to show red colour in box 
#Lambda is used as a nameless function for a short period of time between when the value is entered and when the slider itself is adjusted

        self.redEntry.bind(lambda _:self.__inputLimits(self.redSliderValue))
        self.greenEntry.bind(lambda _:self.__inputLimits(self.greenSlider))
        self.blueEntry.bind(lambda _:self.__inputLimits(self.blueSliderValue))
        self.redEntry.place(x=450, y=65, height=30, width=30)
        self.greenEntry.place(x=450, y=115, height=30, width=30)
        self.blueEntry.place(x=450, y=165, height=30, width=30) 

#---------------------------------HEX COLOURS-----------------------------
#This is the rectangle at the top of the screen to show the hexidecimal equivalent of the colour shown in the box 

        self.hexColours = Entry(self.RGBWindow, textvariable = self.colouringCodes, state = 'readonly', foreground = "#777").pack() 
 
#---------------------------------SLIDERS---------------------------------
#These are the sliders being constructed. The sliders can only go as far as the value of 255 as this is the standard RGB value allowed.
#from_ is 1 which is where it starts and to =255 where it ends. The slider placement is horizontal  

        self.redSlider = Scale(self.RGBWindow, from_ = 1, to = 255, length = 270, variable = self.redSliderValue, orient = HORIZONTAL)
        self.redSlider.place(x=150, y=50) 

        self.greenSlider = Scale(self.RGBWindow, from_ = 1, to = 255, length = 270, variable = self.greenSliderValue, orient = HORIZONTAL)
        self.greenSlider.place(x=150, y=100) 

        self.blueSlider = Scale(self.RGBWindow, from_ = 1, to = 255, length = 270, variable = self.blueSliderValue, orient = HORIZONTAL)  
        self.blueSlider.place(x=150, y=150) 
     

#-----------------------------SWATCH-RGB-REPRESENTATION-------------------
#colourBox is a canvas Tkinter Widget to show that the colour is being changed using #ffffff as the hexidecimal value for the max RGB value 

        self.colourBox = Canvas(self.RGBWindow, background='#ffffff', height=95, width=95)
        self.colourBox.place(x=500, y=80) 

#-----------------------------TRACING-BACK-SLIDER-VALUE------------------
#.trace_add is used in 'write' mode to set the colour and track it  to change the colour of the swatch according to the adjustment of the slider
        
        self.redSliderValue.trace_add("write", self.__settingFill)
        self.greenSliderValue.trace_add("write", self.__settingFill)
        self.blueSliderValue.trace_add("write", self.__settingFill)

        
#-----------------------------ASSIGNING-COLOURS--------------------------
#This is the main function used to assign the colour to the swatch canvas
#colourAssigned is the format specifier for the standard format of an RGB value. 02x is used to get 2 char outputs with mod function for each colour assignment 
#swatch.configure will change the background of the Tkiner colour canvas according to the RGB value calculated.
#Try and except used to try the values being entered, if not valid then it is passed 

    def __settingFill(self, *args):
        try:
            redAssign = int(self.redSliderValue.get())
            greenAssign = int(self.greenSliderValue.get())
            blueAssign = int(self.blueSliderValue.get())
            hexConvertor = ("#%02x%02x%02x")
            colourAssigned = hexConvertor % (redAssign, greenAssign, blueAssign)
            self.colourBox.configure(background = colourAssigned)
            self.colouringCodes.set(colourAssigned)
        except:
            pass

#---------------------------VALIDATING-HEX-COLOUR-RANGE-----------------
#Function use to validate the range of which hex values are allowed: 1-255
#If the value is equal to or above 1 AND equal to or below 255, it will return True and the sliders can run as normal
#If the value is empty, it will be returned as True and slider will be set to the start (value of 1)

    def __RGBLimits(self, inp):
        if inp.isdigit():
            if int(inp) >= 1: 
                if int(inp) <= 255: 
                    return True
            elif inp == "":
                return True
        elif inp == "":
            return True
        else:
            return False
        return False 
        

#---------------------------VALIDATING-SLIDER-ENTRY---------------------
#
#The slider will 'focus' depending on the input by the user 
    def __inputLimits(self, *args):
        textEntry = args[0]
        inputRGB = str(textEntry)
        if inputRGB == 'redSliderValue':
                self.redEntry.focus()
        elif inputRGB == 'blueSliderValue':
                self.blueEntry.focus()
        elif inputRGB == 'greenSliderValue':
                self.greenEntry.focus()

#-------------------------RUN-------------------------------------------
#Used to run the main root window in a main loop until it is exited 

    def run(self, *args):
        self.RGBWindow.mainloop() 

#--------------------------------MAIN-----------------------------------       
#callSlider is used as an object constructor to call the RGBHexConversion class
#.run() is used to call the 'run' function from the class using the callSlider object 

def main():
    callSlider = mandelSlider()
    callSlider.run() 

#Important if statement to make sure this module does not run straight away when importing into another module (loginlogin) 
if __name__ == '__main__':
    main()
            
