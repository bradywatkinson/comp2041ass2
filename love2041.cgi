#!/usr/bin/perl

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
warningsToBrowser(1);

use DBI;

$dbh = DBI->connect('dbi:SQLite:database/love2041_DB', 'root', 'password') or die;


#===actual execution=====
page_header();
serve_page();
page_trailer();
exit 0;	
#========================


#======Functions========
sub serve_page
{
	if (defined param("Home")) {
		landing_page();
	} elsif (defined param('Browse') or defined param('Next Student')) {
		$n = param('n');
		param('n',$n+1);
		nice_browse($n);
	} else {
		landing_page();
	}
}


sub page_header
{
print "Content-type: text/html

<html>
<head>
 <title>LOVE2041</title>
 <link rel=\"stylesheet\" type=\"text/css\" href=\"assets/love2041.css\">
 <link rel=\"stylesheet\" type=\"text/css\" href=\"assets/css/buttons.css\">
</head>"
}

#
# HTML placed at bottom of every screen
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
	my $html = "";
	$html .= join("", map("<!-- $_=".param($_)." -->\n", param()));# if $debug;
	$html .= end_html;
	print p, $html;
}

sub landing_page
{
	print 		div({-id=>'head_space'},h1('Welcome to LOVE2041')), "\n",
			div({-id=>'centreDoc'},
				start_form, "\n",
				hidden('n', '-1'),"\n",
				a(submit({-class=>"button button-pill button-action",-name=>'Login',-value=>'Login'})),"\n",
				a(submit({-class=>"button button-pill button-action",-name=>'Register',-value=>'Register'})),"\n",
				a(submit({-class=>"button button-pill button-action",-name=>'Browse',-value=>'Browse'})),"\n",
				#a(submit({-class=>"button button-pill button-action",-name=>'Nice',-value=>'Nice'})),"\n",
				end_form, "\n",
				p('With a proven match record, find love with LOVE2041'),"\n",
			);
}

sub nice_browse
{

	#===========Get all the data we need to make the page==============
	my $nstu;
	($nstu) = (@_);
	#===get the user info===
	$sth = $dbh->prepare("SELECT * FROM USERS LIMIT 1 OFFSET ?");
	$sth->execute($nstu) or die "SQL Error: $DBI::errstr\n";	
	my @user_info = $sth->fetchrow_array();	
	
	#===create user hash===
	my %user;
	$user{"Student Number"} = $nstu+2;
	$user{"User ID"} = $user_info[0];
	$user{"First Name"} = $user_info[1];
	$user{"Last Name"} = $user_info[2];
	$user{"Gender"} = $user_info[3];
	$user{"Date of Birth"} = $user_info[4];
	$user{"Email"} = $user_info[5];
	$user{"Hair Colour"} = $user_info[6];
	$user{"Degree"} = $user_info[7];
	$user{"Height"} = $user_info[8];
	$user{"Weight"} = $user_info[9];
	$user{"Username"} = $user_info[10];
	$user{"Password"} = $user_info[11];
	
	#===get the user courses===
	$sth = $dbh->prepare('SELECT * FROM USER_COURSES WHERE USER_ID = ?');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";		
	#my $courses = "";
	my @courses;
	while (my @row_courses = $sth->fetchrow_array) {
		#$courses .= "@row"."\n";
		push @courses, p("@row_courses");
	}
	$user{"Courses"} = "@courses";

	#===get the user favourites===
	#===get bands===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_bands"');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	#my $courses = "";
	my @fbands;
	while (my @row_1 = $sth->fetchrow_array) {
		push @fbands, " ".li("@row_1[2]")."\n";
	}
	$user{"Favourite Bands"} = "@fbands";
	
	#===get hobbies===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_hobbies"');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	#my $courses = "";
	my @fhobs;
	while (my @row_2 = $sth->fetchrow_array) {
		push @fhobs, " ".li("@row_2[2]")."\n";
	}
	$user{"Favourite Hobbies"} = "@fhobs";
	
	#===get TV===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_TV_shows"');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	#my $courses = "";
	my @ftv;
	while (my @row_3 = $sth->fetchrow_array) {
		push @ftv, " ".li("@row_3[2]")."\n";
	}
	$user{"Favourite TV Shows"} = "@ftv";
	
	#===get movies===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ? AND TYPE_ID = "favourite_movies"');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	#my $courses = "";
	my @fmovies;
	while (my @row_4 = $sth->fetchrow_array) {
		push @fmovies, " ".li("@row_4[2]")."\n";
	}
	$user{"Favourite Movies"} = "@fmovies";


	@fields = ('Gender','Height','Hair Colour','Favourite Bands','Favourite Hobbies','Favourite TV Shows','Favourite Movies');
	@fields_out = map {h3("$_").p($user{$_} || "Not Supplied")."\n"} @fields;

	#==================Now Make the Page================================

	print 	div({-id=>'head_space'},h1('LOVE2041')), "\n",
			div({-id=>'centreDoc'},
				start_form, "\n",
				hidden('n', $nstu),"\n",
				a(submit({-class=>"button button-pill button-action",-name=>'Next Student',-value=>'Next Student'})),"\n",
				a(submit({-class=>"button button-pill button-action",-name=>'Home',-value=>'Home'})),"\n",
				end_form, "\n",
				h2($user{"Username"}), "\n",
				"@fields_out",
				p, "\n"
			);
}



