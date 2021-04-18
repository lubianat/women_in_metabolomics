import os
import glob
import pandas as pd
import unicodedata
import queries as queries
import render as render

def render_dashboard():

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
  html = render.render_header(site_title) + \
  render.render_top(site_title, site_subtitle) +  \
  render.render_sections(sections_to_add, query_options) + \
  """
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


