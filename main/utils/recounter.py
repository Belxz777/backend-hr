
def recount_hours(hours):
    """
    Convert decimal hours to hours and minutes format
    Example: 1.75 -> (1, 45) meaning 1 hour and 45 minutes
    """
    whole_hours = int(hours)
    decimal_part = hours - whole_hours
    minutes = int(decimal_part * 60)
    
    return whole_hours, minutes