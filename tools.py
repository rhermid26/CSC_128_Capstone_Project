"""
CSC-128 Capstone Project starter: the tools and their schemas
Roberto Hermida Lujan
"""


# Constants should never ever be modified
DEFAULT_AVAILABILITY = {
    "monday": {
        "rooms" : [
            "214", 
            "216"
        ],
        "hours" : [
            "8:00 AM", 
            "8:00 PM"
        ]
    },
    "tuesday": {
        "rooms" : [
            "214"
        ],
        "hours" : [
            "8:00 AM", 
            "8:00 PM"
        ]
    },
    "tuesday": {
        "rooms" : [
            "214", 
            "216", 
            "220"
        ],
        "hours" : [
            "8:00 AM", 
            "8:00 PM"
        ]
    },
    "thursday": {
        "rooms" : [],
        "hours" : []
    },
    "friday": {
        "rooms" : [
            "220"
        ],
        "hours" : [
            "8:00 AM", 
            "5:00 PM"
        ]
    }
}

# Constants can technically be treated as regular variables 
# But it is a good convention to manually clone them
current_availabilities = {}


# This will reset the current availabilities
def reset_availabilities():
    current_availabilities.clear();
    for key, value in DEFAULT_AVAILABILITY.items():
        current_availabilities[key] = {
            "rooms" : list(DEFAULT_AVAILABILITY[key]["rooms"]),
            "hours" : list(DEFAULT_AVAILABILITY[key]["hours"])
        }

reset_availabilities();

def check_availability(day):
    """Return the rooms free on a given weekday."""
    free = current_availabilities.get(day.lower(), {})
    if not free:
        return f"No study rooms are available on {day}."
    return f"Available on {day}: " + ", ".join(free["rooms"])

def get_hours(day):
    """TODO 3: return the opening hours for a weekday."""
    free = current_availabilities.get(day.lower(), {})
    if not free:
        return f"No opening hours are available on {day}."
    return f"Opening hours on {day}: " + ", ".join(free["hours"])

def book_room(day, room, name):
    """
    TODO 4: reserve a room and remove it from availability.

    Think about what this function should NOT be able to do before you
    write it. Do not add a delete function.
    """
    day = day.lower()
    room = str(room)

    if day not in current_availabilities:
        return f"{day} is not a valid weekday."

    if room not in current_availabilities[day]["rooms"]:
        return f"Room {room} is not available on {day}."

    current_availabilities[day]["rooms"].remove(room)

    return f"Room {room} has been booked for {name} on {day}."

AVAILABLE_TOOLS = {
    "check_availability" : check_availability,
    "get_hours" : get_hours,
    "book_room" : book_room,
}


# this schema is the only thing the model sees about the function
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": (
                "Check which study rooms are free on a given weekday. "
                "Use this whenever a student asks about room availability."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "description": "Weekday name, for example Thursday",
                    }
                },
                "required": ["day"],
            },
        },
    },
    {
    "type": "function",
        "function": {
            "name": "get_hours",
            "description": "Check the opening hours for a given weekday.",
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "description": "Weekday name, for example Monday",
                    }
                },
                "required": ["day"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_room",
            "description": "Book an available study room for a student.",
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "description": "Weekday name, for example Monday",
                    },
                    "room": {
                        "type": "string",
                        "description": "Study room number, for example 214",
                    },
                    "name": {
                        "type": "string",
                        "description": "Student's name",
                    },
                },
                "required": ["day", "room", "name"],
            },
        },
    },
]