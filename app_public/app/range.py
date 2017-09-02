"""
    Range class representing a time slot with a begin and an end
"""
import datetime


class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    """
        Test if intersects with other
    """
    def intersects(self, other):
        return other.end > self.start and other.start < self.end

    """
        Tests if other is inside or equal
    """
    def contains(self, other): # intersects with another Range
        return other.start >= self.start and other.end <= self.end

    """
        Converts object to a dict
    """
    def get_dict(self):
        return {'start': self.start, 'end': self.end}

    """
        Substract other
        Returns a list of 0, 1 or 2 Ranges
    """
    def __sub__(self, other):
        if not self.intersects(other): # No intersection
            return [self]
        if other.start <= self.start: # No available before appointment
            if other.end >= self.end: # None available
                return []
            # Available after appointment
            return [Range(other.end, self.end)]
        if other.end >= self.end: # Available before appointment
            return [Range(self.start, other.start)]
        # Available before and after appointment
        return [Range(self.start, other.start), Range(other.end, self.end)]
        
    """
        Substract other
        Returns a list of 0, 1 or 2 Ranges
    """
    def __add__(self, other):
        if not self.intersects(other): # No intersection
            return [self, other]
        return [Range(min(self.start, other.start), max(self.end, other.end))]

    def __str__(self):
        return 'Range <{} - {}>'.format(self.start, self.end)

    """
        Test if finishes before other starts (or same time)
    """
    def __lt__(self, other):
        return self.end <= other.start
 
    """
        Test if starts after other ends (or same time)
    """
    def __gt__(self, other):
        return self.start >= other.end
 
    """
        Tests if starts and ends at the same time as other
    """
    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def get_duration(self) -> datetime.timedelta:
        return self.end - self.start