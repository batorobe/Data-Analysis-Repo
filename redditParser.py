from glob import glob
from pandas import read_csv
import pandas as pb
from datetime import datetime
from collections import defaultdict


filenames = []
glob("*.csv.gz")
for item_object in glob("RS_2008*.csv.gz"):
    print "Appending: " + item_object
    filenames.append(item_object)
filenames.remove("RS_2008-10.csv.gz")

month_counts = defaultdict(int)

for fileName in filenames:
    print "Reading filename: " + fileName
    reddit_data = pb.read_csv(fileName, compression="gzip", 
                          skiprows=[0], names=["author", "created_utc", "domain", "downs", "id", "num_comments", "over_18", 
                                               "permalink", "score", "subreddit", "title", "ups", "url"])
    reddit_data["datetime"]=reddit_data["created_utc"].apply(lambda x: datetime.fromtimestamp(x))
    reddit_data["date"]=reddit_data["datetime"].apply(lambda x: str(x.timetuple()[0]).zfill(4) + "-" + str(x.timetuple()[1]).zfill(2) + "-" 
                                                  + str(x.timetuple()[2]).zfill(2))   
    for date, record in reddit_data.groupby("date"):
        month_counts[date] += record.ups.sum()
        
    with open("total_data.csv", "wb") as out_file:
        out_file.write("Date,Upvotes")
        for date in sorted(month_counts.keys()):
            out_file.write("\n" + date + "," + str(month_counts[date]))
