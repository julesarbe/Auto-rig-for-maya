import maya.cmds as cmds
import maya.OpenMaya as om
import math as math 

# ----------------------------------------------------------------------------------------------------------------------------------

##### WINDOWS #####
    
# Creation of the Auto-rig tool window.
win = cmds.window(title = "Auto-rig Tool", widthHeight = (500, 600))

cmds.columnLayout(adjustableColumn = True)

# Menu formatting.
cmds.rowColumnLayout(numberOfColumns = 2, rowSpacing = [5, 5])

cmds.text("Name of the character", label = "Character_Name")
nameChara = cmds.textFieldGrp(tx = "NormalGuy")

# Button who allow to choose the number of spine locators.
cmds.text("Spine Count (1 at 10)", label = "Number of spine bones")
spineCount = cmds.intField(minValue = 1, maxValue = 10, value = 2, width = 40)

cmds.separator(height = 10, style = "double")
cmds.separator(height = 10, style = "double")

# Button who allows to create the locators of the body.
cmds.button(label = "Create meta-rig", width = 200, command = "create_metarig()")

# Button who allows to delete the locators of the body.
cmds.button(label = "Delete meta-rig", width = 200, command = "delete_metarig()")

cmds.separator(height = 10, style = "double")
cmds.separator(height = 10, style = "double")

# Button who allows to create IK.
cmds.button(label = "Create Rig", width = 200, command = "create_rig()")
cmds.button(label = "Delete Rig", width = 200, command = "delete_rig()")

cmds.separator(height = 10, style = "double")
cmds.separator(height = 10, style = "double")


# Display the window.
cmds.showWindow(win)

# ----------------------------------------------------------------------------------------------------------------------------------

##### GENERAL FUNCTIONS CALLED BY THE UI #####

def create_metarig(): 
    create_locators()
    #create_temporary_joints()
    
def delete_metarig ():
    delete_locators()
    #delete_temporary_joints()
    
def create_rig():
    create_IK()
    create_Controllers()
    createConstraints()
    
def delete_rig():
    return None
# ----------------------------------------------------------------------------------------------------------------------------------

##### MarkingMenu ####

MENU_NAME = "markingMenu"

class markingMenu(): 

    def __init__(self):
        self._removeOld()
        self._build()
    
    def _removeOld(self):
        if cmds.popupMenu(MENU_NAME, ex=1):
            cmds.deleteUI(MENU_NAME)
        
    def _build(self):
        """CTRL_Middle_markingmenu"""
        menu = cmds.popupMenu(MENU_NAME, mm = 1, b = 2, aob = 1, ctl = 1, alt=0, sh=0, p = "viewPanes", pmo=1, pmc = self._buildMarkingMenu)
    
    def _buildMarkingMenu(self, menu, parent):
        ## Radial positioned
        cmds.menuItem(p=menu, l="Match IK/FK", rp="N", c=matchIKFK)
        cmds.menuItem(p=menu, l="Switch IK/FK", rp="E", c=switchIKFK)
        cmds.menuItem(p=menu, l="Match AND Switch ", rp="S", c=switchmatch)
 
markingMenu()   


# ----------------------------------------------------------------------------------------------------------------------------------

##### IKFKSwitch ####
def switchmatch(*args):
    matchIKFK()
    switchIKFK()

def switchIKFK (*args): 
    selection = str(cmds.ls(sl=True, long=True)[0])
    if selection.__contains__("Right"):
        if cmds.getAttr("CTRL_Right_Clavicle.IKFKSwitch")==1:
            cmds.setAttr("CTRL_Right_Clavicle.IKFKSwitch", 0)
        else:
            cmds.setAttr("CTRL_Right_Clavicle.IKFKSwitch", 1)
    if selection.__contains__("Left"):
        if cmds.getAttr("CTRL_Left_Clavicle.IKFKSwitch")==1:
            cmds.setAttr("CTRL_Left_Clavicle.IKFKSwitch", 0)
        else:
            cmds.setAttr("CTRL_Left_Clavicle.IKFKSwitch", 1)
            
def matchIKFK(*args):
    selection = str(cmds.ls(sl=True, long=True)[0])
    if selection.__contains__("IK"):
        if selection.__contains__("Right"):
            mathIKWithFK("Right")
        if selection.__contains__("Left"):
            mathIKWithFK("Left")
    if selection.__contains__("FK"):
        if selection.__contains__("Right"):
            matchFKWithIK("Right")
        if selection.__contains__("Left"):
            matchFKWithIK("Left")
    else: 
        print("please select IK or FK Wrist controller")       
       
def matchFKWithIK(Side):
    stick_upperarm = cmds.ls("CTRL_"+Side+"_UPPERARM_STICK")
    stick_lowerarm = cmds.ls("CTRL_"+Side+"_FOREARM_STICK")
    stick_hand = cmds.ls("CTRL_"+Side+"_HAND_FK_STICK")
    
    rotation_hand = cmds.xform(stick_hand, query = True, rotation = True)
    rotation_upperarm = cmds.xform(stick_upperarm, query = True, rotation = True)
    rotation_lowerarm = cmds.xform(stick_lowerarm, query = True, rotation = True)
    
    cmds.setAttr("CTRL_"+Side+"_HAND_FK.rotateX", rotation_hand[0])
    cmds.setAttr("CTRL_"+Side+"_HAND_FK.rotateY", rotation_hand[1])
    cmds.setAttr("CTRL_"+Side+"_HAND_FK.rotateZ", rotation_hand[2])

    cmds.setAttr("CTRL_"+Side+"_UPPERARM.rotateX", rotation_upperarm[0])
    cmds.setAttr("CTRL_"+Side+"_UPPERARM.rotateY", rotation_upperarm[1])
    cmds.setAttr("CTRL_"+Side+"_UPPERARM.rotateZ", rotation_upperarm[2])

    cmds.setAttr("CTRL_"+Side+"_FOREARM.rotateX", rotation_lowerarm[0])
    cmds.setAttr("CTRL_"+Side+"_FOREARM.rotateY", rotation_lowerarm[1])
    cmds.setAttr("CTRL_"+Side+"_FOREARM.rotateZ", rotation_lowerarm[2])

def mathIKWithFK(Side):
    IK_stick = cmds.ls("CTRL_"+Side+"_HAND_IK_STICK")
    pole_vector_ctrl = cmds.ls("CTRL_"+Side+"_POLE_VECTOR")
    position = cmds.xform (IK_stick, translation = True, query=True)
    rotation = cmds.xform (IK_stick, rotation = True, query=True)
    
    cmds.setAttr("CTRL_"+Side+"_HAND_IK.translateX", position[0])
    cmds.setAttr("CTRL_"+Side+"_HAND_IK.translateY", position[1])
    cmds.setAttr("CTRL_"+Side+"_HAND_IK.translateZ", position[2])

    cmds.setAttr("CTRL_"+Side+"_HAND_IK.rotateX", rotation[0])
    cmds.setAttr("CTRL_"+Side+"_HAND_IK.rotateY", rotation[1])
    cmds.setAttr("CTRL_"+Side+"_HAND_IK.rotateZ", rotation[2])
    
    clavicle_pos = cmds.xform("Tool_RIG_FK_"+Side+"_Clavicle", q=True, ws=True, t=True)
    elbow_pos = cmds.xform("Tool_RIG_FK_"+Side+"_UpperArm", q=True, ws=True, t=True)
    hand_pos = cmds.xform("Tool_RIG_FK_"+Side+"_LowerArm", q=True, ws=True, t=True)
    
    cmds.xform("CTRL_"+Side+"_POLE_VECTOR", t=(0,0,0), ws=True)
    original_pos = cmds.xform("CTRL_"+Side+"_POLE_VECTOR", sp=True, query = True, ws=True)
    projection, pole_vector = getPoleVector (clavicle_pos, elbow_pos, hand_pos)
    
    t = (round(pole_vector.x-original_pos[0],2), round(pole_vector.y-original_pos[1],2), round(pole_vector.z-original_pos[2],2))
    cmds.xform("CTRL_"+Side+"_POLE_VECTOR", t=t, ws=True)


def getPoleVector (clavicle_pos, elbow_pos, hand_pos):
    
   clavicle_pos = om.MVector(clavicle_pos[0], clavicle_pos[1], clavicle_pos[2])
   elbow_pos = om.MVector(elbow_pos[0], elbow_pos[1], elbow_pos[2])
   hand_pos = om.MVector(hand_pos[0], hand_pos[1], hand_pos[2])
   
   elbow_vector = elbow_pos - clavicle_pos
   hand_vector = hand_pos - clavicle_pos
   
   mid_point = (clavicle_pos/2) + (hand_pos/2)
   projection = ((elbow_vector*hand_vector)/(hand_vector*hand_vector))
   projection_pos = clavicle_pos + hand_vector*projection
   
   pole_vector = elbow_pos - projection_pos
   pole_pos = elbow_pos + pole_vector/(pole_vector*pole_vector)*0.2
   
   return projection_pos, pole_pos
