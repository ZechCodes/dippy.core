from datetime import datetime


class Timestamp(float):
    def __new__(cls, value=None):
        return super().__new__(
            cls, datetime.utcnow().timestamp() if value is None else value
        )

    def to_date(self) -> datetime:
        return datetime.utcfromtimestamp(self)

    def __repr__(self):
        return f"<{type(self).__name__} {self}>"

    def __str__(self):
        return self.to_date().isoformat(" ")
