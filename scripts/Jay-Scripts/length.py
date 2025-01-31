import os

def count_files(directory):
    return len([file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))])

# Example usage
dir1 = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/video_data/images_s'
dir2 = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/video_data/labels'
dir3 = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/annotated_images'
dir4 = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/checker_dummy/annotated'
dir5 = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/checker_dummy/labels'

count_dir1 = count_files(dir1)
count_dir2 = count_files(dir2)
count_dir3 = count_files(dir3)
# count_dir4 = count_files(dir4)
# count_dir5 = count_files(dir5)

print(f"Total number of files in {dir1}: {count_dir1}")
print(f"Total number of files in {dir2}: {count_dir2}")
print(f"Total number of files in {dir3}: {count_dir3}")
# print(f"Total number of files in {dir4}: {count_dir4}")
# print(f"Total number of files in {dir5}: {count_dir5}")

# Count of matching images for parot_disco_takeoff: 839
# Count of matching images for dji_matrice_210_hillside: 1501
# Count of matching images for fixed_wing_over_hill_2: 294
# Count of matching images for 2019_11_14_C0001_3922_matrice: 2524
# Count of matching images for parrot_clear_birds_med_range: 819
# Count of matching images for GOPR5846_002: 629
# Count of matching images for 2019_09_02_C0002_3700_mavic: 0
# Count of matching images for gopro_002: 318
# Count of matching images for dji_matrice_210_mountain: 1420
# Count of matching images for 2019_09_02_C0002_2527_inspire: 486
# Count of matching images for dji_phantom_4_long_takeoff: 397
# Count of matching images for gopro_003: 554
# Count of matching images for GOPR5847_003: 456
# Count of matching images for dji_matrice_210_sky: 1318
# Count of matching images for dji_phantom_mountain_cross: 3648
# Count of matching images for 2019_10_16_C0003_1700_matrice: 1298
# Count of matching images for parrot_disco_distant_cross: 2390
# Count of matching images for 00_02_45_to_00_03_10_cut: 399
# Count of matching images for GOPR5847_004: 698
# Count of matching images for gopro_004: 674
# Count of matching images for dji_phantom_4_hillside_cross: 2274
# Count of matching images for parrot_disco_distant_cross_3: 2390
# Count of matching images for dji_phantom_4_swarm_noon: 2791
# Count of matching images for GOPR5845_001: 540
# Count of matching images for gopro_008: 990
# Count of matching images for GOPR5842_007: 480
# Count of matching images for custom_fixed_wing_1: 1431
# Count of matching images for dji_mavick_mountain_cruise: 1375
# Count of matching images for 2019_10_16_C0003_5043_mavic: 426
# Count of matching images for two_parrot_disco_1: 3306
# Count of matching images for dji_matrice_210_off_focus: 1216
# Count of matching images for 00_01_52_to_00_01_58: 122
# Count of matching images for gopro_005: 810
# Count of matching images for GOPR5846_005: 379
# Count of matching images for GOPR5848_004: 644
# Count of matching images for gopro_006: 926
# Count of matching images for parrot_disco_zoomin_zoomout: 665
# Count of matching images for swarm_dji_phantom: 6811
# Count of matching images for matrice_600_2: 3001
# Count of matching images for distant_parrot_with_birds: 648
# Count of matching images for two_uavs_plus_airplane: 1485
# Count of matching images for custom_fixed_wing_2: 1609
# Count of matching images for 2019_10_16_C0003_4613_mavic: 426
# Count of matching images for dji_mavick_mountain: 2810
# Count of matching images for dji_mavick_hillside_off_focus: 1428
# Count of matching images for GOPR5844_002: 446
# Count of matching images for dji_mavick_close_buildings: 1501
# Count of matching images for 00_09_30_to_00_10_09: 1085
# Count of matching images for two_distant_phantom: 1733
# Count of matching images for GOPR5842_005: 492
# Count of matching images for dji_pantom_landing_custom_fixed_takeoff: 2613
# Count of matching images for GOPR5843_005: 524
# Count of matching images for 2019_08_19_GOPR5869_1530_phantom: 964
# Count of matching images for matrice_600_3: 2955
# Count of matching images for gopro_007: 3480
# Count of matching images for 00_10_09_to_00_10_40: 894
# Count of matching images for GOPR5843_002: 393
# Count of matching images for GOPR5842_002: 598
# Count of matching images for 2019_08_19_C0001_5319_phantom: 2820
# Count of matching images for 2019_09_02_GOPR5871_1058_solo: 725
# Count of matching images for 2019_08_19_GP015869_1520_inspire: 876
# Count of matching images for GOPR5848_002: 501
# Count of matching images for parrot_clear_birds: 1579
# Count of matching images for gopro_000: 480
# Count of matching images for parrot_disco_long_session: 3599
# Count of matching images for swarm_dji_phantom4_2: 2910
# Count of matching images for distant_parrot_2: 838
# Count of matching images for 00_06_10_to_00_06_27: 227
# Count of matching images for gopro_001: 480
# Count of matching images for off_focus_parrot_birds: 598
# Count of matching images for 2019_10_16_C0003_3633_inspire: 1406
# Count of matching images for dji_phantom_4_mountain_hover: 1499
# Count of matching images for dji_mavick_distant_hillside: 1501
# Count of matching images for parrot_disco_midrange_cross: 2869
# Count of matching images for fixed_wing_over_hill_1: 203
# Count of matching images for GOPR5845_004: 352
# Count of matching images for GOPR5844_004: 404