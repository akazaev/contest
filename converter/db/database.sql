create table if not exists documents (id integer primary key autoincrement, uuid text, pages integer, ready integer, status text, msg text, filename text);
create table if not exists nlp (id integer primary key autoincrement, uuid text, page integer, status text, json text, final text);
create table if not exists include (id integer primary key autoincrement, word text unique on conflict ignore);
create table if not exists exclude (id integer primary key autoincrement, word text unique on conflict ignore);
