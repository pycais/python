"""
@author: cs
@version: 1.0.0
@file: pagnator.py
@time: 2024/6/7 7:54
@description: 
"""
import pandas as pd


def get_search_results(file_path, current_page, page_size, douban_id):
    # 逐块读取数据，提高内存使用效率
    chunk_size = 100000
    total_count = 0
    filtered_data = []

    # 读取数据块
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # 过滤数据
        filtered_chunk = chunk[chunk['douban_id'] == douban_id]
        total_count += len(filtered_chunk)
        filtered_data.append(filtered_chunk)

    # 将过滤后的数据合并成一个DataFrame
    if filtered_data:
        filtered_data = pd.concat(filtered_data)
    else:
        filtered_data = pd.DataFrame(columns=['movie_name', 'image_name', 'douban_id', 'image_path', 'image_type'])

    # 计算分页起始位置和结束位置
    start_index = (current_page - 1) * page_size
    end_index = start_index + page_size

    # 分页数据
    paged_data = filtered_data.iloc[start_index:end_index]

    # 转换为字典格式
    result_data = paged_data.to_dict(orient='records')

    # 返回结果
    return {
        'data': result_data,
        'total': total_count
    }


if __name__ == '__main__':
    # 示例使用
    file_path = 'path_to_your_file.csv'
    current_page = 1
    page_size = 10
    douban_id = 'some_douban_id'

    results = get_search_results(file_path, current_page, page_size, douban_id)
    print(results)
