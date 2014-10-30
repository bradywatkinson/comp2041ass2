#!/usr/bin/perl

use HTML_Reuse;
use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI::Cookie;
use Data::Dumper;  
use List::Util qw/min max/;
warningsToBrowser(1);

use DBI;


$dbh = DBI->connect('dbi:SQLite:database/love2041_DB', 'root', 'password') or die;

my $authenticated;
my $user_n;

#===actual execution=====

fetch_cookies();
if (param('Login')) {
	process_login();
}

if ($authenticated == 1) {
	page_header_new_cookie();
	authen_page_g();
} elsif ($authenticated == -1) {
	page_header();
	authen_page_b();
} else {
	page_header();
	login_page();
}

page_trailer();
exit 0;	
#========================

sub process_login
{
	#===========Get all the data we need to make the page==============
	my $user_name = param('Username');
	
	#===get the user info===
	$sth = $dbh->prepare("SELECT * FROM USERS WHERE USERNAME = ?");
	$sth->execute($user_name) or die "SQL Error: $DBI::errstr\n";	
	my @user_info = $sth->fetchrow_array();

	my %user;
	$user{"User ID"}  = $user_info[0];
	$user{"Username"} = $user_info[12];
	$user{"Password"} = $user_info[13];
	if (defined $user{"Username"} and param('Password') eq $user{"Password"}) {
		$authenticated = 1;
		$user_n = $user{"Username"};
	} else {
		$authenticated  = -1;
	}
}


sub login_page
{

	#==================Now Make the Page================================

	main_forms();
	print	div({-id=>'centreDoc'},
				start_form, "\n",
				hidden('Make_User','1'),"\n",
				fieldset({},
					legend("Login"),
					table({-cellpadding=>'3'},
						Tr(td({-width=>$table_width},"Username: ".td(textfield("Username","",20,20)))."\n"),
						Tr(td({-width=>$table_width,-type=>"password"},"Password: ".td(textfield("Password","",20,20)))."\n"),
					)
				), "\n",
				submit({-class=>"button button-rounded button-action buttonWidth",-name=>'Login',-value=>'Login'},'Login'),"\n",
				a({-href=>'love2041.cgi',-class=>"button button-rounded button-action buttonWidth"},'Cancel'),"\n",
				end_form
			);
}

sub authen_page_g
{
	main_forms();
	print div({-id=>'centreDoc'},
				h2("Welcome Back $user_m!")
			);
}

sub authen_page_b
{
	main_forms();
	print	div({-id=>'centreDoc'},
				h2("Username/Password combination not recognised")
			);
}

sub page_header_new_cookie
{
	print 	header(-cookie=>"active_user=$user_n"),"
			<html>
			<head>
			 <title>LOVE2041</title>
			 <link rel=\"stylesheet\" type=\"text/css\" href=\"assets/love2041.css\">
			 <link rel=\"stylesheet\" type=\"text/css\" href=\"assets/css/buttons.css\">
			 <!-- $active_user-->
			</head>";
}
