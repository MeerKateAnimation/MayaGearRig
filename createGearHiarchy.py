''' TO DO:
create dictuanry with each gear and it's position
add ability to select desired gears beforehand
delete construction history on gearOffset
rotate stuff so the front is the front view
maybe I should convert some of this stuff to functions (create nodes, connect nodes
'''


def createCon(): # function that creates the control(replace later with arrow control)
    print('Creating gear control...')
    con = cmds.circle(n = 'gear_CON', d = 3, s = 8, nr = (1, 0, 0), cx = 1, r = 1.5, ch = False)
    conOutput = cmds.createNode('multiplyDivide', n = ("conMultiplier"))
    #add attribute for a multiplication factor
    cmds.connectAttr('gear_CON.rotateX', '{}.input1X'.format(conOutput))
    print('Control created\n')
    return conOutput


gearAmount = 2
print(gearAmount)
print(gearAmount - 1)
gearPlacement = 0.0

#create control for gears
rotInput = createCon()

for x in range(1, gearAmount + 1): 
    
    #create hiarchy
    cmds.polyCylinder(n = 'tempGear{}'.format(x), h = 0.25, ax = (1, 0, 0))
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

    if x != 1:
        print(str(x) + ' does not = 1')
    #connect last loop nodes to current loop nodes
    #if statement to bypass first loop?
    #connect offset2 cogs to lastCogConversion
    
    #needs next loop's nodes
    #connect gearOffset pos neg to condition
    #connect gearOffset2 Gear Cogs to CogConversion1 input2 x not made in this loop yet

    
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

'''
gearNumber = 10
lastGearNumber = gearNumber - 1
gearName = "gearCogConversion" + str(gearNumber)
print(gearName)

gearConversion = cmds.createNode('multiplyDivide', n = ("gearCogConversion" + str(gearNumber)))
rotCalc = cmds.createNode('multiplyDivide', n = ("rotationCalculation" + str(gearNumber)))
cmds.createNode('multiplyDivide', n = ("inverseMultiply" + str(gearNumber)))
cmds.createNode('condition', n = ("posNegCondition" + str(gearNumber)))

testAttrA = gearCogConversion10.outputX

cmds.connectAttr(gearCogConversion10.outputX, rotationCalculation10.input2X)

'''