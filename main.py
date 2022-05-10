import shutil
import make_dir
import split_pdf
import send_email

#====================================MAKE DIRECTORY=======================================#
make_dir.create_dir()
try:
    #move payslips.pdf file to the new folder
    shutil.move(make_dir.parent_dir + '\\payslips.pdf', make_dir.path) 
    print(f'payslips.pdf moved to the folder: {make_dir.directory}')
except Exception as e:
    print(e)
#==================================SPLIT AND EXTRACT PDF==================================#
split_pdf.extract_payslips()
#======================================SEND EMAIL=========================================#
send_email.email_payslip()
#======================================EXIT APP===========================================#
print("")
input('Press Enter to close the program!')
quit()