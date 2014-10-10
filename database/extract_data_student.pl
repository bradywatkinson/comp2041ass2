#!/usr/bin/perl -w

use DBI;

my $id = 100000;
my @student_attributes = ('name','birthdate','degree','email','gender','hair_colour',
			'height','password','username','weight');
my @favourite_categories = ('favourite_TV_shows','favourite_bands','favourite_books','favourite_hobbies','favourite_movies');
#=========Creates SQL tables=========

#---open connection to db---
$dbh = DBI->connect('dbi:SQLite:student_DB', 'root', 'password') or die;

#.........Student Table..............
my $sql_drop_users = "DROP TABLE IF EXISTS users";
	$sth = $dbh->prepare($sql_drop_users);
	$sth->execute or die "SQL Error: $DBI::errstr\n";
	while (@row = $sth->fetchrow_array) {
		print "@row\n";
	}

my $sql_make_users = "
	CREATE TABLE IF NOT EXISTS users(
	user_id char(6) PRIMARY KEY, 
	first_name 		VARCHAR, 
	last_name 		VARCHAR, 
	gender 			CHAR(1), 
	dob 				VARCHAR, 
	email 			VARCHAR, 
	hair_colour 	VARCHAR, 
	degree 			VARCHAR, 
	height 			VARCHAR, 
	weight 			VARCHAR, 
	username 		VARCHAR, 
	password 		VARCHAR)";
$sth = $dbh->prepare($sql_make_users);
$sth->execute or die "SQL Error: $DBI::errstr\n";
while (@row = $sth->fetchrow_array) {
	print "@row\n";
}	

#.........Courses Table..............
my $sql_drop_user_courses = "DROP TABLE IF EXISTS user_courses";
$sth = $dbh->prepare($sql_drop_user_courses);
$sth->execute or die "SQL Error: $DBI::errstr\n";
while (@row = $sth->fetchrow_array) {
	print "@row\n";
}

my $sql_make_user_courses = "
	CREATE TABLE IF NOT EXISTS user_courses(
	course_code 		CHAR(8), 
	year 					CHAR(4),
	semester 			CHAR(2),
	user_id 				CHAR(6),
	FOREIGN KEY(user_id)
		REFERENCES users(user_id)
		ON DELETE CASCADE
	PRIMARY KEY(user_id, course_code, semester, year))";
$sth = $dbh->prepare($sql_make_user_courses);
$sth->execute or die "SQL Error: $DBI::errstr\n";
while (@row = $sth->fetchrow_array) {
	print "@row\n";
}

#.........Favourites Table..............
my $sql_drop_user_favourites = "DROP TABLE IF EXISTS user_favourites";
$sth = $dbh->prepare($sql_drop_user_favourites);
$sth->execute or die "SQL Error: $DBI::errstr\n";
while (@row = $sth->fetchrow_array) {
	print "@row\n";
}

my $sql_make_user_favourites = "
	CREATE TABLE user_favourites(
	user_id CHAR(6), 
	type_id VARCHAR,
	name VARCHAR,
	FOREIGN KEY(user_id)
		REFERENCES users(user_id)
		ON DELETE CASCADE
	PRIMARY KEY(user_id, name))";
$sth = $dbh->prepare($sql_make_user_favourites);
$sth->execute or die "SQL Error: $DBI::errstr\n";
while (@row = $sth->fetchrow_array) {
	print "@row\n";
}

#=========End Create Tables===========

#=========sql functions===========

sub queryTable
{
	my ($query_table_name) = (@_); 
	my $sql_query = "select * from $query_table_name";
	my $sth_query = $dbh->prepare($sql_query);
	$sth_query->execute or die "SQL Error: $DBI::errstr\n";
	while (@row = $sth->fetchrow_array) {
		print "@row\n";
	}	
}
#=========end sql functions========

foreach $dir (@ARGV) {
	open F, "<$dir/profile.txt" or die;
	@file = <F>;
	$file = join '', @file;
	@chunk = split '\n', $file;
	
	my %users;
	my @user_courses_course_code;
	my @user_courses_year;
	my @user_courses_semester;
	my %favourites;
	foreach $line (@chunk) {
		$line =~ s/\t//;
		if ($line =~ s/^(\w+):$/$1/) {
			$category = $1;
		} elsif ($category ~~ @student_attributes) {		
			$users{$category} = $line;
		} elsif ($category eq "courses") {
			my @course_items = split ' ', $line;
			push @user_courses_year, 			$course_items[0];
			push @user_courses_semester, 		$course_items[1];
			push @user_courses_course_code, 	$course_items[2];
		} elsif ($category ~~ @favourite_categories) {
			$favourites{$line} = $category;
		}
	}
	
	#my @keys = keys %student;
	#foreach $key (sort @keys) {	
		#printf "%12s: $student{$key}\n", $key;
	#}
	
	#=====insert into user table=====
	$users{"name"} =~ /(\w+) ?(\w*)/;
	my $f_name 	= $1 || "";
	my $l_name 	= $2 || "";
	my $gender 	= $users{"gender"} || "";
	my $dob 		= $users{"birthdate"} || "";
	my $email	= $users{"email"} || "";
	my $hair		= $users{"hair_colour"} || "";
	my $degree	= $users{"degree"} || "";
	my $height	= $users{"height"} || "";
	my $weight	= $users{"weight"} || "";
	my $u_name	= $users{"username"} || "";
	my $pass		= $users{"password"} || "";
	 
	my $sql_insert_users = "insert into users values ('$id','$f_name','$l_name','$gender','$dob','$email','$hair','$degree','$height','$weight','$u_name','$pass')";
	print "$sql_insert_users\n";
	$sth = $dbh->prepare($sql_insert_users);
	$sth->execute or die "SQL Error: $DBI::errstr\n";	
	
	#$sql = "select * from users";
	#$sth = $dbh->prepare($sql);
	#$sth->execute or die "SQL Error: $DBI::errstr\n";
	#while (@row = $sth->fetchrow_array) {
	#	print "@row\n";
	#}
	
	#=====insert into user_courses table=====
	foreach $i (0..$#user_courses_course_code) {
		my $course_code	= $user_courses_course_code[$i] || "";
		my $year				= $user_courses_year[$i] || "";
		my $semester		= $user_courses_semester[$i] || "";
		my $sql_insert_users_courses = "insert into user_courses values ('$course_code','$year','$semester','$id')";
		#print "$sql_insert_users_courses\n";
		$sth = $dbh->prepare($sql_insert_users_courses);
		$sth->execute or die "SQL Error: $DBI::errstr\n";	
	}
	
	#$sql = "select * from user_courses";
	#$sth = $dbh->prepare($sql);
	#$sth->execute or die "SQL Error: $DBI::errstr\n";
	#while (@row = $sth->fetchrow_array) {
	#	print "@row\n";
	#}	
	
	#=====insert into user_courses table=====
	foreach $key (keys %favourites) {
		my $type		= $favourites{$key} || "";
	  (my $name		= $key) =~ s/'/''/g;
		my $sql_insert_users_favourites = "insert into user_favourites values ('$id','$type','$name')";
		#print "$sql_insert_users_favourites\n";
		$sth = $dbh->prepare($sql_insert_users_favourites);
		$sth->execute or die "SQL Error: $DBI::errstr\n";	
	}
	
	#$sql = "select * from user_favourites";
	#$sth = $dbh->prepare($sql);
	#$sth->execute or die "SQL Error: $DBI::errstr\n";
	#while (@row = $sth->fetchrow_array) {
	#	print "@row\n";
	#}
	#
	$id += 10;
	
	
	
}

#---close connection to db---
$dbh->disconnect();
