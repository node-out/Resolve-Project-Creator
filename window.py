import customtkinter as ctk
import os
import pathlib
from PIL import Image
import utility
import resolve_functions
from project_data import ProjectData

LOGO_WHITE = pathlib.Path("./img/nodeout_text_logo.png")
LOGO_BLACK = pathlib.Path("./img/nodeout_text_LOGO_BLACK.png")
ICON_PATH = pathlib.Path("./img/nodeout.ico")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.projects_folder_path = ""
        self.cache_path = ""
        self.initialize_ui()
        self.database_menu.set("")
        self.btn_create.configure(state="disabled")
        self.resolve = resolve_functions.Resolve()
        self.project_data = ProjectData()

        
        load_file_path = utility.load_paths_file()
        self.check_saved_file(load_file_path)


    # -----------------------------------------------------------
    # Methods
    # Buttons -----------
    # Browse Buttons ----
    def browse_projects(self):
        self.projects_folder_path = ctk.filedialog.askdirectory()
        if self.projects_folder_path != "":
            self.projects_entry_box.delete(0,"end")
            self.projects_entry_box.insert(0,self.projects_folder_path)
            dictionary = {"projects": str(self.projects_folder_path), "cache": str(self.cache_path)}
            utility.save_paths_file(dictionary)

    def browse_cache(self):
        self.cache_path = ctk.filedialog.askdirectory()
        if self.cache_path != "":
            self.cache_entry_box.delete(0,"end")
            self.cache_entry_box.insert(0,self.cache_path)
            dictionary = {"projects": str(self.projects_folder_path), "cache": str(self.cache_path)}
            utility.save_paths_file(dictionary)

    # Refesh and Create Buttons ----
    def refresh_button(self):
        self.talk_to_user("Refreshing")
        database_list = self.resolve.check_if_resolve_open()
        if isinstance(database_list, str):
            self.talk_to_user(database_list)
            self.btn_create.configure(state="disabled")
        else:
            self.database_menu.configure(values=database_list)
            self.database_menu.set(database_list[0])
            self.btn_create.configure(state="normal")
            self.update()
            self.talk_to_user("Ready")

    def create_button(self):
        check = self.resolve.check_if_resolve_open()
        if isinstance(check, str):
            self.talk_to_user(check)
            self.btn_create.configure(state="disabled")
        else:
            self.talk_to_user("Starting")
            if self.check_input_data():
                self.talk_to_user("Creating Project")
                database_name = self.project_data.database_name = self.database_menu.get()
                full_database_name = self.resolve.format_database(self.project_data.database_name)
                resolve_project_manager = self.resolve.select_database(full_database_name)
                
                project_name = self.resolve.date_project_name(self.project_data.project_name)
                projects_path = self.project_data.projects_root_path
                cache_path = self.project_data.cache_root_path

                current_project = self.resolve.make_project_from_template(resolve_project_manager, project_name) 

                self.resolve.set_resolve_settings(current_project, database_name, project_name, projects_path, cache_path)

                # Check if creating directories
                create_folders = self.checkbox_folders.get()
                if create_folders:
                    utility.directorys_from_template(projects_path, database_name, project_name)
                self.talk_to_user("Done")
            else:
                self.talk_to_user("Fill all fields")


    def check_input_data(self):
        project_name = self.project_data.project_name = self.project_name.get()
        project_root_path = self.project_data.projects_root_path = self.projects_entry_box.get()
        cache_root_path = self.project_data.cache_root_path = self.cache_entry_box.get()
        
        if project_name != "" and project_root_path != "" and cache_root_path != "":
            # print("valid entry")            
            if os.path.isdir(pathlib.Path(project_root_path)):
                # print("path ok")
                if os.path.isdir(pathlib.Path(cache_root_path)):
                    # print("path ok")
                    return True
                else:
                    # print("bad path")
                    return False
            else:
                # print("bad path")
                return False
            
        else:
            # print("invalid entry")
            return False

    # ----------------------------------
    def talk_to_user(self, user_message):
        self.app_feedback.configure(text=user_message)
        self.update()
    
    def check_saved_file(self, load_file_path):  
        check_file = pathlib.Path("paths.txt")
        if check_file.is_file():
            if os.stat("paths.txt").st_size != 0:
                paths = load_file_path
                if paths["projects"] != "" and paths["cache"] != "":
                    self.projects_entry_box.insert(0, paths["projects"])
                    self.cache_entry_box.insert(0, paths["cache"])
                    self.projects_folder_path = paths["projects"]
                    self.cache_path = paths["cache"]
        else:
            f = open("paths.txt", "x")
            f.close()


