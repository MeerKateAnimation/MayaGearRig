gearAmount = 2

for x in (1, gearAmount):
    #create hiarchy
    cmds.polyCylinder(n = 'tempGear{}'.format(x), h = 0.25, ax = (1, 0, 0))
    gearGeo = cmds.group(n = 'geoGrp{}'.format(x))
    gearRot = cmds.group(n = 'rotGrp{}'.format(x))
    gearCtrl = cmds.circle(n = 'gearOffset{}'.format(x), d = 1, s = 4, nr = (1, 0, 0), cx = 1)
    gearGrp = cmds.group(gearCtrl, gearRot, n = 'gear{}'.format(x))
    cmds.parent(gearRot, gearCtrl)
    
    cmds.addAttr(gearCtrl, at = 'long', longName = 'gearCogs', defaultValue = 10, minValue = 2, h = False, k = True)
    
    
    
    
    
    #create nodes
    gearConversion = cmds.createNode('multiplyDivide', n = ("CogConversion{}".format(x)))
    gearCalc = cmds.createNode('multiplyDivide', n = ("rotationCalculation{}".format(x)))
    
    cmds.connectAttr('{}.outputX'.format(gearConversion), '{}.input2X'.format(gearCalc))


#gearNumber = 10
#lastGearNumber = gearNumber - 1
#gearName = "gearCogConversion" + str(gearNumber)
#print(gearName)

#gearConversion = cmds.createNode('multiplyDivide', n = ("gearCogConversion" + str(gearNumber)))
#gearCalc = cmds.createNode('multiplyDivide', n = ("rotationCalculation" + str(gearNumber)))
#cmds.createNode('multiplyDivide', n = ("inverseMultiply" + str(gearNumber)))
#cmds.createNode('condition', n = ("posNegCondition" + str(gearNumber)))

#testAttrA = gearCogConversion10.outputX

#cmds.connectAttr(gearCogConversion10.outputX, rotationCalculation10.input2X)

