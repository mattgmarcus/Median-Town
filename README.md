MedianProj
==========

This is a web app that makes it easier to view medians for Dartmouth classes. It's hosted on heroku at: median-town.herokuapp.com

I was motivated to do this because I was frustrated by both the format the school organized them in (https://www.dartmouth.edu/~reg/transcript/medians/13f.html) and the need to have multiple tabs open if I wanted to see data from a few terms. 

I wrote scrapers in python using the BeautifulSoup library to get all the course medians over the last few years. I then organized the data into dictionaries and stored them in json documents. I used json's instead of a dedicated database because I want the app to run on a single page and have all the information preloaded, in order to minimize the number of requests. 

The backend runs with node.js and express.

I also learned how to use the d3.js library so that I could represent the data on course medians through graphs. 