# ----------------------------------------------------------------------------------------------------------------------------------

##### Constraints #####
def createConstraints():
    spineCountValue = cmds.intField(spineCount, query = True, value = True)  
    createBasicConstraints(spineCountValue)    
    createIKArmConstraints("Right")
    createIKArmConstraints("Left")
    createFootConstraints("Right")
    createFootConstraints("Left") 
    createFKArmConstraints("Right")
    createFKArmConstraints("Left")
    createIKFKSwitch("Left")
    createIKFKSwitch("Right")
    createFKArmStick("Left")
    createFKArmStick("Right")
    createIKArmStick("Left")
    createIKArmStick("Right")
    lockJoints()
    fix()

def fix():
    cmds.setAttr("Tool_RIG_Right_UpperArm_orientConstraint1.offsetY", 0.0) 
   
def createIKFKSwitch(Side):
    cmds.orientConstraint(cmds.ls("Tool_RIG_IK_"+Side+"_UpperArm"), cmds.ls("Tool_RIG_"+Side+"_UpperArm"), mo=True)
    cmds.orientConstraint(cmds.ls("Tool_RIG_IK_"+Side+"_Clavicle"), cmds.ls("Tool_RIG_"+Side+"_Clavicle"), mo=True)
    cmds.orientConstraint(cmds.ls("Tool_RIG_IK_"+Side+"_LowerArm"), cmds.ls("Tool_RIG_"+Side+"_LowerArm"), mo=True)
    
    cmds.connectAttr("CTRL_"+Side+"_HAND_IK.IK_Blend", "Tool_RIG_"+Side+"_Clavicle_orientConstraint1.Tool_RIG_IK_"+Side+"_ClavicleW0")
    cmds.connectAttr("CTRL_"+Side+"_HAND_IK.IK_Blend", "Tool_RIG_"+Side+"_UpperArm_orientConstraint1.Tool_RIG_IK_"+Side+"_UpperArmW0")
    cmds.connectAttr("CTRL_"+Side+"_HAND_IK.IK_Blend", "Tool_RIG_"+Side+"_LowerArm_orientConstraint1.Tool_RIG_IK_"+Side+"_LowerArmW0")
    
    cmds.orientConstraint(cmds.ls("Tool_RIG_FK_"+Side+"_UpperArm"), cmds.ls("Tool_RIG_"+Side+"_UpperArm"), mo=True)
    cmds.orientConstraint(cmds.ls("Tool_RIG_FK_"+Side+"_Clavicle"), cmds.ls("Tool_RIG_"+Side+"_Clavicle"), mo=True)
    cmds.orientConstraint(cmds.ls("Tool_RIG_FK_"+Side+"_LowerArm"), cmds.ls("Tool_RIG_"+Side+"_LowerArm"), mo=True)    
        
    cmds.connectAttr("CTRL_"+Side+"_HAND_FK.FK_Blend", "Tool_RIG_"+Side+"_Clavicle_orientConstraint1.Tool_RIG_FK_"+Side+"_ClavicleW1")
    cmds.connectAttr("CTRL_"+Side+"_HAND_FK.FK_Blend", "Tool_RIG_"+Side+"_UpperArm_orientConstraint1.Tool_RIG_FK_"+Side+"_UpperArmW1")
    cmds.connectAttr("CTRL_"+Side+"_HAND_FK.FK_Blend", "Tool_RIG_"+Side+"_LowerArm_orientConstraint1.Tool_RIG_FK_"+Side+"_LowerArmW1")
    
    cmds.connectAttr("CTRL_"+Side+"_Clavicle.IKFKSwitch", "CTRL_"+Side+"_HAND_IK.IK_Blend")
    tempNode = cmds.shadingNode("floatMath", au=True)  
    cmds.rename(tempNode, "mathNode_"+Side)
    cmds.connectAttr("CTRL_"+Side+"_Clavicle.IKFKSwitch","mathNode_"+Side+".floatB")
    cmds.setAttr("mathNode_"+Side+".floatA", 1)
    cmds.setAttr("mathNode_"+Side+".operation", 1)
    cmds.connectAttr("mathNode_"+Side+".outFloat", "CTRL_"+Side+"_HAND_FK.FK_Blend")

    
def createIKArmConstraints(Side):
    
    wrist_ctrl = cmds.ls("CTRL_"+Side+"_HAND_IK")
    wrist_IK = cmds.ls("IK_"+Side+"_Arm")
    wrist_joint = cmds.ls("Tool_RIG_IK_"+Side+"_LowerArm")
    
    cmds.pointConstraint(wrist_ctrl, wrist_IK, mo=True)
    cmds.orientConstraint(wrist_ctrl, wrist_joint, mo= True)
    
#    cmds.connectAttr("CTRL_"+Side+"_HAND_IK.Elbow_PV", "IK_"+Side+"_Arm.twist")
#    cmds.connectAttr("CTRL_"+Side+"_HAND_IK.IK_Blend", "IK_"+Side+"_Arm.ikBlend")
    cmds.connectAttr("CTRL_"+Side+"_HAND_IK.IK_Blend", "Tool_RIG_IK_"+Side+"_LowerArm_orientConstraint1.CTRL_"+Side+"_HAND_IKW0")
    #cmds.connectAttr("CTRL_"+Side+"_Clavicle.IKFKSwitch", "CTRL_"+Side+"_HAND_IK.visibility")
    #cmds.connectAttr("CTRL_"+Side+"_Clavicle.IKFKSwitch", "CTRL_"+Side+"_POLE_VECTOR.visibility")
    
def createFKArmStick(Side):
    upperarm_stick_ctrl = cmds.ls("CTRL_"+Side+"_UPPERARM_STICK")
    forearm_stick_ctrl = cmds.ls("CTRL_"+Side+"_FOREARM_STICK")
    wrist_stick_ctrl = cmds.ls("CTRL_"+Side+"_HAND_FK_STICK")
    
    upperarm_joint = cmds.ls("Tool_RIG_IK_"+Side+"_Clavicle")
    forearm_joint = cmds.ls("Tool_RIG_IK_"+Side+"_UpperArm")
    wrist_joint = cmds.ls("Tool_RIG_IK_"+Side+"_LowerArm")
    
    cmds.orientConstraint(upperarm_joint, upperarm_stick_ctrl, mo=True, w=1)
    cmds.orientConstraint(forearm_joint, forearm_stick_ctrl, mo=True, w=1)
    cmds.orientConstraint(wrist_joint, wrist_stick_ctrl, mo=True, w=1)
    
def createIKArmStick(Side):
    wrist_stick_ctrl = cmds.ls("CTRL_"+Side+"_HAND_IK_STICK")
    wrist_joint = cmds.ls("Tool_RIG_FK_"+Side+"_LowerArm")
    
    cmds.pointConstraint(wrist_joint, wrist_stick_ctrl, mo=True, w=1.0)
    cmds.orientConstraint(wrist_joint, wrist_stick_ctrl, mo=True, w=1.0)
    

def createFKArmConstraints(Side):
    upperarm_ctrl = cmds.ls("CTRL_"+Side+"_UPPERARM")
    forearm_ctrl = cmds.ls("CTRL_"+Side+"_FOREARM")
    wrist_ctrl = cmds.ls("CTRL_"+Side+"_HAND_FK")
    
    upperarm_joint = cmds.ls("Tool_RIG_FK_"+Side+"_Clavicle")
    forearm_joint = cmds.ls("Tool_RIG_FK_"+Side+"_UpperArm")
    wrist_joint = cmds.ls("Tool_RIG_FK_"+Side+"_LowerArm")
    
    cmds.orientConstraint(upperarm_ctrl, upperarm_joint, mo=True, w=1.0)
    cmds.orientConstraint(forearm_ctrl, forearm_joint, mo=True, w=1.0)
    cmds.orientConstraint(wrist_ctrl, wrist_joint, mo=True, w=1.0)
    
    #tempNode = cmds.shadingNode("floatMath", au=True)  
    #cmds.rename(tempNode, "Inverse_"+Side)
    #cmds.setAttr("Inverse_"+Side+".floatB", -1) 
    #cmds.connectAttr("CTRL_"+Side+"_Clavicle.IKFKSwitch","Inverse_"+Side+".floatA")
    #cmds.connectAttr("Inverse_"+Side+".outFloat", "CTRL_"+Side+"_UPPERARM.visibility")
    
   
