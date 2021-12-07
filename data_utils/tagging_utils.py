import pickle as pkl
from datetime import datetime
from typing import Optional

import numpy
import pandas
import pandas as pd
from openpyxl import load_workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.formatting.rule import Rule
from openpyxl.styles import PatternFill, Font
from openpyxl.styles.differential import DifferentialStyle

from ParsingFunctions import searching_for_sublet
from unit_tests.TestsDB import TestGroundTruth, TestRawInput, Test


def create_pkl_for_test():
    a = pkl.load(open("dict_of_sublets.p", "rb"))
    data_for_tests = []
    for group_id, posts in a.items():
        for post in posts:
            if len(post['post_text']) > 20 and not searching_for_sublet(post.get('post_title', ''), post['post_text']):
                post['group_id'] = group_id
                data_for_tests.append(post)
    random_400_posts_from_facebook = numpy.random.choice(data_for_tests, size=min(400, len(data_for_tests)),
                                                         replace=False, p=None)
    pkl.dump(random_400_posts_from_facebook, open("data_utils/random_facebook_posts.pkl", "wb"))


def create_excel_for_tagging_data():
    posts = pkl.load(open("data_utils/random_facebook_posts.pkl", "rb"))
    file_path = 'data_utils/data_for_tagging.xlsx'
    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    start_idx, end_idx = 0, 100
    for i in range(4):  # ["facebook_posts.1"]: #["1-100", "100-200", "200-300", "300-400"]:
        text = [x['post_text'] for x in posts[start_idx:end_idx]]
        post_id = [x['post_id'] for x in posts[start_idx:end_idx]]
        start_date = ["start_date" for x in post_id]
        end_date = ["end_date" for x in post_id]
        price = ["price" for x in post_id]
        location = ["location" for x in post_id]
        phone_number = ["phone_number" for x in post_id]
        rooms = ["rooms" for x in post_id]

        # Create some Pandas dataframes from some data.
        from styleframe import StyleFrame
        # Create some Pandas dataframes from some data.
        df1 = pd.DataFrame({'Post_id': post_id,
                            'Text': text,
                            'Start_date': start_date,
                            'End_date': end_date,
                            'Price': price,
                            'Location': location,
                            'Phone_number': phone_number,
                            "Rooms": rooms})
        name = "facebook_posts" + '_' + str(i + 1)
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
    rule6 = Rule(type="containsText", operator="containsText", text="rooms", dxf=dxf)

    rule1.formula = ['NOT(ISERROR(SEARCH("start_date",C2)))']
    rule2.formula = ['NOT(ISERROR(SEARCH("end_date",D2)))']
    rule3.formula = ['NOT(ISERROR(SEARCH("price",E2)))']
    rule4.formula = ['NOT(ISERROR(SEARCH("location",F2)))']
    rule5.formula = ['NOT(ISERROR(SEARCH("phone_number",G2)))']
    rule6.formula = ['NOT(ISERROR(SEARCH("rooms",H2)))']

    wb = load_workbook(file_path)
    yellowFill = PatternFill(start_color='00FFFF00', end_color='00FFFF00', fill_type='solid')

    for ws in wb.worksheets:
        ws.conditional_formatting.add('C2:C101', rule1)
        ws.conditional_formatting.add('D2:D101', rule2)
        ws.conditional_formatting.add('E2:E101', rule3)
        ws.conditional_formatting.add('F2:F101', rule4)
        ws.conditional_formatting.add('G2:G101', rule5)
        ws.conditional_formatting.add('H2:H101', rule6)
        ws.conditional_formatting.add('C1:C101', FormulaRule(formula=['ISBLANK(C1)'], stopIfTrue=True, fill=yellowFill))
        ws.conditional_formatting.add('D1:D101', FormulaRule(formula=['ISBLANK(D1)'], stopIfTrue=True, fill=yellowFill))
        ws.conditional_formatting.add('E1:E101', FormulaRule(formula=['ISBLANK(E1)'], stopIfTrue=True, fill=yellowFill))
        ws.conditional_formatting.add('F1:F101', FormulaRule(formula=['ISBLANK(F1)'], stopIfTrue=True, fill=yellowFill))
        ws.conditional_formatting.add('G1:G101', FormulaRule(formula=['ISBLANK(G1)'], stopIfTrue=True, fill=yellowFill))
        ws.conditional_formatting.add('H1:H101', FormulaRule(formula=['ISBLANK(H1)'], stopIfTrue=True, fill=yellowFill))

        for column in [ws['C'], ws['D'], ws['E'], ws['F'], ws['G'], ws['H']]:
            for cell in column:
                cell.fill = PatternFill(start_color='0000FF00', end_color='0000FF00', fill_type='solid')

        ws['C1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws['D1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws['E1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws['F1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws['G1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws['H1'].fill = PatternFill(start_color='00FFFFFF', end_color='00FFFFFF', fill_type='solid')
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 100
        ws.column_dimensions['B'].heigth = 400
        for column in [ws.column_dimensions['C'], ws.column_dimensions['D'], ws.column_dimensions['E'],
                       ws.column_dimensions['F'], ws.column_dimensions['G'], ws.column_dimensions['H']]:
            column.width = 20

        wb.save(file_path)


def read_excel_and_create_tagged_df(file_name: str = "data_utils/data_for_tagging.xlsx",
                                    name: Optional[str] = None):
    df = read_excel(file_name, name=name)
    return pandas.concat([sheet_df for sheet_df in df.values()])


def read_excel(file_name: str, name: str):
    return pandas.read_excel(file_name, sheet_name=name)


def create_tests_from_tagged_excel():
    def add_zero(x):
        if x[0] != '0':
            return '0' + x
        return x

    def date_str_to_datetime(date_str):
        if type(date_str) == datetime:
            date_str = date_str.strftime('%m/%d/%Y')
        if date_str is None:
            return None
        date_str = date_str.replace('.', '/')
        if '/' not in date_str:
            return None
        d, m, y = date_str.split('/')
        if len(d) == 1:
            d = '0' + d
        if len(m) == 1:
            m = '0' + m
        if len(y) == 2:
            y = '20' + y
        return datetime.strptime('/'.join([d, m, y]), '%d/%m/%Y').date()

    tagged_data_df = read_excel_and_create_tagged_df()
    tagged_data_df = tagged_data_df.where(pd.notnull(tagged_data_df), None)
    posts = pkl.load(open("data_utils/random_facebook_posts.pkl", "rb"))
    post_id_to_post = {str(x['post_id']): x for x in posts}
    tests_db = []
    for _, tagged_item in tagged_data_df.iterrows():

        post = post_id_to_post[str(tagged_item['Post_id'])]
        price = tagged_item['Price']
        if type(price) == int:
            price = [price]
        elif price is None or 'price' in price:
            price = None
        else:
            price = [int(p) for p in price.split(',')]
        phone_number = str(tagged_item['Phone_number'])
        if phone_number is None or 'phone' in phone_number:
            phone_number = None
        elif phone_number.isnumeric():
            phone_number = [add_zero(phone_number)]
        else:
            phone_number = [add_zero(x) for x in phone_number.split(',')]

        start_date = date_str_to_datetime(tagged_item['Start_date'])
        end_date = date_str_to_datetime(tagged_item['End_date'])
        rooms = tagged_item['Rooms']
        if type(rooms) in [int, float]:
            rooms = float(rooms)
        else:
            rooms = None
        location = tagged_item['Location']
        if 'location' in location:
            location = None
        gt = TestGroundTruth(start_date=start_date,
                             end_date=end_date,
                             price=price, location=location,
                             phone_number=phone_number, rooms=rooms)
        raw_input = TestRawInput(group_id=post['group_id'], location=post.get('location'),
                                 post_id=post['post_id'], price=post.get('price'),
                                 text=post['text'], title=post.get('title', ''),
                                 post_time=post['time'])
        test = Test(gt=gt, raw_input=raw_input)
        if test.is_test_tagged():
            tests_db.append(test)
    pkl.dump(tests_db, open('unit_tests/test_db.p', 'wb'))


if __name__ == '__main__':
    # create_pkl_for_test()
    # create_excel_for_tagging_data()
    create_tests_from_tagged_excel()
