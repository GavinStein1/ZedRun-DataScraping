import scrape_speed

TOTAL_HORSES = 525242

def stringify_dict(dict) -> str:
    output = ""
    for key in dict.keys():
        output = output + str(dict[key]) + ","
    # output = output[:-1]
    return output

def main():

    data_file = open("raw_speed_data.csv", 'a')
    ctr = int(input("enter starting ctr: "))
    err_cnt = 0
    while ctr < TOTAL_HORSES:
        try:
            if err_cnt == 3:
                data_file.close()
                break
            print(ctr)
            data_string = ""
            horse = None
            horse = scrape_speed.scrape_data(ctr)
            horse.id = ctr
            data_string = str(horse.id) + "," + horse.name + ","
            for key in horse.stats.keys():
                data_string = data_string + str(key) + "," + ",".join(horse.stats[key])
            data_string = data_string + "," + horse.mother + "," + horse.father
            data_file.write(data_string + "\n")
            err_cnt = 0
            ctr = ctr + 1
        except KeyboardInterrupt:
            data_file.close()
            break
        except AttributeError:
            err_cnt = err_cnt + 1



if __name__== "__main__":
    main()