# newsdata
Database code for newsdata (logs analysis project)
Outputs the answers to three questions.
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Requirements
This program requires Python 3 to be installed.
Get it [here](https://www.python.org/downloads/).  
It also requires vagrant to be installed and configured with a specific
vagrantfile provided by Udacity for this assignment.  
Finally, it requires newsdata.sql to be populated in the same vagrant
directory. newsdata.sql is also provided by Udacity for this assignment.  
The assignment instructions specify not to include those files here, so if you
do not already have them (IE, you are not an instructor or classmate) Then
you will not be able to run this program.  

## Instructions
To summerise the instructions into a shortened version:
Download, extract, move or copy newsdata.py into your vagrant directory,
run vagrant up, vagrant ssh, cd into "/vagrant", then run newsdata.py in
python3.  
If you need further instructions, don't worry- just keep reading.  

First download these files by clicking the green button on GitHub that says
Clone or download, then click Download Zip.  
Next, you'll need to extract the zip file you downloaded. It will be named
newsdata.zip.  

### Windows Users:
- Open Windows Explorer (or any folder) and browse to the location you
downloaded newsdata.zip to.
- Right-click newsdata.zip and then left-click "Extract All...".
(A new window will pop up that says "Extract Compressed (Zipped) Folders"
at the top.)
- Click the button that says "Extract" at the bottom.
This will make a new folder called newsdata (without the .zip at
the end).
- You can now delete the .zip folder as it is no longer needed.
- Open the newsdata folder.

Now you can move or copy newsdata.py into your vagrant directory.
This directory should already be set up with newsdata.sql. See the Requirements
section above.

Once your files are together in your vagrant directory, open your terminal of
choice (I recommend GitBash for Windows users) and type the following
commands:  
"vagrant up"  
"vagrant ssh"  
"cd /vagrant"  
"python3 newsdata.py"  

### Mac Users:
- Open The Finder and search for newsdata or browse to where you
downloaded it.
- Select the zip file and click "Unzip" at the top center of The Finder window.
(If you don't see "Unzip"), then...
- Right-click the file newsdata.zip
- left-click "Open With...",
- left-click "Archive Utility".

Now you can move or copy newsdata.py into your vagrant directory.
This directory should already be set up with newsdata.sql. See the Requirements
section above.

Once your files are together in your vagrant directory, open your terminal and
type the following commands:  
"vagrant up"  
"vagrant ssh"  
"cd /vagrant"  
"python3 newsdata.py"  

### Terminal Users (Linux, Mac, or Windows):
- Open Terminal.
- Navigate to the directory where you downloaded or cloned newsdata.
(Use cd to change directory and ls or dir to list what's in your current
directory.)

Now you can move or copy newsdata.py into your vagrant directory.
This directory should already be set up with newsdata.sql. See the Requirements
section above.

Once your files are together in your vagrant directory, type the following
commands:  
"vagrant up"  
"vagrant ssh"  
"cd /vagrant"  
"python3 newsdata.py"  

## Notes
The instructions for this assignment state that If the code relies on views
created in the database, the README file includes the create view statements
for these views.
(If the code does not depend on views, ignore this requirement.)  
Well, my code is using a custom View, but no action is needed by the user to
make this view because I built that into the code. All the user (or grading
instructor) has to do is run newsdata.py and it will automatically create or
update the view it uses before executing the queries.

None the less it won't hurt to make the view outside of my script because my
script will check and update it if needed, so here is the psql to recreate
the view:  

```CREATE OR REPLACE VIEW slug_from_path AS
SELECT(REPLACE(log.path, '/article/', '')) AS
slug FROM log
WHERE log.path != '/';
```  

## License
MIT Licesne found [here](LICENSE.md)
