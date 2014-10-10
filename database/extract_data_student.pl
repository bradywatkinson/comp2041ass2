#!/usr/bin/perl -w

use DBI;

#---open connection to db---
$dbh = DBI->connect('dbi:SQLite:student_DB', 'root', 'password') or die;

my $id = 100000;

my @student_attributes = ('name','birthdate','degree','email','gender','hair_colour',
			'height','password','username','weight');


#=========Creates SQL tables=========
#.........Student Table..............
my $sql = "DROP TABLE IF EXISTS students";
	$sth = $dbh->prepare($sql);
	$sth->execute or die "SQL Error: $DBI::errstr\n";
	while (@row = $sth->fetchrow_array) {
		print "@row\n";
	}

my $sql = "CREATE TABLE IF NOT EXISTS students(user_id char(6), first_name varchar, last_name varchar, gender char(1), dob varchar, email varchar, hair_colour varchar, degree varchar, height varchar, weight varchar, username varchar, password varchar)";
	$sth = $dbh->prepare($sql);
	$sth->execute or die "SQL Error: $DBI::errstr\n";
	while (@row = $sth->fetchrow_array) {
		print "@row\n";
	}	

#=========End Create Table===========

foreach $dir (@ARGV) {
	open F, "<$dir/profile.txt" or die;
	@file = <F>;
	$file = join '', @file;
	@chunk = split '\n', $file;
	
	my %student;
	foreach $line (@chunk) {
		if ($line =~ s/^(\w+):$/$1/) {
			$category = $1;
		} elsif ($category ~~ @student_attributes) {
			$line =~ s/\t//;
			$student{$category} = $line;
		}
	}
	
	#my @keys = keys %student;
	#foreach $key (sort @keys) {	
		#printf "%12s: $student{$key}\n", $key;
	#}
	
	$student{"name"} =~ /(\w+) (\w*)/;
	$f_name 	= $1 || "";
	$l_name 	= $2 || "";
	$gender 	= $student{"gender"} || "";
	$dob 		= $student{"birthdate"} || "";
	$email	= $student{"email"} || "";
	$hair		= $student{"hair_colour"} || "";
	$degree	= $student{"degree"} || "";
	$height	= $student{"height"} || "";
	$weight	= $student{"weight"} || "";
	$u_name	= $student{"username"} || "";
	$pass		= $student{"password"} || "";
	 
	my $sql = "insert into students values ('$id','$f_name','$l_name','$gender','$dob','$email','$hair','$degree','$height','$weight','$u_name','$pass')";
	print "$sql\n";
	$sth = $dbh->prepare($sql);
	$sth->execute or die "SQL Error: $DBI::errstr\n";	
	#---open connection to db---
	$sql = "select * from students";
	$sth = $dbh->prepare($sql);
	$sth->execute or die "SQL Error: $DBI::errstr\n";
	while (@row = $sth->fetchrow_array) {
		print "@row\n";
	}
	
	$id += 10;
}

#---close connection to db---
$dbh->disconnect();
