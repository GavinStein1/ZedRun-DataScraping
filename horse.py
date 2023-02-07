class Horse:
    
    id = 0
    name = ""
    bloodline = ""
    breed_type = ""
    genotype = 0
    gender = ""
    coat_colour = ""
    distance1000 = {
        "distance": 0,
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0,
        "sixth": 0,
        "seventh": 0,
        "eighth": 0,
        "ninth": 0,
        "tenth": 0,
        "eleventh": 0,
        "twelth": 0,
        "heat": 0.0,
        "profit": 0.0,
        "min": 0.0,
        "mean": 0.0,
        "max": 0.0,
        "std_dev": 0.0,
        "lower_quartile": 0.0,
        "median": 0.0,
        "upper_quartile": 0.0
    }
    distance1200 = {
        "distance": "",
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0,
        "sixth": 0,
        "seventh": 0,
        "eighth": 0,
        "ninth": 0,
        "tenth": 0,
        "eleventh": 0,
        "twelth": 0,
        "heat": 0.0,
        "min": 0.0,
        "mean": 0.0,
        "max": 0.0,
        "std_dev": 0.0,
        "lower_quartile": 0.0,
        "median": 0.0,
        "upper_quartile": 0.0
    }
    distance1400 = {
        "distance": "",
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0,
        "sixth": 0,
        "seventh": 0,
        "eighth": 0,
        "ninth": 0,
        "tenth": 0,
        "eleventh": 0,
        "twelth": 0,
        "heat": 0.0,
        "min": 0.0,
        "mean": 0.0,
        "max": 0.0,
        "std_dev": 0.0,
        "lower_quartile": 0.0,
        "median": 0.0,
        "upper_quartile": 0.0
    }
    distance1600 = {
        "distance": "",
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0,
        "sixth": 0,
        "seventh": 0,
        "eighth": 0,
        "ninth": 0,
        "tenth": 0,
        "eleventh": 0,
        "twelth": 0,
        "heat": 0.0,
        "min": 0.0,
        "mean": 0.0,
        "max": 0.0,
        "std_dev": 0.0,
        "lower_quartile": 0.0,
        "median": 0.0,
        "upper_quartile": 0.0
    }
    distance1800 = {
        "distance": "",
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0,
        "sixth": 0,
        "seventh": 0,
        "eighth": 0,
        "ninth": 0,
        "tenth": 0,
        "eleventh": 0,
        "twelth": 0,
        "heat": 0.0,
        "min": 0.0,
        "mean": 0.0,
        "max": 0.0,
        "std_dev": 0.0,
        "lower_quartile": 0.0,
        "median": 0.0,
        "upper_quartile": 0.0
    }
    distance2000 = {
        "distance": "",
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0,
        "sixth": 0,
        "seventh": 0,
        "eighth": 0,
        "ninth": 0,
        "tenth": 0,
        "eleventh": 0,
        "twelth": 0,
        "heat": 0.0,
        "min": 0.0,
        "mean": 0.0,
        "max": 0.0,
        "std_dev": 0.0,
        "lower_quartile": 0.0,
        "median": 0.0,
        "upper_quartile": 0.0
    }
    distance2200 = {
        "distance": "",
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0,
        "sixth": 0,
        "seventh": 0,
        "eighth": 0,
        "ninth": 0,
        "tenth": 0,
        "eleventh": 0,
        "twelth": 0,
        "heat": 0.0,
        "min": 0.0,
        "mean": 0.0,
        "max": 0.0,
        "std_dev": 0.0,
        "lower_quartile": 0.0,
        "median": 0.0,
        "upper_quartile": 0.0
    }
    distance2400 = {
        "distance": "",
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0,
        "sixth": 0,
        "seventh": 0,
        "eighth": 0,
        "ninth": 0,
        "tenth": 0,
        "eleventh": 0,
        "twelth": 0,
        "heat": 0.0,
        "min": 0.0,
        "mean": 0.0,
        "max": 0.0,
        "std_dev": 0.0,
        "lower_quartile": 0.0,
        "median": 0.0,
        "upper_quartile": 0.0
    }
    distance2600 = {
        "distance": "",
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0,
        "sixth": 0,
        "seventh": 0,
        "eighth": 0,
        "ninth": 0,
        "tenth": 0,
        "eleventh": 0,
        "twelth": 0,
        "heat": 0.0,
        "min": 0.0,
        "mean": 0.0,
        "max": 0.0,
        "std_dev": 0.0,
        "lower_quartile": 0.0,
        "median": 0.0,
        "upper_quartile": 0.0
    }
    offspring = {
        "distance": "",
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0,
        "sixth": 0,
        "seventh": 0,
        "eighth": 0,
        "ninth": 0,
        "tenth": 0,
        "eleventh": 0,
        "twelth": 0
    }
    mother_name = ""
    father_name = ""

class HorseSpeedStats:
    stats = {
        1000: [],
        1200: [],
        1400: [],
        1600: [],
        1800: [],
        2000: [],
        2200: [],
        2400: [],
        2600: []
    }
    name = ""
    mother = ""
    father = ""
    class_rank = ""