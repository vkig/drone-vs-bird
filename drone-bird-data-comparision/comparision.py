import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
import os.path as path

generator_switch_dict = {
    "reflectivity": False,
    "nop": False,
    "3ddistance": False,
    "3dangle": False,
    "2drefldistance": False,
    "2dreflangle": False,
    "2dreflstddistance": False,
    "2dreflstdangle": False,
    "nophist": False,
    "2drefldistancestd": False,
    "2dreflanglestd": False,
    "reflectivityavgstd": True,
    "reflhist": False,
    "std_comparison": False,
    "refl_comparison": False,
}

database_meta = {
    "bird": {
        "name": "madár",
        "root": "..\\database\\2023_04_28_galambok",
        "match_pattern": "bird",
        "longest": "bird_05",
        "max_reflectivity_on_longest": 31,
        "min_reflectivity_on_longest": 0,
    },
    "drone": {
        "name": "drón",
        "root": "..\\database\\2022_09_12_11_02_11_feher_drone",
        "match_pattern": "movement",
        "longest": "movement_04",
        "max_reflectivity_on_longest": 58,
        "min_reflectivity_on_longest": 0,
    }
}
distance_dict = {
    "bird": [],
    "drone": []
}
reflectivity_dict = {
    "bird": [],
    "drone": []
}
reflectivity_std_dict = {
    "bird": [],
    "drone": []
}
point_number_dict = {
    "bird": [],
    "drone": []
}
angle_dict = {
    "bird": [],
    "drone": []
}

longest_movements_reflectivity_histogram = {
    "bird": [],
    "drone": [],
    "drone_points": [],
    "bird_points": [],
}

histogram_range = min(database_meta["bird"]["min_reflectivity_on_longest"],
                      database_meta["drone"]["min_reflectivity_on_longest"]), \
        max(database_meta["bird"]["max_reflectivity_on_longest"],
            database_meta["drone"]["max_reflectivity_on_longest"]),

for database in database_meta:
    dirs = list(filter(lambda x: x.startswith(database_meta[database]["match_pattern"]),
                       listdir(database_meta[database]["root"])))
    files = []
    for actual_dir in dirs:
        for file in listdir(path.join(database_meta[database]["root"], actual_dir)):
            if file.endswith(".csv"):
                files.append(os.path.join(database_meta[database]["root"], actual_dir, file))
    print(files)

    for file in files:
        cloud = pd.read_csv(file, sep=",")

        X = np.array(cloud["X"])
        Y = np.array(cloud["Y"])
        Z = np.array(cloud["Z"])
        Reflectivity = np.array(cloud["Reflectivity"])

        X_avg = np.mean(X)
        Y_avg = np.mean(Y)
        Z_avg = np.mean(Z)
        R_avg = np.mean(Reflectivity)

        if database_meta[database]["longest"] in file:
            longest_movements_reflectivity_histogram[database].append(Reflectivity)
            longest_movements_reflectivity_histogram[database+"_points"].append(len(Reflectivity))

        distance_dict[database].append(np.sqrt(X_avg ** 2 + Y_avg ** 2 + Z_avg ** 2))
        reflectivity_std_dict[database].append(np.std(Reflectivity))
        reflectivity_dict[database].append(R_avg)
        point_number_dict[database].append(len(X))
        angle_dict[database].append(np.rad2deg(np.arctan((np.sqrt(Y_avg ** 2 + Z_avg ** 2)) / X_avg)))

min_reflectivity_value = min(np.min(reflectivity_dict["bird"]), np.min(reflectivity_dict["bird"]))
max_reflectivity_value = max(np.max(reflectivity_dict["drone"]), np.max(reflectivity_dict["drone"]))
min_number_of_points = min(np.min(point_number_dict["bird"]), np.min(point_number_dict["bird"]))
max_number_of_points = max(np.max(point_number_dict["drone"]), np.max(point_number_dict["drone"]))

reflectivity_heatmap_bird, reflectivity_xedges_bird, reflectivity_yedges_bird = np.histogram2d(angle_dict["bird"],
                                                                                               distance_dict["bird"],
                                                                                               weights=
                                                                                               reflectivity_dict[
                                                                                                   "bird"],
                                                                                               bins=25)

number_of_points_heatmap_bird, number_of_points_xedges_bird, number_of_points_yedges_bird = np.histogram2d(
    angle_dict["bird"], distance_dict["bird"], weights=point_number_dict["bird"], bins=25)

reflectivity_extent_bird = [reflectivity_xedges_bird[0], reflectivity_xedges_bird[-1], reflectivity_yedges_bird[0],
                            reflectivity_yedges_bird[-1]]
