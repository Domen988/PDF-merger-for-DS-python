from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from os import listdir
from os.path import isfile, join, dirname, abspath, basename
import re
import sys

# message box thingies
from ctypes import c_int, WINFUNCTYPE, windll
from ctypes.wintypes import HWND, LPCSTR, UINT
prototype = WINFUNCTYPE(c_int, HWND, LPCSTR, LPCSTR, UINT)
paramflags = (1, "hwnd", 0), (1, "text", "Hi"), (1, "caption", None), (1, "flags", 0)
MessageBox = prototype(("MessageBoxA", windll.user32), paramflags)


# check for files inside executable's folder
mypath = dirname(abspath("__file__"))
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, str(f)))]

# reads project name and reports settings
try:
    for f in listdir(mypath):
        if isfile(join(mypath, str(f))):
            if f.startswith("PDF-merger_") and f.endswith(".txt"):
                setupFileLoc = f
                projectName = (f.split("PDF-merger_"))[1].split(".txt")[0]
    fp = open(setupFileLoc, 'r')
    setupFile = fp.readlines()
except:
    MessageBox(text="Setup file 'PDF-merger_ ... .txt' is missing.\nApplicataion will exit.")
    sys.exit()
if len(projectName) == 0:
    MessageBox(text="Setup file has no project name defined.\nApplicataion will exit.")
    sys.exit()

reportsSpec = []
try:
    for line in setupFile:
        if line.startswith("#"):
            continue
        repName = re.split(":", line)[0]
        repSpec = []
        for num in re.split(" ", re.split(":", line)[1].strip()):
            repSpec.append(int(num))
        reportsSpec.append((repName, repSpec))
except:
    MessageBox(text='Setup folder reports setttings corrupted.\nApplication will exit.')
    sys.exit()
fp.close()

print "------------------------------------------------------"
print "PDF-merger-for-DS"
print "Created by Domen Zagar, zagar.domen@gmail.com"
print "version 1.01, 2014-09-02"
print "version 1.02, 2015-02-17: read project name from setup file name"
print "------------------------------------------------------\n"
print "Creating reports for project", projectName
filenames = []
for f in onlyfiles:
    if f.endswith(".pdf"):
        foo = re.split('[ .]', f)[0]            # splits by whitespace or period
        if foo.isdigit() and int(foo) <= 9:
            filenames.append(f)


def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]


notWritten = []
empty = []
problems = False
bar = False
for report in reportsSpec:
    reportName = projectName + report[0] + ".pdf"
    print "------------------"
    print "Combination:"
    print report
    if isfile(join(mypath, reportName)) and bar == False:
        result = MessageBox(flags=1, text= reportName + " allready exists. Continue?\nThis decision will apply to all other existing files.")
        if result == 2:
            sys.exit()
        if result == 1:
            bar = True
    try:
        print "Combining files:"
        merger = PdfFileWriter()
        atLeastOne = False
        for filename in filenames:
            if int(re.split('[ .]', filename)[0]) in report[1]:
                append_pdf(PdfFileReader(mypath + "\\" +filename, 'rb'), merger)
                print "\t", filename
                atLeastOne = True
        if atLeastOne is True:
            merger.write(file(join(mypath, reportName), 'wb'))
            print reportName, "written."
        else:
            empty.append(reportName)
            print reportName, "was not succesfully written - found no files to constitute"
            problems = True
    except:
        print reportName, "was not successfully written. - could not write"
        notWritten.append(reportName)
        problems = True
print "------------------"
if problems == False:
    print "Success!"
else:
    print "Next files were not written:"
    for rep in notWritten:
        print rep, "\t\t\t\tcould not write"
    for rap in empty:
        print rap, "\t\t\t\tnothing to merge"
    MessageBox(text='Some files were not written. See console application for the list of files.\nCheck if this files are closed and try again.')

raw_input("Press any key to exit.")