#==============================
#======OLD=====================
#==============================
sub browse_users
{
	my $nstu;
	($nstu) = (@_);
	#===get the user info===
	$sth = $dbh->prepare("SELECT * FROM USERS LIMIT 1 OFFSET ?");
	$sth->execute($nstu) or die "SQL Error: $DBI::errstr\n";	
	my @user_info = $sth->fetchrow_array();	
	
	#===create user hash===
	my %user;
	$user{"Student Number"} = $nstu+2;
	$user{"User ID"} = $user_info[0];
	$user{"First Name"} = $user_info[1];
	$user{"Last Name"} = $user_info[2];
	$user{"Gender"} = $user_info[3];
	$user{"Date of Birth"} = $user_info[4];
	$user{"Email"} = $user_info[5];
	$user{"Hair Colour"} = $user_info[6];
	$user{"Degree"} = $user_info[7];
	$user{"Height"} = $user_info[8];
	$user{"Weight"} = $user_info[9];
	$user{"Username"} = $user_info[10];
	$user{"Password"} = $user_info[11];
	
	#===get the user courses===
	$sth = $dbh->prepare('SELECT * FROM USER_COURSES WHERE USER_ID = ?');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";		
	#my $courses = "";
	my @courses;
	while (my @row_courses = $sth->fetchrow_array) {
		#$courses .= "@row"."\n";
		push @courses, p("@row_courses");
	}
	$user{"Courses"} = "@courses";

	#===get the user favourites===
	$sth = $dbh->prepare('SELECT * FROM USER_FAVOURITES WHERE USER_ID = ?');
	$sth->execute($user_info[0]) or die "SQL Error: $DBI::errstr\n";	
	#my $courses = "";
	my @favourites;
	while (my @row_favourites = $sth->fetchrow_array) {
		#$courses .= "@row"."\n";
		push @favourites, p("@row_favourites");
	}
	$user{"Favourites"} = "@favourites";

	push @td,td({},["$_","$user{$_}"]) foreach (keys %user);

	print p, 
			start_form, "\n",
			hidden('n', $nstu),"\n",
			a(submit({-class=>"button button-pill button-action",-name=>'Next Student',-value=>'Next Student'})),"\n",
			a(submit({-class=>"button button-pill button-action",-name=>'Home',-value=>'Home'})),"\n",
			end_form, "\n",
			table({-border=>1},
				Tr( \@td )
			);
			p, "\n";
}