# Window Settings
    def initialize_ui(self):
        # Window Look        
        self.title('Resolve Project Creator')
        self.geometry('600x250')
        self.iconbitmap(ICON_PATH)
        self.grid_columnconfigure(0, weight=1)
        self.database_list = [] 
        self.create_folders = "no"


        # Project / Database
        self.project_database_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.project_database_frame.grid(row=0, column = 0, padx=5, pady=5, sticky="ew")
        self.project_database_frame.grid_columnconfigure(0, weight=1)
        self.project_database_frame.grid_columnconfigure(1, weight=1)

        self.project_name = ctk.CTkEntry(self.project_database_frame, placeholder_text="Project Name")
        self.project_name.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.database_menu = ctk.CTkOptionMenu(self.project_database_frame, values=self.database_list)
        self.database_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        

        # Browse Folders
        self.browse_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.browse_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.browse_frame.grid_columnconfigure(0, weight=1)

        self.projects_entry_box = ctk.CTkEntry(self.browse_frame, placeholder_text="Projects Folder")
        self.projects_entry_box.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.btn_project_browse = ctk.CTkButton(self.browse_frame, text="Browse", command=self.browse_projects)
        self.btn_project_browse.grid(row=0, column=1, padx=5, pady=5)

        self.cache_entry_box = ctk.CTkEntry(self.browse_frame, placeholder_text="Cache Folder")
        self.cache_entry_box.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.btn_cache_browse = ctk.CTkButton(self.browse_frame, text="Browse", command=self.browse_cache)
        self.btn_cache_browse.grid(row=1, column=1, padx=5, pady=5)
        

        # Feedback Label
        self.feedback_frame = ctk.CTkFrame(self)
        self.feedback_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.feedback_frame.grid_columnconfigure(0, weight=1)
        self.app_feedback = ctk.CTkLabel(self.feedback_frame, text="Click Refresh", font=("Arial",25))
        self.app_feedback.grid(row=0, column=0, padx=5, pady=5)


        # Refresh / Checkbox / Create
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure(2, weight=1)
        
        self.btn_refresh = ctk.CTkButton(self.button_frame, text="Refresh", command=self.refresh_button)
        self.btn_refresh.grid(row=0, column=1, padx=5, pady=5)

        self.create_folders = ctk.StringVar(value="yes")
        self.checkbox_folders = ctk.CTkCheckBox(self.button_frame, text="Create Folders?", variable=self.create_folders, onvalue="yes", offvalue="no")
        self.checkbox_folders.grid(row=0, column=2, padx=(30,0), pady=5, sticky="ew")

        self.btn_create = ctk.CTkButton(self.button_frame, text="Create Project", command=self.create_button)
        self.btn_create.grid(row=0, column=3, padx=5, pady=5)

        # Nodeout Logo Image
        self.logo = ctk.CTkImage(
            light_image=Image.open(LOGO_BLACK),
            dark_image=Image.open(LOGO_WHITE),
            size=(80, 19)
            )
        self.image_label = ctk.CTkLabel(self.button_frame, image=self.logo, text="")
        self.image_label.grid(row=0, column=0, padx=(0,20))