number_of_points_extent_bird = [number_of_points_xedges_bird[0], number_of_points_xedges_bird[-1],
                                number_of_points_yedges_bird[0], number_of_points_yedges_bird[-1]]

reflectivity_heatmap_drone, reflectivity_xedges_drone, reflectivity_yedges_drone = np.histogram2d(angle_dict["drone"],
                                                                                                  distance_dict[
                                                                                                      "drone"],
                                                                                                  weights=
                                                                                                  reflectivity_dict[
                                                                                                      "drone"],
                                                                                                  bins=25)

number_of_points_heatmap_drone, number_of_points_xedges_drone, number_of_points_yedges_drone = np.histogram2d(
    angle_dict["drone"], distance_dict["drone"], weights=point_number_dict["drone"], bins=25)

reflectivity_extent_drone = [reflectivity_xedges_drone[0], reflectivity_xedges_drone[-1], reflectivity_yedges_drone[0],
                             reflectivity_yedges_drone[-1]]
number_of_points_extent_drone = [number_of_points_xedges_drone[0], number_of_points_xedges_drone[-1],
                                 number_of_points_yedges_drone[0], number_of_points_yedges_drone[-1]]
if generator_switch_dict["reflectivity"]:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(12, 6)
    fig.suptitle("Reflektivitás összehasonlítása madarakon és drónon")
    ax1.set_title("Madarak")
    ax1.set_xlabel("Abszolút szög a LiDAR x tengelye és az objektum között [°]")
    ax1.set_ylabel("Madár távolsága a LiDARtól [m]")
    ax1.imshow(reflectivity_heatmap_bird.T, extent=reflectivity_extent_bird, origin="lower",
               vmin=min_reflectivity_value,
               vmax=max_reflectivity_value)
    ax2.set_title("Drón")
    ax2.set_xlabel("Abszolút szög a LiDAR x tengelye és az objektum között [°]")
    ax2.set_ylabel("Drón távolsága a LiDARtól [m]")
    im = ax2.imshow(reflectivity_heatmap_drone.T, extent=reflectivity_extent_bird, origin="lower",
                    vmin=min_reflectivity_value,
                    vmax=max_reflectivity_value)
    fig.subplots_adjust(right=0.9)
    cbar_ax = fig.add_axes([0.925, 0.15, 0.01, 0.7])
    fig.colorbar(im, cax=cbar_ax)
    plt.show()

if generator_switch_dict["nop"]:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(12, 6)
    fig.suptitle("Az objektumokon mért pontok számának összehasonlítása a drónon és madarakon")
    ax1.set_title("Madár")
    ax1.set_xlabel("Abszolút szög a LiDAR x tengelye és az objektum között [°]")
    ax1.set_ylabel("Madár távolsága a LiDARtól [m]")
    ax1.imshow(number_of_points_heatmap_bird.T, extent=number_of_points_extent_bird, origin="lower",
               vmin=min_number_of_points,
               vmax=max_number_of_points)
    ax2.set_title("Drón")
    ax2.set_xlabel("Abszolút szög a LiDAR x tengelye és az objektum között [°]")
    ax2.set_ylabel("Drón távolsága a LiDARtól [m]")
    ax2.imshow(number_of_points_heatmap_drone.T, extent=number_of_points_extent_bird, origin="lower",
               vmin=min_number_of_points,
               vmax=max_number_of_points)
    fig.subplots_adjust(right=0.9)
    cbar_ax = fig.add_axes([0.925, 0.15, 0.01, 0.7])
    fig.colorbar(im, cax=cbar_ax)
    plt.show()

if generator_switch_dict["3ddistance"]:
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')
    fig.suptitle("A madarak és a drón elhelyezve a mérési adatok terében")
    ax.scatter(distance_dict["bird"], reflectivity_std_dict["bird"], reflectivity_dict["bird"], marker='^', label="madár")
    ax.scatter(distance_dict["drone"], reflectivity_std_dict["drone"], reflectivity_dict["drone"], marker='o', label="drón")
    ax.set_xlabel("Objektum távolsága a LiDARtól [m]")
    ax.set_ylabel("Reflektivitás szórása az objektumon")
    ax.set_zlabel("Átlagos reflektivitás az objektumon")
    ax.legend()
    plt.show()

if generator_switch_dict["3dangle"]:
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')
    fig.suptitle("A madarak és a drón elhelyezve a mérési adatok terében")
    ax.scatter(angle_dict["bird"], reflectivity_std_dict["bird"], reflectivity_dict["bird"], marker='^', label="madár")
    ax.scatter(angle_dict["drone"], reflectivity_std_dict["drone"], reflectivity_dict["drone"], marker='o', label="drón")
    ax.set_xlabel("Abszolút szög a LiDAR x tengelye és az objektum között [°]")
    ax.set_ylabel("Reflektivitás szórása az objektumon")
    ax.set_zlabel("Átlagos reflektivitás az objektumon")
    ax.legend()
    plt.show()

