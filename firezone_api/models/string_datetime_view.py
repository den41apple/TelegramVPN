from datetime import datetime


class StringDatetime:
    """
    Удобное строковое представление даты и времени
    """

    def __init__(self, date_time: datetime | str):
        if isinstance(date_time, datetime):
            self.dt = date_time
        else:
            self.dt = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
        self._dt_str = self.dt.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self._dt_str

    def __repr__(self):
        return str(self)
