import resolve_api
import datetime
import pathlib
import os

class Resolve():
    def __init__(self):
        pass
    # Resolve API Connect
    def connect_resolve_api(self):
        return resolve_api.dvr_script.scriptapp("Resolve")

    #--------------------------------------
    # Runs at start of app or when Refresh button is clicked
    def check_if_resolve_open(self):
        try:
            resolve = self.connect_resolve_api()
            project_manager = resolve.GetProjectManager()
        except:
            return "Check if Resolve is Open"
        else:
            return self.get_database_list(project_manager)
        
    def get_database_list(self, project_manager):
        database_list = []
        database_dictionary = project_manager.GetDatabaseList()
        
        for name in database_dictionary:
            database_list.append(name['DbName'])
        
        database_list.sort()
        return database_list


    #--------------------------------------
    # Database pick from window option menu
    def format_database(self, database_name):
        return {f'DbType': 'Disk', 'DbName': database_name}
    
    def select_database(self, database):
        resolve = self.connect_resolve_api()
        project_manager = resolve.GetProjectManager()
        project_manager.SetCurrentDatabase(database)
        return project_manager

    # Add current date to project name in YYMMDD format
    def date_project_name(self, project_name):
        date_prefix = datetime.date.today().strftime("%y%m%d")
        return f"{date_prefix}_{project_name}"

    # Remember to Pass the Dated Project Name to this function
    def make_project_from_template(self, project_manager, full_project_name):
        project_path = pathlib.Path("project/Template.drp")
        full_path = os.path.abspath(project_path)
        project_manager.ImportProject(full_path, projectName=None)
        project_manager.LoadProject("Template")
        current_project = project_manager.GetCurrentProject()
        current_project.SetName(full_project_name)
        return project_manager.GetCurrentProject()

    #--------------------------------------
    def set_resolve_settings(self, current_project, database, project_name, folder_path, cache_path):
        cache_full_path = pathlib.Path(f"{cache_path}/{database}/{project_name}/CacheClip")
        gallery_full_path = pathlib.Path(f"{cache_path}/{database}/{project_name}/.gallery")
        capture_full_path = pathlib.Path(f"{folder_path}/{database}/{project_name}/2_audio/4_bounce")
        current_project.SetSetting('perfCacheClipsLocation', str(cache_full_path))
        current_project.SetSetting('colorGalleryStillsLocation', str(gallery_full_path))
        current_project.SetSetting('videoCaptureLocation', str(capture_full_path))

