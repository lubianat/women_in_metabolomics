import os
import glob
import urllib.parse
import pandas as pd
import unicodedata

def render_dashboard():


  url1 = get_query_url_for_articles()
  url3 = get_topics_as_table()
  url4 = get_query_url_for_venues()
  url5 = get_query_url_for_locations()
  url7 = get_query_url_for_authors()
  

  site_location_legend = "Map of institutions"
  articles_legend = "100 most recent articles"
  author_list_legend = "List of authors"
  topics_list_legend = "List of co-studied topics"
  journal_list_legend = "List of journals"

  license_statement = '''
            This content is available under a <a target="_blank" href="https://creativecommons.org/publicdomain/zero/1.0/"> 
            Creative Commons CC0</a> license.
  '''
  code_availability_statement = '''
  Source code for the website available at <a target="_blank" href="https://github.com/lubianat/women_in_metabolomics">
            https://github.com/lubianat/women_in_metabolomics </a>
  '''

  scholia_credit_statement = '''
SPARQL queries adapted from <a target="_blank" href="https://scholia.toolforge.org/">Scholia</a>
  '''

  creator_statement = '''
 Based on a curation by <a target="_blank" href="https://legido-quigley-lab.com/"> Prof. Cristina Legido-Quigley</a> and collaborators at <a href="https://docs.google.com/document/d/1-GUNDm0ul0TRkkETYa6U1tjnMJdxwKRPqBftN2gGVAo/edit">
 this Google Docs </a>
 </p>
 <p>
 Dashboard  by <a target="_blank" href="https://www.wikidata.org/wiki/User:TiagoLubiana">TiagoLubiana</a>
  '''

  site_title = "Women in Metabolomics"
  site_subtitle = '''A map via Wikidata from data curated in <a target="_blank" href="https://docs.google.com/document/d/1-GUNDm0ul0TRkkETYa6U1tjnMJdxwKRPqBftN2gGVAo/edit?usp=sharing">
  this Google Docs </a>
'''
  html = """
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>""" + site_title + """</title>
  <meta property="og:description" content="powered by Wikidata">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
  <link href="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js" rel="stylesheet"
    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
</head>

<body>
  <section class="section">
    <div class="container">
      <div class="columns is-centered">
        <div class="column is-half has-text-centered">
          <h1 class="title is-1"> """ + site_title + """</h1>
          <h2>""" + site_subtitle +"""</h2>
        </div>
      </div>
    </div>
    <div class="column is-half has-text-centered">
  </section>
   </section>

    <h5 class="title is-5" style="text-align:center;">""" + author_list_legend + """ </h5>
        <p align="center">
        <iframe width=75%  height="400" src=""" + '"'+ url7 +'"' + """></iframe>
        </p>
        <br></br>

      <h5 class="title is-5" style="text-align:center;display:block;"> """ + site_location_legend + """</h5>
                  <p align="center">
          <iframe width=75%   height="400" src=""" + '"'+ url5 +'"' + """></iframe>
          </p>
   <br></br>

      <h5 class="title is-5" style="text-align:center;"> """ + articles_legend + """</h5>
        <p align="center">
          <iframe width=75% height="400" src=""" + '"'+ url1 +'"' + """></iframe>
        </p>
    <br></br>
      <h5 class="title is-5" style="text-align:center;"> """ + topics_list_legend + """  </h5>
        <p align="center">
            <iframe width=75%  height="400" src=""" + '"'+ url3+'"' + """></iframe>
        </p>
<br></br>
      <h5 class="title is-5" style="text-align:center;"> """ + journal_list_legend + """ </h5>
      <p align="center">
            <iframe width=75%  height="400" src=""" + '"'+ url4 +'"' + """></iframe>
      </p>
<br></br>
  </p>
  </div>
 </br>

  <footer class="footer">
    <div class="container">
      <div class="content has-text-centered">
        <p>""" + license_statement + """  </p>
        <p>""" + code_availability_statement + """ </p>
        <p>""" + scholia_credit_statement + """</p>
        <p>""" + creator_statement + """ </p>
      </div>
    </div>
  </footer>
</body>

</html>
  """
  return(html)


def get_work_selector_for_covid_19():
  selector = """ 
  VALUES ?topic_of_interest { wd:Q84263196 wd:Q82069695 }
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
  """ + get_work_selector_for_covid_19() + """
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
      """ + get_work_selector_for_covid_19() + """
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
      """ + get_work_selector_for_covid_19() + """
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
      """ + get_work_selector_for_covid_19() + """
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
    """ + get_work_selector_for_covid_19() + """
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
