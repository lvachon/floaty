import gps
session = gps.gps(host="localhost",port="2947")
session.stream(flags=gps.WATCH_JSON)
for report in session:
	print(report)
