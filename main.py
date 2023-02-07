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
            print(data_string)
            ctr = ctr + 1
        except KeyboardInterrupt:
            data_file.close()
            break
        # try:
        #     print(ctr)
        #     horse = scrape.scrape_data(ctr)
        #     if horse is not None:
        #         data_string = str(horse.id) + ',' + horse.name + ',' + horse.bloodline + ',' + horse.breed_type + ',' + str(horse.genotype) + ','
        #         data_string = data_string + stringify_dict(horse.distance1000)
        #         data_string = data_string + stringify_dict(horse.distance1200)
        #         data_string = data_string + stringify_dict(horse.distance1400)
        #         data_string = data_string + stringify_dict(horse.distance1600)
        #         data_string = data_string + stringify_dict(horse.distance1800)
        #         data_string = data_string + stringify_dict(horse.distance2000)
        #         data_string = data_string + stringify_dict(horse.distance2200)
        #         data_string = data_string + stringify_dict(horse.distance2400)
        #         data_string = data_string + stringify_dict(horse.distance2600)
        #         data_string = data_string + stringify_dict(horse.offspring)
        #         data_string = data_string + horse.mother_name + "," + horse.father_name
        #         data_file.write(data_string + "\n")
        #         ctr += 1
        #     else:
        #         ctr += 1
        # except Exception:
        #     continue
        # except KeyboardInterrupt:
        #     data_file.close()



if __name__== "__main__":
    main()