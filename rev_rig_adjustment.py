from maya import cmds
import maya.api.OpenMaya as om
import maya.mel as mel
#creating a class for global variables used in different functions.
class globalVar:
	def __init__(self):
		self.new_mesh = None
		self.ogmesh = None
		self.newmesh = None
		self.bone_List = None
		self.rig_root = None
		self.namespace_flag = None

		self.sel1 = None
		self.selection_list = None
		self.dag_path = None
		self.mfn_mesh1 = None
		self.pp = None
		self.length = None
		self.Q = None

		self.selected = None
		self.b = None
		self.bx = None
		self.by = None
		self.bz = None
		self.BonePoint = None
		self.R = None
		self.distList = None
		self.distance = None
		self.minDist = None
		self.minDistID = None
		self.pointMin = None
		self.M1X = None
		self.M1Z = None
		self.M1Y = None

		self.sel2 = None
		self.mfn_mesh2 = None
		self.points2 = None
		self.M2X = None
		self.M2Z = None
		self.M2Y = None

		self.offsetX = None
		self.offsetY = None
		self.offsetZ = None

class MyGlobalVar:
	def __init__(self):
		self.verticeDict = None

#Class to get geo Information from selection to pass along during weight transfer using dictionary
class DictClass:
	def geoInfo(self, vtx=0, geo=0, shape=0, skinC=0): # Returns a list of requested object strings
		returnValues = []
		
		selVTX = [x for x in cmds.ls(sl=1, fl=1) if ".vtx" in x]
		
		if len(selVTX) == 0:
			# geo can be of bool/int type or of string type.
			if type(geo) == int or type(geo) == bool:
				selGEO = cmds.ls(sl=1, objectsOnly=1)[0]
				
			elif type(geo) == str or type(geo) == str:
				selGEO = geo
				
			geoShape = cmds.listRelatives(selGEO, shapes=1)[0]
			
			# Deformed shapes occur when reference geometry has a deformer applied to it that is then cached
			# the additional section will take out the namespace of the shapefile (if it exists) and try to
			# apply the deform syntax on it.
			if ":" in geoShape: # the colon : deliminates namespace references
				deformShape = geoShape.partition(":")[2] + "Deformed"
				if len(cmds.ls(deformShape)) != 0:
					geoShape = deformShape
					print("deformed shape found: " + geoShape)
		
		else:
			geoShape = selVTX[0].partition(".")[0] + "Shape"
			deformTest = geoShape.partition(":")[2] + "Deformed"
			if len(deformTest) != 0:
				geoShape = deformTest
				print("deformed shape found on selected vertices: " + geoShape)
				
				for x in range( len(selVTX) ):
					selVTX[x] = ( selVTX[x].replace(".","ShapeDeformed.") ).partition(":")[2]
				
			selGEO = cmds.listRelatives(geoShape, p=1)[0]
			print(geoShape + " | " + selGEO)
		
		
		if vtx == 1:
			if len(selVTX) != 0: # if vertices are already selected, then we can take that list whole-sale.
				returnValues.append(selVTX)
			else:
				vtxIndexList = ["{0}.vtx[{1}]".format(geoShape, x) for x in cmds.getAttr ( geoShape + ".vrts", multiIndices=True)]
				returnValues.append(vtxIndexList)
		
		
		if geo == 1 or geo == True or type(geo) == str or type(geo) == str: 
			returnValues.append(selGEO)
		
		
		if shape == 1:
			returnValues.append(geoShape)
		
		
		if skinC == 1:
			skinClusterNM = [x for x in cmds.listHistory(geoShape) if cmds.nodeType(x) == "skinCluster" ][0]
			returnValues.append(skinClusterNM)
			
		return returnValues
		

	def getVertexWeights(self, vertexList=[], skinCluster="", thresholdValue=0.001):
		if len(vertexList) != 0 and skinCluster != "":
			mgv.verticeDict = {}
			
			for vtx in vertexList:
				influenceVals = cmds.skinPercent(skinCluster, vtx, q=1, v=1, ib=thresholdValue)
				
				influenceNames = cmds.skinPercent(skinCluster, vtx,  transform=None, q=1,   ib=thresholdValue) 
							
				mgv.verticeDict[vtx] = list(zip(influenceNames, influenceVals))
			
			return mgv.verticeDict
		else:
			cmds.error("No Vertices or SkinCluster passed.")


#instancing this class name into an variable to call variables inside of functions

mgv = MyGlobalVar()
utils = DictClass()
gv = globalVar()


