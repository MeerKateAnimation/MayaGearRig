#define names (might not work as intended if not in an empty scene)
circleNames = ['innCircleLf', 'outCircleLf', 'innCircleRt', 'outCircleRt']
arrowNames = ['arrowLf', 'arrowRt', 'arrowUp', 'arrowDn']
conName = 'gear_CON'

#create arrow components
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
for each in circles:
    cmds.select(each, add = True)
for each in arrows:
    cmds.select(each, add = True)
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



