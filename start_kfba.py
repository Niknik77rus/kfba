from kfba import *
import argparse
import fbacalculator

parser = argparse.ArgumentParser()
parser.add_argument("--config",
                    help="config file")

args = parser.parse_args()

config_file = args.config

print('config file path: ', config_file)
kfba_instance = MainFBA(config_file)

print('Starting the job...')
kfba_instance.parse_cfg()
kfba_instance.read_input()
kfba_instance.make_keepa_call()
kfba_instance.play_with_data()
kfba_instance.write_out()

print('Dummy call of FBA calculator:')
print(fbacalculator.calculate_fees(10,10,10,10))
print('Job is completed...')