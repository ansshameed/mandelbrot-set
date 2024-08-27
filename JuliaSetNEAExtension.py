#--------------EXTENSION-JULIA-SET----------------
#importing necessary libraries and initialising pygame for OOP 
import pygame
import math
from pygame.locals import *
import sys 
 
pygame.init()

#--------------------------juliaFractal---------------------------
#jBounds is the boundaries for the X and Y values for the corners of plotting pixels and RES is the resolution value. Blend type is for colouring.
#jMaxIt is the maximum iterations for the Julia set which determines the resolution and how transparent the image is. C is the complex constant for the 'z' iteration
#--> equation; used to determine the iterations too in the standard calculations for the Julia set. 

class juliaFractal():
    def __init__(self):
        self.width = 512
        jBounds = [-1.6, -1, 1, 1.6]
        self.minimumX = jBounds[0]
        self.maximumX = jBounds[3]
        self.minimumY = jBounds[1]
        self.maximumY = jBounds[2]
        self.RES = 1
        self.jMaxIt = 2000
        self.blendType = 1
        self.C = complex(-0.79, 0.155)

#-------------------setBoundaries----------------------------
#Used to set the boundary values into float values for the purpose of formatting for calculation 
  

    def setBoundaries(self):
        self.minimumX = float(self.minimumX)
        self.maximumX = float(self.maximumX)
        self.minimumY = float(self.minimumY)
        self.maximumY = float(self.maximumY)
        return self.minimumX, self.maximumX, self.minimumY, self.maximumY

#------------------setHeight-----------------------------------
#Standard calculation used for the height of the Julia set window as discovered in research of the Julia set fractal.
#Converted to integer for formatting purposes for later calculations 

    def setHeight(self):
        height = (self.maximumY - self.minimumY) * float(self.width) / (self.maximumX - self.minimumX)
        self.height = int(height) 
        return self.height

#------------------setDisplay-----------------------------------
#dimensions used with width and height values calculated and set. Surface used to initiate the pygame window
#juliaScreen uses format of PixelArray from PyGame to plot the rows of data for the Julia set to speed up optimisation results

    def setDisplay(self):
        imageDimensions = self.width, self.height
        surface = pygame.display.set_mode(imageDimensions)
        self.juliaScreen = pygame.PixelArray(surface)
        return self.juliaScreen

#-----------------setIteration-----------------------------------
#Standard calculation from research for the number of increments according to other values in program when mapping the pixels to points in the complex Julia plane 

    def setIteration(self):
        self.incrementNo = self.RES * ((self.maximumX - self.minimumX)/(float(self.width)))
        return self.incrementNo

#---------------complexToX---------------------------------------
#Calculation for converting the X coordinates for the mapping of the pixels in the complex Julia plane by calculating equivalent complex values for pixel conversion
#plotting is the variable when calling this function to plug in the current coordinate value for the pixel conversion

    def complexToX(self, plotting):
        return int(((self.width)/(self.maximumX - self.minimumX) * plotting) + (self.width * self.minimumX) / (self.minimumX - self.maximumX))

#--------------complexToY-----------------------------------------
#Same algorithm as the complexToX function but with the use of Y coordinates and using height rather than width
    
    def complexToY(self, plotting):
        return int(((self.height)/(self.minimumY - self.maximumY) * plotting) + (self.height * self.maximumY) / (self.maximumY - self.minimumY))

#--------------juliaIteration--------------------------------------
#This is the main calculation used for the iteration and the range of pixels being plotted
#%10.5f is the standard format for plotting the axes necessary for the julia set and the values are converted to float in itValues where the iteration values are
#--> stored in a list format
#the base is the beginning of the iteration and it stops once the condition (base case) is met in the while loop where the increments are calculated

    def juliaIteration(self, initiate, halt, iteration):
        base = initiate
        axesPlot = ('%10.5f' % base) 
        itValues = [float(axesPlot)]
        while base < halt:
            base += iteration
            itValues = itValues + [float('%10.5f' % base)]
        return itValues

