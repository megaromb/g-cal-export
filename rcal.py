from datetime import datetime, timedelta
from enum import Enum
from datetime import datetime

DATE_TIME_FORMAT = "%Y.%m.%d %H:%M:%S"


class RFrequency(Enum):
    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    YEARS = "years"


class RWeekDay(Enum):
    MONDAY = "mon"
    TUESDAY = "tue"
    WEDNESDAY = "wed"
    THURSDAY = "thu"
    FRIDAY = "fri"
    SATURDAY = "sat"
    SUNDAY = "sun"


class RTaskStatus(Enum):
    DONE = "done"
    NEW = "new"
    SNOOZED = "snoozed"
    DOING = "doing"


def str_time(dt: datetime, fmt: str = DATE_TIME_FORMAT):
    return dt.strftime(fmt)


class RReminder:
    def __init__(self, when: datetime):
        self.when = when

    def __str__(self):
        return f"when: {str_time(self.when)}"


class RRecurrence:
    def __init__(self, interval, frequency: RFrequency = None, weekdays: [RWeekDay] = None, month_day: int = None,
                 begin: datetime = None, end: datetime = None):
        now = datetime.now()
        self.interval: int = interval
        self.month_day: int = month_day
        self.period = frequency
        self.weekdays = weekdays
        self.begin = now if begin is None else begin
        self.end = now if end is None else end

    def __str__(self):
        return \
            f"interval: {self.interval}, " \
            f"period: {self.period}, " \
            f"weekdays: {self.weekdays}, " \
            f"begin: {str_time(self.begin)}, " \
            f"end: {str_time(self.end)}"


class RTaskStep:
    def __init__(self, title: str, status: RTaskStatus = RTaskStatus.NEW):
        self.title = title
        self.status = status

    def __str__(self):
        return f"title: {self.title}, status: {self.status}"


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    return cls


@auto_str
class RTask:
    def __init__(self, title: str, due: datetime,
                 recurrence: RRecurrence = None,
                 steps: [RTaskStep] = None,
                 description: str = None,
                 created: datetime = None,
                 modified: datetime = None,
                 all_day: bool = False,
                 categories: [str] = None,
                 duration: timedelta = None,
                 status: RTaskStatus = None,
                 location: str = None,
                 extra=None):
        now = datetime.now()
        self.title = title
        self.due = due
        self.steps = steps
        self.description = description
        self.created = now if created is None else created
        self.modified = now if modified is None else modified
        self.all_day = all_day
        self.categories = categories
        self.duration = duration
        self.status = status
        self.location = location
        self.extra = extra

    # def __str__(self):
    #     return \
    #         f"title: {self.title}, " \
    #         f"due: {str_time(self.due)}, " \
    #         f"steps": {}


