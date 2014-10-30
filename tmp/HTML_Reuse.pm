#!/usr/bin/perl

package HTML_Reuse;
use Exporter 'import';
our @EXPORT = qw/page_header page_trailer $active_user %cookies make_active fetch_cookies main_forms/;

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI::Cookie;
use Data::Dumper;  
warningsToBrowser(1);

our %cookies;

sub fetch_cookies
{
	%cookies = fetch CGI::Cookie;
}

sub page_header
{
	print header,"
	
	<html>
	<head>
	 <title>LOVE2041</title>
	 <link rel=\"stylesheet\" type=\"text/css\" href=\"assets/love2041.css\">
	 <link rel=\"stylesheet\" type=\"text/css\" href=\"assets/css/buttons.css\">
	</head>";
}

sub page_trailer {
	my $html = "\n";
	$html .= join("", map("<!-- $_=".param($_)." -->\n", param()));# if $debug;
	$html .= end_html;
	print p, $html;
}

sub main_forms
{
	print div({-id=>'headSpace'},h1('Welcome to LOVE2041'));
	
	if 	(defined $cookies{'active_user'}) {
	printf	div({-id=>'navigationBar'},
				p("Logged in as %s"),
				start_form, "\n",
				a({-href=>'love2041.cgi',-class=>"button button-rounded button-action buttonWidth"},'Home'),"\n",
				a({-href=>'page_browse_users.cgi?Display_Page=0',-class=>"button button-rounded button-action buttonWidth"},'Browse'),"\n",
				a({-href=>'page_browse_matches.cgi?Display_Page=0',-class=>"button button-rounded button-action buttonWidth"},'Browse Matches'),"\n",
				a({-href=>'page_sign_up.cgi',-class=>"button button-rounded button-action buttonWidth"},'Sign Up'),"\n",
				a({-href=>'page_login.cgi',-class=>"button button-rounded button-action buttonWidth"},'Login'),"\n",
				a({-href=>'page_search_users.cgi',-class=>"button button-rounded button-action buttonWidth"},'Search'),"\n",
				a({-href=>"page_display_user.cgi?Display_User\=%s",-class=>"button button-rounded button-action buttonWidth"},'My Profile'),"\n",
				end_form, "\n",
			),$cookies{'active_user'}->value,$cookies{'active_user'}->value;
	} else {
	print	div({-id=>'navigationBar'},
				start_form, "\n",
				a({-href=>'love2041.cgi',-class=>"button button-rounded button-action buttonWidth"},'Home'),"\n",
				a({-href=>'page_browse_users.cgi?Display_Page=0',-class=>"button button-rounded button-action buttonWidth"},'Browse'),"\n",
				a({-href=>'page_sign_up.cgi',-class=>"button button-rounded button-action buttonWidth"},'Sign Up'),"\n",
				a({-href=>'page_login.cgi',-class=>"button button-rounded button-action buttonWidth"},'Login'),"\n",
				a({-href=>'page_search_users.cgi',-class=>"button button-rounded button-action buttonWidth"},'Search'),"\n",
				end_form, "\n",
			);		
	}	
}

return 1;
