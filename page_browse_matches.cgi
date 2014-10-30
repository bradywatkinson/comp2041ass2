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

my $page = param('Display_Page') || 0;
$page += 1 if defined(param('Next'));
$page -= 1 if defined(param('Previous'));
param('Display_Page',$page);
#make_matches();
page_header();
browse_matches($page);
page_trailer();
exit 0;	
#========================


sub make_matches
{
#=============================make matches table================================
	my $sql_drop_user_favourites = "DROP TABLE IF EXISTS MATCHES";
	$sth = $dbh->prepare($sql_drop_user_favourites);
	$sth->execute or die "SQL Error: $DBI::errstr\n";

	my $sql_make_user_favourites = "
		CREATE TABLE IF NOT EXISTS MATCHES(
		USER_ID         TEXT,
		USERNAME		TEXT,
		GENDER 			CHAR(1), 
		HAIR_COLOUR 	TEXT,
		DEGREE 			TEXT, 
		HEIGHT 			TEXT, 
		WEIGHT 			TEXT, 
		SCORE			TEXT,
		FOREIGN KEY(USER_ID)
			REFERENCES USERS(USER_ID)
			ON DELETE CASCADE
		PRIMARY KEY(USER_ID))";
	$sth = $dbh->prepare($sql_make_user_favourites);
	$sth->execute or die "SQL Error: $DBI::errstr\n";
#=============================get the user info==================================
	#$user_name = $cookies{'active_user'}->value;
	$user_name = 'AwesomeGenius60';
	
	$sth = $dbh->prepare("SELECT * FROM USERS WHERE USERNAME = ?");
	$sth->execute($user_name) or die "SQL Error: $DBI::errstr\n";	
	my @user_info = $sth->fetchrow_array();	
	
	my @me_courses;
	my @me_favs;
	
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
	
	@pref = ('Pref Gender','Pref Hair','Pref Age Min','Pref Age Max','Pref Height Min','Pref Height Max','Pref Weight Min','Pref Weight Max');
	
	@prefs = map {p("$_->$me_user{$_}"),"\n"} @pref;
	
	#print p("making matches for $me_user{'Username'}"),"\n",@prefs;
	@want_hair = split '', $me_user{"Pref Hair"};
		
	#===get the me courses===
	$sth = $dbh->prepare('SELECT * FROM USER_COURSES WHERE USER_ID = ?');
	$sth->execute($user_name) or die "SQL Error: $DBI::errstr\n";		
	while (my @row = $sth->fetchrow_array) {
		push @me_courses, $row[0];
	}
	
	#===get the me favourites===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_bands"');
	$sth->execute($user_name) or die "SQL Error: $DBI::errstr\n";	
	while (my @row = $sth->fetchrow_array) {
		push @me_favs, $row[2];
	}
#=============================get the matchees info==================================
	$sth2 = $dbh->prepare("SELECT * FROM USERS");
	$sth2->execute() or die "SQL Error: $DBI::errstr\n";	

	my %users;
	while (my @rows = $sth2->fetchrow_array) {
		
		$score = 0;
		
		#===create user hash===
		$users{"User ID"} 		= $rows[0] || "Not Supplied";
		$users{"Gender"} 		= $rows[3] || "Not Supplied";
		$users{"Email"} 		= $rows[5] || "Not Supplied";
		$users{"Hair Colour"} 	= $rows[8] || "Not Supplied";
		$users{"Degree"} 		= $rows[9] || "Not Supplied";
		$users{"Height"} 		= $rows[10] || "Not Supplied";
		$users{"Weight"} 		= $rows[11] || "Not Supplied";
		$users{"Username"} 		= $rows[12] || "Not Supplied";

		$socre += 50 if ($users{'Gender'} == $me_user{'Pref Gender'});
		$score += 7  if ($users{'Hair Colour'} ~~ @want_hair);
		$score += 15 if ($users{'Age'} > $me_user{'Pref Age Min'} and $users{'Age'} < $me_user{'Pref Age Max'});
		$score += 12 if ($users{'Height'} > $me_user{'Pref Height Min'} and $users{'Height'} < $me_user{'Pref Height Max'});
		$score += 8  if ($users{'Weight'} > $me_user{'Pref Weight Min'} and $users{'Weight'} < $me_user{'Pref Weight Max'});;

		#===get the user courses===
		$sth = $dbh->prepare('SELECT * FROM USER_COURSES WHERE USER_ID = ?');
		$sth->execute($users{"User ID"}) or die "SQL Error: $DBI::errstr\n";		
		while (my @row_c = $sth->fetchrow_array) {
			$score++ if (@row_c[0] ~~ @me_courses);
		}

		#===get the user favourites===
		$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ?');
		$sth->execute($users{"User ID"}) or die "SQL Error: $DBI::errstr\n";	
		while (my @row_f = $sth->fetchrow_array) {
			$score++ if (@row_f[2] ~~ @me_favs);
		}
#===========================insert into matches==================================
		$mid		= $users{"User ID"};
		$mname 		= $users{"Username"};
		$mgender 	= $users{"Gender"};
		$mhair		= $users{"Hair Colour"};
		$mdegree	= $users{"Degree"};
		$mheight	= $users{"Height"};
		$mweight	= $users{"Weight"};
		
		#print "$users{\"Username\"}->$score","\n";
		
		my $sql_insert_users = "INSERT INTO MATCHES	VALUES ('$mid','$mname','$mgender','$mhair','$mdegree','$mheight','$mweight','$score')";
		#print p("$sql_insert_users\n");
		$sth = $dbh->prepare($sql_insert_users);
		$sth->execute or die "SQL Error: $DBI::errstr\n";		
	}
}

