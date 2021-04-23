class Snowflake(int):
    def __new__(cls, value):
        return super().__new__(cls, 0 if not value else int(value))
