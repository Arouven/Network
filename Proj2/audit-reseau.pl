#!/usr/bin/perl -w
use DBI;


#Recuperations de la liste des switchs ou les backup sont en échec

#$dbh = DBI->connect('dbi:mysql:netmon','netmon','7zBTtvXEy1')
#or die "Connection Error: $DBI::errstr\n";
#
#$sql = "select host_name from backup where (type='HP Procurve' or type like 'Nortel%') and status='Echec'";

#$sth = $dbh->prepare($sql);
#
#$sth->execute
#
#or die "SQL Error: $DBI::errstr\n";
#

print "Bonjour,<br>\n";
print "<h3 align=center>CR Audit </h3>";
print "<br>";

print "<b> Backup des SWITCH </b><br>";
print "<br>\n";

$path = "/home/backups/switch_bkp";
chdir($path) or die "Cant chdir to $path $!";

my @files_hp = glob("*");

my %files_hp;

foreach my $file_hp (sort @files_hp) {
my $file_name_hp = substr($file_hp,0,-15);
$files_hp{$file_name_hp}=1;
}

foreach (sort keys %files_hp) {
no warnings qw(uninitialized);
my @files_latest_hp = glob("$_*");

print "$files_latest_hp[$#files_latest_hp]<br>\n";
}

#
#if ($sth->rows ==0)
#{
#
#  print "Ras<br>\n";
#
#}
#else
#{
# while (@row = $sth->fetchrow_array)
#  {
# print "@row<br>\n";
#  }
#
#}
#

#Backup des Checkpoint, BigIP, Radware et ISA, on recuperer le dernier fichier du chaque repertoire de Backup
#Backup des firewall checkpoint.
print "<br>";
print "<b>Backup CKP</b><br>";
print "<br>";

$path = "/home/backups/checkpoint_bkp";
chdir($path) or die "Cant chdir to $path $!";

my @files_ckp = glob("*ackup_*");

my %files_ckp;

foreach my $file_ckp (sort @files_ckp) {
my $file_name_ckp = substr($file_ckp,0,-13);
$files_ckp{$file_name_ckp}=1;
}

foreach (sort keys %files_ckp) {
no warnings qw(uninitialized);
my @files_latest_ckp = glob("$_*");

print "$files_latest_ckp[$#files_latest_ckp]<br>\n";
}

#Backup des BIGIP
print "<br>";
print "<b>Backup BIGIP</b><br>";
print "<br>";

$path = "/home/backups/bigip_bkp";
chdir($path) or die "Cant chdir to $path $!";

my @files_bigip = glob("*ucs*");

my %files_bigip;

foreach my $file_bigip (sort @files_bigip) {
my $file_name_bigip = substr($file_bigip,0,-12);
$files_bigip{$file_name_bigip}=1;
}

foreach (sort keys %files_bigip) {
no warnings qw(uninitialized);
my @files_latest_bigip = glob("$_*");

print "$files_latest_bigip[$#files_latest_bigip]<br>\n";
}

print "<br>";
print "Bonne journee.<br>";
print "<br>";

print "Cordialement,<br>";
print "Linkbynet <br>";

system("python3 /usr/local/linkbynet/scripts/Audit_Reseau/Highlight.py");


#On execute le script sendmail.sh pour l'envoie mail.
system("/bin/bash /usr/local/linkbynet/scripts/Audit_Reseau/sendmail.sh");

