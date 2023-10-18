import dateutil.parser as parser


def is_a_previous_time(last_update_time, current_time):
    if parser.parse(last_update_time) < parser.parse(current_time):
        return True
    else:
        return False


def covert_to_local_timezone(datetime):
    return parser.parse(datetime).astimezone(tz=None)
