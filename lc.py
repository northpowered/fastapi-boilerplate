import datetime
print(datetime.datetime.now())
td = datetime.timedelta(hours=+3)
tz = datetime.timezone(td)
print(td)
print(tz)
print(datetime.datetime.now(tz=tz))