def createFootConstraints(Side):

    foot_ctrl = cmds.ls("CTRL_"+Side+"_Foot")
    foot_IK = cmds.ls("IK_"+Side+"_Leg")
    foot_joint = cmds.ls("Tool_RIG_"+Side+"_Ankle")
    
    cmds.pointConstraint(foot_ctrl, foot_IK, mo=True)
    cmds.orientConstraint(foot_ctrl, foot_joint, mo= True)
    
    cmds.connectAttr("CTRL_"+Side+"_Foot.Knee_Twist", "IK_"+Side+"_Leg.twist")
    
def createBasicConstraints(spineCount):
    cmds.pointConstraint(cmds.ls("CTRL_HIPS"), cmds.ls("Tool_RIG_Root"))
    cmds.orientConstraint(cmds.ls("CTRL_ROT_HIPS"), cmds.ls("Tool_RIG_Root"), mo=True)
    cmds.pointConstraint(cmds.ls("CTRL_ROT_HIPS"), cmds.ls("Tool_RIG_Root"), mo=True)
    
    
    for i in range(spineCount):
        cmds.orientConstraint(cmds.ls("CTRL_SPINE_"+str(i+1)), cmds.ls("Tool_RIG_Spine"+str(i+1)))
        cmds.pointConstraint(cmds.ls("Tool_RIG_Spine"+str(i+1)), cmds.ls("CTRL_SPINE_"+str(i+1)))

    for Side in ["Right", "Left"]:
        locator = cmds.spaceLocator(name = "Locator_"+Side+"_Clavicle")
        cmds.scale(0.1, 0.1, 0.1, locator)
        position = cmds.xform(cmds.ls("Tool_Locator_"+Side+"_Upper_Arm"), query = True, translation = True, worldSpace = True)
        cmds.move(position[0], position[1], position[2], locator)
        cmds.parent(locator, cmds.ls("CTRL_"+Side+"_Clavicle"))
        cmds.pointConstraint(locator, cmds.ls("Tool_RIG_"+Side+"_Clavicle"))
        cmds.pointConstraint(locator, cmds.ls("Tool_RIG_IK_"+Side+"_Clavicle"))
        cmds.pointConstraint(locator, cmds.ls("Tool_RIG_FK_"+Side+"_Clavicle"))
    
    cmds.orientConstraint(cmds.ls("CTRL_NECK"), cmds.ls("Tool_RIG_Neck_Start"))
    cmds.orientConstraint(cmds.ls("CTRL_HEAD"), cmds.ls("Tool_RIG_Head"))
    
def lockJoints():
    joints = cmds.ls("Tool_RIG_*")
    cmds.setAttr("Tool_RIG_Root.template", 1)
        

# ----------------------------------------------------------------------------------------------------------------------------------

##### Controllers #####

def create_Controllers ():
    spineCountValue = cmds.intField(spineCount, query = True, value = True) 
    charaName = cmds.textFieldGrp(nameChara, query = True, text=True) 
    createSpineControllers(spineCountValue, charaName)  
    createClavicle(spineCountValue, "Right")
    createClavicle(spineCountValue, "Left")
    createWristIK(spineCountValue, "Right")
    createWristIK(spineCountValue, "Left")
    createLegControllers("Right", charaName)
    createLegControllers("Left", charaName)
    createNeck(spineCountValue)
    createHead()
    createArmFK(spineCountValue, "Right")
    createArmFK(spineCountValue, "Left")
    createArmStick(spineCountValue,"Right")
    createArmStick(spineCountValue,"Left")
    addColors()
  
def addColors():
    cmds.setAttr("CTRL_NormalGuy_MASTER.overrideEnabled", 1)
    cmds.setAttr("CTRL_NormalGuy_MASTER.overrideColor", 6)
    
    cmds.setAttr("CTRL_Left_Clavicle.overrideEnabled", 1)
    cmds.setAttr("CTRL_Left_Clavicle.overrideColor", 16)
    cmds.setAttr("CTRL_Left_HAND_IK.overrideEnabled", 1)
    cmds.setAttr("CTRL_Left_HAND_IK.overrideColor", 4)
    cmds.setAttr("CTRL_Left_POLE_VECTOR.overrideEnabled", 1)
    cmds.setAttr("CTRL_Left_POLE_VECTOR.overrideColor", 4)
    
    
    cmds.setAttr("CTRL_Right_Clavicle.overrideEnabled", 1)
    cmds.setAttr("CTRL_Right_Clavicle.overrideColor", 17)
    cmds.setAttr("CTRL_Right_HAND_IK.overrideEnabled", 1)
    cmds.setAttr("CTRL_Right_HAND_IK.overrideColor", 4)
    cmds.setAttr("CTRL_Right_POLE_VECTOR.overrideEnabled", 1)
    cmds.setAttr("CTRL_Right_POLE_VECTOR.overrideColor", 4)
    
    cmds.setAttr("CTRL_Left_Foot.overrideEnabled", 1)
    cmds.setAttr("CTRL_Left_Foot.overrideColor", 4)

    cmds.setAttr("CTRL_Right_Foot.overrideEnabled", 1)
    cmds.setAttr("CTRL_Right_Foot.overrideColor", 4)
    
    cmds.setAttr("CTRL_ROT_HIPS.overrideEnabled", 1)
    cmds.setAttr("CTRL_ROT_HIPS.overrideColor", 29)
    
    cmds.setAttr("CTRL_NECK.overrideEnabled", 1)
    cmds.setAttr("CTRL_NECK.overrideColor", 10)
    
    cmds.getAttr("CTRL_ROT_HIPS.overrideColor")

   
def jointCoordByName (jointName):
    joint = cmds.ls(jointName)[0]
    return cmds.xform(joint, query=True, translation=True, worldSpace=True)
    
def createSpineControllers(spineCount, charaName):
    master_ctrl = cmds.circle(nr=(0,1,0), c=(0,0,0), radius = 1.5, s=16, name = "CTRL_"+charaName+"_MASTER")
    cmds.makeIdentity(master_ctrl, apply = True, t=1, r=1,s=1)
    hip_ctrl = cmds.circle(nr=(0,1,0), c=(0,0,0), radius = 1, s=16, name = "CTRL_HIPS")
    hipsCoord = jointCoordByName("Tool_RIG_Root")
    cmds.move(hipsCoord[0],hipsCoord[1],hipsCoord[2], hip_ctrl) 
    cmds.makeIdentity(hip_ctrl, apply = True, t=1, r=1,s=1)
    cmds.parent(hip_ctrl, "CTRL_"+charaName+"_MASTER")
    
    hip_rot_ctrl = cmds.curve(p = [(0.5,0,0), (0.25, 0, -0.5), (-0.25, 0, -0.5), (-0.5,0,0), (-0.25, 0, 0.5), (0.25, 0, 0.5), (0.5, 0,0)], degree = 1, name = "CTRL_ROT_HIPS")
    hipsrotCoord = jointCoordByName("Tool_RIG_Root")
    hipsrotCoord2=jointCoordByName("Tool_RIG_Spine1")
    cmds.move(hipsCoord[0],hipsCoord[1],hipsCoord[2], hip_rot_ctrl)
    cmds.move(hipsrotCoord2[0], hipsrotCoord2[1], hipsrotCoord2[2], hip_rot_ctrl+".scalePivot", hip_rot_ctrl+".rotatePivot")
    cmds.makeIdentity(hip_rot_ctrl, apply = True, t=1, r=1,s=1)
    cmds.parent(hip_rot_ctrl, "CTRL_HIPS")
    
    for i in range (1,spineCount+1): 
        spineCoord = jointCoordByName("Tool_RIG_Spine"+str(i))
        spine_ctrl = cmds.circle(nr=(0,1,0), c=(0,0,0), radius = 1, s=16, name = "CTRL_SPINE_"+str(i))
        cmds.move(spineCoord[0], spineCoord[1], spineCoord[2], spine_ctrl)
        cmds.scale(0.5, 0.5, 0.5, spine_ctrl)
        if (i == 1):
            cmds.parent(spine_ctrl, "CTRL_HIPS")
        else:
            cmds.parent(spine_ctrl, "CTRL_SPINE_"+str(i-1))
    