#creating a wrapper to store UI values and pass it to the corresponding feilds 
def button_wrapper(fn, *args, **kwargs):
	def wrapped(_):
		fn(*args, **kwargs)
	return wrapped

#passing arguments as values to the variables from UI

def store_og(txt_field):
	ui_sel = cmds.ls(sl=True)
	cmds.textField(txt_field, edit=True, text= ui_sel[0])
	gv.ogmesh
	gv.ogmesh= ui_sel[0]
	return gv.ogmesh

#passing arguments as values to the variables from UI
	
def store_new(txt_field):
	ui_sel = cmds.ls(sl=True)
	cmds.textField(txt_field, edit=True, text= ui_sel[0])
	gv.new_mesh
	gv.new_mesh = ui_sel[0]
	return gv.new_mesh

#passing arguments as values to the variables from UI

def store_joint(txt_field):
	ui_sel = cmds.ls(sl=True)
	cmds.textField(txt_field, edit=True, text= ui_sel[0])
	gv.rig_root
	gv.rig_root = ui_sel[0]
	return gv.rig_root



gv.namespace_flag = "True"

#Main function to align the skeleton
def toolkit(_):
		#setting skin cluster node to 0 before everything
	history = cmds.listHistory(gv.ogmesh)
	skinCluster_node = None
	for node in history:
		node_type = cmds.nodeType(node)
		if node_type == "skinCluster":
			skinCluster_node = node
			break
	if skinCluster_node:
		cmds.setAttr("{}.envelope".format(skinCluster_node), 0)


	#Alright lets go
	cmds.select( clear=True )
	def OG_Mesh_func():
		gv.sel1 = cmds.ls(gv.ogmesh)
		# get the dag path
		gv.selection_list = om.MSelectionList()
		gv.selection_list.add(gv.sel1[0])
		gv.dag_path = gv.selection_list.getDagPath(0)
		# creating Mfn Mesh
		gv.mfn_mesh1 = om.MFnMesh(gv.dag_path)

		#get the full number of vertex in mesh for loop
		gv.pp = gv.mfn_mesh1.getPoints()
		gv.length = len(gv.pp)

		#looping to get vertex coordinates of all points in first mesh
		gv.Q = 0
		while gv.Q < gv.length:
			gv.points1 = gv.mfn_mesh1.getPoint(gv.Q, space=om.MSpace.kWorld)
			gv.Q = gv.Q+1

	def Get_Bone_Data_func():
		gv.selected = cmds.select(gv.bone)
		gv.b = cmds.xform(gv.selected,q=1,ws=1,t=1)
		gv.bx = gv.b[0]
		gv.by = gv.b[1]
		gv.bz = gv.b[2]
		gv.BonePoint = om.MPoint(gv.b)

		#loop to get distances of each verts from the selected bone
		gv.R = 0
		gv.distList = []
		while gv.R < gv.length:
			gv.distance = gv.BonePoint.distanceTo(gv.mfn_mesh1.getPoint(gv.R, space=om.MSpace.kWorld))
			gv.distList.append(gv.distance)
			gv.R = gv.R + 1

		#find the min distance vertex ID
		gv.minDist = (min(gv.distList))
		gv.minDistID = (gv.distList.index(min(gv.distList)))

		#giving the M1 variables the coordinates of the closest vertex to the bone
		gv.pointMin = gv.mfn_mesh1.getPoint(gv.minDistID, space=om.MSpace.kWorld)
		gv.M1X = gv.pointMin.x
		gv.M1Z = gv.pointMin.z
		gv.M1Y = gv.pointMin.y

	def New_mesh_func():
		# get the mesh vertex position
		gv.sel2 = cmds.ls(gv.newmesh)
		# get the dag path
		gv.selection_list = om.MSelectionList()
		gv.selection_list.add(gv.sel2[0])
		gv.dag_path = gv.selection_list.getDagPath(0)
		# creating Mfn Mesh
		gv.mfn_mesh2 = om.MFnMesh(gv.dag_path)

		#creating M2 variables to store coordinate of the closest vertex in the new mesh
		gv.points2 = gv.mfn_mesh2.getPoint(gv.minDistID, space=om.MSpace.kWorld)

		gv.M2X = gv.points2.x
		gv.M2Z = gv.points2.z
		gv.M2Y = gv.points2.y

	def vertex_offset_func():
		gv.offsetX = gv.M2X - (gv.M1X - gv.bx)
		gv.offsetY = gv.M2Y - (gv.M1Y - gv.by)
		gv.offsetZ = gv.M2Z - (gv.M1Z - gv.bz)

	def Set_Bone_Data_func():
		selected = cmds.select(gv.bone)
		#cmds.xform(selected,ws=1,t=(offsetX, offsetY, offsetZ))
		cmds.move(gv.offsetX, gv.offsetY, gv.offsetZ, absolute=True, ws=True, pcp=True)

	def select_loop_bones():
		cmds.select(gv.new_mesh)
		gv.newmesh = cmds.ls( selection=True )

		#selecting the bone
		cmds.select(gv.rig_root, hierarchy=False)
		children_joints = cmds.listRelatives(allDescendents=True, type='joint')
		cmds.select(children_joints, add=True)
		gv.bone_List = cmds.ls( selection=True )
		cmds.select( clear=True )

		#Starting bone loop
		gv.boneID = 0
		while gv.boneID < len(gv.bone_List):
			gv.bone = gv.bone_List[gv.boneID]

			#run OG_Mesh file
			OG_Mesh_func()
			#run Get_Bone_Data file
			Get_Bone_Data_func()
			#run New_Mesh file
			New_mesh_func()
			#run Vertex_Offset file
			vertex_offset_func()
			#run Set_Bone_data file
			Set_Bone_Data_func()

			gv.boneID = gv.boneID+1

	select_loop_bones()




	#Bind New skin
	cmds.select( clear=True )

	cmds.select(gv.rig_root, hierarchy=True)
	root_heirarchy = cmds.ls(sl=True)

	for node in root_heirarchy:
		#print(node)
		node_type = cmds.nodeType(node)
		if node_type == "joint":
			rootjoint_node = node
			break

			

	#now bind skinning
	cmds.select( clear=True )
	cmds.select(rootjoint_node)
	cmds.select(gv.new_mesh, add=True)
	#cmds.bindSkin(toAll=True, byClosestPoint=True, colorJoints=True)
	mel.eval('newSkinCluster " -bindMethod 0  -normalizeWeights 1 -weightDistribution 0 -mi 3  -dr 4 -rui false  , multipleBindPose, 1";')
	cmds.select( clear=True )
	cmds.confirmDialog( title='Skeleton Fitted', message='Skeleton has been moved', button=['Alright'] )

