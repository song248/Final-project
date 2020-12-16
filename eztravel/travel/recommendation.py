import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend_place(region, attraction):
    region_list = ['서울', '경기', '강원', '충북', '충남', 
                    '대전', '광주', '전남', '전북', '제주',
                    '인천', '부산', '울산', '대구', '경북']

    for i in region_list:
        if i == region:
            df = pd.read_csv("C:/Users/songtg/Desktop/Final_project/eztravel/data_file/region_csv/"+region+".csv", index_col='attr', encoding='CP949')
            print('success read')
    similarity = cosine_similarity(df, df)
    similarity_df = pd.DataFrame(similarity, index=df.index, columns=df.index)
    similar_attr = similarity_df[attraction].sort_values(ascending=False)[1:10]

    count = 0
    for i in range(9):
        if list(similar_attr)[i]>0.7:
            count+=1
            
    similarity_list = []
    for i in range(count):
        similarity_list.append(similar_attr.index[i])
    print(similarity_list)
    return similarity_list
