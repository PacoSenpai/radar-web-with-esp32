import logging

class Logger:
    def __init__(self, name, level=logging.DEBUG, log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        formatter = logging.Formatter(log_format)

        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)

        # Add console handler to logger
        self.logger.addHandler(ch)
        
    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


#Declare some constants
PI = 3.14159265359
PI2 = 2*PI

MAX_DISTANCE = 40

MAX_NUMBER_GROUPS = 10
MAX_NUMBER_POINTS = 20



#Utility functions
def validate_group_name(group_name: str):
    """
    Returns:
        Boolean: return True if valid group name, False in other cases.
    """
    if len(group_name) < 0 or len(group_name) >= 7:
        return False

    group_name.lower()
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
                                  "points_number": 1
                                }
    else:
        if points[group_name]["points_number"] < MAX_NUMBER_POINTS:
            points[group_name]["points"].append({"distance": distance, "angle": angle})
            points[group_name]["points_number"] += 1
            
        else:
            points[group_name]["points"].pop(0)
            points[group_name]["points"].append({"distance": distance, "angle": angle})
            
            
    
            
            