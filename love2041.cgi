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
