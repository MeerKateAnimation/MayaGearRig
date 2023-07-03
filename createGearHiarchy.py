''' TO DO:
create dictuanry with each gear and it's position
add ability to select desired gears beforehand
delete construction history on gearOffset
rotate stuff so the front is the front view
maybe I should convert some of this stuff to functions (create nodes, connect nodes)
maybe parent the main gear group to gear offset and pull the offset con out of hiarchy for easier animator use?
What does it do if there's only 1 gear? What do I want it to do?
Add a variable to change scale of controls
should get rotation and scale(?) of gears too
should lock pos neg and maybe even hide it?
if UI popups are an option then make the temp gears number pop up as a prompt

'''

def introduction():
    '''
    print('-----------------------------------------------')
    print('\nWelcome to my gear rig!\n')
    print('this rig and script is written by Emily Broyles')
    print('meerkate.com\n')
    '''
    print('-----------------------------------------------')

def createCon(): # function that creates the control(replace later with arrow control)
    print('Creating gear control...')
    con = cmds.circle(n = 'gear_CON', d = 3, s = 8, nr = (1, 0, 0), cx = 1, r = 1.5, ch = False)
    cmds.select(con, r = True)
    cmds.addAttr(ln = 'rotMult', at = 'float', dv = 1, h = False, k = True)
    conOutput = cmds.createNode('multiplyDivide', n = ("conMultiplier"))
    cmds.connectAttr('gear_CON.rotateX', '{}.input1X'.format(conOutput))
    print('Control created\n')
    return conOutput

''' set up '''

introduction()

gearAmount = 2 #sets default gear amount if nothing is selected
tempGearOffsetDistance = 2.0
tempGearOffset = 0.0
print(gearAmount)
print(gearAmount - 1)
gearPlacement = 0.0

gearGeo = cmds.ls(sl = True)
print(gearGeo)
#cmds.select(cl = True)
#cmds.select(gearGeo[1])
gearPos = {}

if gearGeo == []:
    print('Nothing is selected - creating temporary meshes in place of gears')
    for i in range(gearAmount):
        print(i)
        gear = (cmds.polyCylinder(n = 'tempGear{}'.format(i + 1), h = 0.25, ax = (1, 0, 0), ch = False))
        gearGeo.append(gear[0])
        print(gearGeo)
        print(gear[0])
        gearPos[gearGeo[i]] = [0.0, 0.0, tempGearOffset]
        tempGearOffset = tempGearOffset + tempGearOffsetDistance
        print(gearPos)
else:
    gearAmount = len(gearGeo)
    print(gearAmount)
    print('Saving positions of selected gears')
    for j in range(gearAmount):
        pos = cmds.xform(gearGeo[j], q = True, t = True, ws= True)
        print(pos)
        print(j)
        gearPos[gearGeo[j]] = pos
        print (gearPos)
        


#create control for gears
rotInput = createCon()

for x in range(1, gearAmount + 1): 
    
    #create hiarchy
#    cmds.polyCylinder(n = 'tempGear{}'.format(x), h = 0.25, ax = (1, 0, 0))
    cmds.xform(gearGeo[x-1], t = (0.0, 0.0, 0.0), ws = True)
    #select gear
    cmds.select(gearGeo[x-1])
    geoGrp = cmds.group(n = 'geoGrp{}'.format(x))
    rotGrp = cmds.group(n = 'rotGrp{}'.format(x))
    gearOffset = cmds.circle(n = 'gearOffset{}'.format(x), d = 1, s = 4, nr = (1, 0, 0), cx = 1) #saves as a list. to access the con use gearOffset[0]
    gearGrp = cmds.group(gearOffset, rotGrp, n = 'gear{}'.format(x))
    cmds.parent(rotGrp, gearOffset) #gives an error but doesn't seem to actually mess anything up "Warning: Cannot parent components or objects in the underworld."
    print("Don't know why the previous error shows up... - Emily \n")
    
    cmds.addAttr(gearOffset, at = 'long', longName = 'gearCogs', defaultValue = 10, minValue = 2, h = False, k = True)
    cmds.addAttr(gearOffset, at = 'enum', longName = 'posNeg', defaultValue = (x % 2), en = 'Pos:Neg', h = False, k = True)
    
    
    ''' create nodes '''
    # create node to calculate rotation ratio
    cogConversion = cmds.createNode('multiplyDivide', n = ("cogConversion{}".format(x)))
    cmds.setAttr('{}.operation'.format(cogConversion), 2)
    
    # create node to calculate rotation
    rotCalc = cmds.createNode('multiplyDivide', n = ("rotationCalculation{}".format(x)))
    
    # create condition node to determine if direction needs to be inverted
    invert = cmds.createNode('condition', n = ('invert{}'.format(x)))
    cmds.setAttr('{}.colorIfTrueR'.format(invert), 1)
    cmds.setAttr('{}.colorIfFalseR'.format(invert), -1)
    
    # create node to invert direction
    rotInvert = cmds.createNode('multiplyDivide', n = ('rotInvert{}'.format(x)))

    """connect attrs"""

    cmds.connectAttr('{}.gearCogs'.format(gearOffset[0]), '{}.input1X'.format(cogConversion))
    
    cmds.connectAttr('{}.rotateX'.format(rotGrp), '{}.input1X'.format(rotCalc))


    
    cmds.connectAttr('{}.outputX'.format(rotCalc), '{}.input1X'.format(rotInvert))
    cmds.connectAttr('{}.outColorR'.format(invert), '{}.input2X'.format(rotInvert))
    #connect inverseMultiply to last rotGrp
    cmds.connectAttr('{}.outputX'.format(rotInput), '{}.rotateX'.format(rotGrp))

    cmds.connectAttr('{}.outputX'.format(cogConversion), '{}.input2X'.format(rotCalc))
    #connect gearOffset pos neg to condition
    cmds.connectAttr('{}.posNeg'.format(gearOffset[0]), '{}.firstTerm'.format(invert))


    if x != 1:
        print(str(x) + ' does not = 1')
        #connect last loop nodes to current loop nodes
        cmds.connectAttr('{}.gearCogs'.format(gearOffset[0]), '{}.input2X'.format(lastCogConversion))
    
    #needs next loop's nodes
    
    #connect gearOffset2 Gear Cogs to CogConversion1 input2 x not made in this loop yet

    #position offset
    print(gearPos[gearGeo[x-1]])
    cmds.xform(gearOffset[0], t = gearPos[gearGeo[x-1]], ws = True)
    
    #relabel stuff
    lastCogConversion = cogConversion
    lastRotGrp = rotGrp
    rotInput = rotInvert
    
    
''' doesn't work    
    # move gears (generated version)
    gearPlacement = 0.0
    print(gearOffset[0])
    cmds.move(gearPlacement, 0.0, 0.0, gearOffset[0])
    gearPlacement = gearPlacement + 1.5
    print(gearPlacement)
'''


# connect CON rotx to rotGrp1 rotx

