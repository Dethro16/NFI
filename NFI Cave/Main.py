import cavelib3
import math
import viz
import vizshape
import vizact
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
		#
		viz.phys.enable()
		self.view = viz.MainView;
		
		caveapp.CaveApplication.__init__(self,desktop_mode) #call constructor of super class, you have to do this explicitly in Python		
		
		self.wand = vizshape.addAxes()#load axis model to represent the wand\
		self.cylinder = vizshape.addCylinder(15,0.002,axis=vizshape.AXIS_X)
		self.cylinder.setEuler([0,0,0])
		#self.cylinder.setCenter([0,0,-1])
		self.cylinder.setPosition(7.5,0.08,0)
		
		self.stuff = vizshape.addSphere(0.0001)
		self.cylinder.setParent(self.stuff)
		
#		temp = vizshape.addSphere(0.05)
#		temp.setParent(self.cylinder)
#		temp.setPosition(self.cylinder.getCenter())
		
		self.wand = self.stuff
#		self.wand.setPosition(.5,-1,0)
#		self.cm = self.wand.getMatrix()
#		self.Room = viz.addChild('D:\Cave software\NFI Cave\Scene\ScannedRoom.3DS')
#		self.Room.collidePlane()
#		self.Room.setScale([1.25,1.25,1.25])
#		self.Room.setEuler([90,0,0])
#		self.Room.setPosition([-1.5,0,1.55])
		self.Room = viz.addChild('scene/ScannedRoom.3DS')
		self.Room.collidePlane()
		self.Room.setScale([0.002,0.002,0.002])
		self.Room.setEuler([90,0,0])
		self.Room.setPosition([-1.5,0.015,1.58])
		"""
		mylight = viz.addLight() 
		mylight.enable() 
		mylight.position(0, 1, 0) 
		mylight.spread(180) 
		mylight.intensity(2)
#		vizact.onkeydown('f', dance)
		"""
		
		viz.disable(viz.LIGHTING)
		self.headLight = viz.MainView.getHeadLight() #disable the headlight
		self.headLight.disable() #the headlight is disabled because the piazza.osgb is already shaded
		
		self.use_keyboard = use_keyboard #store if we want to use the keyboard
		
		
		self.time = 0.0 #note that to 0.0 is important because it is a double precision floating point number
		#the variable above will be used to keep track of time
		#there may be a difference between the vizard clock and self.time
		#could be rounding error, could be something else
	
	def formula(gravity, winddirection, windconstant, time, initialdirection, initialpos):
