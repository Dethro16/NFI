import viz
import vizact
import vizshape
import math

viz.setMultiSample(4)
viz.fov(60)
viz.go()
viz.phys.enable()

viz.disable(viz.LIGHTING)
headLight = viz.MainView.getHeadLight() #disable the headlight
headLight.disable() #the headlight is disabled because the piazza.osgb is already shaded

grass = viz.addChild('ground.osgb')
grass.setPosition(0,-.01,0)

Room = viz.addChild('Master\NFI Cave\Scene\ScannedRoom.3DS')
Room.collidePlane()
Room.setScale([1.25,1.25,1.25])
Room.setEuler([90,0,0])
Room.setPosition([-1.5,0,1.55])

cube = vizshape.addBox()

global cubes
cubes = []




def click():
	item = viz.MainWindow.pick(info = True)
	if item.valid:
		pos = item.point
		print 'POS:'
		print pos
		
		global cubes
		size = [0.2,0.2,0.2]
		
		euler = viz.MainView.getEuler()
		print 'Euler:'
		print euler
		
		front = [0,0,0]
		back = [180,0,0]
		left = [-90,0,0]
		right = [90,0,0]
		
		blood = viz.add('C:\Users\Loic Motheu\Desktop\\blood.png')
		transparant = viz.add('C:\Users\Loic Motheu\Desktop\\transparant.png')
		cube = vizshape.addBox(size, splitFaces=True)

		if euler[0] > -135 and euler[0] < -45:#LEFT
			print 'ROTATED LEFT'
			posBloodL = [item.point[0]-.0996,item.point[1],item.point[2]]
			cube.setPosition(posBloodL)
			cube.setEuler(left)
		if euler[0] < 135 and euler[0] > 45:#RIGHT
			print 'ROTATED RIGHT'
			posBloodR = [item.point[0]+.0996,item.point[1],item.point[2]]
			cube.setPosition(posBloodR)
			cube.setEuler(right)
		if euler[0] > -45 and euler[0] < 45:#FRONT
			print 'ROTATED FRONT'
			posBloodF = [item.point[0],item.point[1],item.point[2]+.0996]
			cube.setPosition(posBloodF)
			cube.setEuler(front)
		if (euler[0] > 135 and euler[0] < 180) or (euler[0] < -135 and euler[0] > -180):#BACK
			print 'ROTATED BACK'
			posBloodB = [item.point[0],item.point[1],item.point[2]-.0996]
			cube.setPosition(posBloodB)
			cube.setEuler(back)

		cube.texture(blood,node='back')
		cube.texture(transparant,node='front')
		cube.texture(transparant,node='left')
		cube.texture(transparant,node='right')
		cube.texture(transparant,node='top')
		cube.texture(transparant,node='bottom')
		cubes.append(cube)

		tempEuler = cube.getEuler()
		
		pos = [item.point[0]+.5,item.point[1],item.point[2]-2]
		state = viz.mouse.getState()
		angle = " "
		text_2D_world = viz.addText(angle, pos=pos, parent=viz.WORLD)

		def increaseAngle():
			def onMouseMove(e): 
				tempEuler[1] += int(e.dy*0.1)
				tempEuler[1] = viz.clamp(tempEuler[1], -90.0, 90.0)
				angle = 'Angle: ' + str(tempEuler)
				
				if vizact.onmouseup:
					text_2D_world.message(angle)
			viz.callback(viz.MOUSE_MOVE_EVENT,onMouseMove)
		vizact.whilemousedown(viz.MOUSEBUTTON_LEFT, increaseAngle)

def clear():
	#item = viz.MainWindow.pick(info = True)
	item = viz.pick()
	if item.valid:
		for i in cubes:
			if i == item:
				i.remove()
				print '~~~CLEAR~~~'
vizact.onkeydown('p', clear)
	
