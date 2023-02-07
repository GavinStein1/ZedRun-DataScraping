import scrape_speed

TOTAL_HORSES = 525242

def stringify_dict(dict) -> str:
    output = ""
    for key in dict.keys():
        output = output + str(dict[key]) + ","
    # output = output[:-1]
    return output

def main():

    data_file = open("raw_Data.csv", 'a')
    ctr = 22
    while ctr < TOTAL_HORSES:
        try:
            print(ctr)
            horse = scrape_speed.scrape_data(ctr)
            horse.id = ctr
            data_string = str(horse.id) + "," + horse.name + ","
            for key in horse.stats.keys():
                data_string = data_string + str(key) + "," + ",".join(horse.stats[key])
            data_string = data_string + "," + horse.mother + "," + horse.father
            ctr = ctr + 1
            data_file.write(data_string + "\n")
        except KeyboardInterrupt:
            data_file.close()
            break



if __name__== "__main__":
    main()