sub browse_matches
{
#=============================Browse==================================
	my $matches = 0;
	if (defined param('matches') and param('matches') == 1) {
		$matches = param('matches');
	} else {
		$matches = 1;
		make_matches();
	}
	
	my $page;
	($page) = (@_);
	#===get the user info===
	$sth = $dbh->prepare("SELECT * FROM MATCHES ORDER BY SCORE DESC LIMIT 10 OFFSET ?");
	$sth->execute($page) or die "SQL Error: $DBI::errstr\n";	

	my %users;
	my @profiles;
	my @fields = ('Username','Height','Weight','Hair Colour','Degree','Score');
	while (my @user_info = $sth->fetchrow_array) {
		#===create user hash===
		$users{"User ID"} 		= $user_info[0];
		$users{"Username"} 		= $user_info[1];
		$users{"Gender"} 		= $user_info[2];
		$users{"Hair Colour"} 	= $user_info[3];
		$users{"Degree"} 		= $user_info[4];
		$users{"Height"} 		= $user_info[5];
		$users{"Weight"} 		= $user_info[6];
		$users{"Score"} 		= $user_info[7];

		$user_link = "page_display_user.cgi?Display_User\=$users{\"Username\"}";
		push @profiles, a({-href=>"$user_link",-class=>'profile'},
							div({-class=>'.browseprofile'},
								(img {src=>"database/students/$users{'Username'}/profile.jpg",align=>'LEFT'},"\n", map {p("$_: $users{$_}")} @fields)
							)
						)
	}
	
	main_forms();
	print	div({-id=>'profileSection'},
				prev_next_forms($page, $matches),
				@profiles,
				prev_next_forms($page, $matches)
			);
}

sub prev_next_forms
{
	my $page_num;
	($page_num, $matches) = (@_);
	if ($page_num > 0) {
		return 	start_form, "\n",
				hidden('matches',$matches),"\n",
				hidden('Display_Page',$page_num),"\n",
				hidden('Browse', 'check'),"\n",
				submit({-class=>"button button-rounded button-action buttonWidth",-name=>'Previous',-value=>'Previous'}),"\n",
				submit({-class=>"button button-rounded button-action buttonWidth",-name=>'Next',-value=>'Next'}),"\n",
				end_form;
	} else {
		return 	start_form, "\n",
				hidden('matches',$matches),"\n",
				hidden('Display_Page',$page_num),"\n",
				hidden('Browse', 'Browse'),"\n",
				submit({-class=>"button button-rounded button-action buttonWidth",-name=>'Next',-value=>'Next'}),"\n",
				end_form;
	}
}
