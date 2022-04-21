import datetime


class HoursTimedelta(datetime.timedelta):
    def __str__(self):
        seconds = self.total_seconds()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        microseconds = self.microseconds
        milliseconds = microseconds // 1000
        formatted_time_delta = "{}:{}:{}:{}".format(
            str(int(hours)).zfill(2),
            str(int(minutes)).zfill(2),
            str(int(seconds)).zfill(2),
            str(int(milliseconds)).zfill(3),
        )

        return formatted_time_delta
