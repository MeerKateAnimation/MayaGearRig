''' TO DO:
rotate stuff so the front is the front view 
maybe parent the main gear group to gear offset and pull the offset con out of hiarchy for easier animator use?
What does it do if there's only 1 gear? What do I want it to do?
Add a variable to change scale of controls
should get rotation and scale(?) of gears too
should lock pos neg and maybe even hide it?
if UI popups are an option then make the temp gears number pop up as a prompt
make loops consistant (x+1 vs x)
save each main group and parent them all into a single group
currently breaks if you try and do it mutltiple times in same scene
add attribute to change how far out from the gear the offset control is
set control to go to first gear (or be moved by animator? but default is by first gear))
if gears are zeroed out the offset control will not be in the right place. Gear rotation still works as intended
add attr to control offset control visibility
lock attributes (can use 'l = True' in all the setAttr lines)
change color of cons! (with variables to easily change later)

'''

''' ----------------------------------------------------------
changeable attributes (some only apply if nothing is selected)
---------------------------------------------------------- '''
# These attributes affect the size of the controls
conSizeMain = 1 # changes the size of the main rotation control (currently does nothing)
conSizeOffset = 1.5 # changes the size of the offset control
controlFollowsGear = True # determines if gear spin control follows first gear offset control

# These only apply if nothing is selected
gearAmount = 10 # sets default gear amount if nothing is selected
tempGearOffsetDistance = 2.0 # sets how far apart created gears are initially from each other
tempGearOffset = 0.0 # starting point for created gears
''' --------------------------------------------------- '''

def introduction():
    
    print('\n-----------------------------------------------')
    print('\nWelcome to my gear rig!\n')
    print('this rig and script is written by Emily Broyles')
    print('MeerKate.com\n')
    print('-----------------------------------------------')

def endMessage():
    print('-----------------------------------------------')
    if createdGear == True:
        print('Since there were no objects selected I created temporary gears for you.')
        print('To change the objects just replace the temporary gears by parenting your desired objects to it\'s respective "geoGrp" in the gear hiarchy.')
    print('Thank you again for using my rig. I hope you enjoy!')
    print('Emily Broyles')
    print('MeerKate.com')
    print('-----------------------------------------------')

