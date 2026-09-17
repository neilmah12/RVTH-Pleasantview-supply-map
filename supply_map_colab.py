# ============================================================
# EXISTING TOWNHOME SUPPLY MAP - River Valley & Pleasantview - Colab
# ============================================================
# 1. Edit PROJECTS below as needed
# 2. Run the cell
# 3. Download: Files panel > right-click file > Download
# ============================================================

import re
from IPython.display import IFrame, display

PROJECTS = [
    {"id": 0, "name": "Youngstown Townhomes and Apartments", "address": "16316 106A AVE NW", "units": 36, "year_built": 1964, "subdivision": "Youngstown", "lat": 53.550930015534, "lng": -113.604708990829, "subject": False},
    {"id": 1, "name": "Wedgewood Homes", "address": "12269 131 ST NW", "units": 143, "year_built": 1962, "subdivision": "Sherbrooke", "lat": 53.576998279233, "lng": -113.550342709548, "subject": False},
    {"id": 2, "name": "Summerfield", "address": "3003 116 ST NW", "units": 67, "year_built": 1977, "subdivision": "Sweet Grass", "lat": 53.46249599171, "lng": -113.531042036382, "subject": False},
    {"id": 3, "name": "River Valley Townhomes", "address": "4210 102 AVE NW", "units": 216, "year_built": 1960, "subdivision": "Gold Bar", "lat": 53.54266311905697, "lng": -113.41360683773034, "subject": True},
    {"id": 4, "name": "Delton Townhomes", "address": "8313 130 AVE NW", "units": 280, "year_built": 1960, "subdivision": "Killarney", "lat": 53.587731012883, "lng": -113.469072027816, "subject": False},
    {"id": 5, "name": "Elmwood Townhomes", "address": "8319 169 ST NW", "units": 200, "year_built": 1962, "subdivision": "Elmwood", "lat": 53.517786000631, "lng": -113.610950994124, "subject": False},
    {"id": 6, "name": "Oxford Mews", "address": "13107 153 AVE NW", "units": 180, "year_built": 2004, "subdivision": "Cumberland", "lat": 53.615558596149, "lng": -113.546020497357, "subject": False},
    {"id": 7, "name": "6908 129 Ave Nw", "address": "6908 129 AVE NW", "units": 1, "year_built": 1997, "subdivision": None, "lat": 53.587797984289, "lng": -113.44803303175, "subject": False},
    {"id": 8, "name": "165 Roseland Villge Nw", "address": "165 ROSELAND VILLGE NW", "units": 1, "year_built": 1990, "subdivision": None, "lat": 53.603812616134, "lng": -113.474486737267, "subject": False},
    {"id": 9, "name": "Kameyosek Place", "address": "752 LAKEWOOD RD N NW", "units": 48, "year_built": 1982, "subdivision": None, "lat": 53.462203211832, "lng": -113.447062826458, "subject": False},
    {"id": 10, "name": "11311 102 Ave Nw", "address": "11311 102 AVE NW", "units": 7, "year_built": 1980, "subdivision": None, "lat": 53.542803006034, "lng": -113.516333975604, "subject": False},
    {"id": 11, "name": "Cavell Ridge Townhomes", "address": "1363 HERMITAGE RD NW", "units": 90, "year_built": 1980, "subdivision": None, "lat": 53.57866669706, "lng": -113.378112788023, "subject": False},
    {"id": 12, "name": "Stirlingwood Townhomes", "address": "16824-16874 109 ST", "units": 27, "year_built": 1976, "subdivision": None, "lat": 53.629975008606, "lng": -113.512858000357, "subject": False},
    {"id": 13, "name": "9453 156 St Nw", "address": "9453 156 ST NW", "units": 15, "year_built": 1970, "subdivision": None, "lat": 53.531063982999, "lng": -113.58983999751, "subject": False},
    {"id": 14, "name": "Greenwood Village", "address": "163 GREENWOOD VILLGE", "units": 230, "year_built": 1970, "subdivision": None, "lat": 53.524350120465, "lng": -113.322044728939, "subject": False},
    {"id": 15, "name": "425 Walker Rd Nw", "address": "425 WALKER RD NW", "units": 35, "year_built": 1970, "subdivision": None, "lat": 53.498432982479, "lng": -113.610248003905, "subject": False},
    {"id": 16, "name": "Ascot Gardens", "address": "12911 132 AVE NW", "units": 108, "year_built": 1957, "subdivision": None, "lat": 53.591286993395, "lng": -113.5448359668, "subject": False},
    {"id": 17, "name": "9732 75 Ave Nw", "address": "9732 75 AVE NW", "units": 9, "year_built": 2000, "subdivision": None, "lat": 53.511631001491, "lng": -113.481407171805, "subject": False},
    {"id": 18, "name": "8223 99 St", "address": "8223 99 ST", "units": 14, "year_built": 2000, "subdivision": None, "lat": 53.518775903396, "lng": -113.485824602417, "subject": False},
    {"id": 19, "name": "El Louis Apartments", "address": "10710 127 ST NW", "units": 14, "year_built": 1962, "subdivision": "Westmount", "lat": 53.551395714074, "lng": -113.541768693152, "subject": False},
    {"id": 20, "name": "The Plaza", "address": "14810 121 ST NW", "units": 34, "year_built": 1975, "subdivision": "Caerarvon", "lat": 53.611282316787, "lng": -113.5323563188, "subject": False},
    {"id": 21, "name": "Broadmoor Apt Homes", "address": "9003 184 ST NW", "units": 64, "year_built": 1976, "subdivision": "Belmead", "lat": 53.525150298851, "lng": -113.641082762573, "subject": False},
    {"id": 22, "name": "Castleridge Estates", "address": "1 CAERNARVON CRT NW", "units": 108, "year_built": 1975, "subdivision": "oxford", "lat": 53.613330812013, "lng": -113.531829767642, "subject": False},
    {"id": 23, "name": "Huntington Hill", "address": "1 HUNTINGTON HILL NW", "units": 89, "year_built": 1981, "subdivision": "Empire Park", "lat": 53.485896882362, "lng": -113.497693461132, "subject": False},
    {"id": 24, "name": "Keegano", "address": "1-28 KEEGANO NW", "units": 52, "year_built": 1973, "subdivision": "Richfield", "lat": 53.469384994111, "lng": -113.463144010614, "subject": False},
    {"id": 25, "name": "Hillcrest Place", "address": "100 HILLCREST PL NW", "units": 143, "year_built": 1971, "subdivision": "Patricia Heights", "lat": 53.508348983484, "lng": -113.59216698147, "subject": False},
    {"id": 26, "name": "Cherry Hill Park Estates", "address": "10183 158 AVE NW", "units": 46, "year_built": 1981, "subdivision": "Beaumaris", "lat": 53.618544020512, "lng": -113.498305004788, "subject": False},
    {"id": 27, "name": "Shannon Green", "address": "10185 164 AVE NW", "units": 42, "year_built": 1978, "subdivision": "Lorelei", "lat": 53.625646007073, "lng": -113.499048982514, "subject": False},
    {"id": 28, "name": "Cypress Groves Townhouses", "address": "104 ST & 24 AVE NW", "units": 47, "year_built": 1978, "subdivision": "Ermineskin", "lat": 53.455315005712, "lng": -113.496068964478, "subject": False},
    {"id": 29, "name": "10436 124 St Nw", "address": "10436 124 ST NW", "units": 16, "year_built": 1949, "subdivision": "Oliver", "lat": 53.547473905397, "lng": -113.536407460243, "subject": False},
    {"id": 30, "name": "Sweet Grass", "address": "11320/24 31 AVE NW", "units": 36, "year_built": 1978, "subdivision": "Sweet Grass", "lat": 53.464076986287, "lng": -113.527740991454, "subject": False},
    {"id": 31, "name": "Saddleback II", "address": "11404 25 AVE NW", "units": 28, "year_built": 1982, "subdivision": "Blue Quill", "lat": 53.456771906212, "lng": -113.52810669389, "subject": False},
    {"id": 32, "name": "Blue Quill", "address": "11404/20 31 AVE NW", "units": 19, "year_built": 1978, "subdivision": "Sweet Grass", "lat": 53.464084613819, "lng": -113.529869072852, "subject": False},
    {"id": 33, "name": "Hermitage Village", "address": "1150 HOOKE RD NW", "units": 147, "year_built": 1978, "subdivision": "Homesteader", "lat": 53.584407797821, "lng": -113.396331776584, "subject": False},
    {"id": 34, "name": "Saddleback I", "address": "11504/26 25 AVE NW", "units": 39, "year_built": 1978, "subdivision": "Blue Quill", "lat": 53.45690538802, "lng": -113.529319806737, "subject": False},
    {"id": 35, "name": "Petrolia", "address": "11539 41 AVE NW", "units": 70, "year_built": 1972, "subdivision": "Royal Gardens", "lat": 53.477609988059, "lng": -113.532184992699, "subject": False},
    {"id": 36, "name": "Satoo II", "address": "1204/12 80 ST NW", "units": 22, "year_built": 1978, "subdivision": "Staoo", "lat": 53.443580592723, "lng": -113.455970777877, "subject": False},
    {"id": 37, "name": "Southview Garden Court", "address": "1204/58 54 ST NW", "units": 48, "year_built": 1981, "subdivision": "Sakaw", "lat": 53.441452008412, "lng": -113.423797596909, "subject": False},
    {"id": 38, "name": "Parkview Estates", "address": "32 ST & 116A AVE NW", "units": 104, "year_built": 1972, "subdivision": "Rundle Heights", "lat": 53.568818002738, "lng": -113.390601991392, "subject": False},
    {"id": 39, "name": "Shelbrooke Townhomes", "address": "13704 122 AVE NW", "units": 95, "year_built": 1957, "subdivision": "Dovercourt", "lat": 53.573455793584, "lng": -113.560256992262, "subject": False},
    {"id": 40, "name": "Bronx Townhomes", "address": "13135 131 ST NW", "units": 208, "year_built": 1957, "subdivision": "Athlone", "lat": 53.591673985865, "lng": -113.547221959358, "subject": False},
    {"id": 41, "name": "Wellington Townhouses", "address": "13220 140 ST NW", "units": 220, "year_built": 1960, "subdivision": "Wellington", "lat": 53.593345588815, "lng": -113.562446596828, "subject": False},
    {"id": 42, "name": "Kensington Townhomes", "address": "13302 113A ST NW", "units": 26, "year_built": 1962, "subdivision": "Kensington", "lat": 53.594259006714, "lng": -113.517121036312, "subject": False},
    {"id": 43, "name": "Glenora Patio Homes", "address": "13416 13803 13503 109 AVE & 10931 135 ST NW", "units": 46, "year_built": 1953, "subdivision": "North Glenora", "lat": 53.555744203532, "lng": -113.555069013292, "subject": False},
    {"id": 44, "name": "Brentwood Homes", "address": "13743 115 AVE NW", "units": 207, "year_built": 1956, "subdivision": "Woodcroft", "lat": 53.564431082254, "lng": -113.556476921568, "subject": False},
    {"id": 45, "name": "Village Plaza", "address": "13819 66 ST NW", "units": 68, "year_built": 1972, "subdivision": "York", "lat": 53.601146919467, "lng": -113.441099437625, "subject": False},
    {"id": 46, "name": "Ekota II", "address": "1382 KNOTTWOOD RD E", "units": 17, "year_built": 1977, "subdivision": "Ekota", "lat": 53.447065997611, "lng": -113.443635969164, "subject": False},
    {"id": 47, "name": "Vernon Street Townhouses", "address": "13904 117 ST NW", "units": 23, "year_built": 1978, "subdivision": "Carlisle", "lat": 53.601917006821, "lng": -113.522729032451, "subject": False},
    {"id": 48, "name": "Laurentian Estates", "address": "1426 LAKEWOOD RD W", "units": 78, "year_built": 1978, "subdivision": "Tipaskan", "lat": 53.459741195412, "lng": -113.459199906075, "subject": False},
    {"id": 49, "name": "Castle Brae Place", "address": "14305 121 ST NW", "units": 44, "year_built": 1981, "subdivision": "Carlisle", "lat": 53.605316203835, "lng": -113.528427134048, "subject": False},
    {"id": 50, "name": "Briar Rose Estates", "address": "7804 15 AVE NW", "units": 24, "year_built": 1984, "subdivision": "Menisa", "lat": 53.445434585887, "lng": -113.452331523156, "subject": False},
    {"id": 51, "name": "Dunluce Village", "address": "16401/99 115 ST NW", "units": 55, "year_built": 1981, "subdivision": "Dunluce", "lat": 53.625672996801, "lng": -113.521900984236, "subject": False},
    {"id": 52, "name": "Southwood III", "address": "1693 42 ST NW", "units": 41, "year_built": 1984, "subdivision": "Southwood", "lat": 53.444984393867, "lng": -113.404357867969, "subject": False},
    {"id": 53, "name": "Ekota I", "address": "1703/1851 MILLWOODS RD S", "units": 49, "year_built": 1978, "subdivision": "Ekota", "lat": 53.450197979552, "lng": -113.407758992821, "subject": False},
    {"id": 54, "name": "North Callingwood Place", "address": "7103 171 ST NW", "units": 51, "year_built": 1982, "subdivision": "Callingwood North", "lat": 53.505306184993, "lng": -113.617118817576, "subject": False},
    {"id": 55, "name": "Westwinds of Summerlea", "address": "17425 94 AVE NW", "units": 48, "year_built": 1980, "subdivision": "Summerlea", "lat": 53.528166987713, "lng": -113.621337010349, "subject": False},
    {"id": 56, "name": "Boardwalk Village II", "address": "116 THORNCLIFFE PL NW", "units": 60, "year_built": 1971, "subdivision": "Thorncliffe", "lat": 53.513303987455, "lng": -113.623911008995, "subject": False},
    {"id": 57, "name": "Boardwalk Village I", "address": "106 SPRINGFIELD PLAZA NW", "units": 95, "year_built": 1971, "subdivision": "Thorncliffe", "lat": 53.514386594069, "lng": -113.622553978871, "subject": False},
    {"id": 58, "name": "Lakeview Estates", "address": "17775 95 ST NW", "units": 37, "year_built": 1983, "subdivision": "Lago Lindo", "lat": 53.639964015987, "lng": -113.487490002759, "subject": False},
    {"id": 59, "name": "Cricket Court", "address": "17800 86 AVE NW", "units": 114, "year_built": 1977, "subdivision": "Aldergrove", "lat": 53.519193285655, "lng": -113.630850362229, "subject": False},
    {"id": 60, "name": "King Fisher Estates", "address": "18005 97A AVE NW", "units": 36, "year_built": 1982, "subdivision": "La Perle", "lat": 53.535766985051, "lng": -113.570573019595, "subject": False},
    {"id": 61, "name": "Lymburn Place", "address": "18415 75 AVE NW", "units": 41, "year_built": 1983, "subdivision": "Lymburn", "lat": 53.50821688469, "lng": -113.643226601949, "subject": False},
    {"id": 62, "name": "Yellowbird III", "address": "1904/14 112 ST NW", "units": 47, "year_built": 1982, "subdivision": "Sky Rattler", "lat": 53.450328988698, "lng": -113.51969402913, "subject": False},
    {"id": 63, "name": "The Maples", "address": "1919 147 AVE NW", "units": 60, "year_built": 1982, "subdivision": "Fraser", "lat": 53.609332979475, "lng": -113.371467615185, "subject": False},
    {"id": 64, "name": "Huntington Hill II", "address": "200 HUNTINGTON HILL NW", "units": 144, "year_built": 1992, "subdivision": "Empire Park", "lat": 53.484458589686, "lng": -113.497499336255, "subject": False},
    {"id": 65, "name": "Tweddle Place", "address": "2204 MILLBOURNE RD W", "units": 62, "year_built": 1977, "subdivision": "Tweddle Place", "lat": 53.48054889286, "lng": -113.457069393926, "subject": False},
    {"id": 66, "name": "Lee Ridge II", "address": "250-310 MILLBOURNE RD E", "units": 32, "year_built": 1977, "subdivision": "Lee Ridge", "lat": 53.469892015434, "lng": -113.444294032382, "subject": False},
    {"id": 67, "name": "Kameyosek I", "address": "255 LAKEWOOD RD NW", "units": 65, "year_built": 1979, "subdivision": "Kameyosek", "lat": 53.460867010737, "lng": -113.439866962582, "subject": False},
    {"id": 68, "name": "Garden Oaks", "address": "2803 79 ST NW", "units": 59, "year_built": 1981, "subdivision": "Tipaskan", "lat": 53.459250015886, "lng": -113.452601001343, "subject": False},
    {"id": 69, "name": "Brookside Terrace", "address": "281 BROOKSIDE TERR NW", "units": 131, "year_built": 1969, "subdivision": "Riverbend", "lat": 53.493469219419, "lng": -113.570228607194, "subject": False},
    {"id": 70, "name": "Village On The Park", "address": "100 VILLAGE ON THE PARK NW", "units": 126, "year_built": 1972, "subdivision": "Rundle Heights", "lat": 53.602250416577, "lng": -113.442417336736, "subject": False},
    {"id": 71, "name": "Habitat Village", "address": "305 HABITAT CRES NW", "units": 151, "year_built": 1976, "subdivision": "Homesteader", "lat": 53.590553283501, "lng": -113.416290261511, "subject": False},
    {"id": 72, "name": "Richfield I", "address": "3554 84 ST NW", "units": 26, "year_built": 1973, "subdivision": "Richfield", "lat": 53.469188019386, "lng": -113.458993962714, "subject": False},
    {"id": 73, "name": "Richfield II", "address": "3620/58 85 ST NW", "units": 56, "year_built": 1973, "subdivision": "Richfield", "lat": 53.470832800246, "lng": -113.461280797357, "subject": False},
    {"id": 74, "name": "Richfield III", "address": "3704 78 ST NW", "units": 82, "year_built": 1973, "subdivision": "Lee Ridge", "lat": 53.470859496608, "lng": -113.456611574374, "subject": False},
    {"id": 75, "name": "3724 105 St Nw", "address": "3724 105 ST NW", "units": 108, "year_built": 1971, "subdivision": "Duggan", "lat": 53.472418991603, "lng": -113.502104018583, "subject": False},
    {"id": 76, "name": "Clareview Court", "address": "3810 134 AVE NW", "units": 86, "year_built": 1977, "subdivision": "Belmont", "lat": 53.595680200307, "lng": -113.400093071815, "subject": False},
    {"id": 77, "name": "Hillview IV", "address": "3811/21 62 ST NW", "units": 26, "year_built": 1983, "subdivision": "Greenview", "lat": 53.474630011932, "lng": -113.432416037392, "subject": False},
    {"id": 78, "name": "Hartford County", "address": "433 HOOPER CR NW", "units": 74, "year_built": 1982, "subdivision": "Overlanders", "lat": 53.584578568109, "lng": -113.391393528097, "subject": False},
    {"id": 79, "name": "Lee Ridge I", "address": "451/559 MILLBOURNE RD E", "units": 51, "year_built": 1977, "subdivision": "Lee Ridge", "lat": 53.471764993608, "lng": -113.443268003614, "subject": False},
    {"id": 80, "name": "Hermitage Park Estates", "address": "4504 127 AVE NW", "units": 44, "year_built": 1976, "subdivision": "Homesteader", "lat": 53.585626987547, "lng": -113.413086027565, "subject": False},
    {"id": 81, "name": "1605 48 St Nw", "address": "1605 48 ST NW", "units": 6, "year_built": 1992, "subdivision": "Pollard Meadows", "lat": 53.445068380537, "lng": -113.412826523843, "subject": False},
    {"id": 82, "name": "Huntington Heights Coach Homes", "address": "501 HUNTINGTON HILLS NW", "units": 128, "year_built": 1983, "subdivision": "Empire Park", "lat": 53.482317390611, "lng": -113.496556539785, "subject": False},
    {"id": 83, "name": "Brander Gardens", "address": "5210 RIVERBEND RD NW", "units": 98, "year_built": 1972, "subdivision": "Brander Gardens", "lat": 53.489860013821, "lng": -113.578572959443, "subject": False},
    {"id": 84, "name": "Hillview III", "address": "5503/43 38 AVE NW", "units": 26, "year_built": 1982, "subdivision": "Hillview", "lat": 53.471139996998, "lng": -113.423329970531, "subject": False},
    {"id": 85, "name": "5510 118 Ave Nw", "address": "5510 118 AVE NW", "units": 8, "year_built": 1976, "subdivision": "Newton", "lat": 53.570598989525, "lng": -113.426577706554, "subject": False},
    {"id": 86, "name": "Meyokumin I", "address": "5603/5613 22 AVE NW", "units": 34, "year_built": 1982, "subdivision": "Meyokumin", "lat": 53.45221600656, "lng": -113.427226968774, "subject": False},
    {"id": 87, "name": "Riverbend Villas", "address": "5608 RIVERBEND RD NW", "units": 36, "year_built": 1972, "subdivision": "Brander Gardens", "lat": 53.494014001216, "lng": -113.579204032933, "subject": False},
    {"id": 88, "name": "Glenridge Mews", "address": "501 DUNLUCE RD NW", "units": 40, "year_built": 1979, "subdivision": "Dunluce", "lat": 53.623730993654, "lng": -113.536589012265, "subject": False},
    {"id": 89, "name": "Hillview I", "address": "58 ST & 34 AVE NW", "units": 66, "year_built": 1981, "subdivision": "Hillview", "lat": 53.465504005302, "lng": -113.427698031733, "subject": False},
    {"id": 90, "name": "6103 11A Ave Nw", "address": "6103 11A AVE NW", "units": 8, "year_built": 1993, "subdivision": "Sakaw", "lat": 53.440405988805, "lng": -113.432115965258, "subject": False},
    {"id": 91, "name": "Woodvale Court", "address": "62 ST & 38 AVE NW", "units": 45, "year_built": 1980, "subdivision": "Hillview", "lat": 53.474409986974, "lng": -113.433632000086, "subject": False},
    {"id": 92, "name": "Southwoods Village", "address": "6709 96 ST NW", "units": 236, "year_built": 1955, "subdivision": "Hazeldean", "lat": 53.503855990015, "lng": -113.475403968932, "subject": False},
    {"id": 93, "name": "Kameyosek Place", "address": "700 LAKEWOOD RD N", "units": 62, "year_built": 1982, "subdivision": "Tipaskan", "lat": 53.462043788034, "lng": -113.446922261942, "subject": False},
    {"id": 94, "name": "Menisa I", "address": "7251 MILLWOODS RD S", "units": 25, "year_built": 1982, "subdivision": "Menisa", "lat": 53.444834986443, "lng": -113.445637986737, "subject": False},
    {"id": 95, "name": "Lymburn Lane", "address": "7300 178 ST NW", "units": 48, "year_built": 1977, "subdivision": "Lymburn", "lat": 53.507759107048, "lng": -113.631950427607, "subject": False},
    {"id": 96, "name": "Westridge Manor", "address": "7415 172 ST NW", "units": 64, "year_built": 1978, "subdivision": "Callingwood North", "lat": 53.506607098275, "lng": -113.61832430289, "subject": False},
    {"id": 97, "name": "Jamestown Village", "address": "3504 MILLWOODS RD NW", "units": 54, "year_built": 1973, "subdivision": "Richfield", "lat": 53.467678103348, "lng": -113.45165250518, "subject": False},
    {"id": 98, "name": "Westpark Ridge", "address": "7715 159 ST NW", "units": 102, "year_built": 1971, "subdivision": "Patricia Heights", "lat": 53.509841884258, "lng": -113.594955389199, "subject": False},
    {"id": 99, "name": "Holyrood Gardens", "address": "8318 90 AVE NW", "units": 70, "year_built": 1954, "subdivision": "Holyrood", "lat": 53.525691015425, "lng": -113.456977025353, "subject": False},
    {"id": 100, "name": "Westglen Patio Homes", "address": "9004 182 ST NW", "units": 40, "year_built": 1976, "subdivision": "Primrose", "lat": 53.525399995747, "lng": -113.639511993918, "subject": False},
    {"id": 101, "name": "Tiffinny Mills I", "address": "923 LAKEWOOD RD N", "units": 12, "year_built": 1978, "subdivision": "Tipaskan", "lat": 53.462237200449, "lng": -113.450672995975, "subject": False},
    {"id": 102, "name": "Summerlea Place", "address": "9225 177 ST NW", "units": 39, "year_built": 1980, "subdivision": "Summerlea", "lat": 53.5270799806, "lng": -113.62693695986, "subject": False},
    {"id": 103, "name": "Point West Townhouses", "address": "9633 180 ST NW", "units": 69, "year_built": 1983, "subdivision": "La Perle", "lat": 53.532161718948, "lng": -113.631202678024, "subject": False},
    {"id": 104, "name": "Barclay Square", "address": "9703 185 ST NW", "units": 65, "year_built": 1981, "subdivision": "La Perle", "lat": 53.533100114918, "lng": -113.640228311364, "subject": False},
    {"id": 105, "name": "Hooke County", "address": "975 HOOKE RD NW", "units": 165, "year_built": 1980, "subdivision": "Overlanders", "lat": 53.583671992451, "lng": -113.390549017764, "subject": False},
    {"id": 106, "name": "Caslte Close Place", "address": "9903 169 AVE NW", "units": 35, "year_built": 1982, "subdivision": "Baturyn", "lat": 53.629623387768, "lng": -113.496528628048, "subject": False},
    {"id": 107, "name": "Tamarack West", "address": "1603 MILLWOODS RD E", "units": 62, "year_built": 1980, "subdivision": "Daly Grove", "lat": 53.445178015831, "lng": -113.401252037567, "subject": False},
    {"id": 108, "name": "Tamarack East", "address": "3717 16A AVE NW", "units": 71, "year_built": 1980, "subdivision": "Crawford Plains", "lat": 53.443807993757, "lng": -113.4005219738, "subject": False},
    {"id": 109, "name": "Boardwalk Village III", "address": "200 THORNCLIFFE NW", "units": 100, "year_built": 1971, "subdivision": "Thorncliffe Place", "lat": 53.513717718196, "lng": -113.626319884149, "subject": False},
    {"id": 110, "name": "Lauderdale Manor", "address": "10433 132 AVE NW", "units": 39, "year_built": 1962, "subdivision": "Lauderdale", "lat": 53.591744016666, "lng": -113.500399977667, "subject": False},
    {"id": 111, "name": "Granville Square", "address": "3755 26 AVE NW", "units": 48, "year_built": 1982, "subdivision": "Bisset", "lat": 53.456223981202, "lng": -113.398160037304, "subject": False},
    {"id": 112, "name": "Knottwood Terrace", "address": "2178 MILLWOODS RD NW", "units": 84, "year_built": 1977, "subdivision": "Satoo", "lat": 53.449967309576, "lng": -113.450156670739, "subject": False},
    {"id": 113, "name": "Claremont Court", "address": "4204 139 AVE NW", "units": 144, "year_built": 2001, "subdivision": "Clareview Campus", "lat": 53.601203916409, "lng": -113.406837486386, "subject": False},
    {"id": 114, "name": "Arcadia Gardens", "address": "4217 135 AVE NW", "units": 20, "year_built": 1974, "subdivision": "Sifton Park", "lat": 53.595422079598, "lng": -113.40747861816, "subject": False},
    {"id": 115, "name": "Hillclaire Estates", "address": "14106 22A ST NW", "units": 22, "year_built": 1979, "subdivision": "Bannerman", "lat": 53.604919404539, "lng": -113.376594490081, "subject": False},
    {"id": 116, "name": "10608 106 St Nw", "address": "10608 106 ST NW", "units": 7, "year_built": 1955, "subdivision": "Central McDougall", "lat": 53.550003102771, "lng": -113.503448475852, "subject": False},
    {"id": 117, "name": "Royal Castle", "address": "257 DUNLUCE RD NW", "units": 17, "year_built": 1980, "subdivision": "Dunluce", "lat": 53.626652003092, "lng": -113.532159008799, "subject": False},
    {"id": 118, "name": "Pleasantview Townhomes", "address": "4905 107 ST NW", "units": 216, "year_built": 1961, "subdivision": "Empire Park", "lat": 53.48704977, "lng": -113.5066457, "subject": True},
    {"id": 119, "name": "Lord Byron Townhomes", "address": "1 ROYAL RD NW", "units": 147, "year_built": 1968, "subdivision": None, "lat": 53.4816929720353, "lng": -113.538963371898, "subject": False},
    {"id": 120, "name": "Heritage Place", "address": "10741 25 AVE NW", "units": 40, "year_built": 1978, "subdivision": None, "lat": 53.4556315651811, "lng": -113.506644825932, "subject": False},
    {"id": 121, "name": "Rundle Heights II", "address": "2916 113 AVE NW", "units": 97, "year_built": 1980, "subdivision": "Rundle Heights", "lat": 53.5671090889655, "lng": -113.388399187608, "subject": False},
    {"id": 122, "name": "South Ridge Townhomes", "address": "10542 45 AVE NW", "units": 178, "year_built": 1971, "subdivision": None, "lat": 53.4825364968663, "lng": -113.501697172947, "subject": False},
    {"id": 123, "name": "Shadow Ridge", "address": "2041 SADDLEBACK RD NW", "units": 60, "year_built": 1978, "subdivision": None, "lat": 53.4494685401771, "lng": -113.518216749446, "subject": False},
    {"id": 124, "name": "Yellowbird II", "address": "10470 16 AVE NW", "units": 39, "year_built": 1988, "subdivision": None, "lat": 53.4463045390151, "lng": -113.498768469235, "subject": False},
    {"id": 125, "name": "Park Haven", "address": "3307 116A AVE NW", "units": 204, "year_built": 1980, "subdivision": None, "lat": 53.5681589095027, "lng": -113.392937919315, "subject": False},
    {"id": 126, "name": "Abbottsfield", "address": "353 ABBOTSFIELD RD NW", "units": 132, "year_built": 1974, "subdivision": None, "lat": 53.5747682675171, "lng": -113.388308593721, "subject": False},
    {"id": 127, "name": "Hermitage III", "address": "1181 HYNDMAN RD NW", "units": 58, "year_built": 1982, "subdivision": None, "lat": 53.5758496641324, "lng": -113.376870349513, "subject": False},
]