"""
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot()
fig.suptitle("A madarak és a drón elhelyezve a mérési adatok terében")
ax.scatter(point_number_dict["bird"], reflectivity_dict["bird"], marker='^', label="madár")
ax.scatter(point_number_dict["drone"], reflectivity_dict["drone"], marker='o', label="drón")
ax.set_xlabel("Mért pontok száma az objektumon")
ax.set_ylabel("Átlagos reflektivitás az objektumon")
ax.legend()
plt.show()
"""

if generator_switch_dict["2dreflangle"]:
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot()
    fig.suptitle("Reflektivitás az elhajlási szög függvényében")
    ax.scatter(angle_dict["bird"], reflectivity_dict["bird"], marker='^', label="madár")
    ax.scatter(angle_dict["drone"], reflectivity_dict["drone"], marker='o', label="drón")
    ax.set_xlabel("Abszolút szög a LiDAR x tengelye és az objektum között [°]")
    ax.set_ylabel("Átlagos reflektivitás az objektumon")
    ax.legend()
    plt.show()

if generator_switch_dict["reflectivityavgstd"]:
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot()
    fig.suptitle("Objektumok a reflektivitás átlagának és szórásának terében")
    ax.scatter(reflectivity_std_dict["bird"], reflectivity_dict["bird"], marker='^', label="madár")
    ax.scatter(reflectivity_std_dict["drone"], reflectivity_dict["drone"], marker='o', label="drón")
    ax.set_xlabel("Reflektivitás szórása az objektumon")
    ax.set_ylabel("Átlagos reflektivitás az objektumon")
    ax.plot([0, 32], [30, 0], 'r')
    ax.legend()
    plt.show()

if generator_switch_dict["2drefldistance"]:
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot()
    fig.suptitle("Reflektivitás a LiDAR-tól vett távolság függvényében")
    ax.scatter(distance_dict["bird"], reflectivity_dict["bird"], marker='^', label="madár")
    ax.scatter(distance_dict["drone"], reflectivity_dict["drone"], marker='o', label="drón")
    ax.set_xlabel("Objektum távolsága a LiDARtól [m]")
    ax.set_ylabel("Átlagos reflektivitás az objektumon")
    ax.legend()
    plt.show()

if generator_switch_dict["2dreflstdangle"]:
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot()
    fig.suptitle("Reflektivitás szórása az elhajlási szög függvényében")
    ax.scatter(angle_dict["bird"], reflectivity_std_dict["bird"], marker='^', label="madár")
    ax.scatter(angle_dict["drone"], reflectivity_std_dict["drone"], marker='o', label="drón")
    ax.set_xlabel("Abszolút szög a LiDAR x tengelye és az objektum között [°]")
    ax.set_ylabel("Reflektivitás szórása az objektumon")
    ax.legend()
    plt.show()

if generator_switch_dict["2dreflstddistance"]:
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot()
    fig.suptitle("Reflektivitás szórása a LiDAR-tól vett távolság függvényében")
    ax.scatter(distance_dict["bird"], reflectivity_std_dict["bird"], marker='^', label="madár")
    ax.scatter(distance_dict["drone"], reflectivity_std_dict["drone"], marker='o', label="drón")
    ax.set_xlabel("Objektum távolsága a LiDARtól [m]")
    ax.set_ylabel("Reflektivitás szórása az objektumon")
    ax.legend()
    plt.show()

if generator_switch_dict["nophist"]:
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot()
    fig.suptitle("Madarakról visszaverődött pontok számának gyakorisága")
    ax.hist(point_number_dict["bird"], bins=5, rwidth=0.5)
    ax.set_xlabel("Mért pontok száma az objektumon")
    ax.set_ylabel("Gyakoriság")
    plt.show()

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot()
    fig.suptitle("A drónról visszaverődött pontok számának gyakorisága")
    ax.hist(point_number_dict["drone"], bins=5, rwidth=0.5)
    ax.set_xlabel("Mért pontok száma az objektumon")
    ax.set_ylabel("Gyakoriság")
    plt.show()

