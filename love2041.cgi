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
welcome_page();
page_trailer();
exit 0;	
#========================

sub welcome_page
{
	main_forms();
	print	div({-id=>'centreDoc'},
				h2('With a proven match record, join love2041!'),"\n",				
			);
}
