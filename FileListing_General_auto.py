import os
import time
import datetime
import sys

# Routine to interrogate a folder and create a .csv file listing all folders and files
# includes filename, date, size in megabytes.
# also lists total size of files in each folder.

# Attempting version that reads in  a parameter for folder path to be interrogated during programme call.

# misreads the names  for certain folders or files if I have back slashes in the path so I am using forward slashes
Today = datetime.datetime.today().strftime('%Y-%m-%d-%H%M')
CurrentDirectory = os.getcwd()
if len( sys.argv ) > 1:
    Interrogate = sys.argv[1]
else:
    Interrogate = CurrentDirectory
print (f"You are interrogating the folder {Interrogate}")
ResultsFile = f'{CurrentDirectory}/FileListing-{Today}.csv'
FailureList = f'{CurrentDirectory}/FileListing-fails-{Today}.csv'
#interrogate = 'T:/projects/Twenty-07/ResearchAudit/DataforCollaborators'
#resultsfile = 'R:/Mary-Kate/Python/DataForCollaborators_FileList_2021_04_16.csv'

HeaderForListing = f'Folder or file, Name, Date, Size, Notes, Actions, Date Error, Size Error '
BlankLineFormatted = f',,,,,,,'
DummyDate = datetime.date.isoformat(datetime.datetime(2021, 4, 1))
DefaultFileSize = 1
DateError = 0
SizeError = 0
BadFileList = []
ResultsList = []
#function to obtain the date in the format I need which is YYYY-MM-DD.
def DateFunction (FileOrFolder):
    DateError = 0
    try:
        OurDate = datetime.date.isoformat(datetime.datetime.strptime(time.ctime(os.path.getmtime(FileOrFolder)),'%a %b %d %H:%M:%S %Y'))
    except:
        OurDate = DummyDate
        DateError = 1
    return (OurDate, DateError)

#function to obtain the size of a file.
def SizeOfFile (FileName):
    SizeError = 0
    try:
        FileSize = os.stat(FileName).st_size / (1024 * 1024)
    except:
        FileSize = DefaultFileSize
        SizeError = 1
        BadFileList.append(f'{FileName}')
    return (FileSize,SizeError)
ArchiveMB = 0
ResultsList.append (HeaderForListing)
for dirname, dirnames, filenames in os.walk(Interrogate):
# print path to all subdirectories first.
    ResultsList.append (BlankLineFormatted)
    OurDate, DateError = DateFunction(dirname)
    ResultsList.append (f'Top Level Folder: ,{dirname} ,{OurDate},,,,{DateError},')
    for subdirname in dirnames:
        ResultsList.append (BlankLineFormatted)
        OurDate, DateError = DateFunction(os.path.join(dirname, subdirname))
        ResultsList.append (f'Folder: ,{subdirname} ,{OurDate},,,,{DateError},')
        FolderMB = 0
    for filename in filenames:                
        OurDate, DateError = DateFunction(os.path.join(dirname, filename))              
        filesize, SizeError = SizeOfFile(os.path.join(dirname, filename))                
        FolderMB = FolderMB + filesize
        ResultsList.append (f'File:   ,{filename} ,{OurDate},{filesize:8.2f} MB,,,{DateError},{SizeError}')
        DateError = 0
        SizeError = 0
    ResultsList.append (f'Total size of files within this folder - not including subfolders: ,,,{FolderMB:8.2f} MB,,,,{SizeError}')
    ArchiveMB = ArchiveMB + FolderMB
    FolderMB = 0
#This dot is just to show progress when I am running the programme
#,end='' is to make sure we do not take a new line for each dot
    print ('.',end='', flush=True)
print ('')
print (f'Writing results to {ResultsFile}')    
ResultsList.append (BlankLineFormatted)
ResultsList.append (f'Total size of files within this archive: ,,,{ArchiveMB:8.2f} MB,,,,')
with open(ResultsFile, 'w') as f:
    for item in ResultsList:
        f.write("%s\n" % item)
if BadFileList:
    print (f'Check the date error or size error for the files listed in: \n {FailureList}')
    with open(FailureList, 'w') as f:
        for item in BadFileList:
            f.write("%s\n" % item)
                           
