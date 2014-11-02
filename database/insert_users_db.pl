#!/usr/bin/perl -w

use DBI;

my $id = 1;
my @student_attributes = ('name','birthdate','degree','email','gender','hair_colour',
			'height','password','username','weight');
my @pref_att = ('gender','age_min','age_max','height_min','height_max','weight_min','weight_max');
my @favourite_categories = ('favourite_TV_shows','favourite_bands','favourite_books','favourite_hobbies','favourite_movies');

my $base = "students/";
#---open connection to db---
$dbh = DBI->connect('dbi:SQLite:love2041_DB', 'root', 'password') or die;

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

@users = <$base*>;

foreach (@users) {
	print "$_\n";
	extract_user($_);
}

sub extract_user
{
	my ($dir) = (@_);
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

	open G, "<$dir/preferences.txt" or die;
	@pref = <G>;
	my %prefs;
	my @hairs;
	foreach $line (@pref) {
		chomp $line;
		if ($line =~ /^(\w+):$/) {
			$category1 = $1;
			$category2 = "";
		} elsif ($line =~ /^\t(\w+):$/) {
			$category2 = "_$1";
		} elsif ($category1.$category2 ~~ @pref_att) {
			$line =~ /([\w\.]+)/;
			$prefs{$category1.$category2} = $&;
			#print "category: $category1${category2}->$&\n";
		} elsif ($category1 eq 'hair_colours') {
			$line =~ /(\w+)/;
			push @hairs, $&;
		}
	}

	#=====insert into user table=====
	$users{"name"} =~ /(\w+) ?(\w*)/;
	my $f_name 	= $1 || "";
	my $l_name 	= $2 || "";
	my $gender 	= $users{"gender"} || "";
	my $dob 	= $users{"birthdate"} || "";
	$dob =~ /(\d+)\/(\d+)\/(\d+)/;
	my $year	= $1;
	my $month	= $2;
	my $day		= $3;
	my $email	= $users{"email"} || "";
	my $hair	= $users{"hair_colour"} || "";
	my $degree	= $users{"degree"} || "";
	my $height	= $users{"height"} || "";
	$height =~ s/[^\d]//g;
	my $weight	= $users{"weight"} || "";
	$weight =~ s/[^\d]//g;
	my $u_name	= $users{"username"} || "";
	my $pass	= $users{"password"} || "";
	my $pref_age_min = $prefs{"age_min"} || "";
	my $pref_age_max = $prefs{"age_max"} || "";
	my $pref_height_min = $prefs{"height_min"} || "";
	if ($pref_height_min) {
		$pref_height_min =~ s/m//g;
		$pref_height_min = int($pref_height_min)*100;
	}
	my $pref_height_max = $prefs{"height_max"} || "";
	if ($pref_height_max) {
		$pref_height_max =~ s/m//g;
		$pref_height_max = int($pref_height_max)*100;
	}
	my $pref_weight_min = $prefs{"weight_min"} || "";
	$pref_weight_min =~ s/[^\d]//g;
	my $pref_weight_max = $prefs{"weight_max"} || "";
	$pref_weight_max =~ s/[^\d]//g;
	my $pref_gender = $prefs{"gender_"} || "";
	my $pref_hair_colours = join (' ',@hairs) || "";
	 
	my $sql_insert_users = "INSERT INTO USERS('FIRST_NAME','LAST_NAME','GENDER','YEAR','MONTH','DAY','EMAIL','HAIR_COLOUR','DEGREE','HEIGHT','WEIGHT','USERNAME','PASSWORD','PREF_GENDER','PREF_HAIR','PREF_AGE_MIN','PREF_AGE_MAX','PREF_HEIGHT_MIN','PREF_HEIGHT_MAX','PREF_WEIGHT_MIN','PREF_WEIGHT_MAX')
								VALUES ('$f_name','$l_name','$gender','$year','$month','$day','$email','$hair','$degree','$height','$weight','$u_name','$pass','$pref_gender','$pref_hair_colours','$pref_age_min','$pref_age_max','$pref_height_min','$pref_height_max','$pref_weight_min','$pref_weight_max')";
	#print "$sql_insert_users\n";
	$sth = $dbh->prepare($sql_insert_users);
	$sth->execute or die "SQL Error: $DBI::errstr\n";	

	#=====insert into user_courses table=====
	foreach $i (0..$#user_courses_course_code) {
		my $course_code	= $user_courses_course_code[$i] || "";
		my $year		= $user_courses_year[$i] || "";
		my $semester	= $user_courses_semester[$i] || "";
		my $sql_insert_users_courses = "INSERT INTO USER_COURSES VALUES('$course_code','$year','$semester','$id')";
		#print "$sql_insert_users_courses\n";
		$sth = $dbh->prepare($sql_insert_users_courses);
		$sth->execute or die "SQL Error: $DBI::errstr\n";	
	}

	#=====insert into user_favouties table=====
	foreach $key (keys %favourites) {
		my $type	= $favourites{$key} || "";
	  (my $name		= $key) =~ s/'/''/g;
		my $sql_insert_users_favourites = "INSERT INTO USER_FAVOURITES VALUES('$id','$type','$name')";
		#print "$sql_insert_users_favourites\n";
		$sth = $dbh->prepare($sql_insert_users_favourites);
		$sth->execute or die "SQL Error: $DBI::errstr\n";	
	}

	$id += 1;
}
#---close connection to db---
$dbh->disconnect();
