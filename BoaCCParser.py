
import collections
import cfg

parse_files = cfg.parse_files

out_file = open(cfg.boa_cc_outfile, 'w')
data_csv = 'Filename,Transaction Date,Post Date,Business,Location,Reference Number,Account Number, Amount\n'
out_file.write(data_csv)

for file in sorted(parse_files):
    with open(file, encoding='cp1252') as f:
        lines = f.readlines()
    for parse_range in parse_files[file]['ParseRanges']:
        colm_info = parse_files[file]['Columns']
        for parsed_line in lines[parse_range[0]-1:parse_range[1]]:
            if parsed_line not in ('','\n'):
                data_TransDate = parsed_line[colm_info['TransDate'][0]-1:colm_info['TransDate'][1]-1].strip()
                data_PostDate = parsed_line[colm_info['PostDate'][0]-1:colm_info['PostDate'][1]-1].strip()
                data_Business = parsed_line[colm_info['Business'][0]-1:colm_info['Business'][1]-1].strip()
                data_Location = parsed_line[colm_info['Location'][0]-1:colm_info['Location'][1]-1].strip()
                data_RefNum = parsed_line[colm_info['RefNum'][0]-1:colm_info['RefNum'][1]-1].strip()
                data_ActNum = parsed_line[colm_info['ActNum'][0]-1:colm_info['ActNum'][1]-1].strip()
                data_Amount = parsed_line[colm_info['Amount'][0]-1:colm_info['Amount'][1]-1].strip()
                print(parsed_line)
                print('Transation Date: {0}'.format(data_TransDate))
                print('Post Date: {0}'.format(data_PostDate))
                print('Business: {0}'.format(data_Business))
                print('Location: {0}'.format(data_Location))
                print('Reference Number: {0}'.format(data_RefNum))
                print('Account Number: {0}'.format(data_ActNum))
                print('Amount: {0}'.format(data_Amount))
                data_csv = '{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(file,data_TransDate,data_PostDate,data_Business,data_Location,data_RefNum,data_ActNum,data_Amount)
                out_file.write(data_csv)

out_file.close()
    
