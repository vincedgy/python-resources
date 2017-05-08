
from openpyxl import load_workbook
FILENAME='test.ods'
wb = load_workbook(filename=FILENAME, read_only=True)
ws = wb[0]

for row in ws.rows:
    for cell in row:
        print(cell.value)