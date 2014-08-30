from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from os import listdir
from os.path import isfile, join, dirname, abspath
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
    fp = open('PDF-merger-for-DS-SETUP.txt', 'r')
except:
    MessageBox(text="Setup folder 'PDF-merger-for-DS-SETUP' is missing.\nApplicataion will exit.")
    sys.exit()
try:
    setupFile = fp.readlines()
    projectName = setupFile[0].strip()
except:
    MessageBox(text="Setup folder 'PDF-merger-for-DS-SETUP' is empty. Name could not be read.\nApplicataion will exit.")
    sys.exit()

reportsSpec = []
try:
    for line in setupFile[1:]:
        if line.startswith("#"):
            continue
        repName = re.split(":", line)[0]
        repSpec = []
        for num in re.split(" ", re.split(":", line)[1].strip()):
            repSpec.append(int(num))
        reportsSpec.append((repName, repSpec))
except:
    MessageBox(text='Setup folder reports setttings corrupted.\nApplicataion will exit.')
    sys.exit()
fp.close()

print "------------------------------------------------------"
print "PDF-merger-for-DS"
print "Created by Domen Zagar, zagar.domen@gmail.com"
print "------------------------------------------------------"
print "Creating reports for project", projectName
filenames = []
for f in onlyfiles:
    if f.endswith(".pdf"):
        foo = re.split('[ .]', f)[0]            # splits by whitespace or period
        if foo.isdigit() and int(foo) <= 9:
            filenames.append(f)


def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

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
        for filename in filenames:
            if int(re.split('[ .]', filename)[0]) in report[1]:
                append_pdf(PdfFileReader(mypath + "\\" +filename, 'rb'), merger)
                print "\t", filename
        merger.write(file(join(mypath, reportName), 'wb'))
        print reportName, "written."
    except:
        print reportName, "was not successfully written."
print "------------------"
print "Success!"
raw_input("Press any key to exit.")
