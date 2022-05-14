import os
import fitz
from load_gui import path
from db import create_connection, select_all_employees

#https://pymupdf.readthedocs.io/en/latest/faq.html#how-to-split-single-pages



def extract_payslips():
    employees = select_all_employees(create_connection)
    src = fitz.open(os.path.join(path, 'payslips.pdf'))
    num = 1
    print('Splitting and extracting pdf...')
    for pg in src:  # for each page in input
        r = pg.rect  # input page rectangle

        r1 = fitz.Rect(r.tl, r.width*0.43,r.height)  # left rect
        r2 = fitz.Rect(r.width*0.43,0, r.br) # right rect
        r1_text = pg.get_text(clip=r1)
        r2_text = pg.get_text(clip=r2)
        r1_name = [employee[3][:len(employee[3])-4] for employee in employees if employee[0] in r1_text]
        r2_name = [employee[3][:len(employee[3])-4] for employee in employees if employee[0] in r2_text]
        # r2_name = [name[:len(name)-4] for name in staffs.keys() if name[:len(name)-4] in r2_text]

        #-----CREATE R1 PAYSLIP-------
        new_doc = fitz.open()  # empty output PDF
        page = new_doc.new_page(-1, width=r1.width, height=r1.height)   # new output page with rx dimensions
        page.show_pdf_page(page.rect, src, pg.number, clip = r1) # fill all new page with the image # input document # input page number  # which part to use of input page
        try:
            new_doc.save(f'{path}\\{r1_name[0]}.pdf', garbage=3, deflate=True) # eliminate duplicate objects # compress stuff where possible
        except IndexError:
            new_doc.save(f'{path}\\payslip{num}.pdf', garbage=3, deflate=True) # eliminate duplicate objects # compress stuff where possible
            num +=1
        finally:
            new_doc.close()

        #-----CREATE R2 PAYSLIP-------
        new_doc = fitz.open()  # empty output PDF
        page = new_doc.new_page(-1, width=r2.width, height=r2.height)
        page.show_pdf_page(page.rect, src, pg.number, clip = r2)
        try:
            new_doc.save(f'{path}\\{r2_name[0]}.pdf', garbage=3, deflate=True)
        except IndexError:
            new_doc.save(f'{path}\\payslip{num}.pdf', garbage=3, deflate=True)
            num +=1
        finally:
            new_doc.close()
    print('Splitting and extraction done!')
    return

# extract_payslips()