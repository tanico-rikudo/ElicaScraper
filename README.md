# ElicaScraper
Crawl and Scrape web pages for my use

## What's this? 
1.  This crawler can inspect the following site....<br>
    *Confidential must be written in elica.conf*

    - NIKKEI news

    Not only static contents but also async process such as Jquery objects can be captured and scraped.

2. Results are sent to be designated destinations. <br>
   *Confidential for SMTP  must be written in mail.conf*
   *Destinations must be written in send_list.csv*

## Envs
Refer to requrement.txt
Base env is python2.7. And some basic modules are essential such as csv

## Secret files
<pre>
conf
├── elica.conf
├── mmail.conf
└── send_list.csv
</pre>

