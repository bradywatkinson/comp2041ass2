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
				p('Thank you for signing up!'),
				p('An email has been sent to your address with your temporary password'),"\n",				
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
						Tr(td({-width=>$table_width},"Username: ".td(input({-type=>'text',-pattern=>'\w+',-name=>'Username'})))."\n"),
						#Tr(td({-width=>$table_width},"Password: ([\\w_]{6,})".td(textfield({-pattern=>'\w+'},"Password","",20,20)))."\n"),
						#Tr(td({-width=>$table_width},"First Name: ([a-zA-Z]+)".td(textfield({-pattern=>'[a-zA-Z]+'},"First Name","",20,20)))."\n"),
						#Tr(td({-width=>$table_width},"Last Name: ([a-zA-Z]+)".td(textfield({-pattern=>'[a-zA-Z]+'},"Last Name","",20,20)))."\n"),
						Tr(td({-width=>$table_width},"Email: ".td(input({-type=>'email',-name=>"Email"})))."\n"),
						#Tr(td({-width=>$table_width},"Date of Birth: (YYYY/MM/DD)".td(textfield({-pattern=>'\d{4}'},"Year","",4,4),textfield({-pattern=>'\d{2}'},"Month","",2,2),textfield({-pattern=>'\d{2}'},"Day","",2,2)))."\n"),
						#Tr(td({-width=>$table_width},"Hair Colour: ").td(popup_menu(-name=>"Hair Colour",-values=>[map {$hairs{$_}} keys %hairs],-labels=>\%hairs))."\n"),
						#Tr(td({-width=>$table_width},"Gender: ").td(popup_menu(-name=>"Gender",-values=>[map {$genders{$_}} keys %genders],-labels=>\%genders))."\n"),
						#Tr(td({-width=>$table_width},"Height (cm): ".td(textfield("Height","",20,20)))."\n"),
						#Tr(td({-width=>$table_width},"Weight (kg): ".td(textfield("Weight","",20,20)))."\n")
					)
				), "\n",
				submit({-class=>"button button-rounded button-action buttonWidth",-name=>'Sign Up',-value=>'Sign Up'}),"\n",
				a({-href=>'love2041.cgi',-class=>"button button-rounded button-action buttonWidth"},'Cancel'),"\n",
				end_form
			);
}

sub make_user
{
	my @rand_pass = ('Dwg5JZsT','QnjQnQ9j','sd7MnhUT','zeV4L4LQ','8pFG5cgd','J4kQY2sS','jwC3TVBw','CL775cuS','Jcv6MgE5','NLAzzCdb',
						'py5643ca','E73UxEZm','wcRu5utp','kkjNYsKj','BCSng48A','6UhJP7D6','dvsN4wYy','xMCkYTbk','fa3hs6kf','8Vx7HGgy');
						
	$tmp_pass = $rand_pass[rand(19)];

	#=====insert into user table=====
	#my $f_name 	= param('First Name') || "";
	#my $l_name 	= param('Last Name') || "";
	#my $gender 	= param('Gender') || "";
	#my $year 	= param('Year') || "";
	#my $month 	= param('Month') || "";
	#my $day 	= param('Day') || "";
	my $email	= param('Email') || "";
	#my $hair	= param('Hair Colour') || "";
	#my $degree	= param('Degree') || "";
	#my $height	= param('Height') || "";
	#my $weight	= param('Weight') || "";
	my $u_name	= param('Username') || "";
	my $pass	= $tmp_pass;
	

	$u_name =~ s/'/''/g;
	$u_name =~ s/"/""/g;
	$u_name =~ s/[^\_\"\'\w\d\s]//;
	 
	my $sql_insert_users = "INSERT INTO USERS('USERNAME','EMAIL','PASSWORD')
			VALUES ('$u_name','$email','$pass')";
	print "$sql_insert_users\n";
	#$sth = $dbh->prepare($sql_insert_users);
	#$sth->execute or die "SQL Error: $DBI::errstr\n";
	

	$to = $email;
	$from = 'accountCreation@love2041.com';
	$subject = 'Love 2041 Account Creation Confirmation';
	$message = '
	<h2>Welcome to Love2041<\h2>
	<p>This message is sent to confirm your email address for this account. If you have received this email incorrectly, please ignore this message<\p>
	<p>Your temporary password is:'.$tmp_pass.'<\p>
	<p>You may change your password after you log in<\p>
	<p><\p>
	<Sincerely, Love2041 Team<\p>';
	 
	open(MAIL, "|/usr/sbin/sendmail -t");
	 
	print MAIL "To: $to\n";
	print MAIL "From: $from\n";
	print MAIL "Subject: $subject\n\n";
	print MAIL "Content-type: text/html\n";
	# Email Body
	print MAIL $message;

	close(MAIL);
 

	
}
