
# Publication Event
class Publication:
	def __init__(self, year, title, authors, location ):
		self.year = year
		self.authors = authors.replace('\"', "\\\"")
		self.title = title.replace('\"', "\\\"")
		self.location = location.replace('\"', "\\\"")

	def show(self):
		print(self.title, " | " ,self.authors, " | " , self.year, " | " , self.location)


	def get_turtle_format(self, IRI_domain, instance_name, protagonist):
		  ### Example of a publication in trutle format :
		# ###  http://www.semanticweb.org/kondilidisn/KRW/2021/acbio#f_Example_Dupl_Publ_0
		# :Pub2_2010 rdf:type owl:NamedIndividual ,
		#                     :PublicationEvent ;
		#            :protagonist :Stefan ;
		#            :authors "Stefan et. al"^^xsd:string ;
		#            :date "2010-05-01T00:00:00"^^xsd:dateTime ;
		#            :virtualLocation "KJournal"^^xsd:string ;
		#            :title "Second best paper"^^xsd:string .

		# instance IRI:
		turtle_format = "###  " + IRI_domain + "#" + instance_name + "\n"
		# type of:
		turtle_format += ":" + instance_name + " rdf:type owl:NamedIndividual ,\n                    :PublicationEvent ;\n"
		# protagonist
		turtle_format +="           :protagonist :" + protagonist + " ;\n"
		# authors
		turtle_format +="           :authors \"" + self.authors + "\"^^xsd:string ;\n"
		# date
		turtle_format +="           :date \"" + str(self.year) + "-01-01" + "\"^^xsd:date ;\n"
		# location
		turtle_format +="           :virtualLocation \"" + self.location + "\"^^xsd:string ;\n"
		# title
		turtle_format +="           :title \"" + self.title + "\"^^xsd:string .\n\n"

		return turtle_format

