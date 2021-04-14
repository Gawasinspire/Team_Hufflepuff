import csv

book_file = open('100_books.txt', 'r')
file_list = book_file.readlines()

author_list = []

cleaned_list = [item.replace("\n", "").replace(" â€", "").replace("Want to Read", "").replace("Rate this book", "") \
    .replace("1 of 5 stars", "").replace("2 of 5 stars", "").replace("5 of 5 stars", "").replace("3 of 5 stars", "") \
    .replace("4 of 5 stars", "")for item in file_list]

cleaned_list2 = list(filter(None, cleaned_list))

print(cleaned_list2)
    # for j in i:
    #     if j == 'by':
    #         # print("yes") # Test if the for loop works
    #         author_list.append(i)
    #     if j
# print(author_list)

    # per_page += 1
    # counter += 1
# counter = 1
# counter+=1
# for i in cleaned_list:
#     cleaned_list = cleaned_list.replace(i, "")
# cleaned_list = [item.replace("â€", "") for item in file_list]
# for i in file_list:
#     file_list.replace("\n", "")
# per_page = 1
# counter = 1
# while per_page != 100:
# print(book_file.readlines())

book_file.close()