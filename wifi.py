#!/usr/local/bin/python3
# @Auther: Ramesh Neupane


import subprocess
import datetime
import json
import os


def is_empty(filepath):
    return os.stat(filepath).st_size == 0


def is_file(filepath):
    return os.path.isfile(filepath)


def read_json(filepath):
    if is_file(filepath):
        if is_empty(filepath):
            json_data = False
        else:
            with open(filepath, "r") as f:
                json_data = json.load(f)
    else:
        json_data = False
    return json_data


def write_json(filepath, json_content):
    with open(filepath, "w") as f:
        json.dump(json_content, f)


class DataStructure():
    def __init__(self, date, st={}):
        self.date = date
        self.ssid_time = st

    def add_data(self, ssid, time):
        self.ssid_time[ssid] = []
        self.ssid_time[ssid].append(time)

    def add_mdata(self, ssid_time):
        for ssid, times in ssid_time.items():
            for time in times:
                self.ssid_time[ssid].append(time)

    def get_oldest_time(self, ssid):
        return min(self.ssid_time.get(ssid))

    def get_newest_time(self, ssid):
        return max(self.ssid_time.get(ssid))

    def get_max_diff(self, ssid):
        return str(self.get_newest_time(ssid) - self.get_oldest_time(ssid))

    def __repr__(self):
        ssid_strtime = {}
        for k, v in self.ssid_time.items():
            uv = []
            for vv in v:
                uv.append(str(vv))
            ssid_strtime[k] = uv
        strdate = str(self.date)
        return {strdate: ssid_strtime}

    def get_total_dict_data(self):
        return self.__repr__()


def get_wifi_info():
    process = subprocess.Popen(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    process.wait()

    out = out.decode("utf-8")
    details = out.split("\n")
    details = filter(len, map(str.strip, details))

    info_dict = {}
    for detail in details:
        key, value = detail.split(":", 1)
        info_dict[key.strip()] = value.strip()
    return info_dict


def main():
    json_filepath = os.path.expanduser("~/.wifi_data.json")

    date_ssid_time = DataStructure(datetime.datetime.now().date())
    date_ssid_time.add_data(get_wifi_info().get('SSID'), datetime.datetime.now().time().replace(microsecond=0))

    json_data = read_json(json_filepath)
    if json_data:
        from_file = json.loads(json_data)
        date_ssid_time.add_mdata(from_file.get(str(date_ssid_time.date)))
        write_json(json_filepath, json.dumps(date_ssid_time.get_total_dict_data()))
    else:
        write_json(json_filepath, json.dumps(date_ssid_time.get_total_dict_data()))


if __name__ == "__main__":
    main()
