#! /usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: 

# Done
# Call Procedure `link_store`.`sp_transfer_to_combined`()
# This transfers all records from the current links table
# over to the combined links table

# Done
# Call Procedure `link_store`.`sp_transfer_to_final`()
# This transfers all records from the combined links table
# over to the final links table

# Done
# Run code to fetch youtube data

# Add command arguments to control number of yt searches

import keyring, getpass, time, datetime, subprocess, configparser, argparse
# import multiprocessing

import mysql.connector as mariadb

from collections import namedtuple
# from tqdm.notebook import tqdm as log_progress
from tqdm import tqdm as log_progress

# from StoredLinkItem import StoredLinkItem
from Mariadb_activate import run_mariadb, key_implement

# usr = 'alan'
# dbase = 'link_store'
# db='links'

class LinkProcessor():
    
    current_config:str = 'config.ini'
    config:object
    usr:str
    dbase:str
    db:str
    cursor:object
    mariadb_connection:object
    last_link_date:str
    last_combined_date:str
    logfile:str = 'history.log'
    current_date:str
    
    
    def __init__(self):
        
        self.config = configparser.ConfigParser()
        self.config.read(self.current_config)
        self.usr = self.config['Database']['usr']
        self.dbase = self.config['Database']['dbase']
        self.db = self.config['Database']['db']
        
        self.last_link_date = self.config['Transfers']['links']
        self.last_combined_date = self.config['Transfers']['links_combined']
        
        self.logfile = self.config['Logs']['logfile']
        
        # self.startup()
        
        self.current_date = datetime.datetime.today().strftime('%Y-%m-%d')
        self.move_to_combined()
        self.move_to_final()
        
        # try:
            # self.cursor.close()
            # print("Cursor closed")
        # except ReferenceError:
            # print("Reference is still weak")
        # self.mariadb_connection.close()

    def startup(self)->object:
        
        psswd = key_implement(
                        dbase = self.dbase,
                        usr = self.usr)
        mariadb_state = run_mariadb()

        self.mariadb_connection = mariadb.connect(
                        user=self.usr, 
                        password=psswd, 
                        database=self.dbase)
        self.cursor = self.mariadb_connection.cursor(
                        buffered=True, 
                        named_tuple=True)

    def move_to_combined(self)->None:
        
        if self.last_link_date != self.current_date:
            self.startup()
            self.cursor.callproc( "sp_transfer_to_combined", () )
            # self.cursor.reset()
            self.config['Transfers']['links'] = self.current_date
            self.save_new_config()
            print("Links combined")
            self.cursor.close()
            self.mariadb_connection.close()
        else:
            print("Links have already been combined today")
        
    def move_to_final(self)->None:
        
        if self.last_combined_date != self.current_date:
            self.startup()
            self.cursor.callproc( "sp_transfer_to_final", () )
            self.cursor.reset()
            self.config['Transfers']['links_combined'] = self.current_date
            self.save_new_config()
            print("Links transferred to the final table")
            self.cursor.close()
            self.mariadb_connection.close()
        else:
            print("Links have already been finalised today")

    def save_new_config(self)->None:
        
        with open(self.current_config, 'w') as configfile:
            self.config.write(configfile)

    def yt_result(self, link:str, importdate:str)->namedtuple:
        Output = namedtuple('Output', ['upload_date', 'channel', 'channel_id', 'option'])
        
        # print(link)

        # If the link points to a full channel ID
        if link[:32]=='https://www.youtube.com/channel/':
            channel_output = link.replace('https://www.youtube.com/channel/', '')
            # _channel_date = f'{channel_output[0][:4]}-{channel_output[0][4:6]}-{channel_output[0][6:8]}'
            return Output(upload_date=importdate, channel='Unknown', 
                          channel_id=channel_output.split("/")[0], option=8)
        
        # If the link refers to a user channel
        if link[:29]=='https://www.youtube.com/user/':
            _channel_output = link.replace('https://www.youtube.com/user/', '')
            # _channel_date = f'{channel_output[0][:4]}-{channel_output[0][4:6]}-{channel_output[0][6:8]}'
            try:
                _strip_placement = _channel_output.index("?")
                return Output(upload_date=importdate, channel='Unknown', 
                          channel_id=_channel_output[:_strip_placement], option=8)
            except:
                return Output(upload_date=importdate, channel='Unknown', 
                              channel_id=_channel_output.split("/")[0], option=8)
        
        # If the link points to short form channel
        # https://www.youtube.com/c/Tablestory/videos
        if link[:26]=='https://www.youtube.com/c/':
            return Output(upload_date=importdate, channel='Unknown', channel_id='Unknown', option=1)

        # If the link points to youtube search results
        if link[:32]=='https://www.youtube.com/results?':
            return Output(upload_date=importdate, channel='Unknown',
                          channel_id='Unknown', option=9)
        
        # If the link points to a user's playlist collection - this should never be called because of the user code above
        # TODO: Merge this with the user code above if appropriate
        # if link.split("/")[-1]=='playlists':
            # return Output(upload_date=importdate, channel='Unknown',
                          # channel_id='Unknown', option=7)
        # https://www.youtube.com/user/GophersVids/playlists
        
        # If the link points to a specific playlist
        # https://www.youtube.com/playlist?list=RDCLAK5uy_l2zLaMIWOqWSePvTSmt49GcuR8460ZR10
        if link[:32]=='https://www.youtube.com/playlist':
            return Output(upload_date=importdate, channel='Unknown', channel_id='Unknown', option=1)

        # Otherwise assume the link points to an usable source
        try:
            result = subprocess.run(['youtube-dl', '--get-filename', '--skip-download', '--no-playlist',
                                 # '--cookies', '/home/human1/dwhelper/cookies-chrome-20200721.txt', 
                                 '--force-ipv4',
                                 '-o', '%(upload_date)s - %(uploader)s - %(channel_id)s', 
                                 link], 
                                capture_output=True, encoding='UTF8', timeout=12)
        except:
            # subprocess.run(['paplay', '/usr/share/sounds/freedesktop/stereo/suspend-error.oga'])
            return Output(upload_date=importdate, channel='Unknown', channel_id='Unknown', option=1)
        # print(result)
        # If the channel link is passed to the above, the result will include 
        # *all* the video links and their data!
        
        if result.returncode:
            # If Youtube has blocked the IP
            if "HTTP Error 429: Too Many Requests" in result.stdout:
                subprocess.run(['paplay', '/usr/share/sounds/freedesktop/stereo/suspend-error.oga'])
                raise ConnectionRefusedError(result.stdout)
            # In any case, return something
            return Output(upload_date=importdate, channel='Unknown', channel_id='Unknown', option=1)
        try:
            _date_original, _channel_intermediate = result.stdout.split(' - ', 1)
            _channel, _channel_id_original = _channel_intermediate.rsplit(' - ', 1)
            # _date_original, _channel, _channel_id_original = result.stdout.split(' - ')
            _channel_id = _channel_id_original.rstrip('\n')
            _date_as_date = datetime.datetime.strptime(_date_original, '%Y%m%d')
            _date = datetime.datetime.strftime(_date_as_date, '%Y-%m-%d')
            return Output(upload_date=_date, channel=_channel, channel_id=_channel_id, option=2)
            # print(f'ID: {_row.link_id}, Channel: {_channel}, Upload date: {_date}, Link: {_link}')
            # channel_list.add((_channel, _link))
        except:
            print(result)
            subprocess.run(['paplay', '/usr/share/sounds/freedesktop/stereo/suspend-error.oga'])

    def yt_runner(self, _limit_value:int=50):

        # print(cursor.column_names)
        # print(cursor.description)
        # version = cursor.fetchone()
        # print(version)
        # cursor.reset()

        self.startup()
        link_group = []
        channel_set = set()
        channel_existing = set()
        Linkdata = namedtuple('Linkdata', ['id', 'title', 'link', 'source', 'import_date', 
                                             'channel_id', 'channel_name', 'upload_date', 'available'])
        
        # try:
            # self.cursor.reset()
            # print("Cursor reset")
        # except:
            # self.startup()
            # print("Cursor was not running: restarted")
        
        self.cursor.execute("SELECT * FROM link_store.ytView WHERE upload_date IS NULL ORDER BY importdate DESC LIMIT %s;" % (_limit_value))

        linksList = self.cursor.fetchall()
        progress_count = len(linksList)
        # for item in log_progress(linksList):
        for item in log_progress(linksList, total=progress_count, desc="Processing records"):
            # print(item)
            # print(yt_result(link=item.link, importdate=item.importdate))
            time.sleep(2)
            d = self.yt_result(link=item.link, importdate=item.importdate)
            item_data = Linkdata(id=item.link_id, title=item.title, link=item.link,
                                 source=item.source, import_date=item.importdate,
                                 channel_id=d.channel_id, channel_name=d.channel,
                                 upload_date=d.upload_date, available=d.option)
            link_group.append(item_data)
            channel_set.add((d.channel_id,d.channel))
            
                                     
        # print(link_group)
        self.cursor.reset()

        # print(channel_set)

        self.cursor.execute("SELECT channel_id, channel_name FROM link_store.yt_lookup_channel;")
        # channel_existing = cursor.fetchall()
        # print(channel_existing)
        for che in self.cursor.fetchall():
            channel_existing.add((che.channel_id, che.channel_name))
            # print(che)

        # print(channel_existing)
        # print(channel_set - channel_existing)
        channel_remainder = channel_set - channel_existing
        if channel_remainder:
            print(channel_remainder)
            try:
                self.cursor.executemany('INSERT IGNORE INTO yt_lookup_channel(channel_id, channel_name) VALUES(%s, %s)', 
                                  channel_remainder)
            except:
                print("Failed to insert channel data")
            finally:
                self.cursor.reset()
        else:
            print('No channel changes to make')
        self.cursor.reset()
        channel_data_to_upload = [ (x.id, x.channel_id, x.available, x.upload_date) for x in link_group ]
        # print(channel_data_to_upload)
        try:
            # cursor.execute('INSERT INTO ytlinks(final_id, channel_id, available, upload_date) VALUES(%s, %s, %s, %s)', 
                        # (link_group[0].id, link_group[0].channel_id, link_group[0].available, link_group[0].upload_date))
            self.cursor.executemany('INSERT IGNORE INTO ytlinks(final_id, channel_id, available, upload_date) VALUES(%s, %s, %s, %s)', 
                              channel_data_to_upload)
        finally:
            # self.cursor.close()
            # self.mariadb_connection.close()
            self.cursor.reset()
        # subprocess.run(['paplay', '/usr/share/sounds/freedesktop/stereo/complete.oga'])
        self.cursor.close()
        self.mariadb_connection.close()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Process some links.')
    
    # parser.add_argument("number", help="how many links to process", type=int, default=0)
    # parser.add_argument("-y", "--youtube", help="process youtube links", action="store_true")
    parser.add_argument("-y", "--youtube", help="process youtube links", type=int, default=0)
    parser.add_argument("--force-combined", help="move links to combined", action="store_true")
    parser.add_argument("--force-final", help="transfer combined to final", action="store_true")
    
    args = parser.parse_args()
    linkP = LinkProcessor()
    if args.youtube != 0:
        if args.youtube <= 10:
            linkP.yt_runner(args.youtube)
        else:
            for i in range(10,args.youtube,10):
                linkP.yt_runner(i)
    
    subprocess.run(['paplay', '/usr/share/sounds/freedesktop/stereo/complete.oga'])
