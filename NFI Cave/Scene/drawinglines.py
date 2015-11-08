import viz
import viztask
viz.go()

def DrawLineTask():
	
	while True:
		
		#Wait for left mouse butten to be pressed
		yield viztask.waitMouseDown(viz.MOUSEBUTTON_LEFT)
		
		#Get mouse position
		pos = viz.mouse.getPosition()
		
		#Create line
		viz.startlayer(viz.LINES)
		viz.vertexcolor(viz.RED)
		viz.vertex(pos[0],pos[1],0)
		viz.vertex(pos[0],pos[1],0)
		line = viz.endlayer(parent=viz.SCREEN)
		
		#Create link between mouse position and vertex
		VertexLink = viz.link(viz.Mouse,line.Vertex(1))
		
		#Wait for mouse button to be released
		yield viztask.waitMouseUp(viz.MOUSEBUTTON_LEFT)
		
		#Destroy link
		VertexLink.remove()
		
viztask.schedule( DrawLineTask() )