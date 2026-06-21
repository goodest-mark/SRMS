from system_state import SystemState


def get_grade(mark, level=None):

    if level is None:
        level = SystemState.get_level()

    if level == "A_LEVEL":

        if mark >= 80:
            return "A"
        elif mark >= 70:
            return "B"
        elif mark >= 60:
            return "C"
        elif mark >= 50:
            return "D"
        elif mark >= 40:
            return "E"
        elif mark >= 35:
            return "S"
        else:
            return "F"

    else:

        if mark >= 80:
            return "A"
        elif mark >= 70:
            return "B"
        elif mark >= 60:
            return "C"
        elif mark >= 50:
            return "D"
        else:
            return "F"


def get_points(grade, level=None):

    if level is None:
        level = SystemState.get_level()

    if level == "A_LEVEL":

        return {
            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
            "S": 6,
            "F": 7
        }.get(grade, 7)

    return {
        "A": 1,
        "B": 2,
        "C": 3,
        "D": 4,
        "F": 5
    }.get(grade, 5)