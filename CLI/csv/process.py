import urllib2
import zipfile
import csv
import ntpath

URL="http://spatialkeydocs.s3.amazonaws.com/FL_insurance_sample.csv.zip"

def DownloadFile(url, fileName):
    response = urllib2.urlopen(url)
    zippedData = response.read()
    output = open(fileName,'wb')
    output.write(zippedData)
    output.close()

def Unzip(filename, outputFilename):
    zfobj = zipfile.ZipFile(filename)
    for name in zfobj.namelist():
        uncompressed = zfobj.read(name)
        output = open(outputFilename,'wb')
        output.write(uncompressed)
        output.close()

def ReadCSVFile(outputFilename):
    response = open(outputFilename, 'r')
    for line in response.read():
        print(line)

def main():
    zipFileName = ntpath.basename(URL)
    outputFilename = zipFileName.replace('.zip','')
    DownloadFile(URL, zipFileName)
    Unzip(zipFileName, outputFilename)
    ReadCSVFile(outputFilename)

if __name__ == '__main__':
    main()