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

page_header();
browse_users_page($page);
page_trailer();
exit 0;	
#========================


sub browse_users_page
{

#.........Courses Table..............
my $sql_table = "DROP TABLE IF EXISTS MATCHES";
$sth = $dbh->prepare($sql_table);
$sth->execute or die "SQL Error: $DBI::errstr\n";


my $sql_make_user_courses = "
	CREATE TABLE IF NOT EXISTS MATCHES(
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

#========get my info==============
	my $username = %cookies{'active_user'}->value;
	$sth = $dbh->prepare("SELECT * FROM USERS WHERE USERNAME = ?");
	$sth->execute($username) or die "SQL Error: $DBI::errstr\n";	
	
	my %me;
	@me_info = $sth->fetchrow_array) {
	#===create user hash===
	$me{"User ID"} 		= $me_info[0];
	$me{"First Name"} 	= $me_info[1];
	$me{"Last Name"} 	= $me_info[2];
	$me{"Gender"} 		= $me_info[3];
	$me{"Year"}			= $me_info[4];
	$me{"Month"}		= $me_info[5];
	$me{"Day"}			= $me_info[6];
	$me{"Email"} 		= $me_info[7];
	$me{"Hair Colour"} 	= $me_info[8];
	$me{"Degree"} 		= $me_info[9];
	$me{"Height"} 		= $me_info[10];
	$me{"Weight"} 		= $me_info[11];
	$me{"Username"} 	= $me_info[12];
	$me{"Password"} 	= $me_info[13];
	$me("Pref Gender"}	= $me_info[14];
	$me("Pref Hair"}	= $me_info[14];
	$me("Pref Age Min"}	= $me_info[14];
	$me("Pref Age Max"}	= $me_info[14];
	$me("Pref Height Min"}	= $me_info[14];
	$me("Pref Height Max"}	= $me_info[14];
	$me("Pref Weight Min"}	= $me_info[14];
	$me("Pref Weight Max"}	= $me_info[14];
	
	
#========get my info==============

	#===get the user info===
	$sth = $dbh->prepare("SELECT * FROM USERS LIMIT 10 OFFSET ?");
	$sth->execute($page*10) or die "SQL Error: $DBI::errstr\n";	

	my %users;
	my @profiles;
	my @fields = ('Username','Height','Weight','Hair Colour','Degree');
	while (my @user_info = $sth->fetchrow_array) {
		#===create user hash===
		$users{"User ID"} 		= $user_info[0];
		$users{"First Name"} 	= $user_info[1];
		$users{"Last Name"} 	= $user_info[2];
		$users{"Gender"} 		= $user_info[3];
		$users{"Year"}			= $user_info[4];
		$users{"Month"}			= $user_info[5];
		$users{"Day"}			= $user_info[6];
		$users{"Email"} 		= $user_info[7];
		$users{"Hair Colour"} 	= $user_info[8];
		$users{"Degree"} 		= $user_info[9];
		$users{"Height"} 		= $user_info[10];
		$users{"Weight"} 		= $user_info[11];
		$users{"Username"} 		= $user_info[12];
		$users{"Password"} 		= $user_info[13];

		$user_link = "page_display_user.cgi?Display_User\=$users{\"Username\"}";
		push @profiles, a({-href=>"$user_link",-class=>'profile'},
							div({-class=>'.browseprofile'},
								(img {src=>"students/$users{'Username'}/profile.jpg",align=>'LEFT'},"\n", map {p("$_: $users{$_}")} @fields)
							)
						)
	}
	
#========displat page==============	
	my $page;
	($page) = (@_);
	
	main_forms();
	print	div({-id=>'profileSection'},
				prev_next_form($page),
				@profiles,
				prev_next_form($page)
			);
}

sub prev_next_form
{
	my $page_num;
	($page_num) = (@_);
	if ($page_num > 0) {
		return 	start_form, "\n",
				hidden('Display_Page',$page_num),"\n",
				hidden('Browse', 'Browse'),"\n",
				submit({-class=>"button button-rounded button-action buttonWidth",-name=>'Previous',-value=>'Previous'}),"\n",
				submit({-class=>"button button-rounded button-action buttonWidth",-name=>'Next',-value=>'Next'}),"\n",
				end_form;
	} else {
		return 	start_form, "\n",
				hidden('Display_Page',$page_num),"\n",
				hidden('Browse', 'Browse'),"\n",
				submit({-class=>"button button-rounded button-action buttonWidth",-name=>'Next',-value=>'Next'}),"\n",
				end_form;
	}
}
