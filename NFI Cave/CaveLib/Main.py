import cavelib3
import math
import viz
import vizshape
import caveapp #not strictly required

#x = -left/+right
#y = -below/+above
#z = -behind/+in front

################################################################
#Placement of objects
################################################################

#object.method(x, y, z)

#object = viz.add("map/file.ext")							#Add object to scene
#object.setAxisAngle(0, 1, 0, 90)							#Set the direction of an object
#object.texture(viz.addTexture("textureMap/img.ext")) 		#Connect a texture to an object (.mtl file with the same name pastes the material over the object by itself)
#object.addAction(vizact.spin(0, 1, 0, 20))					#Arguments (x, y, z, speed), a negative number is used to spin in the opposite direction
#object.setScale(0.5, 0.5, 0.5)								#Scaling the object for each specific axis
#object.setPosition(0,2,0)									#Set the position of the object


################################################################
#Code, with respect to she functionality should be in here
################################################################




class CustomCaveApplication(caveapp.CaveApplication):
	"""A custom CAVE application.
	
	You can choose to use or not use this object oriented construct.
	It is also possible to use cavelib3 without the caveapp.CaveApplication class.
	
	Note that this example application is intended to make things simple.
	It says ``intended`` ecause the object oriented layer may be confusing.
	Have a look at caveapp.py This will make things more clear.
	
	In python, if you redefine a function in a subclass, this function is virtual by default.
	The function in the subclass will be called instead of the function in the super class.
	
	If you think that caveapp.py can be improved upon, you can do so.
	Strictly caveapp.py is not part of the cavelib3.
	You should not have to alter the cavelib itself though.
	
	This construct is given as an example.
	Usually, people use vizard by using lots of callbacks.
	These callbacks, have an exectution order.
	Usually these exectution orders are not considered when writing an application, thereby introducing bugs.
	
	When using this class, you do not need to use any callbacks.
	There is just one __onUpdate function which gets called in caveapp.CaveApplication
	This call is distributed over several other calls of which the order is transparent.
	
	Another pitfall in vizard is automatic linking (of simulation objects).
	Instead of using link constructs, it is more transparent to set the world poses of objects at each frame.
	See updateObjects.
	
	A problem that arises with automatic linking of simulation objects is that links can have priorities.
	Priorities can be too low, causing the link to disfunction.
	
	If you have a conflicting transformation within the updateObjects function, then it is clear that only the last assignment will be used.
	Vizard wants to take care of many things, that is why it uses the link mechanism.
	However, other simulation tools usually do not have this.	
	In general, a simulation has an initialization function, an update function and a render function.
	This construct allows the user to initilialize and to update. Rendering is done automatically by vizard (after each update)(this is okay).
	"""
	
	def __init__(self,use_keyboard = True, desktop_mode = False):
		"""Initialization function."""
		
		caveapp.CaveApplication.__init__(self,desktop_mode) #call constructor of super class, you have to do this explicitly in Python		
		
		self.wand = vizshape.addAxes()#load axis model to represent the wand
		self.thing = viz.addChild('plant.osgb') #load plant model to represent the thing
		
		self.horse = viz.addChild('horse.wrl') #load a horse model (this model will be animated in cave space)
		
		self.horse.color(0.5,0.5,0.5)#make the horse gray
		
		self.horse.disable(viz.LIGHTING) #disable the shading of the horse
		
		self.worldModel = viz.add('piazza.osgb') #load a world model
		
		self.headLight = viz.MainView.getHeadLight() #disable the headlight
		self.headLight.disable() #the headlight is disabled because the piazza.osgb is already shaded
		
		self.use_keyboard = use_keyboard #store if we want to use the keyboard
		
		
		self.time = 0.0 #note that to 0.0 is important because it is a double precision floating point number
		#the variable above will be used to keep track of time
		#there may be a difference between the vizard clock and self.time
		#could be rounding error, could be something else
		
	def updateObjects(self,e):
		"""Set the world poses of the objects
		
		Especially those which are defined in the CAVE coordinate system.
		Since this function is called after the CAVE is moved (see movement of CAVE).
		"""
		
		#the delta time that has passed
		#you can use this value to advance your simulation
		elapsed = e.elapsed 
		
		#keep track of time	
		#this is just some time measurement
		#vizard probably has some clock function
		#there is no reason to prefer one time variable/function over the other
		#there is also no reason why the statement below is in this function and not in preUpdate
		self.time += elapsed
		
		
		#where is the horse located in the cave?
		horse_position_in_cave_space = viz.Vector(math.cos(self.time), 1, math.sin(self.time))
		
		#convert the location (without orientation and scale) into a translation matrix
		#(having default orientation and scale)
		horse_matrix_in_cave_space = viz.Transform.translate(horse_position_in_cave_space)
		
		#rotate the horse
		#note that pre euler is used
		#this means first rotate and than apply the translation transformation
		horse_matrix_in_cave_space.preEuler(self.time / math.pi * -180.0,0,0)
		
		#convert the horse matrix to world space and assign it to the model
		
		self.horse.setMatrix(self.cavelib.localMatrixToWorld(horse_matrix_in_cave_space))
		
		#set the wand (i.e. one of the trackers NOT the wiimote)		
		#the wand is viewed as a coordinate system
		self.wand.setMatrix(self.cavelib.localMatrixToWorld(self.cavelib.getWandMatrix()))
		
		#set the thing
		#the thing is the plant model
		#its motion is defined by the second tracker
		self.thing.setMatrix(self.cavelib.localMatrixToWorld(self.cavelib.getThingMatrix()))
		
		
		#print str(self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_BOTTOM_LEFT)) + " " ,
		#print str(self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_BOTTOM_RIGHT)) + " " ,
		#print str(self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_TOP_LEFT)) + " " ,
		#print str(self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_TOP_RIGHT)) + " " ,
		#print str(self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_TOTAL))		
		
	def preUpdate(self,e):
		"""This function is executed before the updates are done."""
		pass
		
	def postUpdate(self,e):
		"""This function is exectuted after the updates are done."""		
		pass
						
	def	leftPressed(self):
		"""Virtual function to use keyboard if indicated.
		
		This function can be omitted.
		If this function is omitted, the wiimote will always be used.
		"""
		if self.use_keyboard:
			return viz.iskeydown(viz.KEY_LEFT) #keyboard input
		
		return caveapp.CaveApplication.leftPressed(self) #wiimote input
			
	def	rightPressed(self):
		"""Virtual function to use keyboard if indicated.
		
		This function can be omitted.
		If this function is omitted, the wiimote will always be used.
		"""
		if self.use_keyboard:
			return viz.iskeydown(viz.KEY_RIGHT)#keyboard input
		
		return caveapp.CaveApplication.rightPressed(self) #wiimote input
			
	def	upPressed(self):
		"""Virtual function to use keyboard if indicated.
		
		This function can be omitted.
		If this function is omitted, the wiimote will always be used.
		"""
		if self.use_keyboard:
			return viz.iskeydown(viz.KEY_UP)#keyboard input
		
		return caveapp.CaveApplication.upPressed(self) #wiimote input
			
	def	downPressed(self):
		"""Virtual function to use keyboard if indicated.
		
		This function can be omitted.
		If this function is omitted, the wiimote will always be used.
		"""
		if self.use_keyboard:
			return viz.iskeydown(viz.KEY_DOWN)#keyboard input
		
		return caveapp.CaveApplication.downPressed(self) #wiimote input
			
	def	joystick(self):
		"""Virtual function to use keyboard if indicated.
		
		This function can be omitted.
		If this function is omitted, the wiimote will always be used.
		"""
		if self.use_keyboard:
			
			#keyboard input
			
			result = [0.0,0.0]
			
			if viz.iskeydown('['): 
				result[0] -= 1.0
				
			if viz.iskeydown(']'): 
				result[0] += 1.0
				
			return result
		
		return caveapp.CaveApplication.joystick(self) #wiimote input
			
################################################################
#Cave functionality
################################################################
#Param: True = DesktopMode on
#		False = DesktopMode off

print "Constructing the application class."
application = CustomCaveApplication(use_keyboard=True, desktop_mode=True) #boolean indicated wheter or not to use the keyboard instead of the wiimote

print "Setting the number of samples per pixel."

viz.setMultiSample(4)

application.go()

