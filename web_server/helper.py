PI = 3.14159265359
PI2 = 2*PI

MAX_DISTANCE = 40

MAX_NUMBER_GROUPS = 10
MAX_NUMBER_POINTS = 20

def validate_group_name(group_name: str):
    """
    Returns:
        Boolean: return True if valid group name, False in other cases.
    """
    if len(group_name) < 0 or len(group_name) > 7:
        return False
    if group_name[0:5] != "group":
        return False
    try:
        num = int(group_name[5:])
        return group_name
    except:
        return False
    
    
def validate_angle(angle: float):
    """
    Returns:
        Boolean: return True if valid angle, False in other cases.
    """
    try:
        angle = float(angle)
        
        if angle <= 0 or angle >= PI2:
            return False
        
        return angle
        
    except:
        return False
    
def validate_distance(distance: float):
    """
    Returns:
        Boolean: return True if valid distance, False in other cases.
    """
    try:
        distance = float(distance)
        if distance <= 0 or distance >= MAX_DISTANCE:
            return False
        
        return distance
        
    except:
        return False
    

def add_point(points: dict, group_name: str, angle: float, distance :float):
    """Add a point in the Points dictionary
    """
    if not group_name in points.keys():
        if len(points.keys()) < MAX_NUMBER_GROUPS:
            points[group_name] = {"points": [{"distance": distance, "angle": angle}
                                            ],
                                  "number_points": 1
                                }
    else:
        if points[group_name]["number_points"] < MAX_NUMBER_POINTS:
            points[group_name]["points"].append({"distance": distance, "angle": angle})
            points[group_name]["number_points"] += 1
            
        else:
            points[group_name]["points"].pop(0)
            points[group_name]["points"].append({"distance": distance, "angle": angle})
            
            
    
            
            