#-------------juliaPlot--------------------------------------------
#The positions are calculated to store the values being increments and therefore iterated for storing the necessary axis points by calling juliaIteration
#Position 1 is for the x coordinate and therefore the width of the axes. The conversion to X is called for the x coordinate of the pixels to convert to coordinates
#The axes in the x position (1) is then using the conversion and the RGB values of 255, 255, 255 to show the user the centre of the axis with the white line
#The same process is repeated for the 'for' loop in the y coordinates for position 2 but here the y coordinates and pixels are converted
#pygame.display.update() is used to plot the axes in run time on the pygame display 

    
    def juliaPlot(self):
        position1 = self.juliaIteration(self.minimumX, self.maximumX, self.incrementNo)
        position2 = self.juliaIteration(self.minimumY, self.maximumY, self.incrementNo)
        for x in position1:
            self.juliaScreen[self.complexToX(x) - 1, self.complexToY(0)] = (255, 255, 255)
        for y in position2:
            self.juliaScreen[self.complexToX(0), self.complexToY(y) - 1] = (255, 255, 255) 
        pygame.display.update()

#-----------drawJulia----------------------------------------------
#the positionX and positionY are the same as the position 1 and 2 in the juliaPlot function but the function is called upon again for the plotting of the pixels
#---> rather than the axes itself
#2 is the radius limit until the Julia set escapes and it is not counted anymore
#The plotting fill is the transparency of the set itself and 80 shows full visibility of the set with corresponding RGB values too
#The colourblend is the standard RGB values for the set
    

    def drawJulia(self):
        pygame.display.set_caption("Julia Set Preview")
        positionX = self.juliaIteration(self.minimumX, self.maximumX, self.incrementNo)
        positionY = self.juliaIteration(self.minimumY, self.maximumY, self.incrementNo)
        radiusLimit = 2 
        plottingFill = 80
        colourBlend = (255, 90, 90)

#The x and y 'for' loops are for the plotting of the x and y coordinates with the conversion to pixels
#z is the standard iteration equation for the Julia set which is the same as the Mandelbrot set equation where complex values are used for the complex plan (x,y)
#currentP is the final value of the iteration which is calculated. i = 0 is to initialise the loop.
#The while loop is looping through the iteration until the radius limit is met and until the maximum iterations is met as it iterates through according to the limit
#--> of the radius until the pixels are not in the Julia set and until the iteration value is met

 
        for x in positionX:
            for y in positionY:
                z = complex(x, y)
                currentP = z
                i = 0

                while abs(z) < radiusLimit and i < self.jMaxIt: 
                    z = z*z + self.C
                    i += 1

#if the iteration value within the Julia set loop has met the maximum Iterations when the x and y coordinates are converted to pixels using the complex number format
#--> of imaginary and real numbers. If the pixel coordinates are less than correspinding height and width then they are coloured using the chosen colour blend RGB
#--> using the screen of pygame as the 2D array of x and y coordinates 

                if i == self.jMaxIt:
                    xCoordinate = self.complexToX(currentP.real)
                    yCoordinate = self.complexToY(currentP.imag)
                    
                    if xCoordinate < self.width and yCoordinate < self.height:
                        if self.blendType == 1:
                            self.juliaScreen[xCoordinate, yCoordinate]  = (colourBlend)

#if the iteration value within the Julia set loop is still under the value of the iterations when the x and y coordinates are still converted to pixels using the
#--> complex plane with the real and imaginary format of the complex numbers of the final iteration value
#the 'if' statement for blend type is used to colour the pixels as long as the iteration value is under the maximum iteration and the dotting blend is used to
#--> blend in the pixels when looping with the pixels that are used in the final calculation in the loop. background fill is the blue background fill used with RGB
#If the x and y coordinate positions are less than the height and width and they are over the value of 0, they are plotted using the pygame display 2d array according
#--> to the blue background colour. the pygame display is then updated 


                if i < self.jMaxIt:

                    xCoordinate = self.complexToX(currentP.real)
                    yCoordinate = self.complexToY(currentP.imag)

                    if self.blendType == 1:
                        dottingBlend = plottingFill * math.log10(i + 1)
                        backgroundFill = (dottingBlend, 50 , 150)
                        if xCoordinate < self.width and yCoordinate < self.height:
                            if yCoordinate > 0 and xCoordinate > 0:
                                self.juliaScreen[xCoordinate, yCoordinate] = (backgroundFill)
            pygame.display.update() 

#This is the standard loop used to quit the pygame window when needed 

        done = True 
        while not done: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
              
#---------------------Julia--------------------------
#Used to call all the functions to run the Julia set. 
def Julia():
    callJulia = juliaFractal()
    callJulia.setBoundaries()
    callJulia.setHeight()
    callJulia.setDisplay()
    callJulia.setIteration()
    callJulia.juliaPlot()  
    callJulia.drawJulia()

if __name__ == "__main__":
     Julia()
                            
                
                
                
                
        
    
        
        
        

    

  

    
        
        
        
        
            

                    
            
        
