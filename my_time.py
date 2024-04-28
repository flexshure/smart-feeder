from collections import namedtuple

# Define the named tuple
Time = namedtuple('Time', ['hours', 'minutes'])

# Define comparison methods for Time objects
def time_to_minutes(time):
    return time.hours * 60 + time.minutes

def __eq__(self, other):
    return time_to_minutes(self) == time_to_minutes(other)

def __lt__(self, other):
    return time_to_minutes(self) < time_to_minutes(other)

def __le__(self, other):
    return time_to_minutes(self) <= time_to_minutes(other)

def __gt__(self, other):
    return time_to_minutes(self) > time_to_minutes(other)

def __ge__(self, other):
    return time_to_minutes(self) >= time_to_minutes(other)

# Bind comparison methods to the named tuple class
Time.__eq__ = __eq__
Time.__lt__ = __lt__
Time.__le__ = __le__
Time.__gt__ = __gt__
Time.__ge__ = __ge__