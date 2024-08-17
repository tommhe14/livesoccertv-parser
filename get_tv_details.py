import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pytz
import datetime

DEFAULT_TIMEZONE = 'Europe/London'

base_url = 'https://www.livesoccertv.com/teams/'

timezone_to_country = {
    'Africa/Abidjan': 'Ivory Coast',
    'Africa/Accra': 'Ghana',
    'Africa/Addis_Ababa': 'Ethiopia',
    'Africa/Algiers': 'Algeria',
    'Africa/Bamako': 'Mali',
    'Africa/Bangui': 'Central African Republic',
    'Africa/Banjul': 'Gambia',
    'Africa/Bissau': 'Guinea-Bissau',
    'Africa/Blantyre': 'Malawi',
    'Africa/Brazzaville': 'Congo',
    'Africa/Bujumbura': 'Burundi',
    'Africa/Cairo': 'Egypt',
    'Africa/Casablanca': 'Morocco',
    'Africa/Ceuta': 'Spain',
    'Africa/Conakry': 'Guinea',
    'Africa/Dakar': 'Senegal',
    'Africa/Dar_es_Salaam': 'Tanzania',
    'Africa/Djibouti': 'Djibouti',
    'Africa/Douala': 'Cameroon',
    'Africa/East_Cape': 'South Africa',
    'Africa/Eldoret': 'Kenya',
    'Africa/Freetown': 'Sierra Leone',
    'Africa/Gaborone': 'Botswana',
    'Africa/Gbagada': 'Nigeria',
    'Africa/Ghana': 'Ghana',
    'Africa/Guinea': 'Guinea',
    'Africa/Johannesburg': 'South Africa',
    'Africa/Kampala': 'Uganda',
    'Africa/Kinshasa': 'Congo (Kinshasa)',
    'Africa/Kisumu': 'Kenya',
    'Africa/Kotonou': 'Benin',
    'Africa/Lagos': 'Nigeria',
    'Africa/Luanda': 'Angola',
    'Africa/Lubumbashi': 'Democratic Republic of Congo',
    'Africa/Lusaka': 'Zambia',
    'Africa/Malabo': 'Equatorial Guinea',
    'Africa/Maseru': 'Lesotho',
    'Africa/Mbabane': 'Swaziland',
    'Africa/Mogadishu': 'Somalia',
    'Africa/Montevideo': 'Uruguay',
    'Africa/Nairobi': 'Kenya',
    'Africa/Ndjamena': 'Chad',
    'Africa/Niamey': 'Niger',
    'Africa/Nouakchott': 'Mauritania',
    'Africa/Ouagadougou': 'Burkina Faso',
    'Africa/Porto-Novo': 'Benin',
    'Africa/Sao_Tome': 'Sao Tome and Principe',
    'Africa/Timbuktu': 'Mali',
    'Africa/Tunis': 'Tunisia',
    'Africa/Windhoek': 'Namibia',
    'America/Adak': 'United States',
    'America/Anchorage': 'United States',
    'America/Anguilla': 'Anguilla',
    'America/Antigua': 'Antigua and Barbuda',
    'America/Araguaina': 'Brazil',
    'America/Argentina/Buenos_Aires': 'Argentina',
    'America/Argentina/Catamarca': 'Argentina',
    'America/Argentina/ComodRivadavia': 'Argentina',
    'America/Argentina/Jujuy': 'Argentina',
    'America/Argentina/La_Rioja': 'Argentina',
    'America/Argentina/Mendoza': 'Argentina',
    'America/Argentina/Rio_Gallegos': 'Argentina',
    'America/Argentina/Salta': 'Argentina',
    'America/Argentina/San_Juan': 'Argentina',
    'America/Argentina/San_Luis': 'Argentina',
    'America/Argentina/Tucuman': 'Argentina',
    'America/Argentina/Ushuaia': 'Argentina',
    'America/Aruba': 'Aruba',
    'America/Asuncion': 'Paraguay',
    'America/Atikokan': 'Canada',
    'America/Bahia': 'Brazil',
    'America/Bahia_Banderas': 'Mexico',
    'America/Barbados': 'Barbados',
    'America/Belem': 'Brazil',
    'America/Belize': 'Belize',
    'America/Blanc-Sablon': 'Canada',
    'America/Boa_Vista': 'Brazil',
    'America/Bogota': 'Colombia',
    'America/Boise': 'United States',
    'America/Cambridge_Bay': 'Canada',
    'America/Campo_Grande': 'Brazil',
    'America/Cancun': 'Mexico',
    'America/Cardenas': 'Mexico',
    'America/Cayenne': 'French Guiana',
    'America/Cayman': 'Cayman Islands',
    'America/Chicago': 'United States',
    'America/Chihuahua': 'Mexico',
    'America/Costa_Rica': 'Costa Rica',
    'America/Creston': 'Canada',
    'America/Cuiaba': 'Brazil',
    'America/Curacao': 'Curacao',
    'America/Danmarkshavn': 'Greenland',
    'America/Dawson': 'Canada',
    'America/Dawson_Creek': 'Canada',
    'America/Denver': 'United States',
    'America/Detroit': 'United States',
    'America/Dominica': 'Dominica',
    'America/Edmonton': 'Canada',
    'America/Eirunepe': 'Brazil',
    'America/El_Salvador': 'El Salvador',
    'America/Fortaleza': 'Brazil',
    'America/Fort_Nelson': 'Canada',
    'America/Grenada': 'Grenada',
    'America/Guadeloupe': 'Guadeloupe',
    'America/Guatemala': 'Guatemala',
    'America/Guayaquil': 'Ecuador',
    'America/Guyana': 'Guyana',
    'America/Halifax': 'Canada',
    'America/Havana': 'Cuba',
    'America/Hermosillo': 'Mexico',
    'America/Indiana/Indianapolis': 'United States',
    'America/Indiana/Knox': 'United States',
    'America/Indiana/Marengo': 'United States',
    'America/Indiana/Petersburg': 'United States',
    'America/Indiana/Tell_City': 'United States',
    'America/Indiana/Vevay': 'United States',
    'America/Indiana/Vincennes': 'United States',
    'America/Indiana/Winamac': 'United States',
    'America/Inuvik': 'Canada',
    'America/Iqaluit': 'Canada',
    'America/Jamaica': 'Jamaica',
    'America/Jujuy': 'Argentina',
    'America/Juneau': 'United States',
    'America/Kentucky/Louisville': 'United States',
    'America/Kentucky/Monticello': 'United States',
    'America/Kralendijk': 'Bonaire',
    'America/La_Paz': 'Bolivia',
    'America/Lima': 'Peru',
    'America/Los_Angeles': 'United States',
    'America/Maceio': 'Brazil',
    'America/Managua': 'Nicaragua',
    'America/Martinique': 'Martinique',
    'America/Matamoros': 'Mexico',
    'America/Mazatlan': 'Mexico',
    'America/Mendoza': 'Argentina',
    'America/Mexico_City': 'Mexico',
    'America/Montreal': 'Canada',
    'America/Montserrat': 'Montserrat',
    'America/Nassau': 'Bahamas',
    'America/New_York': 'United States',
    'America/Nipigon': 'Canada',
    'America/Nome': 'United States',
    'America/Noronha': 'Brazil',
    'America/North_Dakota/Beulah': 'United States',
    'America/North_Dakota/Center': 'United States',
    'America/North_Dakota/New_Salem': 'United States',
    'America/Ojinaga': 'Mexico',
    'America/Panama': 'Panama',
    'America/Paraguay': 'Paraguay',
    'America/Phoenix': 'United States',
    'America/Port-au-Prince': 'Haiti',
    'America/Port_of_Spain': 'Trinidad and Tobago',
    'America/Recife': 'Brazil',
    'America/Regina': 'Canada',
    'America/Rio_Branco': 'Brazil',
    'America/Santa_Isabel': 'Mexico',
    'America/Santarem': 'Brazil',
    'America/Santiago': 'Chile',
    'America/Santo_Domingo': 'Dominican Republic',
    'America/Sao_Paulo': 'Brazil',
    'America/Scoresby_Sund': 'Greenland',
    'America/St_Johns': 'Canada',
    'America/St_Kitts': 'Saint Kitts and Nevis',
    'America/St_Lucia': 'Saint Lucia',
    'America/St_Thomas': 'United States',
    'America/St_Vincent': 'Saint Vincent and the Grenadines',
    'America/Tegucigalpa': 'Honduras',
    'America/Thule': 'Greenland',
    'America/Thunder_Bay': 'Canada',
    'America/Tijuana': 'Mexico',
    'America/Toronto': 'Canada',
    'America/Tortola': 'British Virgin Islands',
    'America/Vancouver': 'Canada',
    'America/Whitehorse': 'Canada',
    'America/Winnipeg': 'Canada',
    'America/Yakutat': 'United States',
    'America/Yellowknife': 'Canada',
    'Antarctica/Palmer': 'Antarctica',
    'Antarctica/Rothera': 'Antarctica',
    'Antarctica/Scott': 'Antarctica',
    'Antarctica/South_Pole': 'Antarctica',
    'Asia/Aden': 'Yemen',
    'Asia/Almaty': 'Kazakhstan',
    'Asia/Amman': 'Jordan',
    'Asia/Anadyr': 'Russia',
    'Asia/Aqtau': 'Kazakhstan',
    'Asia/Aqtobe': 'Kazakhstan',
    'Asia/Ashgabat': 'Turkmenistan',
    'Asia/Baku': 'Azerbaijan',
    'Asia/Bangkok': 'Thailand',
    'Asia/Barnaul': 'Russia',
    'Asia/Beirut': 'Lebanon',
    'Asia/Bishkek': 'Kyrgyzstan',
    'Asia/Brunei': 'Brunei',
    'Asia/Chongqing': 'China',
    'Asia/Colombo': 'Sri Lanka',
    'Asia/Damascus': 'Syria',
    'Asia/Dhaka': 'Bangladesh',
    'Asia/Dili': 'Timor-Leste',
    'Asia/Dubai': 'United Arab Emirates',
    'Asia/Gaza': 'Palestine',
    'Asia/Hebron': 'Palestine',
    'Asia/Ho_Chi_Minh': 'Vietnam',
    'Asia/Hong_Kong': 'Hong Kong',
    'Asia/Irkutsk': 'Russia',
    'Asia/Jakarta': 'Indonesia',
    'Asia/Jayapura': 'Indonesia',
    'Asia/Jerusalem': 'Israel',
    'Asia/Kabul': 'Afghanistan',
    'Asia/Kamchatka': 'Russia',
    'Asia/Karachi': 'Pakistan',
    'Asia/Kathmandu': 'Nepal',
    'Asia/Kolkata': 'India',
    'Asia/Krasnoyarsk': 'Russia',
    'Asia/Kuala_Lumpur': 'Malaysia',
    'Asia/Kuching': 'Malaysia',
    'Asia/Macau': 'Macau',
    'Asia/Magadan': 'Russia',
    'Asia/Makassar': 'Indonesia',
    'Asia/Manila': 'Philippines',
    'Asia/Muscat': 'Oman',
    'Asia/Nicosia': 'Cyprus',
    'Asia/Novokuznetsk': 'Russia',
    'Asia/Novosibirsk': 'Russia',
    'Asia/Omsk': 'Russia',
    'Asia/Oral': 'Kazakhstan',
    'Asia/Phnom_Penh': 'Cambodia',
    'Asia/Pontianak': 'Indonesia',
    'Asia/Pyongyang': 'North Korea',
    'Asia/Qatar': 'Qatar',
    'Asia/Qostanay': 'Kazakhstan',
    'Asia/Riyadh': 'Saudi Arabia',
    'Asia/Saigon': 'Vietnam',
    'Asia/Sakhalin': 'Russia',
    'Asia/Samarkand': 'Uzbekistan',
    'Asia/Seoul': 'South Korea',
    'Asia/Shanghai': 'China',
    'Asia/Singapore': 'Singapore',
    'Asia/Srednekolymsk': 'Russia',
    'Asia/Taipei': 'Taiwan',
    'Asia/Tashkent': 'Uzbekistan',
    'Asia/Tbilisi': 'Georgia',
    'Asia/Tehran': 'Iran',
    'Asia/Thimphu': 'Bhutan',
    'Asia/Tokyo': 'Japan',
    'Asia/Ulaanbaatar': 'Mongolia',
    'Asia/Urumqi': 'China',
    'Asia/Vientiane': 'Laos',
    'Asia/Vladivostok': 'Russia',
    'Asia/Yakutsk': 'Russia',
    'Asia/Yekaterinburg': 'Russia',
    'Asia/Yerevan': 'Armenia',
    'Atlantic/Azores': 'Portugal',
    'Atlantic/Bermuda': 'Bermuda',
    'Atlantic/Canary': 'Spain',
    'Atlantic/Cape_Verde': 'Cape Verde',
    'Atlantic/Faeroe': 'Faroe Islands',
    'Atlantic/Madeira': 'Portugal',
    'Atlantic/Reykjavik': 'Iceland',
    'Atlantic/South_Georgia': 'South Georgia and the South Sandwich Islands',
    'Atlantic/St_Helena': 'Saint Helena',
    'Australia/Adelaide': 'Australia',
    'Australia/Brisbane': 'Australia',
    'Australia/Darwin': 'Australia',
    'Australia/Hobart': 'Australia',
    'Australia/Lord_Howe': 'Australia',
    'Australia/Melbourne': 'Australia',
    'Australia/Perth': 'Australia',
    'Australia/Sydney': 'Australia',
    'Europe/Amsterdam': 'Netherlands',
    'Europe/Andorra': 'Andorra',
    'Europe/Athens': 'Greece',
    'Europe/Belfast': 'United Kingdom',
    'Europe/Belgrade': 'Serbia',
    'Europe/Berlin': 'Germany',
    'Europe/Bratislava': 'Slovakia',
    'Europe/Brussels': 'Belgium',
    'Europe/Bucharest': 'Romania',
    'Europe/Budapest': 'Hungary',
    'Europe/Chisinau': 'Moldova',
    'Europe/Copenhagen': 'Denmark',
    'Europe/Dublin': 'Ireland',
    'Europe/Gibraltar': 'Gibraltar',
    'Europe/Guernsey': 'Guernsey',
    'Europe/Helsinki': 'Finland',
    'Europe/Isle_of_Man': 'Isle of Man',
    'Europe/Istanbul': 'Turkey',
    'Europe/Jersey': 'Jersey',
    'Europe/Kaliningrad': 'Russia',
    'Europe/Kiev': 'Ukraine',
    'Europe/Lisbon': 'Portugal',
    'Europe/Ljubljana': 'Slovenia',
    'Europe/London': 'United Kingdom',
    'Europe/Madrid': 'Spain',
    'Europe/Malta': 'Malta',
    'Europe/Mariehamn': 'Åland Islands',
    'Europe/Minsk': 'Belarus',
    'Europe/Monaco': 'Monaco',
    'Europe/Moscow': 'Russia',
    'Europe/Nicosia': 'Cyprus',
    'Europe/Oslo': 'Norway',
    'Europe/Paris': 'France',
    'Europe/Podgorica': 'Montenegro',
    'Europe/Prague': 'Czech Republic',
    'Europe/Riga': 'Latvia',
    'Europe/Rome': 'Italy',
    'Europe/San_Marino': 'San Marino',
    'Europe/Sarajevo': 'Bosnia and Herzegovina',
    'Europe/Simferopol': 'Russia',
    'Europe/Sofia': 'Bulgaria',
    'Europe/Stockholm': 'Sweden',
    'Europe/Tallinn': 'Estonia',
    'Europe/Tirane': 'Albania',
    'Europe/Uzhgorod': 'Ukraine',
    'Europe/Vaduz': 'Liechtenstein',
    'Europe/Vatican': 'Vatican City',
    'Europe/Vienna': 'Austria',
    'Europe/Vilnius': 'Lithuania',
    'Europe/Volgograd': 'Russia',
    'Europe/Warsaw': 'Poland',
    'Europe/Zagreb': 'Croatia',
    'Europe/Zurich': 'Switzerland',
    'Indian/Antananarivo': 'Madagascar',
    'Indian/Chagos': 'British Indian Ocean Territory',
    'Indian/Christmas': 'Christmas Island',
    'Indian/Cocos': 'Cocos Islands',
    'Indian/Kerguelen': 'French Southern Territories',
    'Indian/Mahe': 'Seychelles',
    'Indian/Maldives': 'Maldives',
    'Indian/Reunion': 'Réunion',
    'Pacific/Apia': 'Samoa',
    'Pacific/Auckland': 'New Zealand',
    'Pacific/Chatham': 'New Zealand',
    'Pacific/Efate': 'Vanuatu',
    'Pacific/Fiji': 'Fiji',
    'Pacific/Funafuti': 'Tuvalu',
    'Pacific/Galapagos': 'Ecuador',
    'Pacific/Gambier': 'French Polynesia',
    'Pacific/Guam': 'Guam',
    'Pacific/Kiritimati': 'Kiribati',
    'Pacific/Kosrae': 'Micronesia',
    'Pacific/Nauru': 'Nauru',
    'Pacific/Niue': 'Niue',
    'Pacific/Norfolk': 'Norfolk Island',
    'Pacific/Pago_Pago': 'American Samoa',
    'Pacific/Palau': 'Palau',
    'Pacific/Pitcairn': 'Pitcairn Islands',
    'Pacific/Ponape': 'Micronesia',
    'Pacific/Port_Moresby': 'Papua New Guinea',
    'Pacific/Rarotonga': 'Cook Islands',
    'Pacific/Saipan': 'Northern Mariana Islands',
    'Pacific/Tarawa': 'Kiribati',
    'Pacific/Tongatapu': 'Tonga',
    'Pacific/Truk': 'Micronesia',
    'Pacific/Wallis': 'Wallis and Futuna',
    'Pacific/Wake': 'Wake Island',
    'Pacific/Wallis': 'Wallis and Futuna',
}