def _val(val):
    if val is None:
        return "null"
    elif isinstance(val, str):
        return '"' + val.replace("\\", "\\\\").replace('"', '\\"') + '"'
    elif isinstance(val, bool):
        return "true" if val else "false"
    else:
        return str(val)


def build_js_array(projects):
    out = "[\n"
    for p in projects:
        out += "  {\n"
        out += "    id: " + str(p["id"]) + ",\n"
        out += "    name: " + _val(p["name"]) + ",\n"
        out += "    address: " + _val(p["address"]) + ",\n"
        out += "    units: " + _val(p["units"]) + ",\n"
        out += "    year_built: " + _val(p["year_built"]) + ",\n"
        out += "    subdivision: " + _val(p["subdivision"]) + ",\n"
        out += "    lat: " + str(p["lat"]) + ",\n"
        out += "    lng: " + str(p["lng"]) + ",\n"
        out += "    subject: " + _val(p["subject"]) + "\n"
        out += "  },\n"
    out += "]"
    return out


_BASE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Existing Townhome Supply</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script><style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#f7f6f3;--surface:#fff;--border:#e8e5df;--border-light:#f0ede8;
  --text-primary:#1a1917;--text-secondary:#6b6760;--text-muted:#a09d99;
  --accent:#c8572a;--accent-subtle:rgba(200,87,42,0.08);
  --navy:#2a3f5f;--navy-subtle:rgba(42,63,95,0.08);
  --green:#2e7d4f;--grey:#a09d99;
  --shadow-md:0 4px 12px rgba(0,0,0,0.08);--shadow-lg:0 12px 32px rgba(0,0,0,0.1);--radius:8px;
}
html,body{height:100%;font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text-primary);overscroll-behavior:none}
body{display:flex;flex-direction:column}
@supports (height:100dvh){body{height:100dvh}}
#header{flex-shrink:0;z-index:1000;height:52px;background:var(--surface);border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;padding:0 20px;box-shadow:0 1px 3px rgba(0,0,0,0.07);gap:16px}
#header-left{display:flex;align-items:center;flex-shrink:0}
#header-title{font-size:13px;font-weight:500;color:var(--text-secondary)}
#header-title strong{color:var(--text-primary);font-weight:600}
#header-right{display:flex;align-items:center;gap:16px;flex-shrink:0}
.stat-chip{text-align:right}
.stat-num{font-size:18px;font-weight:600;color:var(--text-primary);line-height:1;font-variant-numeric:tabular-nums}
.stat-label{font-size:9px;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:var(--text-muted);margin-top:1px;white-space:nowrap}
.stat-div{width:1px;height:28px;background:var(--border)}
#scope-note{font-weight:400;color:var(--navy);display:none}
#subject-nav{display:flex;align-items:center;gap:6px;overflow-x:auto;scrollbar-width:none}
#subject-nav::-webkit-scrollbar{display:none}
.stab{padding:5px 13px;border-radius:20px;border:1.5px solid var(--navy);font-size:11.5px;font-weight:500;cursor:pointer;background:var(--surface);color:var(--navy);display:flex;align-items:center;gap:5px;transition:all .15s;white-space:nowrap;flex-shrink:0}
.stab:hover{background:var(--navy-subtle)}
.stab.active{background:var(--navy);color:#fff}
.stab .sicon{width:7px;height:7px;border-radius:2px;background:var(--navy);flex-shrink:0}
.stab.active .sicon{background:#fff}
#layout{flex:1;min-height:0;display:flex}
#map{flex:1;min-height:0}
#sidebar{width:360px;flex-shrink:0;background:var(--surface);border-left:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;box-shadow:-2px 0 8px rgba(0,0,0,0.04)}
#sb-head{padding:14px 18px 10px;border-bottom:1px solid var(--border-light)}
#sb-head-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
#sb-head h2{font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--text-muted)}
#sb-count{font-size:11px;color:var(--text-muted);font-variant-numeric:tabular-nums}
#sb-controls{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.itab{padding:4px 10px;border-radius:14px;border:1.5px solid var(--border);font-size:10.5px;font-weight:500;cursor:pointer;background:var(--surface);color:var(--text-secondary);transition:all .15s}
.itab:hover{border-color:var(--text-primary);color:var(--text-primary)}
.itab.active{background:var(--text-primary);border-color:var(--text-primary);color:#fff}
#sort-select{margin-left:auto;font-size:10.5px;font-family:'DM Sans',sans-serif;color:var(--text-secondary);background:var(--surface);border:1.5px solid var(--border);border-radius:14px;padding:4px 8px;cursor:pointer}
.radius-row{display:none;width:100%;align-items:center;gap:6px;flex-wrap:wrap;margin-top:8px;padding-top:8px;border-top:1px solid var(--border-light)}
.radius-row.show{display:flex}
#radius-label{font-size:10.5px;color:var(--text-muted);white-space:nowrap}
#radius-label b{color:var(--navy);font-weight:600}
.rtab{padding:3px 9px;border-radius:12px;border:1.5px solid var(--border);font-size:10px;font-weight:500;cursor:pointer;background:var(--surface);color:var(--text-secondary);transition:all .15s}
.rtab:hover{border-color:var(--navy);color:var(--navy)}
.rtab.active{background:var(--navy);border-color:var(--navy);color:#fff}
#proj-list{flex:1;min-height:0;overflow-y:auto;padding:8px 0}
#proj-list::-webkit-scrollbar{width:4px}
#proj-list::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
.pcard{padding:12px 18px;cursor:pointer;border-bottom:1px solid var(--border-light);transition:background .15s;display:flex;gap:10px;align-items:flex-start}
.pcard:hover{background:var(--bg)}
.pcard.active{background:var(--accent-subtle);border-left:3px solid var(--accent);padding-left:15px}
.pcard.excluded{opacity:.45}
.pcard-body{flex:1;min-width:0}
.pcard-top{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:4px}
.pname{font-size:13px;font-weight:600;line-height:1.3;flex:1}
.pname .stag{font-size:9px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--navy);display:block;margin-bottom:1px}
.pbadge{background:var(--text-primary);color:#fff;font-size:11px;font-weight:600;padding:2px 7px;border-radius:12px;white-space:nowrap;flex-shrink:0}
.pcard.active .pbadge{background:var(--accent)}
.pmeta{font-size:11px;color:var(--text-muted);line-height:1.5}
.pmeta b{color:var(--text-secondary);font-weight:500}
.pinclude{flex-shrink:0;padding-top:2px}
.pinclude input{width:16px;height:16px;cursor:pointer;accent-color:var(--accent)}
#detail{border-top:1px solid var(--border);background:var(--surface);flex-shrink:0;max-height:0;overflow:hidden;transition:max-height .3s}
#detail.open{max-height:520px}
#det-inner{padding:18px}
#det-name{font-size:15px;font-weight:600;margin-bottom:2px;line-height:1.3}
#det-subject-tag{font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--navy);margin-bottom:12px}
.dgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.dfield{background:var(--bg);border:1px solid var(--border-light);border-radius:var(--radius);padding:10px 12px}
.dfield.full{grid-column:1/-1}
.dflabel{font-size:9.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:3px}
.dfval{font-size:13px;font-weight:500;line-height:1.3}
#det-toggle{margin-top:12px;width:100%;padding:9px;border-radius:var(--radius);border:1.5px solid var(--border);background:var(--surface);color:var(--text-primary);font-size:12px;font-weight:600;cursor:pointer;transition:all .15s}
#det-toggle:hover{border-color:var(--text-primary)}
#det-toggle.is-excluded{background:var(--text-primary);color:#fff;border-color:var(--text-primary)}
.leaflet-popup-content-wrapper{border-radius:var(--radius)!important;box-shadow:var(--shadow-lg)!important;border:1px solid var(--border)!important;padding:0!important;overflow:hidden;font-family:'DM Sans',sans-serif!important}
.leaflet-popup-content{margin:0!important;width:240px!important;max-width:calc(100vw - 56px)!important}
.leaflet-popup-tip-container{display:none}
.popup-inner{padding:14px 16px}
.popup-tag{font-size:9.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--navy);margin-bottom:2px}
.popup-name{font-size:13px;font-weight:600;margin-bottom:3px;line-height:1.3}
.popup-sub{font-size:11.5px;color:var(--text-secondary);margin-bottom:8px}
.popup-row{display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-top:1px solid var(--border-light);font-size:11.5px}
.popup-row-label{color:var(--text-muted)}
.popup-row-value{font-weight:500;font-family:'DM Mono',monospace}
.cmarker{width:30px;height:30px;border:2.5px solid #fff;border-radius:50% 50% 50% 0;transform:rotate(-45deg);box-shadow:var(--shadow-md);cursor:pointer}
.cmarker.subject{width:38px;height:38px;border-width:3px}
@media (max-width:768px){
  #header{flex-wrap:wrap;height:auto;padding:10px 12px 8px;gap:8px;align-items:flex-start;box-shadow:0 1px 3px rgba(0,0,0,0.07)}
  #header-left{width:100%}
  #header-title{font-size:12px}
  #subject-nav{width:100%;-webkit-overflow-scrolling:touch;padding-bottom:2px}
  .stab{padding:7px 13px}
  #header-right{width:100%;justify-content:flex-start;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;gap:14px}
  #header-right::-webkit-scrollbar{display:none}
  .stat-chip{flex-shrink:0;text-align:left}
  #layout{flex-direction:column}
  #map{flex:1;min-height:200px}
  #sidebar{width:100%;flex:0 0 auto;height:30vh;min-height:220px;max-height:280px;overflow-y:auto;-webkit-overflow-scrolling:touch;border-left:none;border-top:1px solid var(--border);box-shadow:0 -2px 8px rgba(0,0,0,0.04)}
  #proj-list{flex:none;overflow-y:visible}
  #detail.open{max-height:2000px}
  .stab,.pcard,.stat-chip,.itab,.rtab{touch-action:manipulation}
}
</style>
</head>
<body>
<div id="header">
  <div id="header-left">
    <div id="header-title"><strong>Existing Townhome Supply</strong><span id="scope-note"></span></div>
  </div>
  <div id="subject-nav">
    <div class="stab" data-subject="River Valley Townhomes"><span class="sicon"></span>River Valley Townhomes</div>
    <div class="stab" data-subject="Pleasantview Townhomes"><span class="sicon"></span>Pleasantview Townhomes</div>
  </div>
  <div id="header-right">
    <div class="stat-chip">
      <div class="stat-num" id="stat-units">0</div>
      <div class="stat-label">Supply Units</div>
    </div>
    <div class="stat-div"></div>
    <div class="stat-chip">
      <div class="stat-num" id="stat-inc-units">0</div>
      <div class="stat-label">Included Units</div>
    </div>
  </div>
</div>
<div id="layout">
  <div id="map"></div>
  <div id="sidebar">
    <div id="sb-head">
      <div id="sb-head-top"><h2>Townhome Supply</h2><span id="sb-count"></span></div>
      <div id="sb-controls">
        <div class="itab active" data-inc-filter="all">All</div>
        <div class="itab" data-inc-filter="included">Included</div>
        <div class="itab" data-inc-filter="excluded">Excluded</div>
        <select id="sort-select">
          <option value="distance">Sort: Distance</option>
          <option value="units">Sort: Units</option>
          <option value="name">Sort: Name</option>
          <option value="year">Sort: Year Built</option>
        </select>
        <div class="radius-row" id="radius-row">
          <span id="radius-label">Proximity to <b id="radius-subject-name"></b>:</span>
          <div class="rtab" data-radius="0.5">0.5km</div>
          <div class="rtab" data-radius="1">1km</div>
          <div class="rtab" data-radius="2">2km</div>
          <div class="rtab" data-radius="3">3km</div>
          <div class="rtab" data-radius="5">5km</div>
          <div class="rtab active" data-radius="all">All</div>
        </div>
      </div>
    </div>
    <div id="proj-list"></div>
    <div id="detail">
      <div id="det-inner">
        <div id="det-name"></div>
        <div id="det-subject-tag"></div>
        <div class="dgrid" id="det-grid"></div>
        <button id="det-toggle"></button>
      </div>
    </div>
  </div>
</div>
<script>
const PROJECTS = [
  {
    id: 0,
    name: "The Switch",
    address: "10465 101 St NW",
    units: 285,
    year_built: 2024,
    subdivision: null,
    lat: 53.54773198,
    lng: -113.492485,
    subject: false
  },
];

const STORAGE_KEY = 'rvth_pv_included_v1';
let included = {};
try {
  included = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
} catch (e) { included = {}; }
function isIncluded(id) { return included[id] !== false; }
function setIncluded(id, val) {
  included[id] = val;
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(included)); } catch (e) {}
}

let activeId = null, markers = {}, popups = {}, incFilter = 'all', sortMode = 'distance', activeSubjectTab = null, activeRadius = null, radiusCircle = null;

var SHORT_NAME = {'River Valley Townhomes': 'River Valley', 'Pleasantview Townhomes': 'Pleasantview'};
function shortName(n) { return SHORT_NAME[n] || n; }

const map = L.map('map', {zoomControl: false, attributionControl: false});
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {maxZoom: 19}).addTo(map);
L.control.zoom({position: 'topleft'}).addTo(map);
L.control.attribution({position: 'bottomleft', prefix: false}).addAttribution('&copy; Esri &middot; OpenStreetMap contributors').addTo(map);

const subjectSites = PROJECTS.filter(function(p) { return p.subject; });

function haversineKm(lat1, lng1, lat2, lng2) {
  var R = 6371;
  var dLat = (lat2 - lat1) * Math.PI / 180;
  var dLng = (lng2 - lng1) * Math.PI / 180;
  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI/180) * Math.cos(lat2 * Math.PI/180) *
    Math.sin(dLng/2) * Math.sin(dLng/2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

function subjectByName(name) {
  return subjectSites.find(function(s) { return s.name === name; });
}

function nearestSubjectInfo(p) {
  if (p.subject) return {dist: 0, name: p.name};
  var best = null, bestName = null;
  subjectSites.forEach(function(s) {
    var d = haversineKm(p.lat, p.lng, s.lat, s.lng);
    if (best === null || d < best) { best = d; bestName = s.name; }
  });
  return {dist: best, name: bestName};
}
PROJECTS.forEach(function(p) {
  var info = nearestSubjectInfo(p);
  p._dist = info.dist;
  p._distName = info.name;
});

// Distance used for display/sort/filtering: to the active subject-site
// context if one is selected (so numbers always match what's on screen),
// otherwise to whichever subject site is nearest. Only the active anchor
// itself is distance 0 — the *other* subject site still gets a real
// distance so it can't slip through a radius filter.
function activeDist(p) {
  if (activeSubjectTab) {
    if (p.name === activeSubjectTab) return 0;
    var s = subjectByName(activeSubjectTab);
    return haversineKm(p.lat, p.lng, s.lat, s.lng);
  }
  return p._dist;
}
function activeDistName(p) {
  return activeSubjectTab || p._distName;
}
function shouldShowDist(p) {
  if (!activeSubjectTab) return !p.subject;
  return p.name !== activeSubjectTab;
}

function inScope(p) {
  // The active subject site (the one anchoring the radius filter) always
  // shows. Everything else, including the *other* subject site, is
  // subject to the same radius test so a distant comparison site doesn't
  // sneak into an "X km from here" view.
  if (activeSubjectTab && p.name === activeSubjectTab) return true;
  if (!activeSubjectTab || activeRadius === null) return true;
  return activeDist(p) <= activeRadius;
}

var bounds = L.latLngBounds(PROJECTS.map(function(p) { return [p.lat, p.lng]; }));
map.fitBounds(bounds, {padding: [40, 40]});

function markerColor(p) {
  if (p.subject) return '#2a3f5f';
  return isIncluded(p.id) ? '#c8572a' : '#a09d99';
}

function markerIcon(active, p) {
  var color = active ? '#1a1917' : markerColor(p);
  var scale = active ? 'transform:rotate(-45deg) scale(1.25);' : '';
  var cls = 'cmarker' + (p.subject ? ' subject' : '');
  var size = p.subject ? 38 : 30;
  return L.divIcon({
    className: '',
    html: '<div class="' + cls + '" style="background:' + color + ';' + scale + '"></div>',
    iconSize: [size, size], iconAnchor: [size/2, size], popupAnchor: [0, -size-4]
  });
}

function popupHTML(p) {
  var distText = shouldShowDist(p) ? (activeDist(p).toFixed(1) + ' km to ' + shortName(activeDistName(p))) : null;
  return '<div class="popup-inner">'
    + (p.subject ? '<div class="popup-tag">Subject Site</div>' : '')
    + '<div class="popup-name">' + p.name + '</div>'
    + '<div class="popup-sub">' + (p.units != null ? p.units + ' units' : 'Units N/A') + (p.year_built ? ' &middot; Built ' + p.year_built : '') + '</div>'
    + '<div class="popup-row"><span class="popup-row-label">Address</span><span class="popup-row-value">' + p.address + '</span></div>'
    + (distText ? '<div class="popup-row"><span class="popup-row-label">Proximity</span><span class="popup-row-value">' + distText + '</span></div>' : '')
    + '</div>';
}

PROJECTS.forEach(function(p) {
  var marker = L.marker([p.lat, p.lng], {icon: markerIcon(false, p), title: p.name}).addTo(map);
  var popup = L.popup({closeButton: false, offset: [0,0]}).setContent(popupHTML(p));
  marker.bindPopup(popup);
  marker.on('click', function() { selectProject(p.id); });
  markers[p.id] = marker;
  popups[p.id] = popup;
});

function refreshStats() {
  var scoped = PROJECTS.filter(function(p) { return inScope(p) && !p.subject; });
  var units = scoped.reduce(function(s, p) { return s + (p.units || 0); }, 0);
  var incUnits = scoped.filter(function(p) { return isIncluded(p.id); }).reduce(function(s, p) { return s + (p.units || 0); }, 0);
  document.getElementById('stat-units').textContent = units.toLocaleString();
  document.getElementById('stat-inc-units').textContent = incUnits.toLocaleString();
}

function sortedProjects(list) {
  var arr = list.slice();
  if (sortMode === 'distance') arr.sort(function(a,b) { return activeDist(a) - activeDist(b); });
  else if (sortMode === 'units') arr.sort(function(a,b) { return b.units - a.units; });
  else if (sortMode === 'name') arr.sort(function(a,b) { return a.name.localeCompare(b.name); });
  else if (sortMode === 'year') arr.sort(function(a,b) { return (a.year_built||9999) - (b.year_built||9999); });
  return arr;
}

function buildSidebar() {
  var list = document.getElementById('proj-list');
  list.innerHTML = '';
  var scopedTotal = PROJECTS.filter(inScope).length;
  var visible = PROJECTS.filter(function(p) {
    if (!inScope(p)) return false;
    if (incFilter === 'included') return isIncluded(p.id);
    if (incFilter === 'excluded') return !isIncluded(p.id);
    return true;
  });
  visible = sortedProjects(visible);
  document.getElementById('sb-count').textContent = visible.length + ' of ' + scopedTotal;
  visible.forEach(function(p) {
    var inc = isIncluded(p.id);
    var card = document.createElement('div');
    card.className = 'pcard' + (activeId === p.id ? ' active' : '') + (!inc && !p.subject ? ' excluded' : '');
    var metaBits = [];
    if (p.subdivision) metaBits.push(p.subdivision);
    metaBits.push((p.year_built || 'Yr N/A'));
    if (shouldShowDist(p)) metaBits.push(activeDist(p).toFixed(1) + ' km to ' + shortName(activeDistName(p)));
    var nameHtml = (p.subject ? '<span class="stag">Subject Site</span>' : '') + p.name;
    var checkboxHtml = p.subject ? '' : ('<div class="pinclude"><input type="checkbox" ' + (inc ? 'checked' : '') + ' data-toggle-id="' + p.id + '"/></div>');
    card.innerHTML = '<div class="pcard-body">'
      + '<div class="pcard-top"><div class="pname">' + nameHtml + '</div><div class="pbadge">' + (p.units != null ? p.units + ' units' : 'N/A') + '</div></div>'
      + '<div class="pmeta">' + metaBits.join(' &middot; ') + '</div>'
      + '</div>' + checkboxHtml;
    card.addEventListener('click', function(e) {
      if (e.target && e.target.dataset && e.target.dataset.toggleId !== undefined) return;
      selectProject(p.id);
    });
    var cb = card.querySelector('input[data-toggle-id]');
    if (cb) {
      cb.addEventListener('click', function(e) {
        e.stopPropagation();
        setIncluded(p.id, cb.checked);
        markers[p.id].setIcon(markerIcon(activeId === p.id, p));
        refreshStats();
        card.classList.toggle('excluded', !cb.checked);
        if (activeId === p.id) buildDetail(p);
      });
    }
    list.appendChild(card);
  });
}

function buildDetail(p) {
  var inc = isIncluded(p.id);
  document.getElementById('det-name').textContent = p.name;
  document.getElementById('det-subject-tag').textContent = p.subject ? 'SUBJECT SITE' : '';
  document.getElementById('det-subject-tag').style.display = p.subject ? 'block' : 'none';
  var distFields = '';
  if (!p.subject) {
    subjectSites.forEach(function(s) {
      var d = haversineKm(p.lat, p.lng, s.lat, s.lng);
      distFields += '<div class="dfield"><div class="dflabel">To ' + s.name + '</div><div class="dfval">' + d.toFixed(1) + ' km</div></div>';
    });
  }
  document.getElementById('det-grid').innerHTML =
    '<div class="dfield"><div class="dflabel">Total Units</div><div class="dfval">' + (p.units != null ? p.units : 'N/A') + '</div></div>'
    + '<div class="dfield"><div class="dflabel">Year Built</div><div class="dfval">' + (p.year_built || 'N/A') + '</div></div>'
    + '<div class="dfield full"><div class="dflabel">Address</div><div class="dfval">' + p.address + '</div></div>'
    + (p.subdivision ? '<div class="dfield full"><div class="dflabel">Subdivision</div><div class="dfval">' + p.subdivision + '</div></div>' : '')
    + distFields;
  var btn = document.getElementById('det-toggle');
  if (p.subject) {
    btn.style.display = 'none';
  } else {
    btn.style.display = 'block';
    btn.textContent = inc ? 'Included — click to exclude' : 'Excluded — click to include';
    btn.classList.toggle('is-excluded', !inc);
    btn.onclick = function() {
      setIncluded(p.id, !isIncluded(p.id));
      markers[p.id].setIcon(markerIcon(true, p));
      refreshStats();
      buildDetail(p);
      buildSidebar();
    };
  }
}

function updateMapVisibility() {
  PROJECTS.forEach(function(p) {
    var m = markers[p.id];
    if (inScope(p)) {
      if (!map.hasLayer(m)) m.addTo(map);
      m.setIcon(markerIcon(activeId === p.id, p));
    } else {
      if (map.hasLayer(m)) m.remove();
      if (activeId === p.id) {
        activeId = null;
        document.getElementById('detail').classList.remove('open');
      }
    }
  });
}

function updateRadiusCircle() {
  if (radiusCircle) { map.removeLayer(radiusCircle); radiusCircle = null; }
  if (activeSubjectTab && activeRadius !== null) {
    var s = subjectByName(activeSubjectTab);
    radiusCircle = L.circle([s.lat, s.lng], {
      radius: activeRadius * 1000,
      color: '#2a3f5f', weight: 1.5, dashArray: '4,4',
      fillColor: '#2a3f5f', fillOpacity: 0.06
    }).addTo(map);
  }
}

function updateScopeNote() {
  var el = document.getElementById('scope-note');
  if (activeSubjectTab && activeRadius !== null) {
    el.textContent = ' — within ' + activeRadius + 'km of ' + shortName(activeSubjectTab);
    el.style.display = 'inline';
  } else {
    el.textContent = '';
    el.style.display = 'none';
  }
}

function activateSubjectContext(name) {
  var changed = activeSubjectTab !== name;
  activeSubjectTab = name;
  if (changed) activeRadius = null;
  document.querySelectorAll('.stab').forEach(function(t) { t.classList.toggle('active', t.dataset.subject === name); });
  document.getElementById('radius-subject-name').textContent = shortName(name);
  document.getElementById('radius-row').classList.add('show');
  document.querySelectorAll('.rtab').forEach(function(t) { t.classList.toggle('active', t.dataset.radius === (activeRadius === null ? 'all' : String(activeRadius))); });
  updateRadiusCircle();
  updateMapVisibility();
  updateScopeNote();
  refreshStats();
}

function clearSubjectContext() {
  activeSubjectTab = null;
  activeRadius = null;
  document.querySelectorAll('.stab').forEach(function(t) { t.classList.remove('active'); });
  document.querySelectorAll('.rtab').forEach(function(t) { t.classList.toggle('active', t.dataset.radius === 'all'); });
  document.getElementById('radius-row').classList.remove('show');
  updateRadiusCircle();
  updateMapVisibility();
  updateScopeNote();
  refreshStats();
}

function selectProject(id) {
  if (activeId !== null && activeId !== id) {
    var prev = PROJECTS[activeId];
    markers[activeId].setIcon(markerIcon(false, prev));
    markers[activeId].closePopup();
  }
  if (activeId === id) {
    var self_ = PROJECTS[id];
    markers[id].setIcon(markerIcon(false, self_));
    markers[id].closePopup();
    activeId = null;
    document.getElementById('detail').classList.remove('open');
    syncSubjectTabs();
    buildSidebar();
    return;
  }
  activeId = id;
  var p = PROJECTS[id];
  map.flyTo([p.lat, p.lng], 16, {duration: 0.8});
  markers[id].setIcon(markerIcon(true, p));
  markers[id].openPopup();
  buildDetail(p);
  document.getElementById('detail').classList.add('open');
  syncSubjectTabs();
  buildSidebar();
}

function syncSubjectTabs() {
  var activeName = activeId !== null ? PROJECTS[activeId].name : null;
  var isSubject = activeName === 'River Valley Townhomes' || activeName === 'Pleasantview Townhomes';
  if (isSubject) {
    activateSubjectContext(activeName);
  } else {
    document.querySelectorAll('.stab').forEach(function(tab) {
      tab.classList.toggle('active', tab.dataset.subject === activeSubjectTab);
    });
  }
}

document.querySelectorAll('.stab').forEach(function(tab) {
  tab.addEventListener('click', function() {
    var name = tab.dataset.subject;
    if (activeSubjectTab === name) {
      if (activeId !== null && PROJECTS[activeId].name === name) {
        markers[activeId].setIcon(markerIcon(false, PROJECTS[activeId]));
        markers[activeId].closePopup();
        activeId = null;
        document.getElementById('detail').classList.remove('open');
      }
      clearSubjectContext();
      map.fitBounds(bounds, {padding: [40, 40]});
      buildSidebar();
      return;
    }
    var target = PROJECTS.find(function(p) { return p.name === name; });
    if (target) selectProject(target.id);
  });
});

document.querySelectorAll('.rtab').forEach(function(tab) {
  tab.addEventListener('click', function() {
    var val = tab.dataset.radius;
    activeRadius = val === 'all' ? null : parseFloat(val);
    document.querySelectorAll('.rtab').forEach(function(t) { t.classList.remove('active'); });
    tab.classList.add('active');
    updateRadiusCircle();
    updateMapVisibility();
    updateScopeNote();
    refreshStats();
    buildSidebar();
  });
});

document.querySelectorAll('.itab').forEach(function(tab) {
  tab.addEventListener('click', function() {
    incFilter = tab.dataset.incFilter;
    document.querySelectorAll('.itab').forEach(function(t) { t.classList.remove('active'); });
    tab.classList.add('active');
    buildSidebar();
  });
});

document.getElementById('sort-select').addEventListener('change', function(e) {
  sortMode = e.target.value;
  buildSidebar();
});

refreshStats();
buildSidebar();
</script>
</body>
</html>"""

_new_js = "const PROJECTS = " + build_js_array(PROJECTS)
_html = re.sub(r"const PROJECTS = \[.*?\];", _new_js + ";", _BASE, count=1, flags=re.DOTALL)

_path = "/content/existing_townhome_supply_map.html"
with open(_path, "w", encoding="utf-8") as f:
    f.write(_html)

print("Saved:", _path)
print(f"Properties: {len(PROJECTS)} | Total units: {sum(p['units'] for p in PROJECTS if p['units'])}")
display(IFrame(src=_path, width="100%", height="700"))
