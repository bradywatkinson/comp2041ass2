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
if (param('Sign Up')) {
	make_user();
	welcome_page() 
} else {
	sign_up_page();
}
page_trailer();
exit 0;	
#========================

sub welcome_page
{
	main_forms();
	print	div({-id=>'centreDoc'},
				p('Thank you for signing up!'),"\n",				
			);
}

sub sign_up_page
{
	my %hairs = (
		'Blonde' => 'Blonde',
		'Black' => 'Black',
		'Red'	=> 'Red',
		'Silver' => 'Silver',
		'Brown' => 'Brown'
	);
	
	my %genders = (
		'Male' => 'Male',
		'Female' => 'Female'
	);

	$table_width = '200px';
	
	main_forms();
	print	div({-id=>'centreDoc'},
				h2('Sign up'),"\n",
				p('Becoming a member allows you to access our extensive network of attractive people.'),"\n",
				p('You will be able to:'),"\n",
				li('Create a profile to display to other users'),"\n",
				li('Get matched with amazing people who are matched to you with our amazing matching algorithm'),"\n",
				li('Interact with other users'),"\n",
				start_form, "\n",
				hidden('Make_User','1'),"\n",
				fieldset({},
					legend("Enter Your Information"),
					table({-cellpadding=>'3'},
						Tr(td({-width=>$table_width},"Username: ".td(textfield({-pattern=>'[\w_]+'},"Username","",20,20)))."\n"),
						Tr(td({-width=>$table_width},"Password: ".td(textfield({-pattern=>'[\w_]+'},"Password","",20,20)))."\n"),
						Tr(td({-width=>$table_width},"First Name: ".td(textfield({-pattern=>'[a-zA-Z]+'},"First Name","",20,20)))."\n"),
						Tr(td({-width=>$table_width},"Last Name: ".td(textfield({-pattern=>'[a-zA-Z]+'},"Last Name","",20,20)))."\n"),
						Tr(td({-width=>$table_width},"Email: ".td(textfield({-type=>'email'},"Email","",20,100)))."\n"),
						Tr(td({-width=>$table_width},"Date of Birth: ".td(textfield("Year","",4,4),textfield("Month","",2,2),textfield("Day","",2,2)))."\n"),
						Tr(td({-width=>$table_width},"Hair Colour: ").td(popup_menu(-name=>"Hair Colour",-values=>[map {$hairs{$_}} keys %hairs],-labels=>\%hairs))."\n"),
						Tr(td({-width=>$table_width},"Gender: ").td(popup_menu(-name=>"Gender",-values=>[map {$genders{$_}} keys %genders],-labels=>\%genders))."\n"),
						Tr(td({-width=>$table_width},"Height (cm): ".td(textfield("Height","",20,20)))."\n"),
						Tr(td({-width=>$table_width},"Weight (kg): ".td(textfield("Weight","",20,20)))."\n")
					)
				), "\n",
				submit({-class=>"button button-rounded button-action buttonWidth",-name=>'Sign Up',-value=>'Sign Up'},'Sign Up'),"\n",
				a({-href=>'love2041.cgi',-class=>"button button-rounded button-action buttonWidth"},'Cancel'),"\n",
				end_form
			);
}

sub make_user
{
	#=====insert into user table=====
	my $f_name 	= param('First Name') || "";
	my $l_name 	= param('Last Name') || "";
	my $gender 	= param('Gender') || "";
	my $year 	= param('Year') || "";
	my $month 	= param('Month') || "";
	my $day 	= param('Day') || "";
	my $email	= param('Email') || "";
	my $hair	= param('Hair Colour') || "";
	my $degree	= param('Degree') || "";
	my $height	= param('Height') || "";
	my $weight	= param('Weight') || "";
	my $u_name	= param('Username') || "";
	my $pass	= param('Password') || "";
	 
	my $sql_insert_users = "INSERT INTO USERS('FIRST_NAME','LAST_NAME','GENDER','YEAR','MONTH','DAY','EMAIL','HAIR_COLOUR','DEGREE','HEIGHT','WEIGHT','USERNAME','PASSWORD')
			VALUES ('$f_name','$l_name','$gender','$year','$month','$day','$email','$hair','$degree','$height','$weight','$u_name','$pass')";
	print "$sql_insert_users\n";
	#$sth = $dbh->prepare($sql_insert_users);
	#$sth->execute or die "SQL Error: $DBI::errstr\n";	
}