def createLegControllers(Side, charaName):
    footCoord = jointCoordByName("Tool_RIG_"+Side+"_Football")
    foot_ctrl = cmds.curve(p = [(1,0,0),(1,0,2),(-1,0,2),(-1,0,0),(1,0,0)], degree = 1, name = "CTRL_"+Side+"_Foot")
    cmds.move(footCoord[0], 0, footCoord[2], foot_ctrl)
    
    cmds.addAttr(shortName = "KF", longName = "Knee_Twist", attributeType = 'double', defaultValue = 0, minValue = -100, maxValue = 100, keyable = True)            
    cmds.addAttr(shortName = "KR", longName = "Knee_Fix", attributeType = 'double', defaultValue = 0, minValue = 0, maxValue = 100, keyable = True)            
    cmds.addAttr(shortName = "FR", longName = "Foot_Roll", attributeType = 'double', defaultValue = 0, minValue = 0, maxValue = 100, keyable = True)            
    cmds.addAttr(shortName = "BR", longName = "Ball_Roll", attributeType = 'double', defaultValue = 0, minValue = 0, maxValue = 100, keyable = True) 
    
    
    cmds.scale(0.1,0.1,0.2,foot_ctrl)
    cmds.makeIdentity(foot_ctrl, apply = True, t=1, r=1,s=1)
    cmds.parent(foot_ctrl, "CTRL_"+charaName+"_MASTER")
    
def createClavicle (spineCount, Side):
    clavicle_ctrl = cmds.curve(p = [(1,0,0),(1,1,1),(1,1.5,2),(1,1.7,3),(1,1.5,4),(1,1,5),(1,0,6),(-1, 0,6),(-1,1,5),(-1,1.5,4),(-1,1.7,3),(-1,1.5,2),(-1,1,1),(-1,0,0)], degree = 1, name = "CTRL_"+Side+"_Clavicle")
    cmds.scale(0.05, 0.05, 0.05, clavicle_ctrl)
    
    armCoord = jointCoordByName("Tool_RIG_"+Side+"_Clavicle")
    clavicleCoord = jointCoordByName("Tool_RIG_Spine"+str(spineCount))
    
    cmds.move(armCoord[0], armCoord[1]+0.1, armCoord[2]-0.17, clavicle_ctrl)
    cmds.move(clavicleCoord[0], clavicleCoord[1], clavicleCoord[2], clavicle_ctrl+".scalePivot", clavicle_ctrl+".rotatePivot")
    
    cmds.addAttr(shortName = "IKFK", longName = "IKFKSwitch", attributeType = 'double', defaultValue = 0, minValue = 0, maxValue = 1, keyable = True)
    
    cmds.makeIdentity(clavicle_ctrl, apply=True, t=1, r=1, s=1)
    cmds.parent(clavicle_ctrl, "CTRL_SPINE_"+str(spineCount))

def createWristIK(spineCount, Side):
    wrist_ctrl = cmds.circle(nr = (1,0,0), c=(0,0,0), radius = 0.2, s=16, name="CTRL_"+Side+"_HAND_IK")
    IK = cmds.ls("IK_"+Side+"_Arm")
    
    wristCoord = jointCoordByName("Tool_RIG_"+Side+"_LowerArm")
    elbowCoord = jointCoordByName("Tool_RIG_"+Side+"_UpperArm")
    clavicleCoord = jointCoordByName("Tool_RIG_"+Side+"_Clavicle")
    
    cmds.addAttr(shortName = "PV", longName = "Elbow_PV", attributeType = 'double', defaultValue = 0, minValue = -100, maxValue = 100, keyable = True)
    cmds.addAttr(shortName ="IK", longName = "IK_Blend", attributeType = 'double', defaultValue = 1, minValue = 0, maxValue = 1, keyable = True)
    cmds.move(wristCoord[0], wristCoord[1], wristCoord[2], wrist_ctrl)
    cmds.makeIdentity(wrist_ctrl, apply=True, t=1, r=1, s=1)
    cmds.parent(wrist_ctrl, "CTRL_"+Side+"_Clavicle")
    
    polevector_ctrl = cmds.circle(nr = (0,0,1), c=(0,0,0), radius = 0.05, s=16, name="CTRL_"+Side+"_POLE_VECTOR")
    cmds.move(elbowCoord[0], elbowCoord[1], elbowCoord[2]-0.5, polevector_ctrl)
    cmds.makeIdentity(polevector_ctrl, apply=True, t=1, r=1, s=1)
    cmds.parent(polevector_ctrl, "CTRL_"+Side+"_Clavicle")
    
    cmds.poleVectorConstraint(polevector_ctrl, IK)

    pole_vector_curve = cmds.curve(p=[(0,0,0), (.5,0,0)], degree=0, name = "CTRL_"+Side+"_PoleVectorCurve")
    cmds.pointConstraint("Tool_RIG_"+Side+"_UpperArm", pole_vector_curve)
    cmds.aimConstraint("CTRL_"+Side+"_POLE_VECTOR", pole_vector_curve)
    cmds.setAttr("CTRL_"+Side+"_PoleVectorCurve.overrideEnabled", 1)
    cmds.setAttr("CTRL_"+Side+"_PoleVectorCurve.overrideColor", 4)
    
    
def createArmFK(spineCount, Side): 
    upperarm_ctrl = cmds.curve(p = [(0,0.5,0), (0, 0.25, -0.5), (0, -0.25, -0.5), (0,-0.5,0), (0, -0.25, 0.5), (0, 0.25, 0.5), (0, 0.5,0)], degree = 1, name="CTRL_"+Side+"_UPPERARM")
    forearm_ctrl = cmds.curve(p = [(0,0.5,0), (0, 0.25, -0.5), (0, -0.25, -0.5), (0,-0.5,0), (0, -0.25, 0.5), (0, 0.25, 0.5), (0, 0.5,0)], degree = 1, name="CTRL_"+Side+"_FOREARM")
    wrist_ctrl = cmds.curve(p = [(0,0.5,0), (0, 0.25, -0.5), (0, -0.25, -0.5), (0,-0.5,0), (0, -0.25, 0.5), (0, 0.25, 0.5), (0, 0.5,0)], degree = 1, name="CTRL_"+Side+"_HAND_FK")
    
    cmds.scale(0.5, 0.5, 0.5, upperarm_ctrl)
    cmds.scale(0.5, 0.5, 0.5, forearm_ctrl)
    cmds.scale(0.5, 0.5, 0.5, wrist_ctrl)
    
    clavicleCoord = jointCoordByName("Tool_RIG_"+Side+"_Clavicle")
    elbowCoord = jointCoordByName("Tool_RIG_FK_"+Side+"_UpperArm")
    wristCoord = jointCoordByName("Tool_RIG_FK_"+Side+"_LowerArm")
    
    cmds.move((clavicleCoord[0]+elbowCoord[0])/2, (clavicleCoord[1]+elbowCoord[1])/2, (clavicleCoord[2]+elbowCoord[2])/2, upperarm_ctrl)
    cmds.move((elbowCoord[0]+wristCoord[0])/2, (elbowCoord[1]+wristCoord[1])/2, (elbowCoord[2]+wristCoord[2])/2, forearm_ctrl)
    cmds.move(wristCoord[0], wristCoord[1], wristCoord[2], wrist_ctrl)
    
    if Side == "Left" :
        cmds.rotate(0, math.atan(abs(clavicleCoord[2]-elbowCoord[2])/abs(clavicleCoord[0]-elbowCoord[0]))*57.3, 0, upperarm_ctrl) 
        cmds.rotate(0, - math.atan(abs(elbowCoord[2]-wristCoord[2])/abs(elbowCoord[0]-wristCoord[0]))*57.3, 0, forearm_ctrl) 
    else:
        cmds.rotate(0, -math.atan(abs(clavicleCoord[2]-elbowCoord[2])/abs(clavicleCoord[0]-elbowCoord[0]))*57.3, 0, upperarm_ctrl)
        cmds.rotate(0, math.atan(abs(elbowCoord[2]-wristCoord[2])/abs(elbowCoord[0]-wristCoord[0]))*57.3, 0, forearm_ctrl)  
        
    cmds.move(clavicleCoord[0], clavicleCoord[1], clavicleCoord[2],  upperarm_ctrl+".scalePivot", upperarm_ctrl+".rotatePivot")
    cmds.move(elbowCoord[0], elbowCoord[1], elbowCoord[2],  forearm_ctrl+".scalePivot", forearm_ctrl+".rotatePivot")
    
    cmds.addAttr(wrist_ctrl, shortName = "FK", longName = "FK_Blend", attributeType = 'double', defaultValue = 1, minValue = 0, maxValue = 1, keyable = True)
    
    cmds.makeIdentity(upperarm_ctrl, apply = True, t=1, r=1,s=1)
    cmds.makeIdentity(forearm_ctrl, apply = True, t=1, r=1,s=1) 
    cmds.makeIdentity(wrist_ctrl, apply = True, t=1, r=1,s=1)    
    
    cmds.parent (upperarm_ctrl, "CTRL_"+Side+"_Clavicle")
    cmds.parent (forearm_ctrl, upperarm_ctrl)
    cmds.parent(wrist_ctrl, forearm_ctrl)

