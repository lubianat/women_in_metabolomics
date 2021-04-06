from wbib import render_dashboard

with open("index.html", "w") as f:
    html = render_dashboard()
    f.write(html)

