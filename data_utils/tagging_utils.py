import pandas as pd
import pickle as pkl
import pandas
import numpy
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule import Rule
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font
from openpyxl.formatting.rule import FormulaRule


def create_excel_for_tagging_data():
    a = pkl.load(open("list_of_sublets.p", "rb"))
    sublest = {}
    range_start, range_end = 0, 300
    file_path = 'data_utils/data_for_tagging.xlsx'
    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    for name in ["Eliya", "Shaya", "Sharvit", "Avishay"]:
        sublest[name] = a[range_start:range_end]
        range_start += 300
        range_end += 300
        sublets = [x['post_text'] for x in sublest[name] if len(x['post_text'])>20]
        b = numpy.random.choice(sublets, size=100, replace=True, p=None)
        c = range(len(b))
        start_date = ["start_date" for x in c]
        end_date = ["end_date" for x in c]
        price = ["price" for x in c]
        location = ["location" for x in c]
        # Create some Pandas dataframes from some data.
        from styleframe import StyleFrame
    # Create some Pandas dataframes from some data.
        df1 = pd.DataFrame({'Idx': c,
                            'Text': b,
                            'Start_date': start_date,
                            'End_date': end_date,
                            'Price': price,
                            'Location': location})
        StyleFrame(df1).to_excel(writer, sheet_name=name).save()

    red_text = Font(color="9C0006")
    red_fill = PatternFill(bgColor="FFC7CE")
    dxf = DifferentialStyle(font=red_text, fill=red_fill)
    rule1 = Rule(type="containsText", operator="containsText", text="start_date", dxf=dxf)
    rule2 = Rule(type="containsText", operator="containsText", text="end_date", dxf=dxf)
    rule3 = Rule(type="containsText", operator="containsText", text="price", dxf=dxf)
    rule4 = Rule(type="containsText", operator="containsText", text="location", dxf=dxf)


    rule1.formula = ['NOT(ISERROR(SEARCH("start_date",C2)))']
    rule2.formula = ['NOT(ISERROR(SEARCH("end_date",D2)))']
    rule3.formula = ['NOT(ISERROR(SEARCH("price",E2)))']
    rule4.formula = ['NOT(ISERROR(SEARCH("location",F2)))']
    wb = load_workbook(file_path)
    yellowFill = PatternFill(start_color='00FFFF00',end_color = '00FFFF00',fill_type = 'solid')

    for ws in wb.worksheets:
        ws.conditional_formatting.add('C2:C101', rule1)
        ws.conditional_formatting.add('D2:D101', rule2)
        ws.conditional_formatting.add('E2:E101', rule3)
        ws.conditional_formatting.add('F2:F101', rule4)
        ws.conditional_formatting.add('C1:C101', FormulaRule(formula=['ISBLANK(C1)'], stopIfTrue=True, fill=yellowFill))
        ws.conditional_formatting.add('D1:D101', FormulaRule(formula=['ISBLANK(D1)'], stopIfTrue=True, fill=yellowFill))
        ws.conditional_formatting.add('E1:E101', FormulaRule(formula=['ISBLANK(E1)'], stopIfTrue=True, fill=yellowFill))
        ws.conditional_formatting.add('F1:F101', FormulaRule(formula=['ISBLANK(F1)'], stopIfTrue=True, fill=yellowFill))

        for collumn in [ws['C'], ws['D'], ws['E'], ws['F']]:
            for cell in collumn:
                    cell.fill = PatternFill(start_color='0000FF00', end_color='0000FF00', fill_type='solid')

        ws['C1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws['D1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws['E1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws['F1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws.column_dimensions['B'].width = 100
        ws.column_dimensions['B'].heigth = 400
        for collumn in [ws.column_dimensions['C'], ws.column_dimensions['D'], ws.column_dimensions['E'], ws.column_dimensions['F']]:
            collumn.width = 20

        wb.save(file_path)


def read_excel(name:str, file_name:str='data_utils/data_for_tagging.xlsx'):
    return pandas.read_excel(file_name, sheet_name=name)
