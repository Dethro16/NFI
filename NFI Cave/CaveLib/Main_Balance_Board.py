import cavelib3
import math
import viz
import vizshape
import caveapp

class CustomCaveApplication(caveapp.CaveApplication):
	def __init__(self, use_keyboard = True, desktop_mode = True):
		caveapp.CaveApplication.__init__(self, desktop_mode) #call constructor of super class, you have to do this explicitly in Python		
		
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
		
		self.forwardVelocity = 0.0
		#the variable above will be used to keep track of time
		
	def movementOfCave(self,e):
		elapsed = e.elapsed
		
		originTracker = self.cavelib.getOriginTracker() #a reference to the origin tracker
		
		totalWeight = self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_TOTAL)
		
		topLeft = self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_TOP_LEFT)
		bottomLeft = self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_BOTTOM_LEFT)
		
		topRight = self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_TOP_RIGHT)
		bottomRight = self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_BOTTOM_RIGHT)
		
		rotation = (topLeft + bottomLeft - topRight - bottomRight) / (totalWeight + 1e-10)
		
		if abs(rotation) < 1.0 / 16.0:
			rotation = 0.0
			
		forwardMovement = -(topLeft + topRight - bottomLeft - bottomRight) / (totalWeight + 1e-10)
		
		if abs(forwardMovement) < 1.0 / 16.0:
			forwardMovement = 0.0
			
		rotation *= 2.0
		forwardMovement *= 2.0
		
		self.forwardVelocity += forwardMovement * elapsed
		
		self.forwardVelocity -= self.forwardVelocity * (1.0 / 8.0) * elapsed
			
		
		
		originTracker.setPosition([0,0,self.forwardVelocity * elapsed],viz.REL_LOCAL)
		
		self.yaw = self.yaw + self.yawDelta * rotation * elapsed
	
		originTracker.setEuler([self.yaw,self.pitch,0])		
		
		
		
		
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
			
print "Constructing the application class."
application = CustomCaveApplication(use_keyboard = True, desktop_mode = True)

print "Setting the antialiasing factor"

viz.setMultiSample(4)

application.go()

