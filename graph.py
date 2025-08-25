import plotext as plt
from datetime import datetime
from datetime import timedelta

import sqlite3
import os
import yaml


config = yaml.safe_load(open("config.yaml"))
anki_db_path = config["ankiPath"]

conn = sqlite3.connect(anki_db_path)
cur = conn.cursor()

# --- New cards graph --- #

res = cur.execute("""SELECT
  date(id / 1000, 'unixepoch') AS creation_date,
  COUNT(*) AS notes_created
FROM notes
WHERE id >= strftime('%s', 'now', '-30 days') * 1000
GROUP BY creation_date
ORDER BY creation_date ASC;

""")
dates, notes = zip(*res.fetchall())

dates = [datetime.strptime(date, "%Y-%m-%d").strftime("%m/%d") for date in dates]
plt.clear_color()

plt.plot_size(40,20)
plt.date_form('m/d')

plt.bar(dates, notes)

plt.title("New vocab entry per day")
plt.yticks([x for x in range(max(notes)+1)])
plt.ylabel("Entered vocab")

plt.build()
plt.save_fig("content/generated/new.txt")

# --- Revisions graph --- #
plt.clear_figure()
plt.clear_data()

res = cur.execute("""WITH RECURSIVE dates(day) AS (
  SELECT date('now', '-30 days')
  UNION ALL
  SELECT date(day, '+1 day')
  FROM dates
  WHERE day < date('now')
)
SELECT
  dates.day AS review_date,
  SUM(revlog.time) / 60000.0 AS total_minutes
FROM dates
LEFT JOIN revlog
  ON date(revlog.id / 1000, 'unixepoch') = dates.day
GROUP BY dates.day
ORDER BY dates.day ASC;

""")
dates, revs = zip(*res.fetchall())

dates = [datetime.strptime(date, "%Y-%m-%d").strftime("%m/%d") for date in dates]
plt.clear_color()

plt.plot_size(40,20)
plt.date_form('m/d')

plt.plot(dates, revs)

plt.title("Review time in minutes per day")

plt.build()
plt.save_fig("content/generated/revs.txt")
