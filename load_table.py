'''
first part is for testing if data is mongo appropriate format
'''

# import json
#
# with open('data.json', 'r') as json_file:  # do not write as binary
#     data = json.load(json_file)
#
# print(len(data))
# print(type(data))
#
# for_mongo = []
# for key in data:
#     for_mongo.append({key: data[key]})
#
# # with open('paths_collection.json', 'w') as outfile:  # do not write as binary
# #     json.dump(for_mongo, outfile, indent=2)
# #
#
#
# print(len(for_mongo))
# print(type(for_mongo[100]))


'''
test if clean_df is proper format
'''
import json
import pandas as pd
with open('store_clean.h5', 'rb') as file:
    # Pickle the 'data' dictionary using the highest protocol available.
    clean_df = pd.read_hdf('store_clean.h5', 'table')

# print('---', type(clean_df))
# clean_dfT = clean_df.transpose()
# clean_dict = clean_dfT.to_dict()
#
# # print(type(clean_dict))
# # print(len(clean_dict))
#
# for_mongo_clean = []
# for key in clean_dict:
#     for_mongo_clean.append({key: clean_dict[key]})
#
# print(len(for_mongo_clean))
# print(type(for_mongo_clean))
# print(for_mongo_clean[100])
#
# with open('clean_collection_2.json', 'w') as outfile:  # do not write as binary
#     json.dump(for_mongo_clean, outfile, indent=2)
