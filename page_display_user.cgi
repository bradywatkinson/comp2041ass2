#!/usr/bin/perl

use HTML_Reuse;
use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
warningsToBrowser(1);

use DBI;

$dbh = DBI->connect('dbi:SQLite:database/love2041_DB', 'root', 'password') or die;


#===actual execution=====
fetch_cookies();
page_header();
single_user();
page_trailer();
exit 0;	
#========================


sub single_user
{


	#===========Get all the data we need to make the page==============
	my $user_name = param('Display_User');

	if (defined $cookies{'active_user'}) {
		if ($cookies{'active_user'}->value == $user_name) {
			$active = 1;
		}
	}
	
	#===get the user info===
	$sth = $dbh->prepare("SELECT * FROM USERS WHERE USERNAME = ?");
	$sth->execute($user_name) or die "SQL Error: $DBI::errstr\n";	
	my @user_info = $sth->fetchrow_array();	
	
	#===create user hash===
	my %me_user;
	$me_user{"User ID"} 		= $user_info[0];
	$me_user{"First Name"} 		= $user_info[1];
	$me_user{"Last Name"} 		= $user_info[2];
	$me_user{"Gender"} 			= $user_info[3];
	$me_user{"Year"}		 	= $user_info[4];
	$me_user{"Month"}			= $user_info[5];
	$me_user{"Day"}				= $user_info[6];
	$me_user{"Email"} 			= $user_info[7];
	$me_user{"Hair Colour"} 	= $user_info[8];
	$me_user{"Degree"} 			= $user_info[9];
	$me_user{"Height"} 			= $user_info[10];
	$me_user{"Weight"} 			= $user_info[11];
	$me_user{"Username"} 		= $user_info[12];
	$me_user{"Password"} 		= $user_info[13];
	$me_user{"Pref Gender"}		= $user_info[14];
	$me_user{"Pref Hair"}		= $user_info[15];
	$me_user{"Pref Age Min"}	= $user_info[16];
	$me_user{"Pref Age Max"}	= $user_info[17];
	$me_user{"Pref Height Min"}	= $user_info[18];
	$me_user{"Pref Height Max"}	= $user_info[19];
	$me_user{"Pref Weight Min"}	= $user_info[20];
	$me_user{"Pref Weight Max"}	= $user_info[21];
	$me_user{"About Me"}		= $user_info[22];
	
	#===get the user courses===
	$sth = $dbh->prepare('SELECT * FROM USER_COURSES WHERE USER_ID = ?');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";		
	#my $courses = "";
	my @courses;
	while (my @row_courses = $sth->fetchrow_array) {
		#$courses .= "@row"."\n";
		push @courses, p("@row_courses");
	}
	$user{"Courses"} = "@courses";

	#===get the user favourites===
	#===get bands===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_bands"');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	#my $courses = "";
	my @fbands;
	while (my @row_1 = $sth->fetchrow_array) {
		push @fbands, " ".li("@row_1[2]")."\n";
	}
	$user{"Favourite Bands"} = "@fbands";
	
	#===get hobbies===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_hobbies"');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	#my $courses = "";
	my @fhobs;
	while (my @row_2 = $sth->fetchrow_array) {
		push @fhobs, " ".li("@row_2[2]")."\n";
	}
	$user{"Favourite Hobbies"} = "@fhobs";
	
	#===get TV===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_TV_shows"');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	#my $courses = "";
	my @ftv;
	while (my @row_3 = $sth->fetchrow_array) {
		push @ftv, " ".li("@row_3[2]")."\n";
	}
	$user{"Favourite TV Shows"} = "@ftv";
	
	#===get movies===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_movies"');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	#my $courses = "";
	my @fmovies;
	while (my @row_4 = $sth->fetchrow_array) {
		push @fmovies, " ".li("@row_4[2]")."\n";
	}
	$user{"Favourite Movies"} = "@fmovies";

	if ($active) {
		my @fields = ('Degree','Gender','Height','Hair Colour','Favourite Bands','Favourite Hobbies','Favourite TV Shows','Favourite Movies');
		my @fields_out = map {h3("$_").p($user{$_} || "Not Supplied").textfield("$_","0")."\n"} @fields;
	} else {
		my @fields = ('Degree','Gender','Height','Hair Colour','Favourite Bands','Favourite Hobbies','Favourite TV Shows','Favourite Movies');
		my @fields_out = map {h3("$_").p($user{$_} || "Not Supplied")."\n"} @fields;
	}

	#==================Now Make the Page================================

	if ($active) {
		main_forms();
		print	div({-id=>'centreDoc'},
					h2($user{"Username"}), "\n",
					start_form, "\n",
					p({align=>'CENTRE'}, img {src=>"database/students/$user{'Username'}/profile.jpg"}, "\n"),
					"@fields_out",
					submit({-class=>"button button-rounded button-action buttonWidth",-name=>'Update',-value=>'Update'}),"\n",
					end_form, "\n",
					p, "\n"
				);
	} else {
		main_forms();
		print	div({-id=>'centreDoc'},
					h2($user{"Username"}), "\n",
					p({align=>'CENTRE'}, img {src=>"students/$user{'Username'}/profile.jpg"}, "\n"),
					"@fields_out",
					p, "\n"
				);
	}
}

sub update_user
{
	
}
