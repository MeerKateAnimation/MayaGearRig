''' TO DO:
create dictuanry with each gear and it's position
add ability to select desired gears beforehand
'''


gearAmount = 2

for x in (1, gearAmount):
    #create hiarchy
    cmds.polyCylinder(n = 'tempGear{}'.format(x), h = 0.25, ax = (1, 0, 0))
    geoGrp = cmds.group(n = 'geoGrp{}'.format(x))
    rotGrp = cmds.group(n = 'rotGrp{}'.format(x))
    gearOffset = cmds.circle(n = 'gearOffset{}'.format(x), d = 1, s = 4, nr = (1, 0, 0), cx = 1)
    gearGrp = cmds.group(gearOffset, rotGrp, n = 'gear{}'.format(x))
    cmds.parent(rotGrp, gearOffset)
    
    cmds.addAttr(gearOffset, at = 'long', longName = 'gearCogs', defaultValue = 10, minValue = 2, h = False, k = True)
    
    
    #create nodes
    cogConversion = cmds.createNode('multiplyDivide', n = ("cogConversion{}".format(x))) #set mode to divide
    rotCalc = cmds.createNode('multiplyDivide', n = ("rotationCalculation{}".format(x)))
    #create condition node (true = 1, false = -1) (potentual name posNeg)

    #connect attrs

    #connect gearOffset Gear Cogs to CogConversion1 input1 x
    cmds.connectAttr('{}.gearCogs'.format(gearOffset), '{}.input1X'.format(cogConversion))
    #connect gearOffset2 Gear Cogs to CogConversion1 input2 x

    #connect rotGrp1 rotx to RotCalculation


    #connect gearOffset pos neg to condition
    #connect condition to inverseMultiply
    #connect inverseMultiply to next rotGrp

    cmds.connectAttr('{}.outputX'.format(cogConversion), '{}.input2X'.format(rotCalc))


#connect CON rotx to rotGrp1 rotx

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