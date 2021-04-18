import os
import glob
import pandas as pd
import unicodedata
import queries as queries



sections_to_add = ["map of institutions", 
                   "100 most recent articles",
                   "list of authors",
                   "list of topics",
                   "list of journals"]

query_options = {
  "map of institutions": {
    "label": "Map of institutions",
    "query": queries.get_query_url_for_locations() 
  },
  "100 most recent articles": {
    "label": "100 most recent articles",
    "query": queries.get_query_url_for_articles()
  }, 
  "list of authors": {
    "label": "list of authors",
    "query": queries.get_query_url_for_authors()
  },
  "list of topics": {
    "label": "list of co-studied topics",
    "query": queries.get_topics_as_table()
  },
  "list of journals":{
    "label": "list of co-studied topics",
    "query": queries.get_query_url_for_venues()  
  }
}

def render_section(query_name, query_options=query_options):

  legend = query_options[query_name]["label"]
  query_url = query_options[query_name]["query"]
  section = """
    <h5 class="title is-5" style="text-align:center;">""" + legend + """ </h5>
        <p align="center">
        <iframe width=75%  height="400" src=""" + '"'+ query_url +'"' + """></iframe>
        </p>
        <br></br>

  """
  return(section)

def render_sections(query_name_list, query_options=query_options):

  sections = ""
  for name in query_name_list:
    sections += render_section(name, query_options=query_options)
  return(sections)

def render_dashboard():

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
""" +render_sections(sections_to_add) + """
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


