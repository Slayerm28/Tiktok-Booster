import requests,os
from tqdm import tqdm
import zipfile
from datetime import datetime,timedelta
import shutil
from colorama import Fore,Style
import colorama
class ProgramUsage():
    def check_video(VIDEO):
        """
        Check if the video is a 'vm' or 'www' type
        
        Parameters
        ----------
        - VIDEO : str
            - Tiktok Video URL
        
        Returns
        -------
        - vm
            - if Video URL starts with vm
        - www 
            - if Video URL starts with www

        Example
        -------

        >>> check_video("https://www.tiktok.com/@****/video/****")
            'www'
        >>> check_video("https://vm.tiktok.com/****)
            'vm'
        """

        return "vm" if VIDEO.split("/")[2].__contains__("vm") else "www"
    
    def get_vmid(VIDEO):
        """
        Get the video ID from the URL

        Parameters
        ----------
        - VIDEO : str
            - Tiktok Video URL
        
        Returns
        -------
        - str
            - Returns video ID based on the Video URL provided.
        - None 
            - if no Video ID was found.
        """

        response = requests.post("https://countik.com/api/video/exist", json={'url': f"{VIDEO}"}).json()
        try:
            return response['id']
        except KeyError:
            print(f"{Fore.RED}[Warning] Unable to get Video ID{Style.RESET_ALL}")
            return None
        
    def convert_hours(hours = 'ind',sec = 'ind'):
        """
        Convert hours or seconds into HH:MM:SS format
        
        Parameters
        ----------
        - hours : int (or 'ind' if nothing is passed)
            - Amount of hours to transform in hhmmss
        - seconds : int (or 'ind' if nothing is passed)
            - Amount of seconds to transform in hhmmss 
        
        Returns
        -------
        - str
            - the hhmmss based on the parameter passed.
        """

        if hours == 'ind':
            td = timedelta(seconds=sec)
        else:
            td = timedelta(seconds=int(hours * 3600))

        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        hhmmss = f"{hours:02}:{minutes:02}:{seconds:02}"
        
        return hhmmss
    
    def get_numeric_value(value):
        """Convert a value to an integer, returning 0 if conversion fails"""
        try:
            return int(value)
        except ValueError:
            return 0
        
    def download(INFO:colorama,WAITING:colorama,SUCCESS:colorama,WARNING:colorama,download_url, destination='.'):
        """Download and extract a file from the given URL"""
        if "Sneezedip" in download_url:
            print(f'{INFO}{Fore.WHITE}Downloading new version, please wait...{Style.RESET_ALL}')
        else:
            print(f'{INFO}{Fore.WHITE}Downloading Tesseract, please wait...{Style.RESET_ALL}')

        response = requests.get(download_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        zip_path = os.path.join(destination, "downloaded_file.zip")

        with open(zip_path, 'wb') as file:
            with tqdm(total=total_size, unit='B', unit_scale=True,
                    desc=f"{WAITING} {Fore.WHITE}Downloading "
                        f"{'New Version' if 'Sneezedip' in download_url else 'Tesseract'} {Style.RESET_ALL}") as pbar:
                for data in response.iter_content(1024):
                    file.write(data)
                    pbar.update(len(data))

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            total_files = len(zip_ref.infolist())
            with tqdm(total=total_files, unit='file',
                    desc=f"{WAITING} {Fore.WHITE}Extracting "
                        f"{'New Version' if 'Sneezedip' in download_url else 'Tesseract'}{Style.RESET_ALL}") as pbar:
                for file in zip_ref.infolist():
                    zip_ref.extract(file, destination)
                    pbar.update(1)
        os.remove(zip_path)

        if 'Sneezedip' in download_url:
            with os.scandir('Tiktok-Booster-main') as entries:
                for entry in entries:
                    if entry.is_dir():
                        with os.scandir(entry) as entries_folder:
                            for entry_folder in entries_folder:
                                try:
                                    os.replace(f"Tiktok-Booster-main/{entry.name}/{entry_folder.name}",
                                            f"./{entry.name}/{entry_folder.name}")
                                except Exception as e:
                                    print(e)
                                continue
                    if entry.is_file():
                        try:
                            os.replace(f"Tiktok-Booster-main/{entry.name}", f"./{entry.name}")
                        except Exception as e:
                            print(e)
                        continue
            shutil.rmtree("Tiktok-Booster-main")
        print(f'{SUCCESS}{Fore.WHITE}{"New Version" if "Sneezedip" in download_url else "Tesseract"}'
            f' Downloaded and Extracted Successfully!{Style.RESET_ALL}')
        print(f'{WARNING}{Fore.WHITE}Please Restart the program!{Style.RESET_ALL}')
        