def createCon(): # function that creates the control
    print('Creating gear control')
    # define names
    circleNames = ['innCircleLf', 'outCircleLf', 'innCircleRt', 'outCircleRt']
    arrowNames = ['arrowLf', 'arrowRt', 'arrowUp', 'arrowDn']
    conName = 'gearRotate_CON'

    # create arrow components
    circles = []
    arrows = []
    circles.append(cmds.circle(n = circleNames[0], c = (0, 0, 0), nr = (0, 1, 0), r = 1.35, sw = 90, ch = False)[0])
    circles.append(cmds.circle(n = circleNames[1], c = (0, 0, 0), nr = (0, 1, 0), r = 1.65, sw = 90, ch = False)[0])
    circles.append(cmds.circle(n = circleNames[2], c = (0, 0, 0), nr = (0, 1, 0), r = 1.35, sw = 90, ch = False)[0])
    cmds.rotate(0, 180, 0, circles[2])
    circles.append(cmds.circle(n = circleNames[3], c = (0, 0, 0), nr = (0, 1, 0), r = 1.65, sw = 90, ch = False)[0])
    cmds.rotate(0, 180, 0, circles[3])

    arrows.append(cmds.curve(n = arrowNames[0], p = [(0.15, 0, 0), (0.4, 0, -0.04), (0.55, 0, -0.0625),  (0.48, 0, 0.1), (0.1, 0, 0.45), (0, 0, .5), (-0.1, 0, 0.45), (-0.48, 0, 0.1), (-0.55, 0, -0.0625), (-0.4, 0, -0.04), (-0.15, 0, 0)]))
    cmds.move (-1.5, 0, 0, arrows[0])

    arrows.append(cmds.curve(n = arrowNames[1], p = [(0.15, 0, 0), (0.4, 0, -0.04), (0.55, 0, -0.0625),  (0.48, 0, 0.1), (0.1, 0, 0.45), (0, 0, .5), (-0.1, 0, 0.45), (-0.48, 0, 0.1), (-0.55, 0, -0.0625), (-0.4, 0, -0.04), (-0.15, 0, 0)]))
    cmds.move (1.5, 0, 0, arrows[1])
    cmds.rotate (0, 180, 0, arrows[1])

    arrows.append(cmds.curve(n = arrowNames[2], p = [(0.15, 0, 0), (0.4, 0, -0.04), (0.55, 0, -0.0625),  (0.48, 0, 0.1), (0.1, 0, 0.45), (0, 0, .5), (-0.1, 0, 0.45), (-0.48, 0, 0.1), (-0.55, 0, -0.0625), (-0.4, 0, -0.04), (-0.15, 0, 0)]))
    cmds.move (0, 0, -1.5, arrows[2])
    cmds.rotate (0, 90, 0, arrows[2])

    arrows.append(cmds.curve(n = arrowNames[3], p = [(0.15, 0, 0), (0.4, 0, -0.04), (0.55, 0, -0.0625),  (0.48, 0, 0.1), (0.1, 0, 0.45), (0, 0, .5), (-0.1, 0, 0.45), (-0.48, 0, 0.1), (-0.55, 0, -0.0625), (-0.4, 0, -0.04), (-0.15, 0, 0)]))
    cmds.move (0, 0, 1.5, arrows[3])
    cmds.rotate (0, -90, 0, arrows[3])

    #freeze transformations
    for each in circles:
        cmds.makeIdentity(each, a = True, t = True, r = True, s = True, n = False)
    for each in arrows:
        cmds.makeIdentity(each, a = True, t = True, r = True, s = True, n = False)

    #select and combine all shapes
    cmds.select(d = True)
    con = cmds.group(n = conName, em = True)
    cmds.select(circles, arrows)
    '''for each in circles:
        cmds.select(each, add = True)
    for each in arrows:
        cmds.select(each, add = True)'''
    cmds.pickWalk(d = 'down')
        
    cmds.select(con, add = True)
    cmds.parent(r = True, s = True,)

    #select and delete all empty nodes
    cmds.select(d = True)
    for each in circles:
        cmds.select(each, add = True)
    for each in arrows:
        cmds.select(each, add = True)
    cmds.delete()
    
    # rotate control and freeze transformations
    cmds.xform(con, ro = (0, 0, 90), t = (1,0,0))
    cmds.makeIdentity(con, a = True, t = True, r = True, s = True, n = False)

    # add attributes to control
    cmds.addAttr(con, ln = 'rotMult', at = 'float', dv = 1, h = False, k = True)
    cmds.addAttr(con, ln = 'offsetConVis', at = 'bool', dv = 1, h = False, k = True)
    conOutput = cmds.createNode('multiplyDivide', n = ("conMultiplier"))
    cmds.connectAttr('{}.rotateX'.format(con), '{}.input1X'.format(conOutput))
    
    return [con, conOutput]

introduction()

''' 
saves gear positions and creates gears if necessary 
'''
gearGeo = cmds.ls(sl = True)
gearPos = {}
gearRot = {}
gearGrp = []
# these groups are for organizing the outliner in the end
controlGrp = []
offsetGrp = []
geometryGrp = []
masterGrp = []

if gearGeo == []:
    print('Nothing is selected - creating temporary meshes in place of gears')
    createdGear = True
    for i in range(gearAmount):
        gear = (cmds.polyCylinder(n = 'tempGear{}'.format(i + 1), h = 0.25, r = 0.85, ax = (1, 0, 0), sc = 1, ch = False))[0]
        cmds.polyExtrudeFacet('{}.f[1]'.format(gear), '{}.f[3]'.format(gear), '{}.f[5]'.format(gear), '{}.f[7]'.format(gear), '{}.f[9]'.format(gear), '{}.f[11]'.format(gear), '{}.f[13]'.format(gear), '{}.f[15]'.format(gear), '{}.f[17]'.format(gear), '{}.f[19]'.format(gear), ltz = 0.3, ls = (0.8, 0.8, 0), ch = False)
        cmds.select(d = True)
        gearGeo.append(gear)
        gearPos[gearGeo[i]] = [0.0, 0.0, tempGearOffset]
        gearRot[gearGeo[i]] = [0.0, 0.0, 0.0]
        tempGearOffset = tempGearOffset + tempGearOffsetDistance

else:
    gearAmount = len(gearGeo)
    print('Saving positions of selected gears')
    createdGear = False
    for j in range(gearAmount):
        pos = cmds.xform(gearGeo[j], q = True, t = True, ws = True)
        rot = cmds.xform(gearGeo[j], q = True, ro = True, ws = True)
        gearPos[gearGeo[j]] = pos
        gearRot[gearGeo[j]] = rot
   
''' 
creating the rig 
'''
# create control for gears
createConOutput = createCon()
rotInput = createConOutput[1]
rotCon = createConOutput[0]

