from bs4 import BeautifulSoup
import requests
from horse import Horse

BASE_URL = "https://knowyourhorses.com/horses/"
GENDERS = ["Colt", "Stallion", "Filly", "Mare"]

def get_page(url) -> requests.Response:
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    page = requests.get(url, headers=headers)
    if page.status_code == 200:
        return page
    else:
        return None
    
def print_page(page, isSoup=False):
    if isSoup:
        print(page.prettify())
    else:
        print(page.content)

def create_soup(page: requests.Response) -> BeautifulSoup:
    try:
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    except Exception:
        return None
    
def isfloat(value) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False
    

def scrape_data(id: int) -> Horse:
    # try:
    main_page = get_page(BASE_URL + str(id))
    speed_stats_page = get_page(BASE_URL + str(id) + "/speed_statistics")
    # offspring_page = get_page(BASE_URL + str(id) + "/offspring_position_distribution")

    main = create_soup(main_page)
    speed_stats = create_soup(speed_stats_page)
    # offspring = create_soup(offspring_page)

    horse = Horse()
    horse.id = id

    # Name
    temp = main.find_all('a', class_ = "font-sans-serif lh-1 fs-2 mb-1 me-2")
    if len(temp) == 0:
        horse.name = ""
        horse.mother_name = ""
        horse.father_name = ""
    if len(temp) == 1:
        horse.name = temp[0].string.strip()
        horse.mother_name = ""
        horse.father_name = ""
    elif len(temp) >= 3:
        horse.name = temp[0].string.strip()
        horse.name = temp[1].string.strip()
        horse.name = temp[2].string.strip()
    
    # Bloodline, Breed type and Genotype
    temp = main.find_all('span', class_ = "badge badge-soft-success fs--2")
    temp_str = ""
    flag = False
    for span in temp:
        if span.string is None:
            continue
        if span.string.strip()[0] == "Z" and span.string.strip()[1].isnumeric():
            temp_str = span.string.strip()
        if span.string.strip() in GENDERS:
            horse.gender = span.string.strip()
            flag = True
            continue
        if flag:
            horse.coat_colour = span.string.strip()
            flag = False
    if temp_str == "":
        horse.bloodline = ""
        horse.breed_type = ""
        horse.genotype = -1
    else:
        temp_split = temp_str.split()
        if len(temp_split) != 3:
            horse.bloodline = ""
            horse.breed_type = ""
            horse.genotype = -1
        else:
            horse.genotype = int(temp_split[0][1:])
            horse.bloodline = temp_split[1]
            horse.breed_type = temp_split[2]

    distances = [1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600]

    for distance in distances:
        distance_page = get_page(BASE_URL + str(id) + "/horseshoe_class_distance?query%5Blength%5D=" + str(distance))
        distance_soup = create_soup(distance_page)
        num_races = distance_soup.find_all('div', class_="col my-2 stat")[1].find_all('span')[0].text.strip()
        if int(num_races) == 0:
            continue
        tag = distance_soup.find('div', class_='card-body')
        results = tag.contents[1].attrs['data-chart-tally-value']
        if distance == 1000:
            horse.distance1000['distance'] = distance
            horse.distance1000['first'] = int(results.split("\"1\":")[1].split(",")[0])
            horse.distance1000['second'] = int(results.split("\"2\":")[1].split(",")[0])
            horse.distance1000['third'] = int(results.split("\"3\":")[1].split(",")[0])
            horse.distance1000['fourth'] = int(results.split("\"4\":")[1].split(",")[0])
            horse.distance1000['fifth'] = int(results.split("\"5\":")[1].split(",")[0])
            horse.distance1000['sixth'] = int(results.split("\"6\":")[1].split(",")[0])
            horse.distance1000['seventh'] = int(results.split("\"7\":")[1].split(",")[0])
            horse.distance1000['eighth'] = int(results.split("\"8\":")[1].split(",")[0])
            horse.distance1000['ninth'] = int(results.split("\"9\":")[1].split(",")[0])
            horse.distance1000['tenth'] = int(results.split("\"10\":")[1].split(",")[0])
            horse.distance1000['eleventh'] = int(results.split("\"11\":")[1].split(",")[0])
            horse.distance1000['twelth'] = int(results.split("\"12\":")[1].split("}")[0])
            
            temp = distance_soup.find_all('span', class_="badge badge-soft-success fs--2")
            heat = temp[2].previous_sibling.previous_sibling.string.strip()
            heat = float(heat[:len(heat)-1])
            horse.distance1000['heat'] = heat

            temp = distance_soup.find('i', class_="fab fa-ethereum")
            profit = float(temp.parent.text.strip())
            horse.distance1000['profit'] = profit

            # stats
            table = speed_stats.find('table', class_="table text-center").find_all('td')
            temp_var = (distance - 1000)/200
            ctr = int(0 + (temp_var * 9))
            end_ctr = ctr + 9
            while ctr < end_ctr:
                if table[ctr].string is None or not isfloat(table[ctr].string.strip()):
                    ctr = ctr +  1
                    continue
                if ctr == end_ctr - 9:
                    ctr = ctr + 1
                elif ctr == end_ctr - 8:
                    horse.distance1000['min'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 7:
                    horse.distance1000['mean'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 6:
                    horse.distance1000['max'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 5:
                    ctr = ctr + 1
                elif ctr == end_ctr - 4:
                    horse.distance1000['std_dev'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 3:
                    horse.distance1000['lower_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 2:
                    horse.distance1000['median'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 1:
                    horse.distance1000['upper_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
        elif distance == 1200:
            horse.distance1200['distance'] = distance
            horse.distance1200['first'] = int(results.split("\"1\":")[1].split(",")[0])
            horse.distance1200['second'] = int(results.split("\"2\":")[1].split(",")[0])
            horse.distance1200['third'] = int(results.split("\"3\":")[1].split(",")[0])
            horse.distance1200['fourth'] = int(results.split("\"4\":")[1].split(",")[0])
            horse.distance1200['fifth'] = int(results.split("\"5\":")[1].split(",")[0])
            horse.distance1200['sixth'] = int(results.split("\"6\":")[1].split(",")[0])
            horse.distance1200['seventh'] = int(results.split("\"7\":")[1].split(",")[0])
            horse.distance1200['eighth'] = int(results.split("\"8\":")[1].split(",")[0])
            horse.distance1200['ninth'] = int(results.split("\"9\":")[1].split(",")[0])
            horse.distance1200['tenth'] = int(results.split("\"10\":")[1].split(",")[0])
            horse.distance1200['eleventh'] = int(results.split("\"11\":")[1].split(",")[0])
            horse.distance1200['twelth'] = int(results.split("\"12\":")[1].split("}")[0])
            
            temp = distance_soup.find_all('span', class_="badge badge-soft-success fs--2")
            heat = temp[2].previous_sibling.previous_sibling.string.strip()
            heat = float(heat[:len(heat)-1])
            horse.distance1200['heat'] = heat

            temp = distance_soup.find('i', class_="fab fa-ethereum")
            profit = float(temp.parent.text.strip())
            horse.distance1200['profit'] = profit

            # stats
            table = speed_stats.find('table', class_="table text-center").find_all('td')
            temp_var = (distance - 1000)/200
            ctr = int(0 + (temp_var * 9))
            end_ctr = ctr + 9
            while ctr < end_ctr:
                if table[ctr].string is None or not isfloat(table[ctr].string.strip()):
                    ctr = ctr +  1
                    continue
                if ctr == end_ctr - 9:
                    ctr = ctr + 1
                elif ctr == end_ctr - 8:
                    horse.distance1200['min'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 7:
                    horse.distance1200['mean'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 6:
                    horse.distance1200['max'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 5:
                    ctr = ctr + 1
                elif ctr == end_ctr - 4:
                    horse.distance1200['std_dev'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 3:
                    horse.distance1200['lower_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 2:
                    horse.distance1200['median'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 1:
                    horse.distance1200['upper_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
        elif distance == 1400:
            horse.distance1400['distance'] = distance
            horse.distance1400['first'] = int(results.split("\"1\":")[1].split(",")[0])
            horse.distance1400['second'] = int(results.split("\"2\":")[1].split(",")[0])
            horse.distance1400['third'] = int(results.split("\"3\":")[1].split(",")[0])
            horse.distance1400['fourth'] = int(results.split("\"4\":")[1].split(",")[0])
            horse.distance1400['fifth'] = int(results.split("\"5\":")[1].split(",")[0])
            horse.distance1400['sixth'] = int(results.split("\"6\":")[1].split(",")[0])
            horse.distance1400['seventh'] = int(results.split("\"7\":")[1].split(",")[0])
            horse.distance1400['eighth'] = int(results.split("\"8\":")[1].split(",")[0])
            horse.distance1400['ninth'] = int(results.split("\"9\":")[1].split(",")[0])
            horse.distance1400['tenth'] = int(results.split("\"10\":")[1].split(",")[0])
            horse.distance1400['eleventh'] = int(results.split("\"11\":")[1].split(",")[0])
            horse.distance1400['twelth'] = int(results.split("\"12\":")[1].split("}")[0])
            
            temp = distance_soup.find_all('span', class_="badge badge-soft-success fs--2")
            heat = temp[2].previous_sibling.previous_sibling.string.strip()
            heat = float(heat[:len(heat)-1])
            horse.distance1400['heat'] = heat

            temp = distance_soup.find('i', class_="fab fa-ethereum")
            profit = float(temp.parent.text.strip())
            horse.distance1400['profit'] = profit

            # stats
            table = speed_stats.find('table', class_="table text-center").find_all('td')
            temp_var = (distance - 1000)/200
            ctr = int(0 + (temp_var * 9))
            end_ctr = ctr + 9
            while ctr < end_ctr:
                if table[ctr].string is None or not isfloat(table[ctr].string.strip()):
                    ctr = ctr +  1
                    continue
                if ctr == end_ctr - 9:
                    ctr = ctr + 1
                elif ctr == end_ctr - 8:
                    horse.distance1400['min'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 7:
                    horse.distance1400['mean'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 6:
                    horse.distance1400['max'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 5:
                    ctr = ctr + 1
                elif ctr == end_ctr - 4:
                    horse.distance1400['std_dev'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 3:
                    horse.distance1400['lower_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 2:
                    horse.distance1400['median'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 1:
                    horse.distance1400['upper_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
        elif distance == 1600:
            horse.distance1600['distance'] = distance
            horse.distance1600['first'] = int(results.split("\"1\":")[1].split(",")[0])
            horse.distance1600['second'] = int(results.split("\"2\":")[1].split(",")[0])
            horse.distance1600['third'] = int(results.split("\"3\":")[1].split(",")[0])
            horse.distance1600['fourth'] = int(results.split("\"4\":")[1].split(",")[0])
            horse.distance1600['fifth'] = int(results.split("\"5\":")[1].split(",")[0])
            horse.distance1600['sixth'] = int(results.split("\"6\":")[1].split(",")[0])
            horse.distance1600['seventh'] = int(results.split("\"7\":")[1].split(",")[0])
            horse.distance1600['eighth'] = int(results.split("\"8\":")[1].split(",")[0])
            horse.distance1600['ninth'] = int(results.split("\"9\":")[1].split(",")[0])
            horse.distance1600['tenth'] = int(results.split("\"10\":")[1].split(",")[0])
            horse.distance1600['eleventh'] = int(results.split("\"11\":")[1].split(",")[0])
            horse.distance1600['twelth'] = int(results.split("\"12\":")[1].split("}")[0])
            
            temp = distance_soup.find_all('span', class_="badge badge-soft-success fs--2")
            heat = temp[2].previous_sibling.previous_sibling.string.strip()
            heat = float(heat[:len(heat)-1])
            horse.distance1600['heat'] = heat

            temp = distance_soup.find('i', class_="fab fa-ethereum")
            profit = float(temp.parent.text.strip())
            horse.distance1600['profit'] = profit

            # stats
            table = speed_stats.find('table', class_="table text-center").find_all('td')
            temp_var = (distance - 1000)/200
            ctr = int(0 + (temp_var * 9))
            end_ctr = ctr + 9
            while ctr < end_ctr:
                if table[ctr].string is None or not isfloat(table[ctr].string.strip()):
                    ctr = ctr +  1
                    continue
                if ctr == end_ctr - 9:
                    ctr = ctr + 1
                elif ctr == end_ctr - 8:
                    horse.distance1600['min'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 7:
                    horse.distance1600['mean'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 6:
                    horse.distance1600['max'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 5:
                    ctr = ctr + 1
                elif ctr == end_ctr - 4:
                    horse.distance1600['std_dev'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 3:
                    horse.distance1600['lower_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 2:
                    horse.distance1600['median'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 1:
                    horse.distance1600['upper_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
        elif distance == 1800:
            horse.distance1800['distance'] = distance
            horse.distance1800['first'] = int(results.split("\"1\":")[1].split(",")[0])
            horse.distance1800['second'] = int(results.split("\"2\":")[1].split(",")[0])
            horse.distance1800['third'] = int(results.split("\"3\":")[1].split(",")[0])
            horse.distance1800['fourth'] = int(results.split("\"4\":")[1].split(",")[0])
            horse.distance1800['fifth'] = int(results.split("\"5\":")[1].split(",")[0])
            horse.distance1800['sixth'] = int(results.split("\"6\":")[1].split(",")[0])
            horse.distance1800['seventh'] = int(results.split("\"7\":")[1].split(",")[0])
            horse.distance1800['eighth'] = int(results.split("\"8\":")[1].split(",")[0])
            horse.distance1800['ninth'] = int(results.split("\"9\":")[1].split(",")[0])
            horse.distance1800['tenth'] = int(results.split("\"10\":")[1].split(",")[0])
            horse.distance1800['eleventh'] = int(results.split("\"11\":")[1].split(",")[0])
            horse.distance1800['twelth'] = int(results.split("\"12\":")[1].split("}")[0])
            
            temp = distance_soup.find_all('span', class_="badge badge-soft-success fs--2")
            heat = temp[2].previous_sibling.previous_sibling.string.strip()
            heat = float(heat[:len(heat)-1])
            horse.distance1800['heat'] = heat

            temp = distance_soup.find('i', class_="fab fa-ethereum")
            profit = float(temp.parent.text.strip())
            horse.distance1800['profit'] = profit

            # stats
            table = speed_stats.find('table', class_="table text-center").find_all('td')
            temp_var = (distance - 1000)/200
            ctr = int(0 + (temp_var * 9))
            end_ctr = ctr + 9
            while ctr < end_ctr:
                if table[ctr].string is None or not isfloat(table[ctr].string.strip()):
                    ctr = ctr +  1
                    continue
                if ctr == end_ctr - 9:
                    ctr = ctr + 1
                elif ctr == end_ctr - 8:
                    horse.distance1800['min'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 7:
                    horse.distance1800['mean'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 6:
                    horse.distance1800['max'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 5:
                    ctr = ctr + 1
                elif ctr == end_ctr - 4:
                    horse.distance1800['std_dev'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 3:
                    horse.distance1800['lower_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 2:
                    horse.distance1800['median'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 1:
                    horse.distance1800['upper_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
        elif distance == 2000:
            horse.distance2000['distance'] = distance
            horse.distance2000['first'] = int(results.split("\"1\":")[1].split(",")[0])
            horse.distance2000['second'] = int(results.split("\"2\":")[1].split(",")[0])
            horse.distance2000['third'] = int(results.split("\"3\":")[1].split(",")[0])
            horse.distance2000['fourth'] = int(results.split("\"4\":")[1].split(",")[0])
            horse.distance2000['fifth'] = int(results.split("\"5\":")[1].split(",")[0])
            horse.distance2000['sixth'] = int(results.split("\"6\":")[1].split(",")[0])
            horse.distance2000['seventh'] = int(results.split("\"7\":")[1].split(",")[0])
            horse.distance2000['eighth'] = int(results.split("\"8\":")[1].split(",")[0])
            horse.distance2000['ninth'] = int(results.split("\"9\":")[1].split(",")[0])
            horse.distance2000['tenth'] = int(results.split("\"10\":")[1].split(",")[0])
            horse.distance2000['eleventh'] = int(results.split("\"11\":")[1].split(",")[0])
            horse.distance2000['twelth'] = int(results.split("\"12\":")[1].split("}")[0])
            
            temp = distance_soup.find_all('span', class_="badge badge-soft-success fs--2")
            heat = temp[2].previous_sibling.previous_sibling.string.strip()
            heat = float(heat[:len(heat)-1])
            horse.distance2000['heat'] = heat

            temp = distance_soup.find('i', class_="fab fa-ethereum")
            profit = float(temp.parent.text.strip())
            horse.distance2000['profit'] = profit

            # stats
            table = speed_stats.find('table', class_="table text-center").find_all('td')
            temp_var = (distance - 1000)/200
            ctr = int(0 + (temp_var * 9))
            end_ctr = ctr + 9
            while ctr < end_ctr:
                if table[ctr].string is None or not isfloat(table[ctr].string.strip()):
                    ctr = ctr +  1
                    continue
                if ctr == end_ctr - 9:
                    ctr = ctr + 1
                elif ctr == end_ctr - 8:
                    horse.distance2000['min'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 7:
                    horse.distance2000['mean'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 6:
                    horse.distance2000['max'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 5:
                    ctr = ctr + 1
                elif ctr == end_ctr - 4:
                    horse.distance2000['std_dev'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 3:
                    horse.distance2000['lower_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 2:
                    horse.distance2000['median'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 1:
                    horse.distance2000['upper_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
        elif distance == 2200:
            horse.distance2200['distance'] = distance
            horse.distance2200['first'] = int(results.split("\"1\":")[1].split(",")[0])
            horse.distance2200['second'] = int(results.split("\"2\":")[1].split(",")[0])
            horse.distance2200['third'] = int(results.split("\"3\":")[1].split(",")[0])
            horse.distance2200['fourth'] = int(results.split("\"4\":")[1].split(",")[0])
            horse.distance2200['fifth'] = int(results.split("\"5\":")[1].split(",")[0])
            horse.distance2200['sixth'] = int(results.split("\"6\":")[1].split(",")[0])
            horse.distance2200['seventh'] = int(results.split("\"7\":")[1].split(",")[0])
            horse.distance2200['eighth'] = int(results.split("\"8\":")[1].split(",")[0])
            horse.distance2200['ninth'] = int(results.split("\"9\":")[1].split(",")[0])
            horse.distance2200['tenth'] = int(results.split("\"10\":")[1].split(",")[0])
            horse.distance2200['eleventh'] = int(results.split("\"11\":")[1].split(",")[0])
            horse.distance2200['twelth'] = int(results.split("\"12\":")[1].split("}")[0])
            
            temp = distance_soup.find_all('span', class_="badge badge-soft-success fs--2")
            heat = temp[2].previous_sibling.previous_sibling.string.strip()
            heat = float(heat[:len(heat)-1])
            horse.distance2200['heat'] = heat

            temp = distance_soup.find('i', class_="fab fa-ethereum")
            profit = float(temp.parent.text.strip())
            horse.distance2200['profit'] = profit

            # stats
            table = speed_stats.find('table', class_="table text-center").find_all('td')
            temp_var = (distance - 1000)/200
            ctr = int(0 + (temp_var * 9))
            end_ctr = ctr + 9
            while ctr < end_ctr:
                if table[ctr].string is None or not isfloat(table[ctr].string.strip()):
                    ctr = ctr +  1
                    continue
                if ctr == end_ctr - 9:
                    ctr = ctr + 1
                elif ctr == end_ctr - 8:
                    horse.distance2200['min'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 7:
                    horse.distance2200['mean'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 6:
                    horse.distance2200['max'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 5:
                    ctr = ctr + 1
                elif ctr == end_ctr - 4:
                    horse.distance2200['std_dev'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 3:
                    horse.distance2200['lower_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 2:
                    horse.distance2200['median'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 1:
                    horse.distance2200['upper_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
        elif distance == 2400:
            horse.distance2400['distance'] = distance
            horse.distance2400['first'] = int(results.split("\"1\":")[1].split(",")[0])
            horse.distance2400['second'] = int(results.split("\"2\":")[1].split(",")[0])
            horse.distance2400['third'] = int(results.split("\"3\":")[1].split(",")[0])
            horse.distance2400['fourth'] = int(results.split("\"4\":")[1].split(",")[0])
            horse.distance2400['fifth'] = int(results.split("\"5\":")[1].split(",")[0])
            horse.distance2400['sixth'] = int(results.split("\"6\":")[1].split(",")[0])
            horse.distance2400['seventh'] = int(results.split("\"7\":")[1].split(",")[0])
            horse.distance2400['eighth'] = int(results.split("\"8\":")[1].split(",")[0])
            horse.distance2400['ninth'] = int(results.split("\"9\":")[1].split(",")[0])
            horse.distance2400['tenth'] = int(results.split("\"10\":")[1].split(",")[0])
            horse.distance2400['eleventh'] = int(results.split("\"11\":")[1].split(",")[0])
            horse.distance2400['twelth'] = int(results.split("\"12\":")[1].split("}")[0])
            
            temp = distance_soup.find_all('span', class_="badge badge-soft-success fs--2")
            heat = temp[2].previous_sibling.previous_sibling.string.strip()
            heat = float(heat[:len(heat)-1])
            horse.distance2400['heat'] = heat

            temp = distance_soup.find('i', class_="fab fa-ethereum")
            profit = float(temp.parent.text.strip())
            horse.distance2400['profit'] = profit

            # stats
            table = speed_stats.find('table', class_="table text-center").find_all('td')
            temp_var = (distance - 1000)/200
            ctr = int(0 + (temp_var * 9))
            end_ctr = ctr + 9
            while ctr < end_ctr:
                if table[ctr].string is None or not isfloat(table[ctr].string.strip()):
                    ctr = ctr +  1
                    continue
                if ctr == end_ctr - 9:
                    ctr = ctr + 1
                elif ctr == end_ctr - 8:
                    horse.distance2400['min'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 7:
                    horse.distance2400['mean'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 6:
                    horse.distance2400['max'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 5:
                    ctr = ctr + 1
                elif ctr == end_ctr - 4:
                    horse.distance2400['std_dev'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 3:
                    horse.distance2400['lower_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 2:
                    horse.distance2400['median'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 1:
                    horse.distance2400['upper_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
        elif distance == 2600:
            horse.distance2600['distance'] = distance
            horse.distance2600['first'] = int(results.split("\"1\":")[1].split(",")[0])
            horse.distance2600['second'] = int(results.split("\"2\":")[1].split(",")[0])
            horse.distance2600['third'] = int(results.split("\"3\":")[1].split(",")[0])
            horse.distance2600['fourth'] = int(results.split("\"4\":")[1].split(",")[0])
            horse.distance2600['fifth'] = int(results.split("\"5\":")[1].split(",")[0])
            horse.distance2600['sixth'] = int(results.split("\"6\":")[1].split(",")[0])
            horse.distance2600['seventh'] = int(results.split("\"7\":")[1].split(",")[0])
            horse.distance2600['eighth'] = int(results.split("\"8\":")[1].split(",")[0])
            horse.distance2600['ninth'] = int(results.split("\"9\":")[1].split(",")[0])
            horse.distance2600['tenth'] = int(results.split("\"10\":")[1].split(",")[0])
            horse.distance2600['eleventh'] = int(results.split("\"11\":")[1].split(",")[0])
            horse.distance2600['twelth'] = int(results.split("\"12\":")[1].split("}")[0])
            
            temp = distance_soup.find_all('span', class_="badge badge-soft-success fs--2")
            heat = temp[2].previous_sibling.previous_sibling.string.strip()
            heat = float(heat[:len(heat)-1])
            horse.distance2600['heat'] = heat

            temp = distance_soup.find('i', class_="fab fa-ethereum")
            profit = float(temp.parent.text.strip())
            horse.distance2600['profit'] = profit

            # stats
            table = speed_stats.find('table', class_="table text-center").find_all('td')
            temp_var = (distance - 1000)/200
            ctr = int(0 + (temp_var * 9))
            end_ctr = ctr + 9
            while ctr < end_ctr:
                if table[ctr].string is None or not isfloat(table[ctr].string.strip()):
                    ctr = ctr +  1
                    continue
                if ctr == end_ctr - 9:
                    ctr = ctr + 1
                elif ctr == end_ctr - 8:
                    horse.distance2600['min'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 7:
                    horse.distance2600['mean'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 6:
                    horse.distance2600['max'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 5:
                    ctr = ctr + 1
                elif ctr == end_ctr - 4:
                    horse.distance2600['std_dev'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 3:
                    horse.distance2600['lower_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 2:
                    horse.distance2600['median'] = float(table[ctr].string)
                    ctr = ctr + 1
                elif ctr == end_ctr - 1:
                    horse.distance2600['upper_quartile'] = float(table[ctr].string)
                    ctr = ctr + 1
    
    # Offspring results
    # try:
    #     results = offspring.find('canvas', class_="chart").parent.attrs['data-chart-tally-value']

    #     horse.offspring['first'] = int(results.split("\"1\":")[1].split(",")[0])
    #     horse.offspring['second'] = int(results.split("\"2\":")[1].split(",")[0])
    #     horse.offspring['third'] = int(results.split("\"3\":")[1].split(",")[0])
    #     horse.offspring['fourth'] = int(results.split("\"4\":")[1].split(",")[0])
    #     horse.offspring['fifth'] = int(results.split("\"5\":")[1].split(",")[0])
    #     horse.offspring['sixth'] = int(results.split("\"6\":")[1].split(",")[0])
    #     horse.offspring['seventh'] = int(results.split("\"7\":")[1].split(",")[0])
    #     horse.offspring['eighth'] = int(results.split("\"8\":")[1].split(",")[0])
    #     horse.offspring['ninth'] = int(results.split("\"9\":")[1].split(",")[0])
    #     horse.offspring['tenth'] = int(results.split("\"10\":")[1].split(",")[0])
    #     horse.offspring['eleventh'] = int(results.split("\"11\":")[1].split(",")[0])
    #     horse.offspring['twelth'] = int(results.split("\"12\":")[1].split("}")[0])
    # except AttributeError as e:
    #     pass

    return horse

def isfloat(value) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False