bad_country_codes = {
    'ESP': 'ES',
    'USA': 'US',
    'GBR': 'UK',
    'RUS': 'RU',
}

bad_lang_codes = {
    'us': 'en',
    'gb': 'en',
}

def fix_country_code(country):
    for bad, correct in bad_country_codes.items():
        country = country.replace(bad, correct)
    return country

def fix_lang_code(lang):
    for bad, correct in bad_lang_codes.items():
        lang = lang.replace(bad, correct)
    return lang

def get_team_url(country, team):
    # Ensure proper country code conversion for URL formation
    country_code = fix_country_code(country)
    return f"{base_url}{country_code.lower()}/{team}/"  # Ensure the slash at the end

async def get_body(session, country, team, timezone):
    url = get_team_url(country, team)
    print(f"Fetching URL: {url}")
    print(timezone)
    # Handle timezone formatting
    try:
        continent, city = timezone.split('/')
    except ValueError:
        continent, city = 'UTC', 'UTC'

    # Get the country based on the timezone
    country_from_timezone = timezone_to_country.get(timezone, country)

    country_code = fix_country_code(country_from_timezone)
    lang = fix_lang_code(country_from_timezone[:2].lower())
    locale = f"{lang}_{country_code}"

    cookies = {
        'live': 'live',
        'u_scores': 'on',
        'u_continent': continent,
        'u_country': country_from_timezone.replace(' ', '%20'),
        'u_country_code': country_code,
        'u_timezone': timezone.replace('/', '%2F'),
        'u_lang': 'en',
        'u_locale': 'en_US',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }

    async with session.get(url, cookies=cookies, headers=headers) as response:
        print(f"Response status code: {response.status}")
        print(cookies)
        if response.status == 200:
            return await response.text()
        else:
            print(f"Failed to fetch data from {url}")
            return None