def createArmStick(spineCount,Side):
    upperarm_ctrl = cmds.curve(p = [(0,0.1,0), (0, 0.05, -0.1), (0, -0.05, -0.1), (0,-0.1,0), (0, -0.05, 0.1), (0, 0.05, 0.1), (0, 0.1,0)], degree = 1, name="CTRL_"+Side+"_UPPERARM_STICK")
    forearm_ctrl = cmds.curve(p = [(0,0.1,0), (0, 0.05, -0.1), (0, -0.05, -0.1), (0,-0.1,0), (0, -0.05, 0.1), (0, 0.05, 0.1), (0, 0.1,0)], degree = 1, name="CTRL_"+Side+"_FOREARM_STICK")
    wrist_ctrl = cmds.curve(p = [(0,0.1,0), (0, 0.05, -0.1), (0, -0.05, -0.1), (0,-0.1,0), (0, -0.05, 0.1), (0, 0.05, 0.1), (0, 0.1,0)], degree = 1, name="CTRL_"+Side+"_HAND_FK_STICK")
    wrist_IK_ctrl = cmds.curve(p = [(0,0.1,0), (0, 0.05, -0.1), (0, -0.05, -0.1), (0,-0.1,0), (0, -0.05, 0.1), (0, 0.05, 0.1), (0, 0.1,0)], degree = 1, name="CTRL_"+Side+"_HAND_IK_STICK")
    
    cmds.scale(0.5, 0.5, 0.5, upperarm_ctrl)
    cmds.scale(0.5, 0.5, 0.5, forearm_ctrl)
    cmds.scale(0.5, 0.5, 0.5, wrist_ctrl)
    
    clavicleCoord = jointCoordByName("Tool_RIG_"+Side+"_Clavicle")
    elbowCoord = jointCoordByName("Tool_RIG_FK_"+Side+"_UpperArm")
    wristCoord = jointCoordByName("Tool_RIG_FK_"+Side+"_LowerArm")
    
    cmds.move((clavicleCoord[0]+elbowCoord[0])/2, (clavicleCoord[1]+elbowCoord[1])/2, (clavicleCoord[2]+elbowCoord[2])/2, upperarm_ctrl)
    cmds.move((elbowCoord[0]+wristCoord[0])/2, (elbowCoord[1]+wristCoord[1])/2, (elbowCoord[2]+wristCoord[2])/2, forearm_ctrl)
    cmds.move(wristCoord[0], wristCoord[1], wristCoord[2], wrist_ctrl)
    cmds.move(wristCoord[0], wristCoord[1], wristCoord[2], wrist_IK_ctrl)
    
    if Side == "Left" :
        cmds.rotate(0, math.atan(abs(clavicleCoord[2]-elbowCoord[2])/abs(clavicleCoord[0]-elbowCoord[0]))*57.3, 0, upperarm_ctrl) 
        cmds.rotate(0, - math.atan(abs(elbowCoord[2]-wristCoord[2])/abs(elbowCoord[0]-wristCoord[0]))*57.3, 0, forearm_ctrl) 
    else:
        cmds.rotate(0, -math.atan(abs(clavicleCoord[2]-elbowCoord[2])/abs(clavicleCoord[0]-elbowCoord[0]))*57.3, 0, upperarm_ctrl)
        cmds.rotate(0, math.atan(abs(elbowCoord[2]-wristCoord[2])/abs(elbowCoord[0]-wristCoord[0]))*57.3, 0, forearm_ctrl)  
        
    cmds.move(clavicleCoord[0], clavicleCoord[1], clavicleCoord[2],  upperarm_ctrl+".scalePivot", upperarm_ctrl+".rotatePivot")
    cmds.move(elbowCoord[0], elbowCoord[1], elbowCoord[2],  forearm_ctrl+".scalePivot", forearm_ctrl+".rotatePivot")
    
    cmds.makeIdentity(upperarm_ctrl, apply = True, t=1, r=1,s=1)
    cmds.makeIdentity(forearm_ctrl, apply = True, t=1, r=1,s=1) 
    cmds.makeIdentity(wrist_ctrl, apply = True, t=1, r=1,s=1)
    cmds.makeIdentity(wrist_IK_ctrl, apply = True, t=1, r=1,s=1)
    
    cmds.parent (upperarm_ctrl, "CTRL_"+Side+"_Clavicle")
    cmds.parent (forearm_ctrl, upperarm_ctrl)
    cmds.parent(wrist_ctrl, forearm_ctrl)
    cmds.parent(wrist_IK_ctrl, "CTRL_"+Side+"_Clavicle")
    
    cmds.hide(upperarm_ctrl,forearm_ctrl,wrist_ctrl,wrist_IK_ctrl)
    
    
def createNeck(spineCount): 
    neck_ctrl = cmds.curve(p = [(0.5,0,0), (0.25, -0.25, -0.5), (-0.25, -0.25, -0.5), (-0.5,0,0), (-0.25, -0.25, 0.5), (0.25, -0.25, 0.5), (0.5, 0,0)], degree = 1, name = "CTRL_NECK")
    cmds.scale(0.3, 0.3, 0.3, neck_ctrl)
    neckEndCoord = jointCoordByName("Tool_RIG_Neck_End")
    neckStartCoord = jointCoordByName("Tool_RIG_Neck_Start")
    
    cmds.move(neckEndCoord[0], neckEndCoord[1]+0.1, neckEndCoord[2],  neck_ctrl)
    cmds.move(neckStartCoord[0], neckStartCoord[1], neckStartCoord[2],  neck_ctrl+".scalePivot", neck_ctrl+".rotatePivot")
    
    cmds.makeIdentity(neck_ctrl, apply = True, t = 1, r = 1, s = 1) 
    cmds.parent (neck_ctrl, "CTRL_SPINE_"+str(spineCount))

def createHead():
     head_ctrl = cmds.curve(p = [(0.5,0,0), (0.25,-0.25,-0.5), (0.25,-0.5, -0.5), (0,-0.6,-0.5),(-0.25,-0.5,-0.5), (-0.25, -0.25, -0.5), (-0.5,0,0), (-0.25, -0.25, 0.5), (-0.25, -0.5, 0.5), (0,-0.6, 0.5) ,(0.25, -0.5, 0.5),(0.25, -0.25, 0.5), (0.5,0,0)], degree = 1, name = "CTRL_HEAD")
     cmds.scale(0.3, 0.3, 0.3, head_ctrl)
     
     headCoord = jointCoordByName("Tool_RIG_Head")
     neckCoord = jointCoordByName("Tool_RIG_Neck_End")
     
     cmds.move(headCoord[0], headCoord[1]+0.3, headCoord[2],  head_ctrl)
     cmds.move(neckCoord[0], neckCoord[1], neckCoord[2],  head_ctrl+".scalePivot", head_ctrl+".rotatePivot")
     
     cmds.makeIdentity(head_ctrl, apply = True, t = 1, r = 1, s = 1) 
     cmds.parent (head_ctrl, "CTRL_NECK")

         
# ----------------------------------------------------------------------------------------------------------------------------------

##### IK #####
def create_IK ():
    create_joints()
    charaName = cmds.textFieldGrp(nameChara, query = True, text=True)
    create_IKHandles(charaName)
    

def create_IKHandles(charaName):
    
    cmds.select(deselect = True)
    cmds.select(cmds.ls(charaName+"_RIG"))
    
    IK_R_arm = cmds.ikHandle(name = "IK_Right_Arm", sj = cmds.ls("Tool_RIG_IK_Right_Clavicle")[0], ee = cmds.ls("Tool_RIG_IK_Right_LowerArm")[0], sol = "ikRPsolver")
    IK_L_arm = cmds.ikHandle(name = "IK_Left_Arm", sj = cmds.ls("Tool_RIG_IK_Left_Clavicle")[0], ee = cmds.ls("Tool_RIG_IK_Left_LowerArm")[0], sol = "ikRPsolver")
    
    IK_R_leg = cmds.ikHandle(name = "IK_Right_Leg", sj = cmds.ls("Tool_RIG_Right_UpperLeg")[0], ee = cmds.ls("Tool_RIG_Right_Ankle")[0], sol = "ikRPsolver")
    IK_L_leg = cmds.ikHandle(name = "IK_Left_Leg", sj = cmds.ls("Tool_RIG_Left_UpperLeg")[0], ee = cmds.ls("Tool_RIG_Left_Ankle")[0], sol = "ikRPsolver")
    
    cmds.hide(IK_R_arm,IK_L_arm,IK_R_leg,IK_L_leg)
    
     


# ----------------------------------------------------------------------------------------------------------------------------------

##### JOINTS #####

