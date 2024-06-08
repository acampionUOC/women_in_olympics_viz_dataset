# women_in_olympics_viz_dataset
Dataset generation for Women in Olympics visualization


## Description
This project has been created to produce the dataset used in data visualization Women in Olympics. This data visualization has been proposed as the solution for the task PRA2 in Data Visualization subject in Data Science Master from Universitat Oberta de Catalunya. 

<br><br>
Code provided in this repository has two main features:
- dataset generation through  web scraping to allow to update existing datasets in the same domain.
- data preprocessing procedures to integrate the information from the different input datasets used in the data visualization. 

With the resulting dataset it has been published in Tableau Public a storytelling data visualization where it is shown the participation of female athletes at the Olympic games:
- historical gender equality index global and per participating team
- gender equality status in the last Summer and Winter Olympic Games and situation by subcontinent
- relationship of gender equality with Human Development Index per country


<br><br>
project files:
- main.py: main module to run the web scraping procedure to get athletes in Olympic games from PyeongChang 2018 up to last games in Beijing 2022. Web scraper uses https://www.olympiandatabase.com/ web as source of information.
- source\olympics_scraper: class implementation of web scraper
- notebook\olympics_preprocessing.ipynb: notebook used for the data preprocessing and resulting dataset generation
- datasets\athlete_events.csv: all athletes in Olympic Games from 1896 to 2016 (source: https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results) 
- datasets\List_of_countries_by_continent.txt: List of countries by continent and region (source: https://statisticstimes.com/geography/countries-by-continents.php)
- datasets\List_of_countries_by_HDI.txt: List of countries by Human Development Index (source: https://en.wikipedia.org/wiki/List_of_countries_by_Human_Development_Index)
- datesets\athletes_2018_to_2022.csv: resulting dataset from main.py execution (source: https://www.olympiandatabase.com/)
- datasets\all_games_athletes.csv: resulting dataset after data integration of preprocessing of all the datasets in the project
- README.md
- LICENSE
- requirements.txt
<br> 

<br>
Data visualization created for this project is published to Tableau Public:

- https://public.tableau.com/app/profile/alvaro.campion/viz/WomeninOlympics-beforeParis2024/vizhistory

<br>

## Author
Project author is:
- Alvaro Campion Mezquiriz (acampion@uoc.edu)
- done in June 2024 under MIT license