def adjust_local_time(time_str, timezone):
    try:
        time = datetime.datetime.strptime(time_str, '%H:%M')
        local_time = pytz.timezone(timezone).localize(time)
        return local_time.strftime('%I:%M %p')
    except ValueError:
        return time_str

class Match:
    def __init__(self, n, soup):
        match_row = soup.select('tr.matchrow')[n]

        # Extract live status
        self.live = 'livematch' in match_row.get('class', [])

        # Extract played status
        livecell_span = match_row.select_one('td.timecol > div > span.livecell')
        self.played = livecell_span['title'] == 'Match ended' if livecell_span else False

        # Extract competition (from the text inside the <a> tag, if needed)
        self.competition = 'Unknown'

        # Extract date and time
        time_span = match_row.select_one('td.timecol > div > span.ts')
        self.time = time_span.text if time_span else 'Unknown'

        # Extract game details
        game_link = match_row.select_one('td#match a')
        self.game = game_link['title'] if game_link else 'Unknown'

        # Extract TV channels
        tv_links = match_row.select('td#channels a')
        self.tvs = [a.text for a in tv_links if '…' not in a.text]

        # Extract date (if available in the HTML)
        date_span = match_row.select_one('td.timecol > div > span.inprogress')
        self.date = date_span['title'] if date_span and 'title' in date_span.attrs else 'Unknown'

def parse_matches_from_html(body, timezone=None):
    if body is None:
        print("No HTML body to parse.")
        return []
    
    if timezone is None:
        timezone = DEFAULT_TIMEZONE

    soup = BeautifulSoup(body, 'html.parser')
    match_rows = soup.select('tr.matchrow')

    print(f"Found {len(match_rows)} match rows")

    matches = []
    for n in range(len(match_rows)):
        match = Match(n, soup)
        if match.tvs:  # Check if there are any TV channels listed
            match.time = adjust_local_time(match.time, timezone)
            matches.append(match)

    return matches

async def fetch_matches(country, team, timezone=None):
    if timezone is None:
        timezone = DEFAULT_TIMEZONE
    async with aiohttp.ClientSession() as session:
        body = await get_body(session, country, team, timezone)
        return parse_matches_from_html(body, timezone)

# Test the function
if __name__ == '__main__':
    async def test():
        country = 'england'
        team = 'manchester-united'
        timezone = 'Europe/London'
        
        matches = await fetch_matches(country, team, timezone)
        to_show = []
        if matches:
            for match in matches:
                print(match.__dict__)
                if not match.played:
                    to_show.append(match)

            print(to_show)
        else:
            print("No matches found.")

    asyncio.run(test())
