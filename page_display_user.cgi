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

	my $active = -1;
	if (defined $cookies{'active_user'}) {
		if ($cookies{'active_user'}->value eq $user_name) {
			$active = 1;
		}
	}
	
	my $me_id = param('User_ID');
	
	update_user($me_id) if (defined param('Update'));
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
	my @courses;
	while (my @row_courses = $sth->fetchrow_array) {
		push @courses, p("@row_courses");
	}
	$me_user{"Courses"} = "@courses";

	#===get the user favourites===
	#===get bands===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_bands"');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	#my $courses = "";
	my @fbands;
	while (my @row_1 = $sth->fetchrow_array) {
		push @fbands, " ".li("@row_1[2]")."\n";
	}
	$me_user{"Favourite Bands"} = "@fbands";
	
	#===get hobbies===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_hobbies"');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	my @fhobs;
	while (my @row_2 = $sth->fetchrow_array) {
		push @fhobs, " ".li("@row_2[2]")."\n";
	}
	$me_user{"Favourite Hobbies"} = "@fhobs";
	
	#===get TV===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_TV_shows"');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	my @ftv;
	while (my @row_3 = $sth->fetchrow_array) {
		push @ftv, " ".li("@row_3[2]")."\n";
	}
	$me_user{"Favourite TV Shows"} = "@ftv";
	
	#===get movies===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_movies"');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	my @fmovies;
	while (my @row_4 = $sth->fetchrow_array) {
		push @fmovies, " ".li("@row_4[2]")."\n";
	}
	$me_user{"Favourite Movies"} = "@fmovies";
	
	#===get books===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_books"');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	my @fmovies;
	while (my @row_5 = $sth->fetchrow_array) {
		push @fbooks, " ".li("@row_5[2]")."\n";
	}
	$me_user{"Favourite Books"} = "@fbooks";

	my @fields;
	my @fields_out;
	
	if ($active == 1) {
		@fields = ('About Me','First Name','Last Name','Email','Password','Degree','Height','Weight','Hair Colour','Favourite Bands','Favourite Hobbies','Favourite TV Shows','Favourite Movies','Favourite Books',
						'Pref Gender','Pref Hair','Pref Age Min','Pref Age Max','Pref Height Min','Pref Height Max','Pref Weight Min','Pref Weight Max');
		@fields_out = map {h3("$_").p($me_user{$_} || "Not Supplied").p(input({-type=>'text',-pattern=>'\w+',-name=>$_,-value=>'0'}))."\n"} @fields;
	} else {
		@fields = ('About Me','Degree','Gender','Height','Hair Colour','Favourite Bands','Favourite Hobbies','Favourite TV Shows','Favourite Movies','Favourite Books');
		@fields_out = map {h3("$_").p($me_user{$_} || "Not Supplied")."\n"} @fields;
	}

	#==================Now Make the Page================================

	if ($active == 1) {
		main_forms();
		print	div({-id=>'centreDoc'},
					h2($user{"Username"}), "\n",
					start_form, "\n",
					hidden('Display_User', $user_name),"\n",
					hidden('User_ID',$me_user{"User ID"}),"\n",
					submit({-class=>"button button-rounded button-action buttonWidth",-name=>'Update',-value=>'Update'}),"\n",
					p({align=>'centre'}, img {src=>"database/students/$me_user{'Username'}/profile.jpg"}, "\n"),
					"@fields_out","\n",p,
					submit({-class=>"button button-rounded button-action buttonWidth",-name=>'Update',-value=>'Update'}),"\n",
					end_form, "\n",
					p, "\n"
				);
	} else {
		main_forms();
		print	div({-id=>'centreDoc'},
					h2($user{"Username"}), "\n",
					p({align=>'CENTRE'}, img {src=>"database/students/$me_user{'Username'}/profile.jpg"}, "\n"),
					start_form, "\n",
					#p,a({-href=>'page_messages_user.cgi?Display_User='.$me_user{"Username"},-class=>"button button-rounded button-action buttonWidth"},'Message'),"\n",
					end_form, "\n",
					"@fields_out",
					p, "\n"
				);
	}
}

sub update_user
{
	$user = $_[0];
	
	my @updates;
	@fields = ('About Me','First Name','Last Name','Email','Password','Degree','Height','Weight','Hair Colour',
						'Pref Gender','Pref Hair','Pref Age Min','Pref Age Max','Pref Height Min','Pref Height Max','Pref Weight Min','Pref Weight Max');
	foreach $param (param()) {
		if ($param ~~ @fields && param($param) ne '0') {
			my $tmp = param($param);
			$param =~ tr/a-z /A-Z_/;
			push @updates, "$param = '$tmp'";
		}
	}
	
	if (@updates) {
		my $sql = "UPDATE USERS SET ".join (', ',@updates)." WHERE USER_ID = $user";
		#print "$sql\n";
		my $rv = $dbh->do($sql) or die $DBI::errstr;
		print $DBI::errstr if( $rv < 0 );
	}
	
	my @favs = ('Favourite Bands','Favourite Hobbies','Favourite TV Shows','Favourite Movies','Favourite Books');
	
	foreach $fav (@favs) {
		if (param($fav) ne '0') {
			my $name = param($fav);
			$name =~ s/'/''/g;
			$name =~ s/"/""/g;
			$name =~ s/[^\"\'\w\d\s]//;
			$fav =~ tr/FMSHB /fmshb_/;

			my $sql_insert_users_favourites = "INSERT INTO USER_FAVOURITES VALUES('$user','$fav','$name')";
			#print p($sql_insert_users_favourites);
			$sth = $dbh->prepare($sql_insert_users_favourites);
			$sth->execute or die "SQL Error: $DBI::errstr\n";	
		}
	}
}
