import json
import pprint

def main():
    info = json.load(open('countries.json', 'r'))
    source = json.load(open('reddit-users-by-country-2024.json', 'r'))
    output = {}
    total_users = 0

    for country in source:
        name = country['country']
        country_info = list(filter(lambda country: country['name']['common'] == name or country['name']['official'] == name, info))[0]
        region, subregion = country_info['region'], country_info['subregion'] 
        try:
            output[region]['users (mil.)'] += country['RedditUsersTotalVisitsAllDevicesInMillions']
            output[region]['users (mil.)'] = round(output[region]['users (mil.)'], 2)
        except KeyError:
            output.update({
                region: {
                   'users (mil.)': country['RedditUsersTotalVisitsAllDevicesInMillions'], 
                   'share (%)': 0,
                   'subregions': {}, 
                }
            })
        try:
            output[region]['subregions'][subregion]['users (mil.)'] += country['RedditUsersTotalVisitsAllDevicesInMillions']
            output[region]['subregions'][subregion]['users (mil.)'] = round(output[region]['subregions'][subregion]['users (mil.)'], 2)
        except KeyError:          
            output[region]['subregions'].update({
                subregion: {
                    'users (mil.)': country['RedditUsersTotalVisitsAllDevicesInMillions'],
                    'share (%)': 0
                }
            })
        total_users += country['RedditUsersTotalVisitsAllDevicesInMillions']
    
    for region in output.values():
        region['share (%)'] = round(region['users (mil.)']/total_users*100, 2)
        for subregion in region['subregions'].values():
            subregion['share (%)'] = round(subregion['users (mil.)']/total_users*100, 2)
    
    pprint.pprint(output, sort_dicts=False)

if __name__ == '__main__':
    main()