import os
import glob
import pandas as pd
import unicodedata
import queries as queries
import render as render

def render_dashboard(config, query_options, sections_to_add):
  """

  - Args:
     - config: A .yaml file with the configs
  """
  license_statement = config["license_statement"]
  code_availability_statement = config["code_availability_statement"]
  scholia_credit_statement = config["scholia_credit"]
  creator_statement = config["creator_credit"]
  site_title = config["title"]
  site_subtitle = config["subtitle"]

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


