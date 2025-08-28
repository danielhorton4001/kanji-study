import sqlite3
from pathlib import Path



DB_DIR = "userdata/decks.db"
DB_MEMORY = ":memory:"



class DatabaseModel():
	"""
	Unused SQLite3 database class. May return to at a later date but for now I can't justify working on this when the JSON implementation works fine and can be stored in plaintext for external editing should the user prefer.
	"""

	def __init__(self):
		# Create a db if none exists
		db_path = Path(DB_DIR)
		if not db_path.exists():
			self.create_new_db()


	def create_new_db(self):
		sql_statements = [
			"""CREATE TABLE IF NOT EXISTS decks (
				id INTEGER PRIMARY KEY,
				name text NOT NULL
			);""",

			"""CREATE TABLE IF NOT EXISTS kanji (
				id INTEGER PRIMARY KEY,
				name text NOT NULL
			);"""
		]

		try:

			with DatabaseConnection() as db:
				print(f"Created SQLite database with version {sqlite3.sqlite_version} successfully.")
				
				cursor = db.cursor()

				for statement in sql_statements:
					cursor.execute(statement)

				db.commit()

				print("Database setup completed successfully.")



		except sqlite3.OperationalError as e:

			print("Failed to create database:", e)



class DatabaseConnection():
	"""
	For use with the `with` statement. Ensures the database is always closed properly.
	"""
	
	def __enter__(self):
		# Connect to db if exists, otherwise make one
		self.db = sqlite3.connect(DB_MEMORY)
		return self.db

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.db.close()