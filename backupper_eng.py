''' If you want all the files in the folder, remove 'and f.endswith('.py')' from line 33. BY DEFAULT, THE PROGRAM SAVES ALL FILES IN THE CURRENT FOLDER.

If you want specific file types, add as needed to line 33 'or f.endswith('.file_extension')'. These can be chained, e.g., 'or f.endswith('.py') or f.endswith('.js')'

The program also has an option to manually select the files to be saved.'''

import os
import shutil
from datetime import datetime
from tkinter import Tk, Button, Label, Listbox, filedialog

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Backup Program")
        self.file_list = Listbox(root, width=175, height=25)
        self.file_list.pack()
        self.manual_backup_button = Button(root, text="Select Files", command=self.select_files)
        self.manual_backup_button.pack()
        self.backup_folder = os.path.join(os.getcwd(), "Backups")

        # Perform automatic backup on program startup
        self.create_backups(auto=True)

    def create_backups(self, auto=False):
        today = datetime.now().strftime("%d.%m.%Y")
        today_backup_folder = os.path.join(self.backup_folder, today)
        os.makedirs(today_backup_folder, exist_ok=True)

        if auto:
            self.file_list.insert("end", "Automatic Backup:")
            files_to_backup = [f for f in os.listdir(os.getcwd())
                               if os.path.isfile(f)]
        else:
            files_to_backup = filedialog.askopenfilenames(
                initialdir=os.getcwd(), title="Select Files",
                filetypes=(("All Files", "*.*"), ("Python Files", "*.py"), ("JavaScript Files", "*.js"),
                           ("Java Files", "*.java"), ("C++ Files", "*.cpp"))
            )
            if not files_to_backup:
                self.file_list.insert("end", "No files selected, backup not performed.")
                return
            self.file_list.insert("end", "Manual Backup:")

        for file in files_to_backup:
            filename = os.path.basename(file)
            backup_filename = f"{os.path.splitext(filename)[0]}_BACKUP{os.path.splitext(filename)[1]}"
            backup_path = os.path.join(today_backup_folder, backup_filename)

            if os.path.exists(backup_path):
                if self.is_same_file(file, backup_path):
                    message = f"{filename}, an up-to-date backup already exists, new version not saved"
                else:
                    shutil.copy2(file, backup_path)
                    message = f"{filename}, the file is new or has been updated since the last backup. Backup saved."
            else:
                shutil.copy2(file, backup_path)
                message = f"{filename}, backup saved."

            self.file_list.insert("end", message)

        # Print the backup folder path at the end
        self.file_list.insert("end", "")
        self.file_list.insert("end", f"Backups were saved to folder: {today_backup_folder}")

    def is_today_modified(self, file):
        mod_time = datetime.fromtimestamp(os.path.getmtime(file))
        return mod_time.date() == datetime.today().date()

    def is_same_file(self, file1, file2):
        return os.path.getsize(file1) == os.path.getsize(file2) and os.path.getmtime(file1) == os.path.getmtime(file2)

    def select_files(self):
        self.create_backups(auto=False)

if __name__ == "__main__":
    root = Tk()
    app = BackupApp(root)
    root.mainloop()
