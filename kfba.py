from keepa import *
import configparser
from datetime import datetime, timedelta
import csv


class MainFBA:

    def __init__(self, config_file):
        self.config_file = config_file
        self.api = ''
        self.input_file = ''
        self.output_file = ''
        self.asin_list = []
        self.raw_data_list = []
        self.config = []
        self.result = []

    def parse_cfg(self):
        """
        parse the file we provide in script call.
        file with parameters should be UTF-8 encoded.

        :return: parsed configuration file
        """

        self.config = configparser.ConfigParser(delimiters='=', allow_no_value=True)
        self.config.read(self.config_file)
        # assign value to essential attributes
        self.api = Keepa(self.config['DEFAULT']['accesskey'])
        self.input_file = self.config['DEFAULT']['InputFile'].strip('\'')
        self.output_file = self.config['DEFAULT']['OutputFile'].strip('\'')

        # dummy print out for checking
        print("TEST CONFIG KEEPA FIELDs")
        print('Title - ', self.config['StandardKeepaFields']["Title"])
        print('Sales Rank 90 days avg. - ', self.config['StandardKeepaFields']["Sales Rank 90 days avg."])
        print('apikey - ', self.config['DEFAULT']['accesskey'])
        print(self.config.read(self.config_file))

        return self.config

    def read_input(self):
        """
        read input CSV file with ASINs
        :return: list of parsed ASINs
        """

        with open(self.input_file) as f:
            csv_reader = csv.reader(f)
            input_list = list(csv_reader)

        print("INPUT CSV PARSED INTO LIST: ", input_list)

        for i in range(1, len(input_list)):
            self.asin_list.append(input_list[i][0])

        print("check here list of ASINs: ", self.asin_list)

        return self.asin_list

    def make_keepa_call(self):
        """
        fetch  all data from keepa.com
        :return: raw data, fetched from Keepa for particular ASINs
        """

        for item in self.asin_list:
            product = self.api.query(item)
            self.raw_data_list.append(product)

        return self.raw_data_list

    def write_out(self):
        with open(self.output_file, 'w+') as f:
            for item in self.result:
                f.write("%s\n" % item)

    @staticmethod
    def count_average_x_days(dataset, dataset_time, days_num):
        """
        count average value for provided time range
        :param dataset: numpy array
        :param dataset_time: numpy array
        :param days_num: int, amount of days
        :return : average value
        """
        print('Dataset for ', days_num, ' avg. - ')
        past_days_num = datetime.now() - timedelta(days=days_num)
        value_avg_days_num = 0
        count_dates = 0

        # debug printout
        # print('LENGTH OF DATASET_TIME:', len(dataset_time))

        for i in range(len(dataset_time)):
            if dataset_time[i] > past_days_num:
                # print('%20s %s' % (dataset_time[i], dataset[i]))
                count_dates += 1
                value_avg_days_num += dataset[i]
        # debug printout
        print('AVG', days_num,  'value  = ', value_avg_days_num/count_dates)

        return value_avg_days_num/count_dates

    def play_with_data(self):
        """

        :return: result list to write out into a file
        """
        # for tests only - work with first product from the InputFile
        product = self.raw_data_list[0]

        # debug printout
        print('AVAILABLE KEYS: ')
        print(product[0].keys())
        print('DATA ALL KEYS:')
        print(product[0]['data'].keys())

        # adding items mentioned in the config to the result list
        if self.config['StandardKeepaFields']['Title'] == '1':
            self.result.append('Title: ' + product[0]['title'])

        if self.config['StandardKeepaFields']['Sales Rank Current'] == '1':
            self.result.append('Sales Rank Current: ' + str(product[0]['data']['SALES'][-1]))
        if self.config['StandardKeepaFields']['Sales Rank 30 days avg.'] == '1':
            self.result.append('Sales Rank 30 days avg.' +
                               str(self.count_average_x_days(product[0]['data']['SALES'], product[0]['data']['SALES_time'],  30)))
        if self.config['StandardKeepaFields']['Amazon: Current'] == '1':
            self.result.append('Amazon: Current: ' + str(product[0]['data']['AMAZON'][-1]))
        if self.config['StandardKeepaFields']['Categories: Root'] == '1':
            print('HEREEEEE!!!', self.config['StandardKeepaFields']['Categories: Root'] )
            self.result.append('Categories: Root: ' + str(product[0]['rootCategory']))
        if self.config['StandardKeepaFields']['Categories: Sub'] == '1':
            self.result.append('Categories: Sub: ' + str(product[0]['categories']))
        if self.config['StandardKeepaFields']['Categories: Tree'] == '1':
            self.result.append('Categories: Tree: ' + str(product[0]['categoryTree']))

        if self.config['StandardKeepaFields']['Product Codes: UPC'] == '1':
            pass
            # self.result.append('Product Codes: UPC: ' + product[0]['parentAsin'])
        if self.config['StandardKeepaFields']['Parent ASIN'] == '1':
            self.result.append('Parent ASIN: ' + product[0]['parentAsin'])
        if self.config['StandardKeepaFields']['Variation ASINs'] == '1':
            pass
        if self.config['StandardKeepaFields']['Manufacturer'] == '1':
            self.result.append('Manufacturer: ' + product[0]['manufacturer'])
        if self.config['StandardKeepaFields']['Type'] == '1':
            self.result.append('Type: ' + product[0]['type'])
        if self.config['StandardKeepaFields']['Brand'] == '1':
            self.result.append('Brand: ' + product[0]['brand'])
        if self.config['StandardKeepaFields']['Department'] == '1':
            self.result.append('Department: ' + product[0]['department'])
        if self.config['StandardKeepaFields']['Model'] == '1':
            self.result.append('Model: ' + product[0]['model'])
        if self.config['StandardKeepaFields']['Color'] == '1':
            self.result.append('Color: ' + product[0]['color'])
        if self.config['StandardKeepaFields']['Size'] == '1':
            self.result.append('Size: ' + product[0]['size'])
        if self.config['StandardKeepaFields']['Number of Items'] == '1':
            self.result.append('Number of Items: ' + str(product[0]['numberOfItems']))
        if self.config['StandardKeepaFields']['Release Date'] == '1':
            self.result.append('Release Date: ' + str(product[0]['releaseDate']))
        if self.config['StandardKeepaFields']['Package: Dimension (cm³)'] == '1':
            self.result.append('Package: Dimension(cm³): ' + str(product[0]['packageLength'] * product[0]['packageWidth'] * product[0]['packageHeight']))
        if self.config['StandardKeepaFields']['Package: Length (cm)'] == '1':
            self.result.append('Package: Length (cm): ' + str(product[0]['packageLength']))
        if self.config['StandardKeepaFields']['Package: Height (cm)'] == '1':
            self.result.append('Package: Height (cm): ' + str(product[0]['packageHeight']))
        if self.config['StandardKeepaFields']['Package: Width (cm)'] == '1':
            self.result.append('Package: Width (cm): ' + str(product[0]['packageWidth']))
        if self.config['StandardKeepaFields']['Package: Weight (g)'] == '1':
            self.result.append('Package: Weight (g): ' + str(product[0]['packageWeight']))

        return self.result










