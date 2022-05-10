import os


parent_dir = os.getcwd() # Parent Directory path
office = input('Enter the name of the office: ').capitalize()
month = input('Enter the pay month in word: ').capitalize()
directory = office+"_"+month
path = os.path.join(parent_dir, directory) # Path to where new payslip files will be saved


def create_dir():
    '''Creates a salary month directory'''
    if not os.path.isdir(path):
        try: 
            os.mkdir(path) 
            print(f'New directory {directory} created in {parent_dir}')
        except OSError as error: 
            print(error)
    return
    # print(os.listdir(path))