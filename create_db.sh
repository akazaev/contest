#!/bin/bash

# remove old db
rm documents.db

# init db
cat converter/db/database.sql | sqlite3 documents.db
cat converter/db/surnames.sql | sqlite3 documents.db
cat converter/db/names.sql | sqlite3 documents.db
