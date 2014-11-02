#!/usr/bin/perl

use HTML_Reuse;
use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;
use CGI::Cookie;
use List::Util qw/min max/;
warningsToBrowser(1);

use DBI;

$dbh = DBI->connect('dbi:SQLite:database/love2041_DB', 'root', 'password') or die;

#===actual execution=====
fetch_cookies();
if (defined param('Log_Out')) {
	log_out_header();
} else {
	page_header();
}
landing_page();
page_trailer();
exit 0;	
#========================


#======Functions========

sub landing_page
{

	main_forms();
	print	div({-id=>'centreDoc'},
				p('With a proven match record, find love with LOVE2041'),"\n",				
			);
}

sub log_out_header
{
	$cookie = cookie(-value=>'',-expires=>'-1d');
    print header(-cookie=>"active_user=$cookie"),"
			<html>
			<head>
			 <title>LOVE2041</title>
			 <link rel=\"stylesheet\" type=\"text/css\" href=\"assets/love2041.css\">
			 <link rel=\"stylesheet\" type=\"text/css\" href=\"assets/buttons.css\">
			 <!-- logged out-->
			</head>";
	print p($cookie);
}
