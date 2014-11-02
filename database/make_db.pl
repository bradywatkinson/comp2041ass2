#!/usr/bin/perl -w

use DBI;
#=========Creates SQL tables=========

#---open connection to db---
$dbh = DBI->connect('dbi:SQLite:love2041_DB', 'root', 'password') or die;

#.........Student Table..............
my $sql_drop_users = "DROP TABLE IF EXISTS USERS";
	$sth = $dbh->prepare($sql_drop_users);
	$sth->execute or die "SQL Error: $DBI::errstr\n";

my $sql_make_users = "
	CREATE TABLE IF NOT EXISTS USERS(
	USER_ID         INTEGER PRIMARY KEY AUTOINCREMENT, 
	FIRST_NAME 		TEXT, 
	LAST_NAME 		TEXT, 
	GENDER 			TEXT, 
	YEAR 			TEXT, 
	MONTH			TEXT,
	DAY				TEXT,
	EMAIL 			TEXT, 
	HAIR_COLOUR 	TEXT, 
	DEGREE 			TEXT, 
	HEIGHT 			TEXT, 
	WEIGHT 			TEXT, 
	USERNAME 		TEXT, 
	PASSWORD 		TEXT,
	PREF_GENDER		TEXT,
	PREF_HAIR		TEXT,
	PREF_AGE_MIN	TEXT,
	PREF_AGE_MAX	TEXT,
	PREF_HEIGHT_MIN	TEXT,
	PREF_HEIGHT_MAX	TEXT,
	PREF_WEIGHT_MIN	TEXT,
	PREF_WEIGHT_MAX	TEXT,
	ABOUT_ME		TEXT)";
$sth = $dbh->prepare($sql_make_users);
$sth->execute or die "SQL Error: $DBI::errstr\n";


#.........Courses Table..............
my $sql_drop_user_courses = "DROP TABLE IF EXISTS USER_COURSES";
$sth = $dbh->prepare($sql_drop_user_courses);
$sth->execute or die "SQL Error: $DBI::errstr\n";


my $sql_make_user_courses = "
	CREATE TABLE IF NOT EXISTS USER_COURSES(
	COURSE_CODE 		CHAR(8), 
	YEAR 				CHAR(4),
	SEMESTER 			CHAR(2),
	USER_ID 			CHAR(6),
	FOREIGN KEY(USER_ID)
		REFERENCES USERS(USER_ID)
		ON DELETE CASCADE
	PRIMARY KEY(USER_ID, COURSE_CODE, SEMESTER, YEAR))";
$sth = $dbh->prepare($sql_make_user_courses);
$sth->execute or die "SQL Error: $DBI::errstr\n";


#.........Favourites Table..............
my $sql_drop_user_favourites = "DROP TABLE IF EXISTS USER_FAVOURITES";
$sth = $dbh->prepare($sql_drop_user_favourites);
$sth->execute or die "SQL Error: $DBI::errstr\n";


my $sql_make_user_favourites = "
	CREATE TABLE IF NOT EXISTS USER_FAVOURITES(
	USER_ID 	INTEGER, 
	TYPE_ID 	TEXT,
	NAME 		TEXT,
	FOREIGN KEY(USER_ID)
		REFERENCES USERS(USER_ID)
		ON DELETE CASCADE
	PRIMARY KEY(USER_ID, NAME))";
$sth = $dbh->prepare($sql_make_user_favourites);
$sth->execute or die "SQL Error: $DBI::errstr\n";

#.........Messages Table..............
my $sql_drop_messages = "DROP TABLE IF EXISTS MESSAGES";
$sth = $dbh->prepare($sql_drop_messages);
$sth->execute or die "SQL Error: $DBI::errstr\n";

my $sql_make_messages = "
	CREATE TABLE IF NOT EXISTS MESSAGES(
	MESSAGE_ID	INTEGER PRIMARY KEY AUTOINCREMENT,
	GIVE_ID 	TEXT, 
	GET_ID 		TEXT,
	MESSAGE		TEXT,
	SEND_TIME	DATETIME
	FOREIGN KEY(GIVE_ID, GET_ID)
		REFERENCES USERS(USER_ID)
		ON DELETE CASCADE)";
$sth = $dbh->prepare($sql_make_messages);
$sth->execute or die "SQL Error: $DBI::errstr\n";
#=========End Create Tables===========
