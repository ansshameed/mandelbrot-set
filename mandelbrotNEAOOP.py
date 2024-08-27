from math import log, log2
import pygame
import csv
import sys

#----------------------------------STACK-(FILO) -------------------------------------
#Use of stack: To push on the fractal values when zooming in. Use stack to pop off the values in order to zoom out consectutively
#-->isEmpty:
# Checks to see if the stack is empty to prevent underflow errors when zooming out of image
#atleast one set of 'current boundaries' to be pushed onto the stack initially to load the fractal so list is always containing minimum 1 element.
#-->push:
#Pushes the current fractal zoom boundaries (values used to generate the fractal image) onto the stack. Standard '.append' list to add item to front of list
#-->pop:
#The pop function is used to return the last item pushed on the stack, in this case, the last image that was zoomed in and pushed onto the stack
#-->peek:
#To check the length of the list, it is printed and the top item from the list is returned, but not removed as it is just 'peeking'
#-->size:
#Returns the length of the stack (list) in the current point of runtime

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        if len(self.items) == 1:
            return True
        else:
            return False

    def push(self, item):
        self.items.append(item)

    def pop(self):
        retVar = self.items[len(self.items) - 1]
        self.items.pop()
        return retVar

    def peek(self):
        print(len(self.items))
        return self.items[-1]

    def size(self):
        return len(self.items)



class Queue():
    def __init__(self):
        self.queue = []

    def isEmpty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False

    def front(self):
        return self.queue[-1]

    def rear(self):
        return self.queue[0]

    def enqueue(self, a:int):
        self.a = a
        self.queue.append(a)

    def dequeue(self):
        self.queue.pop(0)


#-------------------------------------FRACTAL-----------------------------


#-------------------------------------__init__----------------------------
#SCALE is a constant to show the scale to which the image is being zoomed in. bounds is a variable used to as a list for the minimum and maximum values of x and y
#The bounds are used as each pixel has to represent a complex number (within the complex plane - cartesian coordinate system). The pixels are coloured with RGB values
#----> according to whether or not they belong to the Mandelbrot fractal set

class fractal():
    def __init__(self):
        self.zoomInOut = Stack()
        self.colourGrab = Queue()
        self.SCALE = 0.1
        self.bounds = (-2.5, -1.5, 1, 2.5)

#--------------------------Getter-Procedures------------
#These functions in OOP are defined to protect the data (variables/constants) when creating classes, hence, making them private variables which is standard OOP rule
#They all return the value

#--------------------------getScale---------------------
#Returns the scale constant (0.1)

    def getScale(self):
        return self.SCALE

#--------------------------getBounds-------------------
#Returns the boundary values

    def getBounds(self):
        return self.bounds

#------------------------getMaximumIt------------------
#Used to access the maximum iterations value according to what the user has set it as in the editing window. Opens the file and reads
#Context: This value is used to determine the maximum iterations of the fractal, higher the number the larger the processing time and more detail+quality of fractal

    def getMaximumIt(self):
        accessIterationsFile = open("maximumIterations.txt", "r")
        maximumItValue = accessIterationsFile.read()
        self.maximumItEntry = int(maximumItValue)
        return self.maximumItEntry

#-----------------------getScalingSpeed----------------
#Value is converted to a float for the format of calculations. The scaling speed is changes the rate at which the red, rectangular zooming box changes in size

    def getScalingSpeed(self):
        accessSSFile = open("scalingSpeed.txt", "r")
        ssValue = accessSSFile.read()
        self.scalingSpeed = float(ssValue)
        return self.scalingSpeed

#----------------------getImageDimensions--------------
#Used to retrieve the image dimension values according to what the user has set the values as in the editing window
#The file is organised for direct access (not sequential) as the values are written on separate lines for the convenience of access to height and width image values
#The values are retrieved from the option of the editing window as being standardised industry image dimension values. For PyGame window

    def getImageDimensions(self):
        accessImageSizeFile = open("imageSize.txt", "r")
        lines = accessImageSizeFile.readlines()
        HEIGHT = lines[1]
        WIDTH = lines[2]
        self.HEIGHT = int(HEIGHT)
        self.WIDTH = int(WIDTH)
        return self.HEIGHT, self.WIDTH

#--------------------getZoomSize-------------------------------
#Used to return the value of 'zoomSize' which determines the size of rectangular zooming box with the use of the scale and width of the image
#The width is multiplied by the scale as the scaling of the box is determined by how it stretches in the y direction with the aid of the rate of scale (zoom)

    def getZoomSize(self):
        self.zoomSize = self.WIDTH * self.SCALE
        return self.zoomSize

