PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Apparts ( hash_link varchar(10) PRIMARY KEY, raw_link varchar(300), site varchar(10), insert_time timestamp);
CREATE TABLE proxies(ip_address varchar(20), status varchar(4), insert_time timestamp);
CREATE TABLE subscribers( ID INTEGER PRIMARY KEY);
COMMIT;
