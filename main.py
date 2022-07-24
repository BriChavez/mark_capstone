# import aspose.words as aw
import PyPDF2
import os


# SET RESUME THEME YOU WOULD LIKE TO ACCESS
variable = 'DESIGNER'

# compile all the PDF filenames in that folder:
folder_path = f'data/Resume/{variable}'
# extract folder name based off the variable 
# ---(i know this is redundant, but I wrote it before the variable and i thought it to be clever, so its still in here)---
resume_folder = os.path.basename(folder_path).lower()


"""function to take all resume pdfs from an variable type folder and read them all into one big giant folder named for is folder type"""
# let us begin the extraction process
def extract_resumes():
    # set an empty variable to store our file names in as we read them
    pdfFiles = []
    # for loop to read through every file in our stated folder
    for filename in os.listdir(folder_path):
        # pull the files specifically that are pdfs
        if filename.endswith('.pdf'):
            # if they are, they get to join our cool list
            pdfFiles.append(filename)
    # the ritual naming of our pdf writer function so we can use it
    pdfWriter = PyPDF2.PdfFileWriter()
    # for loop to read through every file in our pdfFile list
    for filename in pdfFiles:
        # one at a time, we will open each file, we pick rb, aka read binary, cause thats normally how pdfs come
        pdfFileObj = open(f'{folder_path}/{filename}', 'rb')
        # name our reader and have it read the file we are on
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        # now, for each of the page numbers, starting from the first one to the files last page....
        for pageNum in range(0, pdfReader.numPages):
            # we will read each page at time
            pageObj = pdfReader.getPage(pageNum)
            # and add it to our writer
            pdfWriter.addPage(pageObj)
    # open a new pdf, we will file path it back to its original folder and name it after its folder name.
    pdfOutput = open(f'{folder_path}/{resume_folder}_resumes.pdf', 'wb')
    # now we write all the pages we have been storing to this new file
    pdfWriter.write(pdfOutput)
    # our work here is done.
    pdfOutput.close()

# runs the function to turn all pdfs in a stated folder into one giant pdf
extract_resumes()

def big_pdf2txt():
    all_resumes_pdf = open(f'{folder_path}/{resume_folder}_resumes.pdf', mode='rb')
    all_resumes_file = PyPDF2.PdfFileReader(all_resumes_pdf)

    text = ""
    for pageNum in range(0, all_resumes_file.numPages):
        page = all_resumes_file.getPage(pageNum)
        text += page.extract_text() + "\n"
    text_file = open(f'{folder_path}/{resume_folder}_resumes.txt', "w")
    text_file.write(text)
    text_file.close()


big_pdf2txt()
