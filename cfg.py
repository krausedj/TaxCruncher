
std_colms = {'TransDate':(8, 19),
             'PostDate': (19, 30),
             'Business': (30, 55),
             'Location': (55, 70),
             'RefNum':   (90, 94),
             'ActNum':   (101, 105),
             'Amount':   (105, 131)}

parse_files = {
    '/home/xxx/eStmt_2016-01-20.txt':{
        'Columns':std_colms,
        'ParseRanges':((61,62), (110,120))},
    '/home/xxx/eStmt_2016-02-20.txt':{
        'Columns':std_colms,
        'ParseRanges':((62,62), (110,140))},
    '/home/xxx/eStmt_2016-03-20.txt':{
        'Columns':std_colms,
        'ParseRanges':((61,62), (110,139))},
    '/home/xxx/eStmt_2016-04-20.txt':{
        'Columns':std_colms,
        'ParseRanges':((58,62), (110,119))},
    '/home/xxx/eStmt_2016-05-20.txt':{
        'Columns':std_colms,
        'ParseRanges':((54,62), (110,132))},
    '/home/xxx/eStmt_2016-06-20.txt':{
        'Columns':std_colms,
        'ParseRanges':((61,62), (110,142))},
    '/home/xxx/eStmt_2016-07-20.txt':{
        'Columns':std_colms,
        'ParseRanges':((61,62), (110,133))},
    '/home/xxx/eStmt_2016-08-20.txt':{
        'Columns':std_colms,
        'ParseRanges':((60,61), (110,127), (131,131))},
    '/home/xxx/eStmt_2016-09-20.txt':{
        'Columns':std_colms,
        'ParseRanges':((59,62), (110,131), (133,147))},
    '/home/xxx/eStmt_2016-10-20.txt':{
        'Columns':std_colms,
        'ParseRanges':((61,62), (110,136))},
    '/home/xxx/eStmt_2016-11-20.txt':{
        'Columns':std_colms,
        'ParseRanges':((58,62), (110,123))},
    '/home/xxx/eStmt_2016-12-20.txt':{
        'Columns':std_colms,
        'ParseRanges':((54,62), (110,139))},             
    '/home/xxx/eStmt_2017-01-20.txt':{
        'Columns':std_colms,
        'ParseRanges':((61,62), (110,120))},     
}
