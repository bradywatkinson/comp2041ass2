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
	my $sql_drop_messages = "DROP TABLE IF EXISTS MESSAGES";
	$sth = $dbh->prepare($sql_drop_messages);
	$sth->execute or die "SQL Error: $DBI::errstr\n";

	my $sql_make_messages = "
		CREATE TABLE IF NOT EXISTS MESSAGES(
		MESSAGE_ID	INTEGER PRIMARY KEY AUTOINCREMENT,
		GIVE_ID 	TEXT, 
		GET_ID 		TEXT,
		MESSAGE		TEXT,
		SEND_TIME	DATETIME)";
	$sth = $dbh->prepare($sql_make_messages);
	$sth->execute or die "SQL Error: $DBI::errstr\n";

	my $get_id = param('Display_User');
	
	my $active = -1;
	if (defined $cookies{'active_user'}) {
		$give_id = $cookies{'active_user'}->value;
		$active = 1;
	}

	$sth = $dbh->prepare('SELECT * FROM MESSAGES WHERE GIVE_ID = ? AND GET_ID = ? ORDER BY MESSAGE_ID');
	$sth->execute($give_id, $get_id) or die "SQL Error: $DBI::errstr\n";
			
	while (my @row = $sth->fetchrow_array) {
		push @messages, $row[3];
	}
	$me_user{"Courses"} = "@courses";

	main_forms();
	print	div({-id=>'centreDoc'},
				start_form, "\n",
				@prev_messages;
				end_form, "\n"
			);
}

sub make_message
{
	my $sql = "INSERT INTO MESSAGES VALUES('','','',datetime('now','localtime'))";
}
