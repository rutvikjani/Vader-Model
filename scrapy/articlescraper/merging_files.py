import pandas as pd

df = pd.read_csv(r'D:\python\scrapy\articlescraper\Output Data.csv')

df.to_excel('Results.xlsx', index=False)


df2 = pd.read_excel(r'D:\python\scrapy\articlescraper\Sorted Data Structure.xlsx')
df1 = pd.read_excel(r'D:\python\scrapy\articlescraper\Results.xlsx')

merged_excel = pd.merge(df2, df1, on='URL_ID', how='left')

merged_excel.to_excel("Output Data Structure.xlsx", index=False)
