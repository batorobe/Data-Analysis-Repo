#~~~Code to read in .csv and output most upvoted posts.
#Apply multiplier
from glob import glob
from pandas import read_csv
import pandas as pd
from datetime import datetime
from collections import defaultdict
from itertools import izip

month_sum_data = pd.read_csv("month_sum_data.csv", 
                          skiprows=[0], names=["date", "upvotes"])
avg_mult = []
''' year in reversed(range(2008,2014,1)):
    for month in reversed(range(1,13,1)):
        dateTime = str(year) + "-" + str(month).rjust(2,"0")
        multiplier = 241434499./month_sum_data[month_sum_data.date > dateTime].upvotes.values
        avg_mult.append(multiplier)'''

month_sum_data["inflation_multiplier"]=241434499./month_sum_data.upvotes.values
#print month_sum_data.inflation_multiplier[1]


######

def convertTimeStamp(x):
    if(x > 1):
        return datetime.fromtimestamp(x)
    else:
        return datetime.fromtimestamp(946684800)

date_incr=1
filenames = []
glob("*.csv.gz")
for item_object in glob("*.csv.gz"):
    filenames.append(item_object)
#filenames.remove("RS_2008-01.csv.gz")


print "Finished appending..."
month_counts = defaultdict(int)
most_upvoted_post = defaultdict(int)
most_upvoted_permalink = defaultdict(int)

for fileName in filenames:
    print "Reading filename: " + fileName
    reddit_data = pd.read_csv(fileName, compression="gzip", 
                          skiprows=[0], names=["author", "created_utc", "domain", "downs", "id", "num_comments", "over_18", 
                                               "permalink", "score", "subreddit", "title", "ups", "url"])
    reddit_data["datetime"]=reddit_data["created_utc"].apply(lambda x: convertTimeStamp(x))
    reddit_data["date"]=reddit_data["datetime"].apply(lambda x: str(x.timetuple()[0]).zfill(4) + "-" + str(x.timetuple()[1]).zfill(2) + "-" 
                                                  + str(x.timetuple()[2]).zfill(2))
    
    reddit_data["ups"] = reddit_data["ups"].apply(lambda x: x*month_sum_data.inflation_multiplier[date_incr])
    for date, record in reddit_data.groupby("date"):
        for ups,permalink in izip(record.ups,record.permalink):
            if(ups > most_upvoted_post[date]):
                most_upvoted_post[date] = ups
                most_upvoted_permalink[date] = permalink
            
            
        #month_counts[date] += record.ups.sum() 
        #Keep outside dictionary to find post with most upvotes. W/Permalink & Upvotes
    date_incr += 1

with open("most_upvoted_posts_list.csv", "wb") as out_file:
    out_file.write("Date,Adjusted_Upvotes,Permalink")
    """for date in sorted(month_counts.keys()):
        out_file.write("\n" + date + "," + str(month_counts[date]))"""
    for date in sorted(most_upvoted_post.keys()):
        out_file.write("\n" + date + "," + str(most_upvoted_post[date]) + "," + str(most_upvoted_permalink[date]))

print "Finally Done!"

#~~~Code to output .csv to .png as graph
%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Set some Pandas options
pd.set_option('display.notebook_repr_html', False)

reddit_data = pd.read_csv("most_upvoted_posts_list.csv", sep='\t', 
                          skiprows=[0], names=["date", "Upvotes"])
dates = [0, 366, 731, 1096, 1461, 1827, 2191]

reddit_data.plot(figsize=(12,7), lw=1)
plt.xticks(dates,
          range(2008,2015))
plt.yticks(np.arange(0, 1.8e6, 0.2e6), ["", ".2 M", ".4 M", ".6 M", ".8 M", 
                                         "1 M", "1.2 M", "1.4 M", "1.6 M"])
plt.ylabel("Total Upvotes")
plt.title("Most Upvoted Posts Adjusted for Inflation, 2008-2013")
plt.savefig("reddit-daily-adjusted-upvotes.png")
;

