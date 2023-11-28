import requests

r = requests.head("https://www.semanticscholar.org/paper/Machine-Learning-Operations-(MLOps)%253A-Overview%252C-and-Kreuzberger-K%25C3%25BChl/aba92bb029e81cb6c4c1b90a5adec57c738ea9bd")
print(r.headers)
print("text/html" in r.headers["Content-Type"])