# Procedure who allows to create all the bones.
def create_joints():
    # Retrieve the values given by the user.
    name = cmds.textFieldGrp(nameChara, query = True, text=True)
    
    cmds.select(deselect = True)
    spineAmount = cmds.ls("Tool_Locator_Spine*", type = "transform")
    fingersAmount = cmds.ls("Tool_Locator_Fingers_*_0", type = "transform")
    
    if cmds.objExists(name+"_RIG"):
        print("RIG already exists")
    else:
        cmds.group(name = name+"_RIG", empty = True)
    
    allSpines = cmds.ls("Tool_Locator_Spine*", type = "locator")
    spine = cmds.listRelatives(allSpines, parent = True, fullPath = True)
    
    rootPos = cmds.xform(cmds.ls("Tool_Locator_Hips"), query=True, translation=True, worldSpace=True)
    rootJoint = cmds.joint(radius = 0.2, position = rootPos, name = "Tool_RIG_Root")
    
    n = create_joint_spine()
    create_joint_head(n)
    create_joint_arm(n, "Right")
    create_joint_arm(n, "Left")
    create_joint_leg("Right")
    create_joint_leg("Left")
    create_joint_fingers("Right")
    create_joint_fingers("Left")
    
    orient_joints("Right")
    orient_joints("Left")
    
    selection = cmds.ls("Tool_Locator_*", "Tool_Root")
    for empty in selection:
        cmds.hide(empty)
    
def orient_joints(Side):
    cmds.joint(cmds.ls("Tool_RIG_"+Side+"_Clavicle"), edit = True, sao = "yup", oj = "xyz", zso =True)
    cmds.joint(cmds.ls("Tool_RIG_"+Side+"_UpperArm"), edit = True, sao = "yup", oj = "xyz", zso =True)
    
    cmds.joint(cmds.ls("Tool_RIG_IK_"+Side+"_Clavicle"), edit = True, sao = "yup", oj = "xyz", zso =True)
    cmds.joint(cmds.ls("Tool_RIG_IK_"+Side+"_UpperArm"), edit = True, sao = "yup", oj = "xyz", zso =True)
    
    cmds.joint(cmds.ls("Tool_RIG_FK_"+Side+"_Clavicle"), edit = True, sao = "yup", oj = "xyz", zso =True)
    cmds.joint(cmds.ls("Tool_RIG_FK_"+Side+"_UpperArm"), edit = True, sao = "yup", oj = "xyz", zso =True)
        
def create_joint_spine ():
    allSpines = cmds.ls("Tool_Locator_Spine*", type = "locator")
    spine = cmds.listRelatives(allSpines, parent = True, fullPath = True)
    
    for i, s in enumerate(spine):
        pos = cmds.xform(s, query = True, translation = True, worldSpace = True)
        j = cmds.joint(radius = 0.1, position = pos, name = "Tool_RIG_Spine" + str(i+1))
    cmds.select(deselect = True)
    return (i)
        
def create_joint_head(n):
    cmds.select(deselect = True)
    cmds.select("Tool_RIG_Spine" + str(n+1))
    
    positionNeckStart = cmds.xform(cmds.ls("Tool_Locator_Neck_Start"), query = True, translation = True, worldSpace = True)
    positionNeckEnd = cmds.xform(cmds.ls("Tool_Locator_Neck_End"), query = True, translation = True, worldSpace = True)
    positionHead = cmds.xform(cmds.ls("Tool_Locator_Head"), query = True, translation = True, worldSpace = True)

    neckJoint = cmds.joint(radius = 0.05, position = positionNeckStart, name = "Tool_RIG_Neck_Start")
    cmds.joint(radius = 0.05, position = positionNeckEnd, name = "Tool_RIG_Neck_End")
    cmds.joint(radius = 0.15, position = positionHead, name = "Tool_RIG_Head")
    
    positionjawStart = cmds.xform(cmds.ls("Tool_Locator_Jaw_Start"), query = True, translation = True, worldSpace = True)
    positionjawEnd = cmds.xform(cmds.ls("Tool_Locator_Jaw_End"), query = True, translation = True, worldSpace = True)
    
    jawJointStart = cmds.joint(radius = 0.05, position = positionjawStart, name = "Tool_RIG_Jaw_Start")
    jawJointEnd = cmds.joint(radius = 0.05, position = positionjawEnd, name = "Tool_RIG_Jaw_End")
    cmds.select(deselect = True)
    
def create_joint_arm(n, attribute):
    cmds.select(deselect = True)
    cmds.select("Tool_RIG_Spine" + str(n+1))
    
    positionClavicle = cmds.xform(cmds.ls("Tool_Locator_"+attribute+"_Clavicle"), query = True, translation = True, worldSpace = True)
    positionArmStart = cmds.xform(cmds.ls("Tool_Locator_"+attribute+"_Upper_Arm"), query = True, translation = True, worldSpace = True)
    positionElbow = cmds.xform(cmds.ls("Tool_Locator_"+attribute+"_Elbow"), query = True, translation = True, worldSpace = True)
    positionWrist = cmds.xform(cmds.ls("Tool_Locator_"+attribute+"_Wrist"), query = True, translation = True, worldSpace = True)
    
    Clavicle = cmds.joint(radius = 0.05, position = positionArmStart, name = "Tool_RIG_"+attribute+"_Clavicle")
    Elbow = cmds.joint(radius = 0.1, position = positionElbow, name = "Tool_RIG_"+attribute+"_UpperArm")
    Wrist = cmds.joint(radius = 0.02, position = positionWrist, name = "Tool_RIG_"+attribute+"_LowerArm")
    cmds.select(deselect = True)
    
    cmds.select("Tool_RIG_Spine" + str(n+1))
    IKClavicle = cmds.joint(radius = 0.05, position = positionArmStart, name = "Tool_RIG_IK_"+attribute+"_Clavicle")
    IKUpper = cmds.joint(radius = 0.1, position = positionElbow, name = "Tool_RIG_IK_"+attribute+"_UpperArm")
    IKLower = cmds.joint(radius = 0.02, position = positionWrist, name = "Tool_RIG_IK_"+attribute+"_LowerArm")
    cmds.select(deselect = True)
    
    cmds.select("Tool_RIG_Spine" + str(n+1))
    FKClavicle = cmds.joint(radius = 0.05, position = positionArmStart, name = "Tool_RIG_FK_"+attribute+"_Clavicle")
    FKUpper = cmds.joint(radius = 0.1, position = positionElbow, name = "Tool_RIG_FK_"+attribute+"_UpperArm")
    FKLower = cmds.joint(radius = 0.02, position = positionWrist, name = "Tool_RIG_FK_"+attribute+"_LowerArm")
    
    list = [IKClavicle, IKUpper, IKLower, FKClavicle, FKUpper, FKLower]
    for joints in list:
        cmds.hide(joints)
    cmds.select(deselect = True)
    
def create_joint_leg(attribute):
    cmds.select(deselect = True)
    cmds.select("Tool_RIG_Root")
    
    positionUpperLeg = cmds.xform(cmds.ls("Tool_Locator_"+attribute+"_Upper_Leg"), query = True, translation = True, worldSpace = True)
    positionKnee = cmds.xform(cmds.ls("Tool_Locator_"+attribute+"_Lower_Leg"), query = True, translation = True, worldSpace = True)
    positionFoot = cmds.xform(cmds.ls("Tool_Locator_"+attribute+"_Foot"), query = True, translation = True, worldSpace = True)
    positionFootball = cmds.xform(cmds.ls("Tool_Locator_"+attribute+"_Football"), query = True, translation = True, worldSpace = True)
    positionToes = cmds.xform(cmds.ls("Tool_Locator_"+attribute+"_Toes"), query = True, translation = True, worldSpace = True)
    
    cmds.joint(radius = 0.05, position = positionUpperLeg, name = "Tool_RIG_"+attribute+"_UpperLeg")
    cmds.joint(radius = 0.1, position = positionKnee, name = "Tool_RIG_"+attribute+"_Knee")
    cmds.joint(radius = 0.1, position = positionFoot, name = "Tool_RIG_"+attribute+"_Ankle")
    cmds.joint(radius = 0.1, position = positionFootball, name = "Tool_RIG_"+attribute+"_Football")
    cmds.joint(radius = 0.1, position = positionToes, name = "Tool_RIG_"+attribute+"_Toes")
    cmds.select(deselect = True)
    
