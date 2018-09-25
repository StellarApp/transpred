# prepare tasks for data loading(dl)
from typing import List, Tuple
from functools import reduce, partial
#import wget
import urllib.request as ur
from utils import persistence as ps
import os

#TODO
def make_transit(*args) -> List[str]:
    return []

#TODO
def make_traffic(*args) -> List[str]:
    return []

#TODO
def make_cabs(*args) -> List[str]:
    print('constructing tasks for years '+str(args))
    tasks_for_year = lambda tasks, year: tasks + [year+"-"+str(quarter) for quarter in range(1, 4)]
    return reduce(tasks_for_year, list(*args), [])

#TODO
def perform_transit(task: bytes) -> bool:
    return False

#TODO
def perform_traffic(task: bytes) -> bool:
    return False


def perform_cabs(b_task: bytes) -> bool:
    task: str = str(b_task, 'utf-8')
    task_split: List[str] = task.split('-')
    year: str = task_split[0]
    quarter: int = int(task_split[1])
    prefix_zero = lambda x: "0"+str(x) if x < 10 else str(x)
    months = lambda quarter: range( (quarter-1)*3+1, (quarter-1)*3+4 )
    get_url = lambda month: "https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_"+year+"-"+prefix_zero(month)+".csv"
    urls: List[str] = list(map(get_url, months(quarter)))
    print('downloading from urls '+str(urls))
    source_folder: str = os.path.dirname(__file__)+'/gcabs/'
    os.makedirs(source_folder, exist_ok=True)
    print('created source folder '+source_folder)
    try:
        #download_from_urls(urls, source_folder)
        for url in urls:
            print('downloading file from '+url)
            #file: str = wget.download(url, out=source_folder)
            filename: str = download_from_url(url, source_folder)
            print('copying file '+filename+' to bucket gcabs')
            status: bool = ps.copy_file(dest_bucket='gcabs', file=filename, source=source_folder+filename)

    except Exception as err:
        raise err
    #else:
        #try:
            #ps.copy_files(source_folder,'gcabs')
        #except Exception as err:
            #raise err
    else:
        return status


def download_from_urls(urls: List[str], folder) -> bool:
    try:
        #download=partial(wget.download, out=folder)
        #map(download, urls)
        pass
    except Exception as err:
        raise err
    else:
        return True



def download_from_url(url: str, folder: str) -> str:
    try:
        filename: str = url.split('/')[-1]
        ur.urlretrieve(url, folder+filename)
        print('downloaded file to '+folder+filename)

    except Exception as err:

        raise err
    else:
        return filename



