from wbib import render_dashboard
import yaml
import queries as queries

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



with open("index.html", "w") as f:
    with open("config.yaml") as f2:
        config = yaml.load(f2, Loader=yaml.FullLoader)

    sections_to_add = []


    for query_names in config["sections"]:
        for key, value in query_names.items():
            query_options[key]["label"] = value
            print(value)
            sections_to_add.append(key)


    html = render_dashboard(config, query_options, sections_to_add)
    f.write(html)

