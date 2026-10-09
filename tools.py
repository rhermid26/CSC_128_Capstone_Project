"""
CSC-128 Capstone Project starter: the tools and their schemas
Roberto Hermida Lujan
"""



import re


def check_course_number(course_number):
    """Check the format of a course number."""

    course_number = course_number.strip().upper()

    if re.fullmatch(r"[A-Z]{3}-\d{3}", course_number):
        return f"{course_number} has a valid course number format."

    return "Use three letters, a hyphen, and three numbers. Example: CSC-128."


def calculate_study_time(total_minutes, break_minutes):
    """Calculate study time after breaks."""

    if total_minutes <= 0 or break_minutes < 0:
        return "Enter a positive study time and a non-negative break time."

    if break_minutes >= total_minutes:
        return "Break time must be less than total study time."

    study_minutes = total_minutes - break_minutes

    return f"You have {study_minutes} minutes of study time."


def create_study_schedule(subjects, available_minutes):
    """Create a simple study schedule for a list of subjects."""

    if not subjects or available_minutes <= 0:
        return "Provide at least one subject and a positive amount of time."

    minutes_per_subject = available_minutes // len(subjects)

    if minutes_per_subject == 0:
        return "There is not enough time to assign each subject a minute."

    schedule = []

    for subject in subjects:
        schedule.append(f"{subject}: {minutes_per_subject} minutes")

    return "\n".join(schedule)


AVAILABLE_TOOLS = {
    "check_course_number": check_course_number,
    "calculate_study_time": calculate_study_time,
    "create_study_schedule": create_study_schedule,
}


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "check_course_number",
            "description": "Check whether a course number follows a format such as CSC-128.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_number": {"type": "string"}
                },
                "required": ["course_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_study_time",
            "description": "Calculate study time remaining after breaks, in minutes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "total_minutes": {"type": "integer"},
                    "break_minutes": {"type": "integer"},
                },
                "required": ["total_minutes", "break_minutes"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_study_schedule",
            "description": "Divide available study time evenly among subjects.",
            "parameters": {
                "type": "object",
                "properties": {
                    "subjects": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "available_minutes": {"type": "integer"},
                },
                "required": ["subjects", "available_minutes"],
            },
        },
    },
]