#Function to copy skin weights using maya inbuilt UV space
def copySkinWeightsUV(_):
	# transferring skin weights using UV space
	cmds.select(gv.ogmesh)
	cmds.select(gv.new_mesh, add=True)

	mel.eval('copySkinWeights -noMirror -surfaceAssociation closestPoint -uvSpace UVChannel_1 UVChannel_1 -influenceAssociation closestJoint -influenceAssociation oneToOne -influenceAssociation oneToOne;')


	cmds.select( clear=True )
	cmds.confirmDialog( title='Skin Weights Copied', message='Skin Weights Copied', button=['Dismiss'] )

#Copying skin weights using vertex ID 
def exportWeightsdiceat(*args): 
	cmds.select(clear=True)
	cmds.select(gv.ogmesh)
	geoData = utils.geoInfo(vtx=1, geo=1, skinC=1)
	selVTX = geoData[0]
	skinClusterNM = geoData[2]
	thV = 0.001



	# dictionary to hold all the vertice & relationships
	mgv.verticeDict = utils.getVertexWeights(vertexList=selVTX, skinCluster=skinClusterNM, thresholdValue=thV)



	cmds.select(clear=True)
	cmds.select(gv.new_mesh)
	selectGeoData = utils.geoInfo(geo=1, skinC=1)
	geoName = selectGeoData[0]
	skinClusterNM = selectGeoData[1]
	
	if len(mgv.verticeDict) > 0:
		
		for key in list(mgv.verticeDict.keys()):
			
			newKey = str(gv.new_mesh)+"."+key.split("Shape.")[1]

			try:
				cmds.skinPercent(skinClusterNM, newKey, tv=mgv.verticeDict[key], zri=1)
			except:
				cmds.error("Something went wrong with the skinning")
		
		print("{0} vertices were set to specificed values.".format(len(list(mgv.verticeDict.keys())))) ##
	else:
		cmds.error("Dict was empty ")

	cmds.confirmDialog( title='Skin Weights Copied', message='Skin Weights Copied Using Dictionary', button=['Dismiss'] )


