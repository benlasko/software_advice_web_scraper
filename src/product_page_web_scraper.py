from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time
import pymongo
from pymongo import MongoClient

if __name__ == "__main__":
    response = requests.get('https://www.softwareadvice.com/categories/')
    html = response.content
    soup = bs(html,"lxml")


    category_urls = []

    a_tag_soup = soup('a')

    for h2s in soup('h2'):
        h2s.decompose()

    category_url_index_all = -16
    category_url_index_selection = 13

    for text in a_tag_soup[10:category_url_index_selection]:
        url = ''
        str_text = str(text)[28:]

        for ch in str_text:
            if ch != '"':
                url += ch
            else:
                break

        url += 'p/all/'
        if url != 'p/all/':
            category_urls.append(url)


    print(len(category_urls))

    for url in category_urls:
        print(url)


    all_urls = []

    for url in category_urls:
        response = requests.get(url)
        # time.sleep(1)
        html = response.content
        url_soup = bs(html)

        for url in url_soup('a', href=True):
            all_urls.append(url['href'])


    product_urls = []

    for url in all_urls:
        if url[-3] == 'l' and url not in product_urls and url[-1] != 'g':
            product_urls.append(url)


    print(len(product_urls))

    for url in product_urls:
        print(url)


    all_names = []
    all_avg_reviews = []
    all_total_reviews = []
    all_total_recommendations = []
    all_frontrunner_or_not = []
    all_overviews = []
    all_guides_featured_in = []


    product_url_scrape_selection = product_urls[:20]
    product_url_scrape_all = product_urls

    for i,v in enumerate(product_url_scrape_selection):
        while i < len(product_url_scrape_selection):
            url = v
            response = requests.get(url)
            # time.sleep(1)
            html = response.content
            soup = bs(html,"lxml")


            try:
                if soup(class_='seo-header'):
                    seo_header_soup = soup(class_='seo-header')
                    seo_header_name_lst = [string.get_text(strip=True) for string in seo_header_soup]
                    seo_header_name = seo_header_name_lst[0]

                    all_names.append(seo_header_name)
                else:

                    h1_name_soup = soup('h1', class_ = 'bold')
                    h1_tag_name_list = [string.get_text(strip=True) for string in h1_name_soup]
                    h1_tag_name = h1_tag_name_list[0]

                    all_names.append(h1_tag_name)
            except:
                all_names.append('')


            try:
                if soup('span', class_ = 'rank-average strong'):
                    avg_review_soup = soup('span', class_ = 'rank-average strong')
                    spans = [string.get_text(strip=True) for string in avg_review_soup]
                    try:
                        float(spans[0])
                        avg_review = float(spans[0])
                        all_avg_reviews.append(avg_review)
                    except ValueError:
                        all_avg_reviews.append(0)

                else:
                    lead_class_soup = soup(class_='lead')
                    lead_class_avg_review_lst = [string.get_text(strip=True) for string in lead_class_soup]
                    avg_review = float(lead_class_avg_review_lst[0])

                    all_avg_reviews.append(avg_review)
            except:
                all_avg_reviews.append(0)


            a_tag_strings = [string.get_text(strip=True) for string in a_tag_soup]
            complete = False

            for string in a_tag_strings:
                if string[-7:] == 'reviews':
                    total_reviews = string[:-7]
                    try:
                        int(total_reviews)
                        all_total_reviews.append(total_reviews)
                        complete = True
                        break
                    except:
                        all_total_reviews.append(0)

            if complete == False:
                for string in a_tag_strings:
                        reviews_text = soup('p')
                        reviews = [string.get_text(strip=True) for string in reviews_text]
                        reviews_string = str(reviews[4:5])
                        total_reviews = reviews_string[reviews_string.find('(')+1:reviews_string.find(')')]
                        all_total_reviews.append(total_reviews)
                        break


            if soup('p', class_='lead'):
                total_recommendations = ''

                p_lead_soup = soup('p', class_='lead')
                p_lead_strings = str(p_lead_soup[1])
                total_rec_ints = [ch for ch in p_lead_strings[23:27] if ch.isdigit()]

                for ch in total_rec_ints:
                    total_recommendations += ch

                if len(total_recommendations) > 0:
                    all_total_recommendations.append(total_recommendations)
                else:
                    all_total_recommendations.append(0)
            else:
                strong_soup = soup('strong')
                strong_strings = [string.get_text(strip=True) for string in strong_soup]
                if len(strong_strings) > 0:
                    total_recommendations_in_last_30_days = strong_strings[0]

                    if total_recommendations_in_last_30_days.isdigit():
                        all_total_recommendations.append(total_recommendations_in_last_30_days)
                    else:
                        all_total_recommendations.append(0)
                else:
                    all_total_recommendations.append(0)


            frontrunner_soup = soup('span', class_ = 'ui strong')

            if soup(class_='details__frontrunners--tag'):
                all_frontrunner_or_not.append('Yes')
            else:
                if 'FrontRunner' in str(frontrunner_soup):
                    all_frontrunner_or_not.append('Yes')
                else:
                    all_frontrunner_or_not.append('No')


            if soup(id='overview-text'):
                overview_soup = soup(id='overview-text')
                overview = str(overview_soup)[58:]
                all_overviews.append(overview)
            else:
                overview = ''
                overview_soup = soup('p')
                overview_str = [string.get_text(strip=True) for string in overview_soup]
                for string in overview_str[10:20]:
                    if len(string) > 30:
                        overview += string

                all_overviews.append(overview)


            if soup('li', class_ ='chips-chip'):
                guide_soup = soup('li', class_ ='chips-chip')
                guides_featured_in = [string.get_text(strip=True) for string in guide_soup]
                all_guides_featured_in.append(guides_featured_in)
            else:
                all_guides_featured_in.append('None.')


            i = i+1


    names = pd.Series(all_names)
    avg_reviews = pd.Series(all_avg_reviews)
    total_reviews = pd.Series(all_total_reviews)
    total_recommendations = pd.Series(all_total_recommendations)
    frontrunner_or_not = pd.Series(all_frontrunner_or_not)
    overviews = pd.Series(all_overviews)
    guides_featured_in = pd.Series(all_guides_featured_in)

    frame = {'Name': names,
            'Avg Stars/5': avg_reviews,
            'Total Reviews': total_reviews,
            'Recommendations': total_recommendations,
            'Ever a FrontRunner': frontrunner_or_not,
            'Product Overview': overviews,
            'Guides Featured In': guides_featured_in}

    df = pd.DataFrame(frame)

    df_no_dups = df.drop_duplicates(subset='Name', keep="first")
    df_no_nan_names = df_no_dups[df_no_dups['Name'].notna()]
    df_no_nan_names.reset_index(level=0, inplace=True)
    softwareadvice_product_page_scrape = df_no_nan_names.drop(['index'], axis=1)

    softwareadvice_product_page_scrape["Recommendations"].replace({"": 0}, inplace=True)
    softwareadvice_product_page_scrape["Total Reviews"].replace({"": 0}, inplace=True)
    softwareadvice_product_page_scrape['Recommendations'] = softwareadvice_product_page_scrape['Recommendations'].astype(int)
    softwareadvice_product_page_scrape['Total Reviews'] = softwareadvice_product_page_scrape['Total Reviews'].astype(int)

    print(softwareadvice_product_page_scrape)


    softwareadvice_product_page_scrape.to_csv('softwareadvice_product_page_scrape.csv')

    to_mongo_df = pd.read_csv('softwareadvice_product_page_scrape.csv')

    connection_string = 'pymongo_driver_connection_string_here'

    client =  MongoClient(connection_string)

    db = client['softare_advice_scrape_db']
    collection = db['softare_advice_scrape_coll']

    to_mongo_df.reset_index(inplace=True)
    to_mongo_df_dict = to_mongo_df.to_dict('records')

    collection.insert_many(to_mongo_df_dict)
