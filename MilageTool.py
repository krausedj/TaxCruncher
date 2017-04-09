

import googlemaps
import csv
import decimal
import json

"""Simple abstraction of a trip hop"""
class Hop(object):
    def __init__(self, Source, Dest, GMaps=None):
        self.Src = Source
        self.Dst = Dest
        self.Dist = 0
        if GMaps != None:
            self.MapDist = GMaps.distance_matrix(Source, Dest)
            self._UpdateDist()
        else:
            self.MapDist = None
            
    def _UpdateDist(self):
        try:
            self.Dist = decimal.Decimal(self.MapDist['rows'][0]['elements'][0]['distance']['value'])
        except:
            print('Could Not Find Distance: {0} to {1}'.format(self.Src, self.Dst))
            
    def CalcDistance(self, GMaps, ForceCalc=False):
        if self.MapDist == None or ForceCalc == True:
            self.MapDist = GMaps.distance_matrix(self.Src, self.Dst)
            self._UpdateDist()
            
"""Database of known hops"""
class HopManager(object):
    def __init__(self):
        self.Hops = {}
        
    def AddHop(self, Source, Dest):
        if (Source, Dest) not in self.Hops:
            self.Hops[(Source, Dest)] = Hop(Source, Dest)
            
        return self.Hops[(Source, Dest)]
            
    def CalcDistances(self, GMaps):
        for hop in self.Hops:
            self.Hops[hop].CalcDistance(GMaps)
            
    def LoadCache(self, FileName):
        try:
            file_cache = open(FileName,'r')
            data = json.load(file_cache)
            for hop in data:
                if (hop['Src'], hop['Dst']) not in self.Hops:
                    if decimal.Decimal(hop['Dist']) != 0:
                        self.Hops[(hop['Src'], hop['Dst'])] = Hop(hop['Src'], hop['Dst'])
                        self.Hops[(hop['Src'], hop['Dst'])].Dist = decimal.Decimal(hop['Dist'])
                        self.Hops[(hop['Src'], hop['Dst'])].MapDist = hop['MapDist']
            file_cache.close()
        except:
            print('Hop Cache {0} Could not be Loaded'.format(FileName))
            
    def SaveCache(self, FileName):
        #try:
        hop_data = []
        file_cache = open(FileName,'w')
        for hop_key in self.Hops:
            hop = self.Hops[hop_key]
            hop_elem = {'Src':hop.Src,'Dst':hop.Dst,'Dist':'{0}'.format(hop.Dist),'MapDist':hop.MapDist}
            hop_data.append(hop_elem)
        json.dump(hop_data, file_cache, sort_keys = True, indent = 4)
        file_cache.close()
        #except:
        #    print('Hop Cache {0} Could not be Writen'.format(FileName))

"""A trip, which has a list of locations traveled to, and the hops associated with it"""
class Trip(object):
    def __init__(self, CvsRowData, LocationDb, HopMgr):
        self.Date = CvsRowData[0]
        self.Vehicle = CvsRowData[1]
        self.Job = CvsRowData[2]
        self.Locs = []
        for data in CvsRowData[3:]:
            location = ''
            for line in ' '.join(data.split()).split('\n'):
                if line.strip() not in ('\r',''):
                    if location != '':
                        location = location + ',' + line.strip()
                    else:
                        location = line.strip()
            if location.lower() in LocationDb:
                location = LocationDb[location.lower()]
            if location not in ('','\n'):
                self.Locs.append(location)
        self.Hops = []
        self.Dist = 0
        for idx, loc in enumerate(self.Locs[0:-1]):
            self.AddHop(self.Locs[idx], self.Locs[idx+1], HopMgr)
            
    def AddHop(self, Source, Dest, HopMgr):
        self.Hops.append(HopMgr.AddHop(Source, Dest))
        
    def CalcDistances(self, GMaps):
        dist = decimal.Decimal(0)
        for hop in self.Hops:
            hop.CalcDistance(GMaps)
            dist = dist + decimal.Decimal(hop.Dist)
        self.Dist = dist

gmaps = googlemaps.client.Client('you have to put your API key here')

"""Lookup database for locations that you will commonly use in the CSV file"""
location_db = {
    'home':'some address',
    'work':'some other address'}

#data = gmaps.distance_matrix(location_db['home'], location_db['stratton'])

trips = []

"""Running this a lot could eat the google API key up, so cache data"""
hop_mgr = HopManager()
hop_mgr.LoadCache('hop_cache.json')

with open('/home/xxx/mileage_raw.csv', 'rt') as csvfile:
    locations = csv.reader(csvfile, delimiter=';', quotechar='"')

    start = True
    for row in locations:
        if start == False:
            trips.append(Trip(row, location_db, hop_mgr))
        else:
            start = False

hop_mgr.CalcDistances(gmaps)

"""Save the cache now incase something crashes"""
hop_mgr.SaveCache('hop_cache.json')

vehicle_dist = {}
for trip in trips:
    trip.CalcDistances(gmaps)
    if trip.Vehicle not in vehicle_dist:
        vehicle_dist[trip.Vehicle] = trip.Dist
    else:
        vehicle_dist[trip.Vehicle] = vehicle_dist[trip.Vehicle] + trip.Dist

out_file = open('/home/xxx/mileage_data.csv', 'w')

out_file.write('Summary;\n')
for veh in vehicle_dist:
    out_file.write('{0};{1} km;\n'.format(veh, vehicle_dist[veh] / 1000))
out_file.write('\n')
out_file.write('Details;\n')

for trip in trips:
    out_file.write('{0};{1};{2};\n'.format(trip.Date, trip.Job, trip.Vehicle))
    for hop in trip.Hops:
        out_file.write('     ;{0} km;{1};{2};\n'.format(hop.Dist / 1000, hop.Src, hop.Dst))
    out_file.write('Total;{0} km;\n\n'.format(trip.Dist / 1000))
    
out_file.close()