#Creating UI
def RevUI(*args):
	if cmds.window("RevBS", q=1, exists=1) == True:
		cmds.deleteUI("RevBS")
	
	#main Window
	cmds.window("RevBS", title="Rev's Rig Tool v2.0", width=450, height=650, sizeable=False)

	cmds.columnLayout("AllLayout", width=450, height=650,  parent="RevBS")

	#first column - Title
	cmds.columnLayout("TitleColumn", width=450, height=50,  parent="AllLayout")
	cmds.text(label="TRANSFER RIGGED SKELETON TO SCALED OR MODIFIED MESH",  width=450, height=50, align="center", fn="boldLabelFont")

	#selecting the mesh UI
	cmds.columnLayout("col_selectmesh", parent="AllLayout")
	cmds.text(label="PART I",  width=450, height=30, backgroundColor=[0.274, 0.619, 0.920], align="center")
	cmds.text(label="Select and click corresponding buttons.",  width=450, height=30, align="left")

	#each of the select mesh rows
	cmds.rowLayout("row_selectmesh1", numberOfColumns=2, parent="col_selectmesh")
	headmeshTXT = cmds.textField("headmeshTXT", backgroundColor=[0.1, 0.1, 0.1], editable=False, width=300, height=28, p="row_selectmesh1")
	cmds.button("selectHeadBtn", label="<<    Original Mesh", width = 150, height=26, command=button_wrapper(store_og, headmeshTXT))

	#each of the select mesh rows
	cmds.rowLayout("row_selectmesh2", numberOfColumns=2, parent="col_selectmesh")
	teethmeshTXT= cmds.textField("teethmeshTXT",backgroundColor=[0.1, 0.1, 0.1], editable=False, width=300, height=28, p="row_selectmesh2")
	cmds.button("selectTeethBtn", label="<<    Modified Mesh", width = 150, height=26, command=button_wrapper(store_new, teethmeshTXT))

	#each of the select mesh rows
	cmds.rowLayout("row_selectmesh3", numberOfColumns=2, parent="col_selectmesh")
	teethmeshTXT= cmds.textField("jointTXT",backgroundColor=[0.1, 0.1, 0.1], editable=False, width=300, height=28, p="row_selectmesh3")
	cmds.button("selectJointBtn", label="<<    Root Joint", width = 150, height=26, command=button_wrapper(store_joint, teethmeshTXT))


	#Fit skeleton button
	cmds.columnLayout("col_getbs", parent="AllLayout")
	cmds.text(label="IF ALL IS SELECTED, THEN RUN THIS",  width=450, height=30, align="center")

	cmds.rowLayout("row_get_bs", numberOfColumns=3,  width=450, height=30, parent="col_getbs")
	cmds.text(label="        ",  width=112, height=5, align="center") #empty space to align the button in middle
	cmds.button(width=225, label="FIT THE SKELETON", backgroundColor=[0.80, 0.65, 0.0], align="center", command=  toolkit)
	cmds.text(label="        ",  width=112, height=5, align="center")  #empty space to align the button in middle


	#Part II
	cmds.columnLayout("col_skin", parent="AllLayout")
	cmds.text(label="PART II",  width=450, height=30, backgroundColor=[0.274, 0.619, 0.920], align="center")
	cmds.text(label="ONCE FITTED, SKIN USING EITHER BUTTON",  width=450, height=30, align="center")

	cmds.rowLayout("row_skin", numberOfColumns=2,  width=450, height=50, parent="col_skin")
	cmds.button(label="UV Method", backgroundColor=[0.80, 0.65, 0.0], align="left", width = 225, height=26, command=  copySkinWeightsUV)
	cmds.button(label="Dictionary Method (Slow)", backgroundColor=[0.80, 0.65, 0.0], align="center", width = 225, height=26, command=  exportWeightsdiceat)

	cmds.columnLayout("col_note", parent="AllLayout")
	cmds.text(label="              ",  width=450, height=30, align="left")
	cmds.text(label=" NOTE: The old mesh and new mesh should have the same topology and vertex ID",  width=450, height=30, align="left", bgc=[0.79, 0.45, 0.45])
	cmds.text(label="              ",  width=450, height=5, align="left")
	cmds.text(label=" UV METHOD: Quick but needs same UV (same sets as well) without overlap",  width=450, height=30, align="left", bgc=[0.79, 0.45, 0.45])
	cmds.text(label="              ",  width=450, height=5, align="left")
	cmds.text(label=" DICTIONARY METHOD: Very SLOW but accurate, independent of UV  (RECOMMENDED)",  width=450, height=30, align="left", bgc=[0.79, 0.45, 0.45])
	cmds.text(label="              ",  width=450, height=5, align="left")
	cmds.text(label="Written by Rev O'Conner    |     Go to www.revoconner.com",  width=450, height=50, align="center")
	cmds.text(label="Non Commercial Use Only",  width=450, height=15, align="center", fn="boldLabelFont")





	cmds.separator(h=50,p="col_getbs")

	cmds.showWindow("RevBS")


RevUI()

