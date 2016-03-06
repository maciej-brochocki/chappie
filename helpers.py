import numpy as np


def merge_area(area, areas):
    result = []
    x, y, w, h = area
    for element in areas:
        x2, y2, w2, h2 = element
        if x < x2 + w2 and x + w > x2 and x + w > x2 and x < x2 + w2:
            w = max(x + w, x2 + w2)
            h = max(y + h, y2 + h2)
            x = min(x, x2)
            y = min(y, y2)
            w = w - x
            h = h - y
        else:
            result.append(element)
    return (x, y, w, h), result


def merge_areas(before, areas):
    if len(areas) == 0:
        return before
    head = areas[0]
    after = areas[1:]
    head, before = merge_area(head, before)
    head, after = merge_area(head, after)
    before.append(head)
    return merge_areas(before, after)


def overlapping_areas(src, prv):
    result = []
    for element in src:
        x1, y1, w1, h1 = element
        found = 0
        for match in prv:
            x2, y2, w2, h2 = match
            if x2 <= x1 and y2 <= y1 and x1 + w1 <= x2 + w2 and y1 + h1 <= y2 + h2:
                result.append(match)
                found = 1
                break
        if found == 0:
            result.append(element)
    return result


def sort_objects_by_index(objects, index):
    if len(objects) > 0:
        objects = np.hstack((np.reshape(index, (-1, 1)), objects))
        objects = objects[np.argsort(objects[:, 0])]
        objects = objects[:, 1:]
        objects = objects[::-1]
    return objects