if generator_switch_dict["2drefldistancestd"]:
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot()
    fig.suptitle("Reflektivitás a LiDAR-tól vett távolság függvényében")
    ax.errorbar(distance_dict["bird"], reflectivity_dict["bird"], reflectivity_std_dict["bird"], linestyle="None",
                marker='^', label="madár")
    ax.errorbar(distance_dict["drone"], reflectivity_dict["drone"], reflectivity_std_dict["drone"], linestyle="None",
                marker='o', label="drón")
    ax.set_xlabel("Objektum távolsága a LiDARtól [m]")
    ax.set_ylabel("Átlagos reflektivitás az objektumon")
    ax.legend()
    plt.show()

if generator_switch_dict["2dreflanglestd"]:
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot()
    fig.suptitle("Reflektivitás az elhajlási szög függvényében")
    ax.errorbar(angle_dict["bird"], reflectivity_dict["bird"], reflectivity_std_dict["bird"], linestyle="None",
                marker='^', label="madár")
    ax.errorbar(angle_dict["drone"], reflectivity_dict["drone"], reflectivity_std_dict["drone"], linestyle="None",
                marker='o', label="drón")
    ax.set_xlabel("Abszolút szög a LiDAR x tengelye és az objektum között [°]")
    ax.set_ylabel("Átlagos reflektivitás az objektumon")
    ax.legend()
    plt.show()

if generator_switch_dict["reflhist"]:
    i = 0
    for i in range(len(longest_movements_reflectivity_histogram["drone"])):
        fig = plt.figure()
        ax = fig.add_subplot()
        fig.suptitle(f"Reflektivitás hisztogram a kiválasztott drónon a mozdulat {i}. lépésében")
        ax.hist(longest_movements_reflectivity_histogram["drone"][i], 10, histogram_range)
        ax.set_xlabel("Reflectivitás érték")
        ax.set_ylabel("Pontok száma")
        plt.savefig("movement_05_" + str(i) + ".png")
        plt.close(fig)

if generator_switch_dict["std_comparison"]:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(12, 6)
    fig.suptitle(f"Az objektumokról visszaverődött pontok reflektivitásának szórásáról készült hisztogramok összehasonlítása")
    ax1.set_title("Szórás hisztogram a madarakon")
    ax1.hist(reflectivity_std_dict["bird"], 20, (0, 35), rwidth=0.8)
    ax1.set_xlabel("Szórás értékek")
    ax1.set_ylabel("A mérések száma adott szórással")
    ax1.set_ylim([0, 25])
    ax2.set_title("Szórás hisztogram a drónon")
    ax2.hist(reflectivity_std_dict["drone"], 20, (0, 35), rwidth=0.8, color="orange")
    ax2.set_xlabel("Szórás értékek")
    ax2.set_ylabel("A mérések száma adott szórással")
    ax2.set_ylim([0, 25])
    plt.show()

if generator_switch_dict["refl_comparison"]:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(12, 6)
    fig.suptitle(f"Az objektumokról visszaverődött pontok reflektivitásának átlagáról készült hisztogramok összehasonlítása")
    ax1.set_title("Reflektivitás átlag hisztogram a madarakon")
    ax1.hist(reflectivity_dict["bird"], 20, (0, 35), rwidth=0.8)
    ax1.set_xlabel("Átlag értékek")
    ax1.set_ylabel("A mérések száma adott szórással")
    ax1.set_ylim([0, 25])
    ax2.set_title("Reflektivitás átlag hisztogram a drónon")
    ax2.hist(reflectivity_dict["drone"], 20, (0, 35), rwidth=0.8, color="orange")
    ax2.set_xlabel("Átlag értékek")
    ax2.set_ylabel("A mérések száma adott szórással")
    ax2.set_ylim([0, 25])
    plt.show()


# ax.errorbar(distance_dict["bird"], reflectivity_dict["bird"], reflectivity_std_dict["bird"], linestyle="None", marker='^', label="madár")
def drone_or_bird(std, avg, a, b):
    return "drone" if - a/b * std + b < avg else "bird"


accuracy = 0
best_a = 0
best_b = 0
for a in range(20, 35):
    for b in range(30, 50):
        count_correct = 0
        count_all = 0
        for i in range(len(reflectivity_dict["drone"])):
            count_correct += 1 if "drone" == drone_or_bird(reflectivity_std_dict["drone"][i], reflectivity_dict["drone"][i], a, b) else 0
            count_all += 1
        for i in range(len(reflectivity_dict["bird"])):
            count_correct += 1 if "bird" == drone_or_bird(reflectivity_std_dict["bird"][i], reflectivity_dict["bird"][i], a, b) else 0
            count_all += 1

        print(count_correct)
        print(count_all)
        print(count_correct / count_all)
        if count_correct / count_all > accuracy:
            accuracy = count_correct / count_all
            best_a = a
            best_b = b

print(accuracy, best_a, best_b)