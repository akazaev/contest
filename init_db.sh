# init db
mongoimport --type csv --drop -d documents -c include --fields word converter/db/surnames.csv
mongoimport --type csv -d documents -c include --fields word converter/db/names.csv
mongoimport --type csv --drop -d documents -c exclude --fields word converter/db/exclude.csv
