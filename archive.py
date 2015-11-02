from argparse import ArgumentParser
import requests
import os
import re

parser = ArgumentParser()

parser.add_argument("website",
        help="the website to scrape")

parser.add_argument("-s",
        "--start",
        dest="start",
        type=int,
        help="date to start scraping (e.g., 20150929004644)")

parser.add_argument("-e",
    "--end",
    dest="end",
    type=int,
    help="date to stop scraping (e.g., 20150930005925)")

args = parser.parse_args()


# pull down archive directory

response = requests.get("https://web.archive.org/cdx/search/xd?url=" + args.website)


# extract individual valid pages (must have HTTP 200)

results = [(line[1], "https://web.archive.org/web/" + line[1] + "id_/" + line[2])
            for line
            in [line.split(" ") for line in response.text.strip().split("\n")]
            if (not args.start or line[1] >= str(args.start))
                and (not args.end or line[1] <= str(args.end))
                and line[4] == "200"]


# make directory for site

directory = re.sub(r"[/\\:*?\"<>|]", '', args.website)

if not os.path.exists(directory):
    os.makedirs(directory)

os.chdir(directory)


# download and add new HTML file in directory (if it does not exist already)

for result in results:
    time, url = result

    if os.path.isfile(time + ".html"):
        continue

    try:
        response = requests.get(url)

        try:

            with open(time + ".html", "w") as f:
                f.write(response.text.encode("utf-8"))

        except:

            with open(time + ".html", "wb") as f:
                f.write(response.text.encode("utf-8"))

    except KeyboardInterrupt:
        break

    except:
        continue
