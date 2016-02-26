def mergeArea(area, areas):
    result = []
    x, y, w, h = area
    for element in areas:
        x2, y2, w2, h2 = element
        if (x < x2+w2 and x+w > x2 and x+w > x2 and x < x2+w2 ):
            w = max(x+w,x2+w2)
            h = max(y+h,y2+h2)
            x = min(x,x2)
            y = min(y,y2)
            w = w-x
            h = h-y
        else:
            result.append(element)
    return ((x, y, w, h), result)

def mergeAreas(before, areas):
    if len(areas)==0:
        return before
    head = areas[0]
    after = areas[1:]
    head, before = mergeArea(head, before)
    head, after = mergeArea(head, after)
    before.append(head)
    return mergeAreas(before, after)

def overlappingAreas(src, prv):
    result = []
    for element in src:
        x1, y1, w1, h1 = element
        found = 0
        for match in prv:
            x2, y2, w2, h2 = match
            if x2 <= x1 and y2 <= y1 and x1+w1 <= x2+w2 and y1+h1 <= y2+h2:
                result.append(match)
                found = 1
                break
        if found == 0:
            result.append(element)
    return result

