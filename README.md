Hey there!


It's good to have versions. But it's a drag to manually perform backups. Worry no more. Here is a little software that does that for you.


1. 	  Download backupper_eng.py


2.	  Save it to your project folder.


3.	  Run the file to automatically back up every file in your project folder.


3.1 	The program checks the last time files in the folder have been saved. If there has been a save since the last backup, it'll create a new backup in project_folder/Backups/*date*/backed_up_file.
	    This means that if you require a reliable backup during the same day, copy the *date* folder and remove it from the Backup folder so it won't be overwritten.


3.2 	If you like, you can configure the program to back up only specific types of files. Step-by-step instructions for this are in the backupper_eng.py file as a docstring.


4.	  The program also has the option to manually choose which files you want to back up. However, since that is manual work, the emphasis of this program is on automatic functionality.
