from fastapi import APIRouter, Depends
from database import get_db
from src.schema import DateAvailability
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse as response
import models


router = APIRouter(tags=["time-slots"])


def find_common_time_slots(slots):
    # Sort slots by start time
    slots.sort(key=lambda x: x.start_time)

    # Initialize a list to store common available time slots
    common_slots = []

    # Iterate over sorted slots and check for overlaps
    current_start = None
    current_end = None

    for slot in slots:
        if current_start is None:  # First slot
            current_start = slot.start_time
            current_end = slot.end_time
        else:
            # Check if there is an overlap with the current slot
            if slot.start_time <= current_end:
                # Overlapping, merge the intervals
                current_end = min(current_end, slot.end_time)
            else:
                # No overlap, store the previous common slot
                common_slots.append((current_start, current_end))
                # Reset to the new slot
                current_start = slot.start_time
                current_end = slot.end_time

    # Append the last slot
    if current_start is not None:
        common_slots.append((current_start, current_end))

    return common_slots


def format_time_range(start_time, end_time):
    """Helper function to format datetime into 'HH:MMam/pm-HH:MMam/pm'"""
    return f"{start_time.strftime('%I:%M%p').lower()}-{end_time.strftime('%I:%M%p').lower()}"


@router.post("/get-available-time-slots")
def get_available_time_slots(
    request: DateAvailability,
    db: Session = Depends(get_db),
):
    # Available time slots query
    try:

        available_slots = (
            db.query(models.TimeSlot)
            .filter(
                models.TimeSlot.user_id.in_(request.user_id),
                models.TimeSlot.time_zone == request.time_zone,
                models.TimeSlot.date.between(
                    request.date_range[0], request.date_range[1]
                ),
            )
            .all()
        )

        if not available_slots:
            return response(
                status_code=404, content={"status": True, "message": "No data found"}
            )

    except:
        return response(
            status_code=400,
            content={"status": False, "message": "something went wrong"},
        )
    # Call the function to find common time slots from the available slots
    common_slots = find_common_time_slots(available_slots)

    # Group common slots by date
    result = {}
    for start_time, end_time in common_slots:
        date_str = start_time.date().strftime("%d-%m-%Y")
        time_range = format_time_range(start_time, end_time)

        # Add time range to the correct date in the result
        if date_str not in result:
            result[date_str] = []
        result[date_str].append(time_range)

    return response(status_code=200, content=result)
