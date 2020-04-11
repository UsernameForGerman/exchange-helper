import time
import random

from celery.utils.log import get_task_logger

from news.models import Company, Stock

from scraping.quering import get_soup


company_url = 'quote/'
base_url = 'https://finance.yahoo.com/'
stocks_url = 'most-active/'

logger = get_task_logger('scraping')


def sleep():
    time.sleep(3 + random.random() * 3)

def to_billions(value):
    float_value = float(value[0:-1])
    if value[-1] == 'M':
        return round(float_value / 1000, 3)
    elif value[-1] == 'B':
        return float(float_value)
    elif value[-1] == 'T':
        return round(float_value * 1000, 3)

def scrap_companies(dont_stop=False):
    logger.info('Start scraping manufacturers')

    soup = get_soup(base_url + 'most-active/?count=200')
    # print(soup)
    # sleep()


    # links = [span.find('a') for span in soup.find_all('span', attrs={"data-slot": "makeslist.item"})]
    companies = list(tr for tr in soup.find('table').find_all('tr'))

    random.shuffle(companies)
    total_count = 0

    for company in companies:
        company_obj = None
        created = False
        for child in company.children:
            if child.get('aria-label') == "Symbol":
                if company_obj is None:
                    ticker = child.find('a').text
                    #print(ticker)
                    try:
                        company_obj = Company.objects.get(ticker=ticker)
                    except Company.DoesNotExist:
                        company_obj = Company(ticker=ticker)
                        created = True
            elif child.get('aria-label') == 'Name':
                if company_obj is not None:
                    name = child.text
                    company_obj.name = name
                #print(child.text)
            elif child.get('aria-label') == "Market Cap":
                market_cap = to_billions(child.find('span').text)
                #print(market_cap)
                if company_obj is not None and market_cap >= 0.250:
                    company_obj.enterprise_value = market_cap
                    if created:
                        company_obj.save()
                    else:
                        company_obj.save(update_fields=['enterprise_value'])
                break

        print(company_obj)
        total_count += 1





    logger.info('Finish scraping manufacturers (total added: %d)', total_count)


"""
def scrap_manufacturer(name, url, limit=3):
    logger.info('Scraping manufacturer "%s" (url=%s) with limit %s',
                name, url, limit)

    manuf, _ = Manufacturer.objects.get_or_create(name=name, slug=name)
    soup = get_soup(url)
    sleep()


    links = [span.find('a') for span in soup.find_all('span', attrs={"data-slot": "makeslist.item"})]

    if len(links) == 0:
        return False

    logger.debug('%d car models to scrap', len(links))
    for link in links:
        logger.debug('link: %s', link.get('href'))

    random.shuffle(links)

    counter = 0
    total_added = 0
    for link in links:
        added_count = scrap_car(
            name=link.contents[0],
            manufacturer=manuf,
            url=base_url + link.get('href')
        )

        total_added += added_count

        logger.info('scrap_manufacturer: Added %d photos fo car', total_added)

        if limit is not None and added_count:
            counter += 1
            if counter >= limit:
                logger.info('scrap_manufacturer: run of limit (%s)', limit)
                break

    # else:
    #     return scrap_catalog(soup)

    logger.info('scrap_manufacturer: Added %d photos in total',
                total_added)

    return total_added


def scrap_car(name, url, manufacturer):
    logger.info('Start scraping car "%s" (url=%s)', name, url)

    car, _ = Car.objects.get_or_create(
        name=name,
        manufacturer=manufacturer,
        slug=name,
    )
    soup = get_soup(url)
    sleep()

    return scrap_catalog(soup, car)


def scrap_catalog(soup, car):
    logger.info('Start scraping car "%s" catalog', car.name)

    links = [a for a in soup.find_all('a', attrs={"data-slot": "makeslist.item"})]

    random.shuffle(links)


    c = 0
    if len(links):
        for link in links:
            c += scrap_photos(
                soup=get_soup(base_url + link.get('href')),
                # url=base_url + link.get('href'),
                car=car
            )
    else:
        c += scrap_photos(
            soup=soup,
            car=car
        )

        # if added:
        #     break

    return c


def scrap_photos(car, soup):

    logger.info('Start scraping photos for car "%s"', car.name)

    # soup = get_soup(url)
    img_divs = [div.find_all('img') for div in soup.find_all('div', attrs={'class': 'o-img u-grayscale-70'})]

    imgs = [img for div in img_divs for img in div]

    sleep()

    # added = False
    c = 0
    for img in imgs:
        img_url = img.get('src')

        try:
            ExternalPhoto.objects.get(unique_token=img_url)
        except ExternalPhoto.DoesNotExist:
            ExternalPhoto.objects.create(
                car=car,
                url=img_url,
                unique_token=img_url
            )

            logger.info('Photo added "%s"', img_url)

            # added = True
            c += 1

    return c
    
"""
