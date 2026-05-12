import os
import getpass
import psycopg2


# Password auth using DB_PASSWORD env var or prompt.
DB_HOST = "database-1.c5sw4iu0ohno.ap-south-1.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
SSL_ROOT_CERT = "./global-bundle.pem"


def main() -> None:
	password = os.getenv("DB_PASSWORD") or getpass.getpass("DB password: ")

	conn = None
	try:
		conn = psycopg2.connect(
			host=DB_HOST,
			port=DB_PORT,
			database=DB_NAME,
			user=DB_USER,
			password=password,
			sslmode="verify-full",
			sslrootcert=SSL_ROOT_CERT,
		)
		cur = conn.cursor()
		cur.execute("SELECT version();")
		print(cur.fetchone()[0])

		cur.execute(
			"""
			SELECT datname
			FROM pg_database
			WHERE datistemplate = false
			ORDER BY datname;
			"""
		)
		db_names = [row[0] for row in cur.fetchall()]
		print("Databases:")
		for name in db_names:
			print(f"- {name}")

		cur.execute(
			"""
			SELECT table_schema, table_name
			FROM information_schema.tables
			WHERE table_type = 'BASE TABLE'
			  AND table_schema NOT IN ('pg_catalog', 'information_schema')
			ORDER BY table_schema, table_name;
			"""
		)
		tables = cur.fetchall()
		print(f"Tables in {DB_NAME}:")
		if tables:
			for schema, table in tables:
				print(f"- {schema}.{table}")
		else:
			print("- (none)")
		cur.close()
	except Exception as exc:
		print(f"Database error: {exc}")
		raise
	finally:
		if conn:
			conn.close()


if __name__ == "__main__":
	main()
