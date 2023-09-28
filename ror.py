import requests
import pandas as pd

session = requests.session()

def search_ror(row):
    response = session.get("https://api.ror.org/organizations", params={"query": row['Institution Name']})
    if response.status_code == 200:
        d = response.json()
        for i, item in enumerate(d['items']):

            row[f"Name_{str(i).zfill(2)}"] = item['name']
            row[f"ID_{str(i).zfill(2)}"] = item['id']
    else:
        row['Name_00'] = "None"
        row['ID_00'] = "None"

    return row


def get_columns(first, number_of_columns):

    columns = [*first]

    for i in range(number_of_columns):
        columns.append(f"Name_{str(i).zfill(2)}")
        columns.append(f"ID_{str(i).zfill(2)}")

    return columns




if __name__ == "__main__":
    df = pd.read_json("data/2023-09-12-final_w_supplemental.json")

    # Search for the ROR ID

    df = df.apply(lambda x: search_ror(x), axis=1)

    # Reorder nicely
    columns = get_columns(["Institution Name"], 5)
    df = df[columns]

    # Write to excel
    df.to_excel("ror_search.xlsx", index=False)