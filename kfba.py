from kfba_config import *
from keepa import *
import configparser
from datetime import datetime, timedelta
import csv


class MainFBA:

    def __init__(self, config_file):
        self.config_file = config_file
        self.api = Keepa(accesskey)
        self.input_file = ''
        self.output_file = ''
        self.asin_list = []
        self.raw_data_list = []
        self.config = []
        self.result = []

    def parse_cfg(self):
        #file name we provide in script call
        #file with parameters should be UTF-8 encoded
        self.config = configparser.ConfigParser(delimiters='=', allow_no_value=True)
        self.config.read(self.config_file)

        self.input_file = self.config['DEFAULT']['InputFile'].strip('\'')
        self.output_file = self.config['DEFAULT']['OutputFile'].strip('\'')

        #dummy print out for checking
        print("TEST CONFIG KEEPA FIELDs")
        print('Title - ', self.config['StandardKeepaFields']["Title"])
        print('Sales Rank 90 days avg. - ', self.config['StandardKeepaFields']["Sales Rank 90 days avg."])

        print(self.config.read(self.config_file))

        return self.config

    def read_input(self):
        #read input CSV file with ASINs
        with open(self.input_file) as f:
            csv_reader = csv.reader(f)
            input_list = list(csv_reader)

        print("INPUT CSV PARSED INTO LIST: ", input_list)

        for i in range(1,len(input_list)):
            self.asin_list.append(input_list[i][0])

        print("check here list of ASINs: ", self.asin_list)
        return self.asin_list

    def make_keepa_call(self):
        #fetch and return all data from keepa.com
        for item in self.asin_list:
            product = self.api.query(item)
            self.raw_data_list.append(product)
        return self.raw_data_list

    def write_out(self):
        with open(self.output_file, 'w+') as f:
            for item in self.result:
                f.write("%s\n" % item)

    def play_with_data(self):

        #for tests only - work with first product from the InputFile
        product = self.raw_data_list[0]

        print('AVAILABLE KEYS: ')
        print(product[0].keys())

        print('DATA ALL KEYS:')
        print(product[0]['data'].keys())

        print('AMAZON PRICE - RAW ARRAY')
        print(product[0]['data']['AMAZON'])

        #add Title to the result list
        if self.config['StandardKeepaFields']['Title'] == '1':
            print('TITLE HERE - ', product[0]['title'])
            self.result.append('Title: ' + product[0]['title'])

        if self.config['StandardKeepaFields']['Amazon: Current'] == '1':
            print('Amazon: Current HERE - ', product[0]['data']['AMAZON'][-1])
            self.result.append('Amazon: Current: ' + str(product[0]['data']['AMAZON'][-1]))


        print('length: ', product[0]['packageLength'])
        print('width: ', product[0]['packageWidth'])
        print('weight: ', product[0]['packageWeight'])
        print('model: ', product[0]['model'])
        #print('hasReviews: ')
        #print(product[0]['hasReviews'])
        #print('RAW DATA: -> SALES ')
        #print(product[0]['data']['SALES'])
        #print('categories: ')
        #print(product[0]['categories'])
        newprice = product[0]['data']['NEW']
        newpricetime = product[0]['data']['NEW_time']
        # print the first 10 prices
        #print('%20s %s' % ('Date', 'Price'))
        #for i in range(100):
        #    print('%20s $%.2f' % (newpricetime[i], newprice[i]))

        print('New - 90 days avg. - ')
        past_90 = datetime.now() - timedelta(days=90)
        print('LENGTH OF NEWPRICE TIME:', len(newpricetime))
        price_avg_90 = 0
        count_dates = 0
        for i in range(len(newpricetime)):
            #print('CHECK HERE', newpricetime[i])
            if newpricetime[i] > past_90:
                print('%20s $%.2f' % (newpricetime[i], newprice[i]))
                count_dates += 1
                price_avg_90 += newprice[i]
        #print('AVG 90 days PRICE = ', price_avg_90/count_dates)


        amazonprice = product[0]['data']['AMAZON']
        amazonpricetime = product[0]['data']['AMAZON_time']

        print('AMAZON - 90 days avg. - ')
        past_90 = datetime.now() - timedelta(days=90)
        print('LENGTH OF AMAZONPRICE TIME:', len(newpricetime))
        price_amazon_90 = 0
        count_dates = 0
        for i in range(len(amazonpricetime)):
            # print('CHECK HERE', amazonpricetime[i])
            if amazonpricetime[i] > past_90:
                print('%20s $%.2f' % (amazonpricetime[i], amazonprice[i]))
                count_dates += 1
                price_amazon_90 += amazonprice[i]
        print('amazon 90 days PRICE = ', price_amazon_90 / count_dates)


        print('Sales Rank: ALL: - ')
        print(product[0]['data']['SALES'])

        salesrank = product[0]['data']['SALES']
        salesranktime = product[0]['data']['SALES_time']

        print('salesrank - 30 days avg. - ')
        past_30 = datetime.now() - timedelta(days=30)
        print('LENGTH OF salesrank TIME:', len(salesranktime))
        salesrank_30 = 0
        count_dates = 0
        for i in range(len(salesranktime)):
            # print('CHECK HERE', amazonpricetime[i])
            if salesranktime[i] > past_90:
                print(salesranktime[i], salesrank[i])
                count_dates += 1
                salesrank_30 += salesrank[i]
        print('salesrank 30 days average', salesrank_30 / count_dates)

        #for tests - return all data fetched for ASIN
        #self.result = self.raw_data_list

        return self.result