# main loop for creating the gear rig
for x in range(1, gearAmount + 1): 
    print('Setting up rig for gear ' + str(x))
    # center gear and create hiarchy
    cmds.xform(gearGeo[x-1], t = (0.0, 0.0, 0.0), ro = (0,0,0), ws = True, a = True)
    cmds.select(gearGeo[x-1])
    geoGrp = cmds.group(n = 'geoGrp{}'.format(x))
    rotGrp = cmds.group(n = 'rotGrp{}'.format(x))
    gearGrp = cmds.group(rotGrp, n = 'gear{}'.format(x))
    geometryGrp.append(gearGrp)
    
    gearOffset = cmds.circle(n = 'gearOffset{}'.format(x), r = (conSizeOffset / 2), d = 1, s = 4, nr = (1, 0, 0), cx = 1, ch = False)[0]
    cmds.addAttr(gearOffset, at = 'long', longName = 'gearCogs', defaultValue = 10, minValue = 2, h = False, k = True)
    cmds.addAttr(gearOffset, at = 'bool', longName = 'directionOverride', defaultValue = False, h = False, k = True)
    offsetGrp.append(gearOffset)
    
    # create node to calculate rotation ratio
    cogConversion = cmds.createNode('multiplyDivide', n = ("cogConversion{}".format(x)))
    cmds.setAttr('{}.operation'.format(cogConversion), 2)
    
    # create node to calculate rotation
    rotCalc = cmds.createNode('multiplyDivide', n = ("rotationCalculation{}".format(x)))
    
    # create node to invert direction
    rotInvert = cmds.createNode('multiplyDivide', n = ('rotInvert{}'.format(x)))
    cmds.setAttr('{}.input2X'.format(rotInvert), -1)
    
    #create override direction condition node
    override = cmds.createNode('condition', n = ('invertOverride{}'.format(x)))
    cmds.setAttr('invertOverride{}.secondTerm'.format(x), 1)
    cmds.setAttr('invertOverride{}.colorIfTrueR'.format(x), 1)
    cmds.setAttr('invertOverride{}.colorIfFalseR'.format(x), -1)

    # connect attributes
    cmds.connectAttr('{}.gearCogs'.format(gearOffset), '{}.input1X'.format(cogConversion))
    cmds.connectAttr('{}.rotateX'.format(rotGrp), '{}.input1X'.format(rotCalc))
    cmds.connectAttr('{}.outputX'.format(rotCalc), '{}.input1X'.format(rotInvert))
    cmds.connectAttr('{}.outputX'.format(rotInput), '{}.rotateX'.format(rotGrp))
    cmds.connectAttr('{}.outputX'.format(cogConversion), '{}.input2X'.format(rotCalc))
    cmds.connectAttr('{}.outColorR'.format(override), '{}.input2X'.format(rotInvert))
    cmds.connectAttr('{}.translate'.format(gearOffset), '{}.translate'.format(gearGrp))
    cmds.connectAttr('{}.rotate'.format(gearOffset), '{}.rotate'.format(gearGrp))    

    if x != 1:
        # connects nodes from the last gear to the current gear's nodes
        cmds.connectAttr('{}.gearCogs'.format(gearOffset), '{}.input2X'.format(lastCogConversion))
        cmds.connectAttr('{}.directionOverride'.format(gearOffset), '{}.firstTerm'.format(lastOverride))
    else:
        # set gear rotate con to follow first offset con
        conGrp = cmds.group(rotCon, n = 'gearRotateGrp')
        print(conGrp)
        cmds.connectAttr('{}.translate'.format(gearOffset), '{}.translate'.format(conGrp))
        cmds.connectAttr('{}.rotate'.format(gearOffset), '{}.rotate'.format(conGrp))

    # moves the gear back to assigned offset position
    cmds.xform(gearOffset, t = gearPos[gearGeo[x-1]], ro = gearRot[gearGeo[x-1]], ws = True)
    
    # relabel variables
    lastCogConversion = cogConversion
    lastRotGrp = rotGrp #i don't think this one is needed anymore
    rotInput = rotInvert
    lastOverride = override
    
#organizing the end result
controlGrp.append(conGrp)
offsetConVis = cmds.group(offsetGrp, n = 'offset controls')
controlGrp.append(offsetConVis)
masterGrp.append(cmds.group(controlGrp, n = 'controls'))
masterGrp.append(cmds.group(geometryGrp, n = 'geometry'))

cmds.group(masterGrp, n = 'gear rig')

# last minute attribute hook-ups
cmds.connectAttr('{}.offsetConVis'.format(rotCon), '{}.visibility'.format(offsetConVis), l = True)

'''
controlGrp = []
offsetGrp = []
geometryGrp = []
masterGrp = []
'''
    
endMessage()
