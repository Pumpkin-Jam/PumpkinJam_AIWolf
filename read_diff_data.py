def read_diff_data(diff_data):
    data_list = []
    for index, row in diff_data.iterrows():
        data_list.append((index, row))
    
    return data_list