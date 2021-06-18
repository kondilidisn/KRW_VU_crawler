from bs4 import BeautifulSoup
import requests


import pickle

from Publication import Publication

frank_research_vu = "https://research.vu.nl/en/persons/fah-van-harmelen/publications/"

vossen_research_vu = "https://research.vu.nl/en/persons/ptjm-vossen/publications/"

bal_research_vu = "https://research.vu.nl/en/persons/he-bal/publications/"

boomsma_research_vu = "https://research.vu.nl/en/persons/di-boomsma/publications/"


def get_vu_site_publications(url):

	publication_objects = []

	page_counter = 0

	while True:

		page_addition = "" if page_counter == 0 else "?page=" + str(page_counter)

		current_url = url + page_addition


		webpage = requests.get(current_url)

		content = webpage.content
		soup = BeautifulSoup(content,'lxml')

		pub_list = soup.find_all("li", {"class": "list-result-item"})

		for publication in pub_list:


			year = publication.find("div", {"class": "search-result-group"})

			if year is not None:
				year = year.text.strip()
				prev_year = year
			else:
				year = prev_year

			actual_pub_object = publication.find("div", {"class": "result-container"})

			title = actual_pub_object.find("span").text


			long_text = actual_pub_object.find("div", {"class": "rendering_short"}).text


			long_text = long_text [ len(title) : ]

			year_index = long_text.find(year)

			last_comma_position_before_year = long_text[: year_index].rfind(",")

			authors = long_text[ :last_comma_position_before_year ]

			location = long_text[ year_index + 6 : ]


			research_output_index = location.find("Research output")

			location = location [ : research_output_index]

			pub_object = Publication(year = year, title = title, authors = authors, location = location)

			publication_objects.append(pub_object)

		if len(pub_list) == 0:
			break

		page_counter += 1

	return publication_objects


protagonist_names = ["harmelen", "vossen", "henriBal", "boomsma"]

protagonist_vu_websites = [frank_research_vu, vossen_research_vu, bal_research_vu, boomsma_research_vu]

publication_individual_prefix = ["f_P_", "v_P_", "ba_P_", "boo_P_"]

IRI_domain = "http://www.semanticweb.org/kondilidisn/KRW/2021/acbio"

with open("VU_crawled_publications.ttl", 'w') as out:
    
	for i in range(len(protagonist_names)):

		publications = get_vu_site_publications(protagonist_vu_websites[i])

		print("# Number of publications by ", protagonist_names[i], ": ", len(publications))

		for j, publication in enumerate(publications):


			instance_name = publication_individual_prefix[i] + str(j)

			out.write(publication.get_turtle_format(IRI_domain = IRI_domain, instance_name = instance_name, protagonist = protagonist_names[i]) + '\n')
