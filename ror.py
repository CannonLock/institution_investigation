import requests
import pandas as pd

session = requests.session()

def search_ror(row):
    response = session.get("https://api.ror.org/organizations", params={"query": row['Institution Name']})
    if response.status_code == 200:
        d = response.json()
        for i, item in enumerate(d['items']):

            if i == 3:
                continue

            row[f"Name_{str(i).zfill(2)}"] = item['name']
            row[f"ID_{str(i).zfill(2)}"] = item['id']
    else:
        row['Name_00'] = "None"
        row['ID_00'] = "None"

    return row

if __name__ == "__main__":
    df = pd.read_json("data/2023-09-12-final_w_supplemental.json")
    df = df.apply(lambda x: search_ror(x), axis=1)
    df.to_excel("ror_search.xlsx", index=False)