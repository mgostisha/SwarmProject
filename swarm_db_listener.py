import sqlite3
import time

#---------- Connect to the swarm database ----------
db = sqlite3.connect('/Users/Martin/swarm-django/swarm_project/swarm.sqlite3')
cursor = db.cursor()

#---------- Set the id of the current row to be worked on ----------
CURRENT_ID = 1

#---------- Define SQLite commands to be used ----------
# Get initial simulation parameters that determine the drag options
SQL_drag = '''SELECT drag_option, potential, vel_field, den_field FROM swarm_simulationparameters WHERE id=?'''

cursor.execute(SQL_drag, (CURRENT_ID,))
current_row = cursor.fetchone()

while True:

	cursor.execute(SQL_drag, (CURRENT_ID,))
	current_row = cursor.fetchone()

	if current_row != None:
		print 'Drag: {0}, Potential: {1}, Velocity Field: {2}, Density Field: {3}'.format(
			current_row[0], current_row[1], current_row[2], current_row[3])

		CURRENT_ID += 1
	else:
		time.sleep(5)

db.close()


