from maya import cmds
import maya.api.OpenMaya as om
import os
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


#instancing this class name into an variable to call variables inside of functions

gv = globalVar()

def button_wrapper(fn, *args, **kwargs):
	def wrapped(_):
		fn(*args, **kwargs)
	return wrapped

def store_og(txt_field):
	ui_sel = cmds.ls(sl=True)
	cmds.textField(txt_field, edit=True, text= ui_sel[0])
	gv.ogmesh
	gv.ogmesh= ui_sel[0]
	return gv.ogmesh
	
def store_new(txt_field):
	ui_sel = cmds.ls(sl=True)
	cmds.textField(txt_field, edit=True, text= ui_sel[0])
	gv.new_mesh
	gv.new_mesh = ui_sel[0]
	return gv.new_mesh

def store_joint(txt_field):
	ui_sel = cmds.ls(sl=True)
	cmds.textField(txt_field, edit=True, text= ui_sel[0])
	gv.rig_root
	gv.rig_root = ui_sel[0]
	return gv.rig_root





#Enter Wrapped Head Mesh Name below
# gv.new_mesh = "UE4_Male002"
# gv.ogmesh = "UE4_Male001"
# gv.rig_root = "UE:Masterhlpr1C"
gv.namespace_flag = "True"






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

	cmds.select(gv.ogmesh)
	cmds.select(gv.new_mesh, add=True)

	mel.eval('copySkinWeights -noMirror -surfaceAssociation closestPoint -uvSpace UVChannel_1 UVChannel_1 -influenceAssociation closestJoint -influenceAssociation oneToOne -influenceAssociation oneToOne;')


	cmds.select( clear=True )
	cmds.delete(gv.ogmesh)
	#confirm box
	cmds.confirmDialog( title='Reset Done', message='Proceed now', button=['Yes'] )




def RevUI(*args):
	if cmds.window("RevBS", q=1, exists=1) == True:
		cmds.deleteUI("RevBS")
	
	#main Window
	cmds.window("RevBS", title="Rev's Rig Tool", width=450, height=350, sizeable=False)

	cmds.columnLayout("AllLayout", width=450, height=350,  parent="RevBS")

	#first column - Title
	cmds.columnLayout("TitleColumn", width=450, height=50,  parent="AllLayout")
	cmds.text(label="Fit rigged skeleton to scaled or modified mesh",  width=450, height=50, align="center", fn="boldLabelFont")


	#selecting the mesh UI
	cmds.columnLayout("col_selectmesh", parent="AllLayout")
	cmds.text(label="Written by Rev O'Conner    |     Go to www.revoconner.com",  width=450, height=30, backgroundColor=[0.274, 0.519, 0.720], align="center")
	cmds.text(label="Select and click corresponding buttons.",  width=450, height=30, align="left")
	cmds.text(label="The old mesh and the new mesh should have same topology and UV.",  width=450, height=30, align="left")

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


	#getting the bs buttons
	cmds.columnLayout("col_getbs", parent="AllLayout")
	cmds.text(label="IF ALL IS SELECTED, THEN RUN THIS",  width=450, height=30, align="center")

	cmds.rowLayout("row_get_bs", numberOfColumns=2,  width=450, height=50, parent="col_getbs")
	cmds.button(width=450, label="FIT THE SKELETON", backgroundColor=[0.79, 0.73, 0.93], align="center", command=  toolkit)



	cmds.separator(h=50,p="col_getbs")

	cmds.showWindow("RevBS")


RevUI()