def create_joint_fingers(attribute):
    cmds.select(deselect = True)
    
    for i in range (5):
        cmds.select("Tool_RIG_"+attribute+"_LowerArm")
        
        positionFinger0 = cmds.xform(cmds.ls("Tool_Locator_"+attribute+"_Finger"+str(i)+"_0"), query = True, translation = True, worldSpace = True)
        positionFinger1 = cmds.xform(cmds.ls("Tool_Locator_"+attribute+"_Finger"+str(i)+"_1"), query = True, translation = True, worldSpace = True)
        positionFinger2 = cmds.xform(cmds.ls("Tool_Locator_"+attribute+"_Finger"+str(i)+"_2"), query = True, translation = True, worldSpace = True)
        positionFinger3 = cmds.xform(cmds.ls("Tool_Locator_"+attribute+"_Finger"+str(i)+"_3"), query = True, translation = True, worldSpace = True)
        
        cmds.joint(radius = 0.01, position = positionFinger0, name = "Tool_RIG_"+attribute+"_Finger"+str(i)+"_0")
        cmds.joint(radius = 0.01, position = positionFinger1, name = "Tool_RIG_"+attribute+"_Finger"+str(i)+"_1")
        cmds.joint(radius = 0.01, position = positionFinger2, name = "Tool_RIG_"+attribute+"_Finger"+str(i)+"_2")
        cmds.joint(radius = 0.01, position = positionFinger3, name = "Tool_RIG_"+attribute+"_Finger"+str(i)+"_3")
        
    cmds.select(deselect = True)
    
# ----------------------------------------------------------------------------------------------------------------------------------    

##### Locators #####   


# Procedure who allows to connect the nodes.
def connection_nodes(i, right, left):

    # Creation of the multiplyDivide node.
    Node_mirrorT = cmds.createNode("multiplyDivide", name = "Node_mirrorT")
        
    # Connection of the left translation of an element (locator/group) with the right translation of an element (locator/group).
    cmds.connectAttr(left + ".translateX", Node_mirrorT + ".input1X")
    cmds.connectAttr(left + ".translateY", Node_mirrorT + ".input1Y")
    cmds.connectAttr(left + ".translateZ", Node_mirrorT + ".input1Z")
    
    cmds.connectAttr(Node_mirrorT + ".outputX", right + ".translateX")
    cmds.connectAttr(Node_mirrorT + ".outputY", right + ".translateY")
    cmds.connectAttr(Node_mirrorT + ".outputZ", right + ".translateZ")
    
    # To make the mirror of an element (locator/group).
    cmds.setAttr(Node_mirrorT + ".input2X", -1)



# Procedure who creates the legs locators.
def create_legs():

    ##### RIGHT #####

    if cmds.objExists("Tool_Group_Locator_Right_Leg"):
        print("Already exists")
    else:
        rightLeg = cmds.group(name = "Tool_Group_Locator_Right_Leg", empty = True)
        cmds.parent(rightLeg, "Tool_Locator_Hips")
        cmds.move(-0.1, 1, 0, rightLeg)

    # Right upper leg.
    rightUpperLeg = cmds.spaceLocator(name = "Tool_Locator_Right_Upper_Leg")
    cmds.scale(0.1, 0.1, 0.1, rightUpperLeg)
    cmds.parent(rightUpperLeg, rightLeg)
    cmds.move(-0.15, 1.5, 0, rightUpperLeg)

    # Right lower leg.
    rightLowerLeg = cmds.spaceLocator(name = "Tool_Locator_Right_Lower_Leg")
    cmds.scale(0.1, 0.1, 0.1, rightLowerLeg)
    cmds.parent(rightLowerLeg, rightUpperLeg)
    cmds.move(-0.15, 0.75, 0.05, rightLowerLeg)

    # Right foot.
    rightFoot = cmds.spaceLocator(name = "Tool_Locator_Right_Foot")
    cmds.scale(0.1, 0.1, 0.1, rightFoot)
    cmds.parent(rightFoot, rightLowerLeg)
    cmds.move(-0.15, 0.15, 0.02, rightFoot)

    # Right football.
    rightFootball = cmds.spaceLocator(name = "Tool_Locator_Right_Football")
    cmds.scale(0.1, 0.1, 0.1, rightFootball)
    cmds.parent(rightFootball, rightFoot)
    cmds.move(-0.15, 0, 0, rightFootball)

    # Right toes.
    rightToes = cmds.spaceLocator(name = "Tool_Locator_Right_Toes")
    cmds.scale(0.1, 0.1, 0.1, rightToes)
    cmds.parent(rightToes, rightFoot)
    cmds.move(-0.15, 0, 0.3, rightToes)
    
    
    ##### LEFT #####

    if cmds.objExists("Tool_Group_Locator_Left_Leg"):
        print("Already exists")
    else:
        leftLeg = cmds.group(name = "Tool_Group_Locator_Left_Leg", empty = True)
        cmds.parent(leftLeg, "Tool_Locator_Hips")
        cmds.move(-0.1, 1, 0, leftLeg)

    # Left upper leg.
    leftUpperLeg = cmds.spaceLocator(name = "Tool_Locator_Left_Upper_Leg")
    cmds.scale(0.1, 0.1, 0.1, leftUpperLeg)
    cmds.parent(leftUpperLeg, leftLeg)
    cmds.move(-0.15, 1.5, 0, leftUpperLeg)

    # Left lower leg.
    leftLowerLeg = cmds.spaceLocator(name = "Tool_Locator_Left_Lower_Leg")
    cmds.scale(0.1, 0.1, 0.1, leftLowerLeg)
    cmds.parent(leftLowerLeg, leftUpperLeg)
    cmds.move(-0.15, 0.75, 0.05, leftLowerLeg)

    # Left foot.
    leftFoot = cmds.spaceLocator(name = "Tool_Locator_Left_Foot")
    cmds.scale(0.1, 0.1, 0.1, leftFoot)
    cmds.parent(leftFoot, leftLowerLeg)
    cmds.move(-0.15, 0.15, 0.02, leftFoot)

    # Left football.
    leftFootball = cmds.spaceLocator(name = "Tool_Locator_Left_Football")
    cmds.scale(0.1, 0.1, 0.1, leftFootball)
    cmds.parent(leftFootball, leftFoot)
    cmds.move(-0.15, 0, 0, leftFootball)

    # Left toes.
    leftToes = cmds.spaceLocator(name = "Tool_Locator_Left_Toes")
    cmds.scale(0.1, 0.1, 0.1, leftToes)
    cmds.parent(leftToes, leftFoot)
    cmds.move(-0.15, 0, 0.3, leftToes)



# Procedure who creates the fingers locators.
def create_fingers(positionRightWrist, positionLeftWrist, i):

    # Tree locators on each finger.
    for x in range(0, 4):

        rightFinger = cmds.spaceLocator(name = "Tool_Locator_Right_Finger" + str(i) + "_" + str(x))
        cmds.scale(0.05, 0.05, 0.05, rightFinger)

        # The first right locator finger is attached to the hand.
        if x == 0:
            cmds.parent(rightFinger, "Tool_Group_Locator_Right_Hand")
        else:
            cmds.parent(rightFinger, "Tool_Locator_Right_Finger" + str(i) + '_' + str(x - 1))

        cmds.move(positionRightWrist[0] - (0.1 + (0.1 * x)), positionRightWrist[1], positionRightWrist[2] + -(0.05 * i) +0.1, rightFinger)
        
        leftFinger = cmds.spaceLocator(name = "Tool_Locator_Left_Finger" + str(i) + "_" + str(x))
        cmds.scale(0.05, 0.05, 0.05, leftFinger)

        # The first left locator finger is attached to the hand.
        if x == 0:
            cmds.parent(leftFinger, "Tool_Group_Locator_Left_Hand")
        else:
            cmds.parent(leftFinger, "Tool_Locator_Left_Finger" + str(i) + '_' + str(x - 1))

        cmds.move(positionLeftWrist[0] - (0.1 + (0.1 * x)), positionLeftWrist[1], positionLeftWrist[2] + -(0.05 * i) +0.1, leftFinger)



# Procedure who creates the right hand locators.
def create_hand(rightWrist, leftWrist):

    ##### RIGHT #####

    if cmds.objExists("Tool_Group_Locator_Right_Hand"):
        print("Already exists")
    else:
        rightHand = cmds.group(name = "Tool_Group_Locator_Right_Hand", empty = True)

        # Retrieve the position of the right wrist.
        positionRightWrist = cmds.xform(rightWrist, query = True, translation = True, worldSpace = True)
        cmds.move(positionRightWrist[0], positionRightWrist[1], positionRightWrist[2], rightHand)
        cmds.parent(rightHand, "Tool_Locator_Right_Wrist")
            
    
    ##### LEFT #####

    if cmds.objExists("Tool_Group_Locator_Left_Hand"):
        print("Already exists")
    else:
        leftHand = cmds.group(name = "Tool_Group_Locator_Left_Hand", empty = True)

        # Retrieve the position of the left wrist.
        positionLeftWrist = cmds.xform(leftWrist, query = True, translation = True, worldSpace = True)
        cmds.move(positionLeftWrist[0], positionLeftWrist[1], positionLeftWrist[2], leftHand)
        cmds.parent(leftHand, "Tool_Locator_Left_Wrist")

    for i in range(0, 5):
        create_fingers(positionRightWrist, positionLeftWrist, i)



