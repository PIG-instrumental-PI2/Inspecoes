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
            int(hours), int(minutes), int(seconds), int(milliseconds)
        )
        return formatted_time_delta
