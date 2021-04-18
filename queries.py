import urllib.parse



def get_selector():
    """
    The selector that decides the scope of the dashboard. It MUST have the keywords
    ?work and ?author. 
    The specific works and authors can be added by adapting the query on WDQS:
    https://w.wiki/3Cmd
    After crafting it on WDQS, transclude the clauses inside "WHERE{} to here, 
    omitting the "SERVICE wikibase..." line.
    """

    selector = """ 
    ?work wdt:P50 ?author.
    ?author wdt:P101 wd:Q12149006.
    ?author wdt:P21 wd:Q6581072.
    """

    return(selector)



def render_url(query):
  return "https://query.wikidata.org/embed.html#" + urllib.parse.quote(query, safe='')
  
def get_query_url_for_articles():
  query = """

  #defaultView:Table
  SELECT
  (MIN(?dates) AS ?date)
  ?work ?workLabel
  (GROUP_CONCAT(DISTINCT ?type_label; separator=", ") AS ?type)
  ?journal ?journalLabel
  (GROUP_CONCAT(DISTINCT ?author_label; separator=", ") AS ?authores)
  WHERE {
  """ + get_selector() + """
  OPTIONAL {
    ?author rdfs:label ?author_label_ . FILTER (LANG(?author_label_) = 'en')
  }
  BIND(COALESCE(?author_label_, SUBSTR(STR(?author), 32)) AS ?author_label)
  OPTIONAL { ?work wdt:P31 ?type_ . ?type_ rdfs:label ?type_label . FILTER (LANG(?type_label) = 'pt') }
  ?work wdt:P577 ?datetimes .
  BIND(xsd:date(?datetimes) AS ?dates)
  OPTIONAL { ?work wdt:P1433 ?journal }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,da,de,es,fr,jp,no,ru,sv,zh". }  
  }
  GROUP BY ?work ?workLabel ?journal ?journalLabel
  ORDER BY DESC(?date)
  LIMIT 100 

  """
  
  return render_url(query)

def get_topics_as_table():
  query_3 = """


  #defaultView:Table
  SELECT ?count ?theme ?themeLabel ?example_work ?example_workLabel
  WITH {
    SELECT (COUNT(?work) AS ?count) ?theme (SAMPLE(?work) AS ?example_work)
    WHERE {
      """ + get_selector() + """
      ?work wdt:P921 ?theme .
    }
    GROUP BY ?theme
  } AS %result
  WHERE {
    INCLUDE %result
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en,da,de,es,fr,jp,nl,no,ru,sv,zh" . } 
  }
  ORDER BY DESC(?count) 
  LIMIT 100

  """
  return render_url(query_3) 

def get_query_url_for_venues():
  query_4 = """
  # Venue statistics for a collection
  SELECT
    ?count (SAMPLE(?short_name_) AS ?short_name)
    ?journal ?journalLabel
    ?topics ?topicsUrl
  WITH {
    SELECT
      (COUNT(DISTINCT ?work) as ?count)
      ?journal
      (GROUP_CONCAT(DISTINCT ?topic_label; separator=", ") AS ?topics)
    WHERE {
      """ + get_selector() + """
      ?work wdt:P1433 ?journal .
      OPTIONAL {
        ?journal wdt:P921 ?topic .
        ?topic rdfs:label ?topic_label . FILTER(LANG(?topic_label) = 'en') }
    }
    GROUP BY ?journal
  } AS %result
  WHERE {
    INCLUDE %result
    OPTIONAL { ?journal wdt:P1813 ?short_name_ . }
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en,da,de,es,fr,jp,nl,no,ru,sv,zh". }  
  } 
  GROUP BY ?count ?journal ?journalLabel ?topics ?topicsUrl
  ORDER BY DESC(?count)

  """
  return render_url(query_4) 

def get_query_url_for_locations():
  query_5 = """


  #defaultView:Map
  SELECT ?organization ?organizationLabel ?geo ?count ?layer
  WITH {
    SELECT DISTINCT ?organization ?geo (COUNT(DISTINCT ?work) AS ?count) WHERE {
      """ + get_selector() + """
      ?author ( wdt:P108 | wdt:P463 | wdt:P1416 ) / wdt:P361* ?organization . 
      ?organization wdt:P625 ?geo .
    }
    GROUP BY ?organization ?geo ?count
    ORDER BY DESC (?count)
    LIMIT 2000
  } AS %organizations
  WHERE {
    INCLUDE %organizations
    BIND(IF( (?count < 1), "No results", IF((?count < 2), "1 result", IF((?count < 5), "1 < results ≤ 10", IF((?count < 101), "10 < results ≤ 100", IF((?count < 1001), "100 < results ≤ 1000", IF((?count < 10001), "1000 < results ≤ 10000", "10000 or more results") ) ) ) )) AS ?layer )
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }        
  }
  ORDER BY DESC (?count)


  """
  return render_url(query_5)


def get_query_url_for_authors():
  query_7 = """
  #defaultView:Table
  SELECT (COUNT(?work) AS ?article_count) ?author ?authorLabel ?orcids  ?organizationLabel  ?countryLabel WHERE {
    """ + get_selector() + """
  OPTIONAL { ?author ( wdt:P108 | wdt:P463 | wdt:P1416 ) ?organization .
           OPTIONAL { ?organization wdt:P17 ?country . }               
           }
  OPTIONAL { ?author wdt:P496 ?orcids }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,da,de,es,fr,jp,nl,no,ru,sv,zh". }

    }
  GROUP BY ?author ?authorLabel ?orcids  ?organizationLabel ?countryLabel
  ORDER BY DESC(?article_count)

  """
  return render_url(query_7)
