from googleDriveFileDownloader import googleDriveFileDownloader
import sys

file = sys.argv[1]
a = googleDriveFileDownloader()
a.downloadFile(file)
