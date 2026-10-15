import matplotlib.pyplot as plt
import csv

# 0,1,Image ID,Total Number of Contours,Number of Correctly Captured Grains,
# Number of Adhesion Cases,Number of Missed Cases,Number of Miscaptured Cases

slice_indices = []

with open("2D Result Summary - Sheet1.csv", "r") as f:
    next(f)
    data = csv.reader(f)
    for row in data:
        index = int(row[2][7:10])
        # cases = int(row[5])   # adhesion
        # cases = int(row[6])    # misses
        cases = int(row[7])  # miscaptures
        for x in range(cases):
            slice_indices.append(index)

plt.hist(
    slice_indices,
    bins=25,
    # color="steelblue",
    # color="orangered",
    color="olivedrab",
    edgecolor="black",
    # alpha=0.8
)

plt.xlabel("Slice Index")
plt.ylabel("Number of Cases")
# plt.title("Distribution of Adhesion Cases Across Slices")
# plt.title("Distribution of Missed Cases Across Slices")
# plt.title("Distribution of Miscaptured Cases Across Slices")
plt.show()