#-------------------getAspectRatio-----------------------
#The aspect ratio formula used below is the standardised formula for determining the relationship between the width and height of the window (image dimensions)
#This is used to maintain the correct ratio to ensure the overall resolution and proportionality of pixels is maintained. The aspect ratio value is returned

    def getAspectRatio(self):
        self.aspectRatio = self.WIDTH / self.HEIGHT
        return self.aspectRatio

#------------------getThemes------------------------------
#The 'for row' will read through every row in the text file and the 'strip' method is used to return a copy of the string by removing any leading and trailing
#--> characters. If there are no spaces, it will continue on to read through the file until there is a space (where the 2D array RGB values ends)
#The 'for RGB' loop will loop for every string in the file to split the strings in every row into a list for later use in the program when using the RGB values
#The self.colourBoundaries list will append the values from the colourRows list and the 2D array is returned

    def getThemes(self):
        self.colourBoundaries = []
        with open("mandelbrotThemes.txt") as themesFile:
            for row in themesFile:
                if not row.strip():
                    continue
                colourRows = []
                for RGB in row.split():
                    '''
                    self.colourGrab.isEmpty()
                    self.colourGrab.enqueue(int(RGB))
                    print("RGB value enqueued!")
                    self.colourGrab.isEmpty()
                    self.colourGrab.dequeue()
                    print("RGB value dequeued!")
                    '''
                    colourRows.append(int(RGB))
                self.colourBoundaries.append(colourRows)
        return self.colourBoundaries


#---------------mandelbrotCalculation------------
#Standard mathematical algorithm for Mandelbrot set . The starting location of the set is determines by the constant C. Starts with z = 0
#The resulting value is put into z and the original location is determined by C for the purpose of the iteration and the value of z is a mathematical reccurring loop
#Complex numbers are used a real and an imaginary part of it on the standard cartesian coordinate system of where the pixels are plotted upon

    def __mandelbrotCalculation(self, z, c):
        z = z * z + c
        return z

#-------------mandelbrotRecursion-----------------
#The fractal is limited to the value of 1 to determine which values calculated are part of the Mandelbrot set and which values are not. Coloured black if not in set.
#Then, the overall function is implemented through recursion, mandelbrotCalculation is called upon again until the base case is met.

    def __mandelbrotRecursion(self, z, c, iterations):
        if iterations <= 1 :
            return self.__mandelbrotCalculation(z, c)
        return self.__mandelbrotRecursion(self.__mandelbrotCalculation(z, c), c,
                                        iterations - 1)

#-----------checkRadiusLimit-----------------------
#It checks if Z went further than as a radius from the origin which therefore indicates which values are within the Mandelbrot set (radius of 2, diameter=4)
#This is the overall determinant for how many iterations are completed in each zoom before extending past radius of 2 where it is no longer part of the Mandelbrot set
#cRealSquared squares the constant c. Real and Imag(inary) are part of the complex numbers.

    def __checkRadiusLimit(self, c):
        cRealSquared = c.real * c.real
        cImagSquared = c.imag * c.imag
        return cRealSquared + cImagSquared > 4


#---------linearInterpolation-----------------------
#This is the standard linear interpolation calculation in the stasticial part of Mathematics for the colouring algorithm of the fractal
#The values are plugged into the equation whenever it is called upon by other functions in the class

    def __linearInterpolation(self, v0, v1, t):
        linearPEquation = (1 - t) * v0 + t * v1
        return linearPEquation

