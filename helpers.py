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

