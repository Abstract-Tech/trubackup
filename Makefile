dump:
	python ./src/scripts/dump_mysql.py
	python ./src/scripts/dump_mongo.py

restore:
	python ./src/scripts/restore_mysql.py
	python ./src/scripts/restore_mongo.py
