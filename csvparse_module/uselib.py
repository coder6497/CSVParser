import csvparse

data_table = csvparse.get_data_table("table.csv", ',')
data_dict = csvparse.get_dict_from_table(data_table)
result = csvparse.get_parse_result(data_dict, 'id')

print(data_table)
print(data_dict)
print(result)