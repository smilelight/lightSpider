from lightspider.baike import href
from lightspider.baike import info
from lightspider.baike import search

if __name__ == '__main__':
    word = '曹操'
    href_result = href.query(word)
    info_result = info.query(word)
    search_result = search.query(word)
    print(href_result)
    print(info_result)
    print(search_result)
