import pandas as pd

def clean_data(input_file, output_file):
    try:
        # 读取数据
        df = pd.read_excel(input_file, sheet_name='Sheet1')

        # 数据清洗
        df['数量'] = df['数量'].replace(-99, 0)
        df['数量'] = pd.to_numeric(df['数量'], errors='coerce').fillna(0)

        # 按学校和分类汇总
        result = df.groupby(['学校', '总分类'])['数量'].sum().unstack(fill_value=0)
        result = result.reset_index()

        # 保存结果
        result.to_excel(output_file, index=False)
        print(f"数据清洗完成，结果已保存到 {output_file}")
    except FileNotFoundError:
        print(f"错误: 文件 {input_file} 未找到。")
    except Exception as e:
        print(f"发生未知错误: {e}")

clean_data('C:/Users/HP/Desktop/南核数据.xlsx', 'C:/Users/HP/Desktop/clean_南核数据.xlsx')

def clean_data(input_file, output_file):
    try:
        # 读取数据
        df = pd.read_excel(input_file, sheet_name='Sheet1')

        # 数据清洗
        df['数量'] = df['数量'].replace(-99, 0)
        df['数量'] = pd.to_numeric(df['数量'], errors='coerce').fillna(0)

        # 按学校和分类汇总
        result = df.groupby(['学校', '总分类'])['数量'].sum().unstack(fill_value=0)
        result = result.reset_index()

        # 保存结果
        result.to_excel(output_file, index=False)
        print(f"数据清洗完成，结果已保存到 {output_file}")
    except FileNotFoundError:
        print(f"错误: 文件 {input_file} 未找到。")
    except Exception as e:
        print(f"发生未知错误: {e}")


# 使用示例
clean_data('C:/Users/HP/Desktop/北核数据.xlsx', 'C:/Users/HP/Desktop/clean_北核数据.xlsx')