from sentinelsat import SentinelAPI
from shapely.geometry import Polygon


def get_tallinn_polygon():
    tln_points = [
        (59.455947169131946, 24.532626930520898),
        (59.47862155366181, 24.564212623880273),
        (59.49535595077547, 24.69810849790371),
        (59.51138530046753, 24.825137916849023),
        (59.459087606762346, 24.907535377786523),
        (59.4147455486766, 24.929508034036523),
        (59.39832075950073, 24.844363991067773),
        (59.37664183245853, 24.814151588724023),
        (59.35249898189222, 24.75304013852871),
        (59.32798867805195, 24.573825660989648)
    ]

    # Copernicus Hub likes coordinates in lng,lat format
    return Polygon([(y, x) for x, y in tln_points])


username = "..."
password = "..."

hub = SentinelAPI(username, password, "https://scihub.copernicus.eu/dhus")

data_products = hub.query(
    get_tallinn_polygon(),  # which area interests you
    date=("20200101", "20200420"),
    cloudcoverpercentage=(0, 10),  # we don't want clouds
    platformname="Sentinel-2",
    processinglevel="Level-2A"  # more processed, ready to use data
)

data_products = hub.to_geodataframe(data_products)
# we want to avoid downloading overlapping images, so selecting by this keyword
data_products = data_products[data_products["title"].str.contains("T35VLF")]

print(data_products.shape)
