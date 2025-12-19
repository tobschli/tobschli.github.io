import plotext as plt
from datetime import datetime

import sqlite3
import yaml


config = yaml.safe_load(open("config.yaml"))
anki_db_path = config["ankiPath"]

conn = sqlite3.connect(anki_db_path)
cur = conn.cursor()

# --- Revisions graph --- #
plt.clear_figure()
plt.clear_data()

res = cur.execute("""
WITH RECURSIVE dates(day) AS (
  SELECT date('now', '-30 days')
  UNION ALL
  SELECT date(day, '+1 day')
  FROM dates
  WHERE day < date('now')
)
SELECT
  dates.day AS review_date,
  COALESCE(SUM(revlog.time), 0) / 60000.0 AS total_minutes
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