#---------colouring--------------------------------
#I used linear interpolation as part of my extension objectives for smooth colouring to render the normalised iteration count with bands of colours being replaced with
#--> a smoother colour gradient between each colourised pixel. #LinearP is carried out on the RGB values to determine the colour of pixels.
#Number of colours determines the detail of imagery of the colour. Higher the value, higher the processing time and colours become more enhanced.
#A nested for loop is used for the scaling and colouring of each and every x and y coordinate across the fractal according to the iterative values previously solved
#Looped through as a list where [i], [i+1]... to loop through all the overall sets of RGB values within the 2D array
#The values following such as [0], [1]... are used to plug in each RGB value within the overall sets in the 2D array into the linear interpolation calculation

    def __colouring(self):
        numberOfColours = 17
        colours = [(self.__linearInterpolation(self.colourBoundaries [i][0], self.colourBoundaries [i + 1][0],
                                    t / (numberOfColours / len(self.colourBoundaries ))),
                self.__linearInterpolation(self.colourBoundaries [i][1], self.colourBoundaries [i + 1][1],
                                    t / (numberOfColours / len(self.colourBoundaries ))),
                self.__linearInterpolation(self.colourBoundaries [i][2], self.colourBoundaries [i + 1][2],
                                    t / (numberOfColours / len(self.colourBoundaries ))))
               for i in range(-1, len(self.colourBoundaries ) - 1) for t in range(numberOfColours // len(self.colourBoundaries ))]
        return colours

#------assignColour--------------------------------
#The recursive algorithm now carried out for the colouring of the pixels to make sure the iterative values are under the maximum iterations value
#The initial recursiveZ variable is used to assign 0 to it for the start of the while loop of the 'mandelbrotCalculation' where the value of 0 and constant c are
#--> plugged in. recursiveZ used for recursion purpose.
#The RGB value of (0,0,0) is returned for when the value is exceeding the radius limit to colour the fractal black, indicating values not within the Mandelbrot

    def __assignColour(self, c, maximumItEntry, colours):
        i = 0
        recursiveZ = complex(0)
        while i < self.maximumItEntry:
            recursiveZ = self.__mandelbrotCalculation(recursiveZ, c)
            if self.__checkRadiusLimit(recursiveZ):
                return colours[i % len(colours)]
            i += 1
        return (0, 0, 0)

#---------smoothColouring-------------------------
#EXTENSION OBJECTIVE MET. #If the maximum iterations value is met, the overall function will halt and the value is retuned
#Once the while loop is finished, the standard log base 10 and log base 2 functions are applied to the recursive z value. Equation = 'potential function'

    def __smoothColouring(self, c, maximumItEntry):
        z = 0
        n = 0
        while abs(z) <=2 and n < self.maximumItEntry:
            z = z * z + c
            n += 1
            if n == self.maximumItEntry:
                return self.maximumItEntry
        return n + 1 - log(log2(abs(z)))

#-------convertToComplex-------------------------
#This is the standard mathmatical function used to convert the standard x and y coordinates to complex numbers e.g. (0 + 5j)
#The real part of the complex number is using linear interpolation with the x values and the width dimension of the image as the width corresponds to the x axis
#The equation assigned to the real variable calculates a resulting value for the displacement of the real part of the complex number
#The same equation is applied to the imaginary part of complex number for the displacement along the y axis
#Pixel coordinates are converted to complex number as part of the cartesian coordinate system

    def __convertToComplex(self, x, y, bounds=(-2.5, -1.5, 1, 1.5)):
        minimumX = bounds[0]
        maximumX = bounds[2]
        minimumY = bounds[1]
        maximumY = bounds[3]
        real = self.__linearInterpolation(minimumX, maximumX, x / self.WIDTH)
        imaginary = self.__linearInterpolation(minimumY, maximumY, y / self.HEIGHT)
        return complex(real, imaginary)

#------convertFromComplex------------------------
#Used to convert the x and y coordinate values plotted sequentially across the coordinate plan back to the complex number
#Standardised mathematical algorithm of the reverse of 'convertToComplex' function
#The complex numbers represent the distance/displacement between each pixel and the minimum/maximum values represent the corners of the coordinate cartesian plane
#The minumum, real part of the complex number is the left border of the image and the maximum, real part is the right border of the image
#The coordinates are calculated manually with the algorithm to disallow the image from stretching no matter what the dimensions are - could distort real part
#The subtraction of height and width is used to calculate the corner pixels of the fractal

    def __convertFromComplex(self, real, imaginary, bounds=(-2.5, -1.5, 1, 1.5)):
        minimumX = bounds[0]
        maximumX = bounds[2]
        minimumY = bpunds[1]
        maximumY = bounds[3]
        x = (real * self.WIDTH - self.WIDTH * minimumX) / (-minimumX + maximumX)
        y = (imaginary * self.HEIGHT - self.HEIGHT * minimumY) / (-minimumY + maximumY)
        return (x, y)



#------main--------------------------------------
#All the functions are called and pixels are plotted and colourised, also enabling the user to zoom in and out of the image

    def main(self):

#----Initialising-variables---------------------
#mousePosition is the variable to retrieve the current state of the mouse device
#screen is the variable to create an instance of the pygame window.
#imageRep is the image representation used in pygame surface function. Surface has a fixed resolution and pixel format. In an 8-bit pixel format to map 24-bit colours
#currentBounds is the current boundaries of each zoom within the zoom box

        mousePosition = pygame.mouse.get_pos()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        imageRep = pygame.Surface((self.WIDTH, self.HEIGHT))
        currentBounds = (-2.5, -1.5, 1, 1.5)


#The pygame image is drawn on using the current x and y coordinates. The assignColour function is called on the current x, y, and currentBounds. In addition, the
#--> the pixels are iterating and plotting onto the image according to the maximumItEntry. The colouring function is also called to colour the pixels
#zoomNumber is initialised to allow the user to zoom into the image
#The stack defined as the object 'zoomInOut' and the currentBounds are pushed on as the tracking of the bounds being used for the pixels and to call them once the user
#--> requests to zoom out.

        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                imageRep.set_at((x, y), self.__assignColour(self.__convertToComplex(x, y, currentBounds),  self.maximumItEntry,
                                                          self.__colouring()))
                self.__smoothColouring(self.__convertToComplex(x, y, currentBounds), self.maximumItEntry)
        zoomNumber = 1
        self.zoomInOut.push(currentBounds)

#sleepOver is defined as False to pause the program when needed (set as True) to minimise lag in case the user spams mouse clicks to frequently
#done is defined as False to indicate the interaction with the GUI from the user is not done yet (button clicking, zooming etc...)

        sleepOver = False
        done = False

#The functions to allow the user to interact with the pygame GUI is within the while loop until the user is done
#The mousePosition is once again initialised to track the movement of the current state of the mouse

        while not done:
            mousePosition = pygame.mouse.get_pos()

#pygame.event.get() for loop is used to register all the events of the interaction of the user into an abstract data type of a queue (FIFO) where actions are
#-->internally queued on internally in the pygame module to keep track of the users' actions
#Each event type is enqueued to the queue. buttons variable uses the internal pygame function, this returns a list of all the states of the keys being pressed
#Internal list contains 0 for all the keys not pressed and 1 for all keys which are pressed

            for event in pygame.event.get():
                buttons = pygame.key.get_pressed()


#EXIT program button

                if event.type == pygame.QUIT:
                    done = True
                    sys.exit()

#Calls the event type which will call the mouseClick function when the mouse button is clicked

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseClick(mousePosition, currentBounds, zoomNumber, imageRep, False)


#'if' BACKSPACE is clicked the fractal will zoom out by popping off last boundaries and checking if stack is empty
#The given parameters are assigned to 'params' to track the values and return the last used values on the stack to peek the top of the stack
#The mouseClick function is called for the fractal boundaries to be pushed on
#'if' statement used to check if the stack is empty preventing'out of range' error or 'underflow' error occurring on stack when attempting to zoom out with empty stack

            if buttons[pygame.K_BACKSPACE]:
                if self.zoomInOut.isEmpty():
                    pygame.display.set_caption("Can Not Zoom Out...")
                    continue
                else:
                    pygame.display.set_caption("Zooming out...")
                    self.zoomInOut.pop()
                    params = self.zoomInOut.peek()
                    self.mouseClick(mousePosition, params, zoomNumber, imageRep, True, currentBounds)


#'if' the UP arrow key is pressed, this will increase the overall size of the zoom rectangle box of where the user wishes to zoom
#'zoomSize' is used to maintain the size of the rectangle as the overall size is strethched out in the x direction


            if buttons[pygame.K_UP]:
                self.SCALE = min(1, self.SCALE + self.scalingSpeed)
                self.zoomSize = self.WIDTH * self.SCALE

#'if' the DOWN arrow key is pressed, the function is the similar concept to the UP arrow key being pressed but the reverse happens and the rectangle decreases the size


            if buttons[pygame.K_DOWN]:
                self.SCALE = max(0.01, self.SCALE - self.scalingSpeed)
                self.zoomSize = self.WIDTH * self.SCALE

#'if' the SPACE key (SPACEBAR) is pressed, the conversion to complex is called to print current position of mouse in a complex format for the fractal plane.

            if buttons[pygame.K_SPACE]:
                print(self.__convertToComplex(*mousePosition, currentBounds))

#'if' the 's' button is pressed (s for 'save') the current image of the fractal is saved to the user's default file directory of where pygame is installed

            if buttons[pygame.K_s]:
                pygame.image.save(screen, "MandelbrotFractal.jpeg")

#.blit is used to draw one image onto another which will draw the next fractal image when the image is zoomed in on
#imageRep represents the image being drawn and sets 0 as the initial values needed for the 'blit'
#pygame.draw.rect will draw the rectangle used to draw the red rectangular zoom box
#(255, 0, 0)=red RGB for the clear indication of zoom box. The caption is set to show retrieve the current mouse position of the user and print on top of the window.
#pygame.display.update() will update the display of the pygame window in runtime

            screen.blit(imageRep, (0, 0))
            pygame.draw.rect(screen, (255, 0, 0),
                         (mousePosition[0] - self.zoomSize / 2, mousePosition[1] - (self.zoomSize / self.aspectRatio) / 2,
                          self.zoomSize, self.zoomSize / self.aspectRatio), 1)
            pygame.display.set_caption(str(self.__convertToComplex(*pygame.mouse.get_pos(), currentBounds)))
            pygame.display.update()

#-----------mouseClick----------------------
#This function is the zooming into the fractal when the mouse button is clicked
#positionVar and 2 are the new boundaries of pixels being converted to complex numbers when zooming into the fractal as the boundaries and coordinates change
#Passes the calculation for obtaining the current mouse position and the size of the rectangular zooming box and dividing it by 2 as a parameter for the
#--> complex conversion. Current boundaries set to the last boundaries on stack using peek function.


    def mouseClick(self, mousePosition, currentBoundsP, zoomNumber, imageRep, useParams=False, currentBounds=False):
        currentBounds = self.zoomInOut.peek()
        pygame.display.set_caption("Processing...")
        positionVar1 = self.__convertToComplex(mousePosition[0] - self.zoomSize / 2, mousePosition[1] - (self.zoomSize / self.aspectRatio) /  2,
                                             currentBounds)
        positionVar2 = self.__convertToComplex(mousePosition[0] + self.zoomSize / 2, mousePosition[1] + (self.zoomSize / self.aspectRatio) /  2,
                                             currentBounds)

#useParams is set to the boolean value of False to indicate the parameters have not been used
#if useParams used to track progress of whether parameters have been used, if so, no zoom is made. Else, new boundaries calculated for zoom to track it with
#This is also evident of polymorphism as 'zoomInOut' is being used for different purposes such as zooming in and zooming out using push and pop in different cases
#The zoom number is then incremented and divided by the scale to finalise the zoom of the fractal and to readjust the zoom value of the image. Boundaries are pushed
#--> onto stack for later usage of zooming in/out


        if useParams:
            currentBounds = currentBoundsP
        else:
            currentBounds = (positionVar1.real, positionVar1.imag,
                             positionVar2.real, positionVar2.imag)
            self.zoomInOut.push(currentBounds)
        zoomNumber += 1 / self.SCALE

#For loop used as the height and width are finite which is complemented by the finite number of pixles within the fractal window for coordinated plotting on the plane
#The image is now set to the zoomed in fractal using the correct parameters and then it is saved to a list; '', for tracking purposes of values of parameters
#--> being used. pygame.event.clear used to clear the events of the user clicking the mouse button within the internal pygame module queue.
#This is used so that if the user double clicks, the program will not respond to the image being zooming in twice and therefore resulting in lag

        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                imageRep.set_at((x, y), self.__assignColour(self.__convertToComplex(x, y, currentBounds),
                                                 self.maximumItEntry + 4 * zoomNumber, self.__colouring()))
                imageSave = [(x, y), self.__assignColour(self.__convertToComplex(x, y, currentBounds),
                                                          self.maximumItEntry + 4 * zoomNumber, self.__colouring())]

        pygame.event.clear(pygame.MOUSEBUTTONDOWN)


#---------------------run-Subroutine--------------------------
#The 'get' functions are used to execute and return the required values needed to run the program in the different methods within the class. callFractal is the object
#--> of main Mandelbrot class. #callFractal.main() calls the main function within the class for the overall execution of the program

def run():
    pygame.init()
    callFractal = fractal()
    callFractal.getBounds()
    callFractal.getScale()
    callFractal.getImageDimensions()
    callFractal.getZoomSize()
    callFractal.getAspectRatio()
    callFractal.getMaximumIt()
    callFractal.getScalingSpeed()
    callFractal.getThemes()
    callFractal.main()

#This specific function disallows the program from being run as soon as it is imported from another module (editing window and main menu)
#The run function is called upon when 'mandelbrotNEAOOP' is called from another module; the editing window
#Actual function: When the Python interpreter reads a file the __name__ variable is set as __main__ if the module is being run or as modules name if it's imported

if __name__ == "__main__":
    run()
