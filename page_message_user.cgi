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
page_header();
message_page();
page_trailer();
exit 0;	
#========================


#======Functions========

sub message_page
{
	my $user_name = param('Display_User');

	main_forms();
	print	div({-id=>'centreDoc'},
				start_form, "\n",
				@prev_messages;
				end_form, "\n"
			);
}