#	if(windconstant!=0):
#		tempgrav = (gravity[0]/windconstant,gravity[1]/windconstant,gravity[2]/windconstant)
#		k1 = (initialdirection[0]-tempgrav[0]-winddirection[0],initialdirection[1]-tempgrav[1]-winddirection[1],initialdirection[2]-tempgrav[2]-winddirection[2])
#		k2 = (initialpos[0] + (k1[0]/windconstant),initialpos[1] + (k1[1]/windconstant),initialpos[2] + (k1[2]/windconstant))
#		fs = (((gravity[0]+(winddirection[0]*windconstant))/windconstant)*time)-(k1[0]*pow(math.e,-(windconstant*time)))+k2[0]
#		ss = (((gravity[1]+(winddirection[1]*windconstant))/windconstant)*time)-(k1[1]*pow(math.e,-(windconstant*time)))+k2[1]
#		ts = (((gravity[2]+(winddirection[2]*windconstant))/windconstant)*time)-(k1[2]*pow(math.e,-(windconstant*time)))+k2[2]
#		result = ([fs,ss,ts])
#	else:
		part1 = initialpos
		temp = ()
		for i in initialdirection:
			temp +=(i*time,)
		part2 = temp
		subpart1 = pow(time,2)
		temp = ()
		for g in gravity:
			temp +=(g*subpart1,)
		subpart2 = temp
		temp = ()
		for s in subpart2:
			temp +=(s*0.5,)
		part3 = temp
		result = (part1[0]+part2[0]+part3[0],part1[1]+part2[1]+part3[1],part1[2]+part2[2]+part3[2])
		return result

	wd = [0,0,0]
	wc = 0
	grav = [0.0,9.81,0.0]
	bl = ([-1.5186548233032227, 1.7569714784622192, 0.42380595207214355],
[-1.5157184600830078, 0.9477821588516235, 0.4928368330001831],
[-1.5135573148727417, 0.9329770803451538, 0.6889349222183228],
[-1.5147682428359985, 0.7391808032989502, 0.5009629726409912],
[-1.515607476234436, 0.6143998503684998, 0.09025046229362488],
[-1.509002923965454, 0.6631836891174316, 0.9177209734916687],
[-0.24511753022670746, 0.8049251437187195, 1.5476268529891968],
[-0.9331315755844116, 1.4313745498657227, 1.5488107204437256],
[-0.7725428342819214, 1.3719626665115356, 1.5481754541397095],
[-0.6045324206352234, 1.3867779970169067, 1.5477062463760376],
[-0.5039831399917603, 1.4481874704360962, 1.5472277402877808],
[-0.8401618003845215, 1.8455625772476196, 1.5475212335586548],
[-0.7861605286598206, 1.734692931175232, 1.5466915369033813],
[-0.5333393812179565, 1.8137447834014893, 1.5458786487579346],
[-0.31605958938598633, 1.9746060371398926, 1.5463721752166748],
[-0.2979672849178314, 1.8013648986816406, 1.5463511943817139],
[-0.2653859853744507, 1.5959784984588623, 1.5464332103729248],
[-0.2048081010580063, 1.5073721408843994, 1.546447515487671],
[0.2041378915309906, 1.83889901638031, 1.5406838655471802],
[0.418000191450119, 1.9112932682037354, 1.5416533946990967],
[0.6379923820495605, 2.032597541809082, 1.5421932935714722],
[0.7319793701171875, 2.1154985427856445, 1.5422788858413696],
[0.6247239708900452, 2.240435838699341, 1.542487382888794],
[0.5285359025001526, 2.4131922721862793, 1.5422946214675903],
[0.76174396276474, 1.836247205734253, 1.54171621799469],
[0.8672671318054199, 1.7679400444030762, 1.5408480167388916],
[0.7455712556838989, 1.651633620262146, 1.5419487953186035],
[0.9777757525444031, 1.5065670013427734, 1.5393511056900024],
[0.8060051202774048, 1.2854902744293213, 1.5425981283187866],
[1.3488842248916626, 1.8830739259719849, 1.5355942249298096],
[1.478007197380066, 1.8205766677856445, 1.171138882637024],
[1.4733483791351318, 2.0495986938476562, 0.9953248500823975],
[1.4700955152511597, 2.4099817276000977, 0.6066880822181702],
[1.4701241254806519, 2.6104142665863037, 0.5644940733909607],
[1.4649194478988647, 2.4387924671173096, 0.24266688525676727],
[1.4644279479980469, 2.3569350242614746, 0.17129123210906982],
[1.4646551609039307, 2.6615219116210938, -0.10032745450735092],
[1.4652283191680908, 2.2228739261627197, -0.3981189727783203],
[1.4709352254867554, 1.787745475769043, 0.841178834438324]
)
	al = []
	
	target = [-0.5709398627281189, 0.03, 0.4417222142219543]
	masterpointlist = []
	for b in bl:
		viz.startLayer(viz.LINE_STRIP)
		viz.vertexcolor(viz.BLUE)
		viz.vertex(b)
		x=0
		al += ([(target[0]-b[0])*2,(target[1]-b[1])*2,(target[2]-b[2])*2],)
		temp = al[bl.index(b)]
		pointlist = []
		while x <=2:
			point = formula(grav,wd,wc,x,temp,b)
			#viz.vertex(point)
			pointlist += [point]
			x += 0.05
		masterpointlist += [pointlist]
		viz.endLayer()
	area = []
	z=0
	#print al
	zcount = len(masterpointlist)-1
	while z < zcount:
		y=z+1
		fpl = masterpointlist[z]
		while y <= zcount:
			spl = masterpointlist[y]
			for i in fpl:
				for j in spl:
					dist = math.sqrt(pow((i[0]-j[0]),2) + pow((i[1]-j[1]),2) + pow((i[2]-j[2]),2))
					if dist <0.02:
						if area.count(i) == 0:
							area += [i]
						if area.count(j) == 0:
							area += [j]
			y += 1
		z += 1
	centroidx = [a[0] for a in area]
	centroidy = [a[1] for a in area]
	centroidz = [a[2] for a in area]
	for a in area:
		circle = vizshape.addSphere(0.02)
		circle.setPosition(a)
	if len(area)!=0:
		centroid = [(sum(centroidx)/len(area)),(sum(centroidy)/len(area)),(sum(centroidz)/len(area))]
		wound = vizshape.addSphere(0.05)
		wound.color(viz.RED)
		wound.setPosition(centroid)
		for b in al:
			temp =[]
			temp += (b[0]*-1,)
			temp += (b[1]*-1,)
			temp += (b[2]*-1,)
			viz.startLayer(viz.LINE_STRIP)
			viz.vertexcolor(viz.BLUE)
			viz.vertex(wound.getPosition())
			pointlist = []
			x=0
			while x <=2:
				point = formula([0.0,-9.81,0.0],wd,wc,x,temp,wound.getPosition(viz.ABS_GLOBAL))
				viz.vertex(point)
				pointlist += [point]
				x += 0.05
			viz.endLayer()
		male = viz.add('vcc_male.cfg')
		male.setCenter(1,0,0)
		male.setEuler(180,0,0)
		male.setPosition(-0.45,-1.3,-0.15)
		#male.setScale(0.03,0.03,0.03)
		male.setParent(wound)
		#wound.setEuler(0,-90,0)
	else:
		print 'No points are close enough together.'
	
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
		#horse_position_in_cave_space = viz.Vector(math.cos(self.time), 1, math.sin(self.time))
		#bench_pos_in_cave_space = viz.Vector(0,1,2)
		
		#convert the location (without orientation and scale) into a translation matrix
		#(having default orientation and scale)
		#horse_matrix_in_cave_space = viz.Transform.translate(horse_position_in_cave_space)
		#nslate(bench_pos_in_cave_space)
	
		#rotate the horse
		#note that pre euler is used
		#this means first rotate and than apply the translation transformation
		#horse_matrix_in_cave_space.preEuler(self.time / math.pi * -180.0,0,0)
		
		#convert the horse matrix to world space and assign it to the model
		
		#self.bench.setMatrix(self.cavelib.localMatrixToWorld(bench_matrix_in_cave_space))
		
		#set the wand (i.e. one of the trackers NOT the wiimote)		
		#the wand is viewed as a coordinate system
#		offset = viz.Matrix()
#		offset.setPosition(1,0,0)
		offset = self.cavelib.localMatrixToWorld(self.cavelib.getWandMatrix())
		self.wand.setMatrix(self.cavelib.localMatrixToWorld(self.cavelib.getWandMatrix()))
		#self.wand.setEuler([0,90,0])
		
		#set the thing
		#the thing is the plant model
		#its motion is defined by the second tracker
		
		#self.bench.setMatrix(self.cavelib.localMatrixToWorld(self.cavelib.getThingMatrix()))
		"""
		self.bench.setPosition(.2,.3,-.5)
		print 'x: ', self.view.getPosition()[0]
		print 'y: ', self.view.getPosition()[1]
		print 'z: ', self.view.getPosition()[2]
		self.bench.setScale(0.1, 0.15, 0.1)
		"""
		
		#self.dude.setMatrix(self.cavelib.localMatrixToWorld(self.cavelib.getThingMatrix()))
		#self.bench.setMatrix(self.cavelib.localMatrixToWorld(0,1,2))
		
		
		
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

