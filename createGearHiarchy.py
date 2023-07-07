''' TO DO:
rotate stuff so the front is the front view (should I change the rotation channel to z?)
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
add attribute to change visible orientation??? 
set control to go to first gear (or be moved by animator? but default is by first gear))
if gears are zeroed out the offset control will not be in the right place. Gear rotation still works as intended
maybe add an attribute to offset 'direction override' or something like that to reverse the direction if needed may be easier then rotating the offset by 180 degrees

'''

''' ----------------------------------------------------------
changeable attributes (some only apply if nothing is selected)
---------------------------------------------------------- '''
# These attributes affect the size of the controls
conSizeMain = 1 # changes the size of the main rotation control (currently does nothing)
conSizeOffset = 1.5 # changes the size in units of the offset control

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

def createCon(): # function that creates the control (replace later with arrow control)
    # creates the control
    print('Creating gear control')
    con = cmds.circle(n = 'gear_CON', d = 3, s = 8, nr = (1, 0, 0), cx = 1, r = 1.5, ch = False)
    grps = [con]
    print(grps)
    # add attributes to control
    cmds.select(con, r = True)
    cmds.addAttr(ln = 'rotMult', at = 'float', dv = 1, h = False, k = True)
    conOutput = cmds.createNode('multiplyDivide', n = ("conMultiplier"))
    cmds.connectAttr('gear_CON.rotateX', '{}.input1X'.format(conOutput))
    return conOutput

introduction()

''' 
saves gear positions and creates gears if necessary 
'''
gearGeo = cmds.ls(sl = True)
gearPos = {}
gearRot = {}
#grps = []

if gearGeo == []:
    print('Nothing is selected - creating temporary meshes in place of gears')
    createdGear = True
    for i in range(gearAmount):
        gear = (cmds.polyCylinder(n = 'tempGear{}'.format(i + 1), h = 0.25, r = 0.85, ax = (1, 0, 0), sc = 1, ch = False))[0]
        cmds.polyExtrudeFacet('{}.f[1]'.format(gear), '{}.f[3]'.format(gear), '{}.f[5]'.format(gear), '{}.f[7]'.format(gear), '{}.f[9]'.format(gear), '{}.f[11]'.format(gear), '{}.f[13]'.format(gear), '{}.f[15]'.format(gear), '{}.f[17]'.format(gear), '{}.f[19]'.format(gear), ltz = 0.3, ls = (0.8, 0.8, 0), ch = False)
        cmds.select(d = True)
        gearGeo.append(gear)
        gearPos[gearGeo[i]] = [0.0, 0.0, tempGearOffset]
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
rotInput = createCon()
print(grps)

# main loop for creating the gear rig
print(gearGeo)
for x in range(1, gearAmount + 1): 
    print('Setting up rig for gear ' + str(x))
    # center gear and create hiarchy
    cmds.xform(gearGeo[x-1], t = (0.0, 0.0, 0.0), ro = (0,0,0), ws = True, a = True)
    cmds.select(gearGeo[x-1])
    geoGrp = cmds.group(n = 'geoGrp{}'.format(x))
    rotGrp = cmds.group(n = 'rotGrp{}'.format(x))
    gearOffset = cmds.circle(n = 'gearOffset{}'.format(x), r = (conSizeOffset / 2), d = 1, s = 4, nr = (1, 0, 0), cx = 1, ch = False)[0]
    gearGrp = cmds.group(gearOffset, rotGrp, n = 'gear{}'.format(x))
    grps.append(gearGrp)
    cmds.parent(rotGrp, gearOffset)
    
    cmds.addAttr(gearOffset, at = 'long', longName = 'gearCogs', defaultValue = 10, minValue = 2, h = False, k = True)
    cmds.addAttr(gearOffset, at = 'bool', longName = 'directionOverride', defaultValue = False, h = False, k = True)
    
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
    

    if x != 1:
        # connects nodes from the last gear to the current gear's nodes
        cmds.connectAttr('{}.gearCogs'.format(gearOffset), '{}.input2X'.format(lastCogConversion))
        cmds.connectAttr('{}.directionOverride'.format(gearOffset), '{}.firstTerm'.format(lastOverride))

    # moves the gear back to assigned offset position
    cmds.xform(gearOffset, t = gearPos[gearGeo[x-1]], ro = gearRot[gearGeo[x-1]], ws = True)
    
    # relabel variables
    lastCogConversion = cogConversion
    lastRotGrp = rotGrp #i don't think this one is needed anymore
    rotInput = rotInvert
    lastOverride = override
    
#organizing the end result
cmds.group(grps, n = 'gear rig')
    
endMessage()