# Procedure who creates the arms locators.
def create_arms(spineCountValue, lastSpine):

    ##### RIGHT #####

    # Creation of the group if he doesn't exists.
    if cmds.objExists("Tool_Group_Locator_Right_Arm"):
        print("Already exists")
    else:
        # Right arm.
        rightArm = cmds.group(name = "Tool_Group_Locator_Right_Arm", empty = True)
        cmds.parent(rightArm, "Tool_Locator_Spine" + str(spineCountValue - 1))
        cmds.move(-0.35, 2.5, 0, rightArm)

        # Right clavicle.
        rightClavicle = cmds.spaceLocator(name = "Tool_Locator_Right_Clavicle")
        cmds.scale(0.1, 0.1, 0.1, rightClavicle)
        cmds.parent(rightClavicle, "Tool_Locator_Spine" + str(spineCountValue - 1))
        cmds.move(-0.1, 2.5, 0.1, rightClavicle)

        # Right upper arm.
        rightUpperArm = cmds.spaceLocator(name = "Tool_Locator_Right_Upper_Arm")
        cmds.scale(0.1, 0.1, 0.1, rightUpperArm)
        cmds.parent(rightUpperArm, rightClavicle)
        cmds.move(-0.35, 2.5, 0, rightUpperArm) 

        # Right elbow.
        rightElbow = cmds.spaceLocator(name = "Tool_Locator_Right_Elbow")
        cmds.scale(0.1, 0.1, 0.1, rightElbow)
        cmds.parent(rightElbow, rightUpperArm)
        cmds.move(-0.9, 2.5, -0.2, rightElbow)

        # Right wrist.
        rightWrist = cmds.spaceLocator(name = "Tool_Locator_Right_Wrist")
        cmds.scale(0.1, 0.1, 0.1, rightWrist)
        cmds.parent(rightWrist, rightElbow)
        cmds.move(-1.6, 2.5, 0, rightWrist)

    
    ##### LEFT #####

    # Creation of the group if he doesn't exists.
    if cmds.objExists("Tool_Group_Locator_Left_Arm"):
        print("Already exists")
    else:
        # Left arm.
        leftArm = cmds.group(name = "Tool_Group_Locator_Left_Arm", empty = True)
        cmds.parent(leftArm, "Tool_Locator_Spine" + str(spineCountValue - 1))
        cmds.move(-0.35, 1 + (0.25 * spineCountValue), 0, leftArm)

        # Left clavicle.
        leftClavicle = cmds.spaceLocator(name = "Tool_Locator_Left_Clavicle")
        cmds.scale(0.1, 0.1, 0.1, leftClavicle)
        cmds.parent(leftClavicle, "Tool_Locator_Spine" + str(spineCountValue - 1))
        cmds.move(-0.1, 2, 0.1, leftClavicle)

        # Left upper arm.
        leftUpperArm = cmds.spaceLocator(name = "Tool_Locator_Left_Upper_Arm")
        cmds.scale(0.1, 0.1, 0.1, leftUpperArm)
        cmds.parent(leftUpperArm, leftClavicle)
        cmds.move(-0.35, 2, 0, leftUpperArm) 

        # Left elbow.
        leftElbow = cmds.spaceLocator(name = "Tool_Locator_Left_Elbow")
        cmds.scale(0.1, 0.1, 0.1, leftElbow)
        cmds.parent(leftElbow, leftUpperArm)
        cmds.move(-0.6, 2, -0.2, leftElbow)

        # Left wrist.
        leftWrist = cmds.spaceLocator(name = "Tool_Locator_Left_Wrist")
        cmds.scale(0.1, 0.1, 0.1, leftWrist)
        cmds.parent(leftWrist, leftElbow)
        cmds.move(-0.8, 1.5, 0, leftWrist)

    # Left hand and fingers.
    create_hand(rightWrist, leftWrist)



# Procedure who allows to create the head locators.
def create_head(spineCountValue, lastSpine):
    
    # Neck.
    neckStart = cmds.spaceLocator(name = "Tool_Locator_Neck_Start")
    cmds.parent(neckStart, "Tool_Locator_Spine" + str(spineCountValue - 1))
    cmds.scale(1, 1, 1, neckStart)
    cmds.move(0, 2.6, 0, neckStart)

    neckEnd = cmds.spaceLocator(name = "Tool_Locator_Neck_End")
    cmds.parent(neckEnd, neckStart)
    cmds.scale(1, 1, 1, neckEnd)
    cmds.move(0, 2.75, 0, neckEnd)

    # Head.
    head = cmds.spaceLocator(name = "Tool_Locator_Head")
    cmds.parent(head, "Tool_Locator_Neck_End")
    cmds.scale(1, 1, 1, head)
    cmds.move(0, 3, 0, head)

    # Jaw.
    jawStart = cmds.spaceLocator(name = "Tool_Locator_Jaw_Start")
    cmds.parent(jawStart, head)
    cmds.scale(0.5, 0.5, 0.5, jawStart)
    cmds.move(0, 2.9, 0.02, jawStart)

    jawEnd = cmds.spaceLocator(name = "Tool_Locator_Jaw_End")
    cmds.parent(jawEnd, jawStart)
    cmds.scale(1, 1, 1, jawEnd)
    cmds.move(0, 2.9, 0.15, jawEnd)



# Procedure who allows to create the spine locators.
def create_spine(spineCountValue):
    print("spinenumber="+str(spineCountValue))
    # Based on the number of spine locators the user has chosen.
    for i in range(0, spineCountValue):

        # Creation of a spine locator.
        spineLocator = cmds.spaceLocator(name = "Tool_Locator_Spine" + str(i))
        cmds.scale(0.1, 0.1, 0.1, spineLocator)
        print("Spine"+str(i))
        # The first spine locator is attached to the hips.
        if i == 0:
            cmds.parent(spineLocator, "Tool_Locator_Hips")
            cmds.move(0, 1.5 + float (i+1)/spineCountValue, 0, spineLocator)
        # The others locators spine are attached between them.
        else:
            cmds.parent(spineLocator, "Tool_Locator_Spine*" + str(i - 1))
            cmds.move(0, 1.5 + float (i+1)/spineCountValue, 0, spineLocator)
        if i == spineCountValue - 1 : 
            lastSpine = spineLocator
            return (lastSpine)



# Procedure who allows to create the locators of the body.
def create_locators():
    
    # Retrieve the values given by the user.
    spineCountValue = cmds.intField(spineCount, query = True, value = True)
    fingerCountValue = 5
    name = cmds.textFieldGrp(nameChara, query = True, text=True)
    print(spineCountValue)
    # Creation of the group if he doesn't exists.
    if cmds.objExists("Tool_Root"):
        print("Already exists")
    else:
        cmds.group(name = "Tool_Root", empty = True)

    # Creation of the hips locator.
    hipsLocator = cmds.spaceLocator(name = "Tool_Locator_Hips")
    cmds.scale(0.1, 0.1, 0.1, hipsLocator)
    cmds.move(0, 1.5, 0, hipsLocator)

    # The group becomes the parent of the locator.
    cmds.parent(hipsLocator, "Tool_Root")

    # Creation of the spine.
    lastSpine = create_spine(spineCountValue)
    create_head(spineCountValue, lastSpine)
    create_arms(spineCountValue, lastSpine)
    create_legs()
    
    allRightLocators = cmds.listRelatives(cmds.ls("Tool_Locator_Right*", type = "locator"), parent = True)
    allLeftLocators = cmds.listRelatives(cmds.ls("Tool_Locator_Left*", type = "locator"), parent = True)
    allRightGroups = cmds.ls("Tool_Group_Locator_Right*")
    allLeftGroups = cmds.ls("Tool_Group_Locator_Left*")
    
    # Connection of a left group and a right group.
    for i in range (0, len(allRightGroups)):
        connection_nodes(i, allLeftGroups[i], allRightGroups[i])
    
    # Connection of a left locator and a right locator.
    for i in range (0, len(allRightLocators)):
        connection_nodes(i, allLeftLocators[i], allRightLocators[i])
        


# Procedure who allows to delete the locators.
def delete_locators():
    cmds.delete(cmds.ls("Tool_Locator*", "Tool_Root", "Tool_Group*"))

# Procedure who allows to delete the joints.
def delete_joints():
    cmds.delete(cmds.ls("Tool_RIG", "Tool_Joint*"))
    
def delete_ik():
    cmds.delete(cmds.ls("IK"))
    
def delete_controllers():
    cmds.delete(cmds.ls("CTRL"))