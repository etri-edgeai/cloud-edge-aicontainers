import redis 
import pandas
import time

#configuration
r = redis.Redis(host='host.docker.internal',port=6379)
states = {
    'ID':'9ry6syr7us0',
    'NH':'drv4kczq940',
    'MA':'drt1pxuzut0',
    'CA':'9qe14x68bs0',
    'OH':'dphvxkevxf0',
    'IN':'dp4v05s60h0',
    'NJ':'dr4f8781000',
    'WY':'9xetn99xen0',
    'AZ':'9w118n2j270',
    'NY':'drdst7ftjk0',
    'KY':'dnsp62kqn40',
    'PA':'dr347kudv00',
    'AL':'djdpy7remd0',
    'HI':'8e90m9vs130',
    'OK':'9y7j63pbpu0',
    'WV':'dnyvb5txqn0',
    'WA':'c26pskzdrf0',
    'GA':'djutjk84bj0',
    'AK':'befbmupuzu0',
    'CT':'drkk9tj3x30',
    'NV':'9rhdue0n8h0',
    'MI':'dpggkgpupb0',
    'MN':'cbhxyt2p250',
    'MO':'9yy5kwpvry0',
    'UT':'9x02k2pcxg0',
    'MD':'dqcqpup9bz0',
    'VA':'dq8xb82h000',
    'NE':'9z2uh6y5p00',
    'ND':'cb2x46xbzc0',
    'TX':'9v8bk7qhp50',
    'AR':'9ynmvznh8q0',
    'CO':'9wvnd2rczf0',
    'FL':'dhvz72pzpy0',
    'KS':'9yf71bwwf20',
    'NM':'9whe5t2j840',
    'DC':'dqcjqfz6y50',
    'IA':'9zmrn7zgzf0',
    'NC':'dnqe99bn0p0',
    'OR':'9rf63cywd60',
    'RI':'drmjhzr2150',
    'VT':'dru639vqx60',
    'MT':'c8655tb02n0',
    'IL':'dp0ewcb0vs0',
    'WI':'dpbm5kup6c0',
    'SC':'dnn23pdmkn0',
    'TN':'dn6kh00h240',
    'SD':'9zbvhkypr10',
    'LA':'9vqkfuxvpz0',
    'MS':'djb58p2nbj0',
    'ME':'f2nfn6zvrf0',
    'DE':'dqfmcgwx6q0'
}

while True:
    for state in states:
        geohash = states[state]
        r.delete('tested:' + state)
        r.delete('positive:' + state)
        r.delete('deaths:' + state)
        url = "http://coronavirusapi.com/getTimeSeries/" + str(state)
        print(url)
        data = pandas.read_csv(url)
        for i in range(0, len(data)):
            ts=str(int(data['seconds_since_Epoch'][i])*1000)
            r.execute_command('ts.add tested:' + str(state) + ' ' + ts + ' ' + str(data['tested'][i]) + ' LABELS state ' + str(state) + ' metric tested geohash ' + geohash)
            r.execute_command('ts.add positive:' + str(state) + ' ' + ts + ' ' + str(data['positive'][i]) + ' LABELS state ' + str(state) + ' metric positive geohash ' + geohash)
            r.execute_command('ts.add deaths:' + str(state) + ' ' + ts + ' ' + str(data['deaths'][i]) + ' LABELS state ' + str(state) + ' metric deaths geohash ' + geohash)
        r.sadd("states:abbr:list", state)
    print('Done, now sleep until tomorrow')
    time.sleep(86400)