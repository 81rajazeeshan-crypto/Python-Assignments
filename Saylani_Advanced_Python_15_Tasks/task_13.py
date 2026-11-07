### Task 13 | Booking Conflict Scheduler
### Concepts: Datetime, sorting, interval algorithms
### Problem: Implement a room booking scheduler. Each booking has room, start datetime, end datetime, and booking ID. Accept bookings only when they do not overlap existing bookings for the same room.
### Requirements: Use datetime objects; reject end<=start and duplicate IDs. Adjacent bookings are allowed. Return conflicts for rejected requests.
### Sample / expected behavior: Room A: 09:00–10:00 and 10:00–11:00 accepted; 09:30–10:30 rejected.


from datetime import datetime

class BookingScheduler:
    def __init__(self):
        self._bookings = {}  
        self._room_bookings = {}  

    def add_booking(self, booking_id: str, room: str, start_time: datetime, end_time: datetime):
       
        if end_time <= start_time:
            raise ValueError("End time must be strictly greater than start time.")
            
        
        if booking_id in self._bookings:
            raise ValueError(f"Booking ID '{booking_id}' already exists.")
            
       
        if room not in self._room_bookings:
            self._room_bookings[room] = []
            
        
        conflicts = []
        for existing in self._room_bookings[room]:
            ex_start = existing["start"]
            ex_end = existing["end"]
            
            
            if max(start_time, ex_start) < min(end_time, ex_end):
                conflicts.append(existing)
                
        if conflicts:
            return {
                "status": "rejected",
                "booking_id": booking_id,
                "room": room,
                "conflicts": conflicts,
                "reason": "Time slot overlaps with existing booking(s)."
            }
            
        
        booking_record = {
            "booking_id": booking_id,
            "room": room,
            "start": start_time,
            "end": end_time
        }
        
        self._bookings[booking_id] = booking_record
        self._room_bookings[room].append(booking_record)
        
        return {
            "status": "accepted",
            "booking_id": booking_id,
            "room": room
        }

    def get_room_bookings(self, room: str):
        return self._room_bookings.get(room, [])



if __name__ == "__main__":
    scheduler = BookingScheduler()
    
    date_format = "%Y-%m-%d %H:%M"
    
    
    b1 = scheduler.add_booking(
        "B001", "Room A",
        datetime.strptime("2026-11-10 09:00", date_format),
        datetime.strptime("2026-11-10 10:00", date_format)
    )
    print("Booking 1:", b1["status"])
    
    
    b2 = scheduler.add_booking(
        "B002", "Room A",
        datetime.strptime("2026-11-10 10:00", date_format),
        datetime.strptime("2026-11-10 11:00", date_format)
    )
    print("Booking 2:", b2["status"])
    
    
    b3 = scheduler.add_booking(
        "B003", "Room A",
        datetime.strptime("2026-11-10 09:30", date_format),
        datetime.strptime("2026-11-10 10:30", date_format)
    )
    print("Booking 3:", b3["status"], "| Reason:", b3["reason"])