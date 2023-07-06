''' TO DO:
-create dictuanry with each gear and it's position
-add ability to select desired gears beforehand
-delete construction history on gearOffset
rotate stuff so the front is the front view
maybe I should convert some of this stuff to functions (create nodes, connect nodes)
maybe parent the main gear group to gear offset and pull the offset con out of hiarchy for easier animator use?
What does it do if there's only 1 gear? What do I want it to do?
Add a variable to change scale of controls
should get rotation and scale(?) of gears too
should lock pos neg and maybe even hide it?
if UI popups are an option then make the temp gears number pop up as a prompt
make loops consistant (x+1 vs x)
can I extrude the tempGear to give it cogs?
save each main group and parent them all into a single group
 
'''

''' -------------------------------------------------------
changeable attributes (some only applies if nothing is selected)
------------------------------------------------------- '''
conSizeMain = 1 # changes the size of the main rotation control
conSizeOffset = 3 # changes the size in units of the offset control

gearAmount = 10 # sets default gear amount if nothing is selected
tempGearOffsetDistance = 2.0 # sets how far apart created gears are initially from each other
tempGearOffset = 0.0 # starting point for created gears
''' --------------------------------------------------- '''

def introduction():
    
    print('\n-----------------------------------------------')
    print('\nWelcome to my gear rig!\n')
    print('this rig and script is written by Emily Broyles')
    print('meerkate.com\n')
    print('-----------------------------------------------')

def createCon(): # function that creates the control(replace later with arrow control)
    # creates the control
    print('Creating gear control')
    con = cmds.circle(n = 'gear_CON', d = 3, s = 8, nr = (1, 0, 0), cx = 1, r = 1.5, ch = False)
    #print(con)
    
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

if gearGeo == []:
    print('Nothing is selected - creating temporary meshes in place of gears')
    createdGear = True
    for i in range(gearAmount):
        gear = (cmds.polyCylinder(n = 'tempGear{}'.format(i + 1), h = 0.25, ax = (1, 0, 0), ch = False))

        gearGeo.append(gear[0])
        gearPos[gearGeo[i]] = [0.0, 0.0, tempGearOffset]
        tempGearOffset = tempGearOffset + tempGearOffsetDistance

else:
    gearAmount = len(gearGeo)
    print('Saving positions of selected gears')
    createdGear = False
    for j in range(gearAmount):
        pos = cmds.xform(gearGeo[j], q = True, t = True, ws= True)
        gearPos[gearGeo[j]] = pos

        
''' 
creating the rig 
'''
# create control for gears
rotInput = createCon()

# main loop for creating the gear rig
for x in range(1, gearAmount + 1): 
    print('Setting up rig for gear ' + str(x))
    # center gear and create hiarchy
    cmds.xform(gearGeo[x-1], t = (0.0, 0.0, 0.0), ws = True)
    cmds.select(gearGeo[x-1])
    geoGrp = cmds.group(n = 'geoGrp{}'.format(x))
    rotGrp = cmds.group(n = 'rotGrp{}'.format(x))
    gearOffset = cmds.circle(n = 'gearOffset{}'.format(x), r = (conSizeOffset / 2), d = 1, s = 4, nr = (1, 0, 0), cx = 1, ch = False)
    gearOffset = gearOffset[0]
    gearGrp = cmds.group(gearOffset, rotGrp, n = 'gear{}'.format(x))
    cmds.parent(rotGrp, gearOffset)
    
    cmds.addAttr(gearOffset, at = 'long', longName = 'gearCogs', defaultValue = 10, minValue = 2, h = False, k = True)
    #cmds.addAttr(gearOffset, at = 'enum', longName = 'posNeg', defaultValue = (x % 2), en = 'Pos:Neg', h = False, k = True) #prob not needed
    
    
    ''' create nodes '''
    # create node to calculate rotation ratio
    cogConversion = cmds.createNode('multiplyDivide', n = ("cogConversion{}".format(x)))
    cmds.setAttr('{}.operation'.format(cogConversion), 2)
    
    # create node to calculate rotation
    rotCalc = cmds.createNode('multiplyDivide', n = ("rotationCalculation{}".format(x)))
    
    
    # create node to invert direction
    rotInvert = cmds.createNode('multiplyDivide', n = ('rotInvert{}'.format(x)))
    cmds.setAttr('{}.input2X'.format(rotInvert), -1)

    """connect attrs"""

    cmds.connectAttr('{}.gearCogs'.format(gearOffset), '{}.input1X'.format(cogConversion))
    
    cmds.connectAttr('{}.rotateX'.format(rotGrp), '{}.input1X'.format(rotCalc))


    
    cmds.connectAttr('{}.outputX'.format(rotCalc), '{}.input1X'.format(rotInvert))
    
    #connect inverseMultiply to last rotGrp
    cmds.connectAttr('{}.outputX'.format(rotInput), '{}.rotateX'.format(rotGrp))

    cmds.connectAttr('{}.outputX'.format(cogConversion), '{}.input2X'.format(rotCalc))

    if x != 1:
        # connects nodes from the last loop to this loop's nodes
        cmds.connectAttr('{}.gearCogs'.format(gearOffset), '{}.input2X'.format(lastCogConversion))


    # moves the gear back to assigned offset position
    cmds.xform(gearOffset, t = gearPos[gearGeo[x-1]], ws = True)
    
    #relabel variables
    lastCogConversion = cogConversion
    lastRotGrp = rotGrp
    rotInput = rotInvert
    
''' 
end message
'''
print('-----------------------------------------------')
if createdGear == True:
    print('Since there were no objects selected I created temporary gears for you.')
    print('To change the objects just replace the temporary gears by parenting your desired objects to it\'s respective "geoGrp" in the gear hiarchy.')
print('Thank you again for using my rig. I hope you enjoy!')