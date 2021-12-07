import pandas as pd
import pickle as pkl
from typing import Optional
import pandas
import numpy
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule import Rule
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font
from openpyxl.formatting.rule import FormulaRule

def create_pkl_for_test():
    a = pkl.load(open("list_of_sublets.p", "rb"))
    data_for_tests = [x for x in a if len(x['post_text'])>20]
    random_400_posts_from_facebook = numpy.random.choice(data_for_tests, size=400, replace=True, p=None)
    pkl.dump(random_400_posts_from_facebook, open("data_utils/random_facebook_posts.pkl", "wb"))


def create_excel_for_tagging_data():
    posts = pkl.load(open("data_utils/random_facebook_posts.pkl", "rb"))
    file_path = 'data_utils/data_for_tagging.xlsx'
    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    start_idx, end_idx = 0,100
    for i in range(4): #["facebook_posts.1"]: #["1-100", "100-200", "200-300", "300-400"]:
        text = [x['post_text'] for x in posts[start_idx:end_idx]]
        post_id = [x['post_id'] for x in posts[start_idx:end_idx]]
        start_date = ["start_date" for x in post_id]
        end_date = ["end_date" for x in post_id]
        price = ["price" for x in post_id]
        location = ["location" for x in post_id]
        phone_number = ["phone_number" for x in post_id]

        # Create some Pandas dataframes from some data.
        from styleframe import StyleFrame
    # Create some Pandas dataframes from some data.
        df1 = pd.DataFrame({'Post_id': post_id,
                            'Text': text,
                            'Start_date': start_date,
                            'End_date': end_date,
                            'Price': price,
                            'Location': location,
                            'Phone_number': phone_number})
        name = "facebook_posts" + '_' + str(i+1)
        StyleFrame(df1).to_excel(writer, sheet_name=name).save()
        start_idx += 100
        end_idx += 100
    red_text = Font(color="9C0006")
    red_fill = PatternFill(bgColor="FFC7CE")
    dxf = DifferentialStyle(font=red_text, fill=red_fill)
    rule1 = Rule(type="containsText", operator="containsText", text="start_date", dxf=dxf)
    rule2 = Rule(type="containsText", operator="containsText", text="end_date", dxf=dxf)
    rule3 = Rule(type="containsText", operator="containsText", text="price", dxf=dxf)
    rule4 = Rule(type="containsText", operator="containsText", text="location", dxf=dxf)
    rule5 = Rule(type="containsText", operator="containsText", text="phone_number", dxf=dxf)

    rule1.formula = ['NOT(ISERROR(SEARCH("start_date",C2)))']
    rule2.formula = ['NOT(ISERROR(SEARCH("end_date",D2)))']
    rule3.formula = ['NOT(ISERROR(SEARCH("price",E2)))']
    rule4.formula = ['NOT(ISERROR(SEARCH("location",F2)))']
    rule5.formula = ['NOT(ISERROR(SEARCH("phone_number",G2)))']

    wb = load_workbook(file_path)
    yellowFill = PatternFill(start_color='00FFFF00',end_color = '00FFFF00',fill_type = 'solid')

    for ws in wb.worksheets:
        ws.conditional_formatting.add('C2:C101', rule1)
        ws.conditional_formatting.add('D2:D101', rule2)
        ws.conditional_formatting.add('E2:E101', rule3)
        ws.conditional_formatting.add('F2:F101', rule4)
        ws.conditional_formatting.add('G2:G101', rule5)
        ws.conditional_formatting.add('C1:C101', FormulaRule(formula=['ISBLANK(C1)'], stopIfTrue=True, fill=yellowFill))
        ws.conditional_formatting.add('D1:D101', FormulaRule(formula=['ISBLANK(D1)'], stopIfTrue=True, fill=yellowFill))
        ws.conditional_formatting.add('E1:E101', FormulaRule(formula=['ISBLANK(E1)'], stopIfTrue=True, fill=yellowFill))
        ws.conditional_formatting.add('F1:F101', FormulaRule(formula=['ISBLANK(F1)'], stopIfTrue=True, fill=yellowFill))
        ws.conditional_formatting.add('G1:G101', FormulaRule(formula=['ISBLANK(G1)'], stopIfTrue=True, fill=yellowFill))

        for column in [ws['C'], ws['D'], ws['E'], ws['F'], ws['G']]:
            for cell in column:
                    cell.fill = PatternFill(start_color='0000FF00', end_color='0000FF00', fill_type='solid')

        ws['C1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws['D1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws['E1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws['F1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws['G1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 100
        ws.column_dimensions['B'].heigth = 400
        for column in [ws.column_dimensions['C'], ws.column_dimensions['D'], ws.column_dimensions['E'], ws.column_dimensions['F'], ws.column_dimensions['G']]:
            column.width = 20

        wb.save(file_path)


def read_excel_end_create_dict_of_tagged_data(file_name:str="data_utils/data_for_tagging.xlsx", name:Optional[str] = None):
    df = read_excel(file_name, name=name)
    return get_dict_of_tagged_data(df)


def read_excel(file_name: str, name: str):
    return pandas.read_excel(file_name, sheet_name=name)


def get_dict_of_tagged_data(df):
    posts_data_dict = {'post_id': df['Post_id'].tolist(),
                      'post_text': df['Text'].tolist(),
                      'start_date': df['Start_date'].tolist(),
                      'end_date': df['End_date'].tolist(),
                      'price': df['Price'].tolist(),
                      'location': df['Location'].tolist(),
                      'phone_number': df['Phone_number'].tolist(),
                      }
    return posts_data_dict