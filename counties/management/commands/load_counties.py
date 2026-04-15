from django.core.management.base import BaseCommand
from django.utils.text import slugify
from counties.models import County

class Command(BaseCommand):
    help = 'Load all 47 Kenya counties into the database'

    def handle(self, *args, **kwargs):
        counties = [
            # (code, name, region, population, area_km2, hospitals, health_centres, primary_schools, secondary_schools, poverty_index, main_activity, latitude, longitude)
            (1,  "Mombasa",        "Coast",          1208333,  212.5,   18, 62,  393,  102, 11.7, "Trade, Tourism, Port",              -4.0435,  39.6682),
            (2,  "Kwale",          "Coast",          866820,   8270.0,  8,  89,  567,  98,  69.5, "Agriculture, Tourism",              -4.1740,  39.4601),
            (3,  "Kilifi",         "Coast",          1453787,  12245.9, 11, 104, 712,  121, 57.3, "Agriculture, Tourism, Fishing",     -3.5107,  39.9093),
            (4,  "Tana River",     "Coast",          315943,   35375.8, 4,  42,  198,  34,  79.4, "Pastoralism, Fishing",              -1.0551,  39.9020),
            (5,  "Lamu",           "Coast",          143920,   6497.7,  3,  28,  132,  22,  41.2, "Tourism, Fishing, Trade",          -2.2686,  40.9020),
            (6,  "Taita-Taveta",   "Coast",          340671,   17083.9, 5,  44,  289,  56,  44.8, "Agriculture, Mining, Tourism",     -3.3159,  38.4846),
            (7,  "Garissa",        "North Eastern",  841353,   44175.1, 5,  48,  312,  47,  77.9, "Pastoralism, Trade",               -0.4532,  39.6461),
            (8,  "Wajir",          "North Eastern",  781263,   56685.9, 4,  39,  267,  38,  84.0, "Pastoralism",                      1.7471,  40.0573),
            (9,  "Mandera",        "North Eastern",  1025756,  25991.5, 5,  44,  298,  42,  79.8, "Pastoralism, Trade",               3.9366,  41.8670),
            (10, "Marsabit",       "North Eastern",  459785,   66923.1, 4,  36,  243,  35,  73.8, "Pastoralism, Fishing",             2.3284,  37.9899),
            (11, "Isiolo",         "North Eastern",  268002,   25336.1, 3,  28,  187,  29,  60.2, "Pastoralism, Trade",               0.3556,  37.5822),
            (12, "Meru",           "Central",        1545714,  6936.2,  16, 118, 834,  189, 24.9, "Agriculture, Trade",               0.0472,  37.6490),
            (13, "Tharaka-Nithi",  "Central",        393177,   2609.5,  5,  44,  312,  67,  36.7, "Agriculture",                      -0.3167, 37.9167),
            (14, "Embu",           "Central",        608599,   2821.1,  7,  62,  423,  98,  27.8, "Agriculture, Trade",               -0.5300, 37.4500),
            (15, "Kitui",          "Eastern",        1136187,  30496.0, 8,  78,  612,  123, 55.4, "Agriculture, Mining",              -1.3667, 38.0167),
            (16, "Machakos",       "Eastern",        1421932,  6208.2,  14, 112, 745,  178, 32.1, "Agriculture, Trade, Industry",     -1.5177, 37.2634),
            (17, "Makueni",        "Eastern",        987653,   8008.9,  9,  84,  589,  132, 47.3, "Agriculture",                      -2.2588, 37.8939),
            (18, "Nyandarua",      "Central",        638289,   3107.7,  6,  58,  398,  89,  29.4, "Agriculture",                      -0.1833, 36.5167),
            (19, "Nyeri",          "Central",        759164,   3337.3,  10, 89,  534,  134, 20.1, "Agriculture, Tourism, Trade",      -0.4167, 36.9500),
            (20, "Kirinyaga",      "Central",        610411,   1478.1,  7,  62,  412,  98,  18.3, "Agriculture, Trade",               -0.6590, 37.3822),
            (21, "Murang'a",       "Central",        1056640,  2558.8,  9,  84,  612,  145, 22.7, "Agriculture, Trade",               -0.7833, 37.0333),
            (22, "Kiambu",         "Central",        2417735,  2543.5,  22, 167, 934,  267, 13.2, "Trade, Industry, Agriculture",     -1.1833, 36.8333),
            (23, "Turkana",        "Rift Valley",    926976,   68680.3, 6,  52,  389,  54,  79.2, "Pastoralism, Fishing, Oil",        3.1220,  35.5980),
            (24, "West Pokot",     "Rift Valley",    621241,   9169.4,  5,  47,  312,  48,  67.4, "Pastoralism, Agriculture",         1.7500,  35.1167),
            (25, "Samburu",        "Rift Valley",    310327,   20826.0, 3,  28,  198,  29,  75.3, "Pastoralism, Tourism",             1.2167,  36.9667),
            (26, "Trans-Nzoia",    "Rift Valley",    990341,   2495.5,  9,  78,  567,  128, 30.8, "Agriculture",                      1.0167,  35.0000),
            (27, "Uasin Gishu",    "Rift Valley",    1163186,  3345.2,  14, 112, 712,  178, 22.5, "Agriculture, Trade",               0.5167,  35.2833),
            (28, "Elgeyo-Marakwet","Rift Valley",    454480,   3030.0,  5,  44,  312,  67,  38.9, "Agriculture",                      0.9000,  35.5167),
            (29, "Nandi",          "Rift Valley",    885711,   2884.5,  8,  72,  512,  112, 27.6, "Agriculture, Tea",                 0.1833,  35.1333),
            (30, "Baringo",        "Rift Valley",    666763,   11075.3, 7,  62,  423,  87,  44.7, "Pastoralism, Agriculture",         0.7167,  36.0833),
            (31, "Laikipia",       "Rift Valley",    518560,   9462.5,  6,  52,  334,  72,  31.2, "Agriculture, Tourism",             0.3500,  36.9333),
            (32, "Nakuru",         "Rift Valley",    2162202,  7509.5,  22, 167, 934,  256, 20.4, "Agriculture, Industry, Tourism",   -0.2833, 36.0667),
            (33, "Narok",          "Rift Valley",    1157873,  17921.2, 9,  78,  534,  98,  48.3, "Agriculture, Tourism, Pastoralism",-1.0833, 35.8667),
            (34, "Kajiado",        "Rift Valley",    1107296,  21292.7, 10, 89,  589,  123, 35.7, "Pastoralism, Trade, Tourism",      -2.0983, 36.7819),
            (35, "Kericho",        "Rift Valley",    901777,   2479.1,  9,  78,  534,  128, 19.8, "Tea, Agriculture",                 -0.3833, 35.2833),
            (36, "Bomet",          "Rift Valley",    875689,   1997.9,  7,  62,  445,  98,  32.4, "Tea, Agriculture",                 -0.7833, 35.3500),
            (37, "Kakamega",       "Western",        1867579,  3033.8,  16, 128, 867,  198, 35.6, "Agriculture, Trade",               0.2833,  34.7500),
            (38, "Vihiga",         "Western",        590013,   563.4,   6,  52,  389,  89,  38.9, "Agriculture",                      0.0833,  34.7167),
            (39, "Bungoma",        "Western",        1670570,  3032.4,  13, 104, 756,  167, 36.4, "Agriculture, Trade",               0.5667,  34.5667),
            (40, "Busia",          "Western",        893681,   1694.9,  8,  67,  489,  98,  42.8, "Agriculture, Trade, Fishing",      0.4667,  34.1167),
            (41, "Siaya",          "Nyanza",         993183,   2530.3,  9,  78,  578,  123, 40.2, "Agriculture, Fishing",             0.0617,  34.2883),
            (42, "Kisumu",         "Nyanza",         1155574,  2085.9,  16, 128, 712,  178, 33.8, "Trade, Fishing, Industry",        -0.1022, 34.7617),
            (43, "Homa Bay",       "Nyanza",         1131950,  3183.3,  10, 89,  623,  132, 51.7, "Fishing, Agriculture",            -0.5167, 34.4500),
            (44, "Migori",         "Nyanza",         1116436,  2586.4,  10, 84,  612,  128, 44.6, "Agriculture, Mining, Fishing",    -1.0634, 34.4731),
            (45, "Kisii",          "Nyanza",         1266860,  1317.5,  12, 98,  712,  167, 27.4, "Agriculture, Trade",              -0.6817, 34.7667),
            (46, "Nyamira",        "Nyanza",         605576,   912.5,   6,  52,  423,  89,  29.8, "Agriculture, Tea",                -0.5667, 34.9333),
            (47, "Nairobi",        "Nairobi",        4397073,  696.1,   56, 312, 1867, 456, 17.4, "Trade, Industry, Services, Tech", -1.2921, 36.8219),
        ]

        created = 0
        updated = 0

        for data in counties:
            (code, name, region, population, area_km2, hospitals,
             health_centres, primary_schools, secondary_schools,
             poverty_index, main_activity, latitude, longitude) = data

            county, was_created = County.objects.update_or_create(
                code=code,
                defaults={
                    'name': name,
                    'slug': slugify(name),
                    'region': region,
                    'population': population,
                    'area_km2': area_km2,
                    'hospitals': hospitals,
                    'health_centres': health_centres,
                    'primary_schools': primary_schools,
                    'secondary_schools': secondary_schools,
                    'poverty_index': poverty_index,
                    'main_activity': main_activity,
                    'latitude': latitude,
                    'longitude': longitude,
                }
            )

            if was_created:
                created += 1
                self.stdout.write(f'  ✅ Created: {name}')
            else:
                updated += 1
                self.stdout.write(f'  🔄 Updated: {name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {created} counties created, {updated} updated.'
        ))
