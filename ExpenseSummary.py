
import decimal
import operator

class ExpenseType(object):
    colm_id_Filename = 0
    colm_id_TransDate = 1
    colm_id_PostDate = 2
    colm_id_Business = 3
    colm_id_Loc = 4
    colm_id_RefNum = 5
    colm_id_AccNum = 6
    colm_id_Amount = 7
    colm_id_Recipt = 8
    colm_id_Type = 9

    def __init__(self, Filename, TransDate, PostDate, Business, Loc, RefNum, AccNum, Amount, Recipt, Type):
        self.Filename = Filename
        self.TransDate = TransDate
        self.PostDate = PostDate
        self.Business = Business
        self.Loc = Loc
        self.RefNum = RefNum
        self.AccNum = AccNum
        self.Amount = Amount
        self.Recipt = Recipt
        self.Type = Type
    
    def __init__(self, CsvData):
        self.Filename = CsvData[self.colm_id_Filename].strip()
        self.TransDate = CsvData[self.colm_id_TransDate].strip()
        self.PostDate = CsvData[self.colm_id_PostDate].strip()
        self.Business = CsvData[self.colm_id_Business].strip()
        self.Loc = CsvData[self.colm_id_Loc].strip()
        self.RefNum = CsvData[self.colm_id_RefNum].strip()
        self.AccNum = CsvData[self.colm_id_AccNum].strip()
        self.Amount = decimal.Decimal(CsvData[self.colm_id_Amount].strip())
        self.Recipt = CsvData[self.colm_id_Recipt].strip()
        self.Type = CsvData[self.colm_id_Type].strip()
        

parse_files = (
    '/home/xxx/mergedcc_classified.csv',
    '/home/xxx/cashdebit_classified.csv')



classified_expenses = {}

for file in parse_files:
    with open(file, encoding='cp1252') as f:
        lines = f.readlines()
    
    for line in lines[1:]:
        split_line = line.split(',')
        expense_data = ExpenseType(CsvData=split_line)
        
        if expense_data.Type not in classified_expenses:
            classified_expenses[expense_data.Type] = []
        classified_expenses[expense_data.Type].append(expense_data)
    
out_file = open('/home/xxx/unified_expenses.csv', 'w', encoding='utf-8')
    
out_file.write('Expenses Summary\n')
summary_total = decimal.Decimal(0)  
for expense_type in classified_expenses:
    expense_type_total = decimal.Decimal(0)
    for expense_item in classified_expenses[expense_type]:
        expense_type_total = expense_type_total + expense_item.Amount
    out_file.write('{0},{1}\n'.format(expense_type, expense_type_total))
    summary_total = summary_total + expense_type_total
out_file.write('\n')
out_file.write('Total,{0}\n'.format(summary_total))

out_file.write('\n\n')
out_file.write('Detailed Expenses,\n\n')
for expense_type in classified_expenses:
    sorted_expense = sorted(classified_expenses[expense_type], key=operator.attrgetter('TransDate'))
    out_file.write('\n')
    out_file.write('{0} Expenses,\n'.format(expense_type))
    out_file.write('Source,Date,Business,Location,Amount,\n')
    expense_type_total = decimal.Decimal(0)
    for expense_item in sorted_expense:
        out_file.write('{0},{1},{2},{3},{4},\n'.format(
            expense_item.Filename, 
            expense_item.TransDate, 
            expense_item.Business,
            expense_item.Loc,
            expense_item.Amount))
        expense_type_total = expense_type_total + expense_item.Amount
    out_file.write('\n')
    out_file.write(',,,Total,{0},\n\n'.format(expense_type_total))

out_file.close()
    
    
    
    