#vizact.onmousedown(viz.MOUSEBUTTON_LEFT, click) 
vizact.onkeydown(' ', click)
"""
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
bl = ([-4.970107078552246, 5.897994518280029, 1.4124407768249512],[-4.973110198974609, 6.1175079345703125, 2.1125693321228027],[-4.975081920623779, 6.5309247970581055, 2.8221869468688965],[-4.975322246551514, 6.759340286254883, 3.1336262226104736],[-4.975906848907471, 7.1793365478515625, 2.779799699783325],[-4.97451114654541, 5.308044910430908, 3.1625561714172363],[-4.973536014556885, 5.8962178230285645, 3.2122514247894287],[-4.9707231521606445, 5.660599231719971, 3.5753281116485596],[-4.966211795806885, 4.887547492980957, 3.882848024368286],[-2.7433903217315674, 5.715956211090088, 5.507270812988281],[-3.2320258617401123, 6.556395053863525, 5.514878273010254],[-3.798262596130371, 5.829957008361816, 5.529846668243408],[-2.0034732818603516, 7.698963642120361, 5.504480361938477],[-4.953855037689209, 6.041557788848877, 5.1223649978637695],[-1.3830612897872925, 5.617004871368408, -4.059776782989502],[-1.6367100477218628, 3.0266971588134766, -4.050085544586182],[-2.242931604385376, 2.975187301635742, -4.043353080749512],[-2.9772372245788574, 2.110835075378418, -4.028698921203613],[-1.6415677070617676, 2.3813564777374268, -4.04733943939209],[-0.3302052915096283, 1.9607874155044556, -4.049890518188477],[-4.9920268058776855, 5.900781631469727, -1.8857085704803467],[-4.989490985870361, 5.56298828125, -1.7206439971923828],[-4.996257305145264, 4.581329345703125, -2.1972899436950684],[-4.994059085845947, 4.407802581787109, -1.6545305252075195],[-4.992647171020508, 4.442633628845215, -1.1358085870742798],[-4.988626480102539, 4.823823928833008, 0.1453738659620285],[-4.988673210144043, 5.07926607131958, -0.048772379755973816],[-4.988332748413086, 5.744387149810791, -0.1320347636938095],[-4.9886860847473145, 6.315260410308838, -0.23182286322116852],[-4.986820697784424, 5.827799320220947, -0.9230077862739563],[-4.991076946258545, 4.644659042358398, -0.8074011206626892],[-4.9762864112854, 4.111218452453613, 3.3881337642669678],[-4.9752607345581055, 7.730223178863525, 2.4686429500579834],[0.26733750104904175, 8.535117149353027, 5.487018585205078],[1.2186188697814941, 7.103093147277832, 5.488711833953857],[-0.5966476202011108, 7.537855625152588, 5.486145973205566],[-0.8177675008773804, 7.79792594909668, 5.4877166748046875],[-1.8698996305465698, 8.362137794494629, 5.504770755767822],[-4.992286205291748, 2.577256441116333, 0.02785523794591427])
al = []
target = [1.1959341764450073, 3.428847789764404, 0.7743394374847412]
masterpointlist = []
for b in bl:
	viz.startLayer(viz.LINE_STRIP)
	viz.vertexcolor(viz.BLUE)
	viz.vertex(b)
	x=0
	al += ([(target[0]-b[0])*2,(target[1]-b[1])*2,(target[2]-b[2])*2],)
	temp = al[bl.index(b)]
	pointlist = []
	while x <=5:
		point = formula(grav,wd,wc,x,temp,b)
		viz.vertex(point)
		pointlist += [point]
		x += 0.1
	masterpointlist += [pointlist]
	viz.endLayer()
area = []
z=0
print al
zcount = len(masterpointlist)-1
while z < zcount:
	y=z+1
	fpl = masterpointlist[z]
	while y <= zcount:
		spl = masterpointlist[y]
		for i in fpl:
			for j in spl:
				dist = math.sqrt(pow((i[0]-j[0]),2) + pow((i[1]-j[1]),2) + pow((i[2]-j[2]),2))
				if dist <0.1:
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
	circle = vizshape.addSphere(0.1)
	circle.setPosition(a)
if len(area)!=0:
	centroid = [(sum(centroidx)/len(area)),(sum(centroidy)/len(area)),(sum(centroidz)/len(area))]
	wound = vizshape.addSphere(0.2)
	wound.color(viz.RED)
	wound.setPosition(centroid)
	for b in al:
		temp =[]
		temp += (b[0]*-1,)
		temp += (b[1]*-1,)
		temp += (b[2]*-1,)
		viz.startLayer(viz.LINE_STRIP)
		viz.vertexcolor(viz.GREEN)
		viz.vertex(wound.getPosition())
		pointlist = []
		x=0
		while x <=5:
			point = formula([0.0,-9.81,0.0],wd,wc,x,temp,wound.getPosition(viz.ABS_GLOBAL))
			viz.vertex(point)
			pointlist += [point]
			x += 0.1
		viz.endLayer()
else:
	print 'No points are close enough together.'
"""

#viz.MainView.setPosition(0,5,-10)