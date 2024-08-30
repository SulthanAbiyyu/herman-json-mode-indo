import pandas as pd
from tqdm import tqdm
from datasets import load_dataset
from translate import (
    translate_system_prompt,
    translate_user_prompt,
    CATEGORIES,
    SUBCATEGORIES
)

tqdm.pandas()

def read_data():
    data = load_dataset("NousResearch/hermes-function-calling-v1", "json_mode_singleturn")
    data = pd.DataFrame(data['train'])
    return data

def transforms(data):
    data["conversations"] = data['conversations'].progress_apply(translate_system_prompt)
    data["conversations"] = data['conversations'].progress_apply(translate_user_prompt)
    
    data["sistem"] = data["conversations"].apply(lambda x: x[0]["value"])
    data["instruksi"] = data["conversations"].apply(lambda x: x[1]["value"])
    data["output"] = data["conversations"].apply(lambda x: x[2]["value"])
    
    data["category"] = data["category"].map(CATEGORIES)
    data["subcategory"] = data["subcategory"].map(SUBCATEGORIES)

    data = data[["id", "category", "subcategory", "sistem", "instruksi", "output"]]
    return data

def write_data(data, format="csv"):
    import os
    os.makedirs("data", exist_ok=True)
    if format == "csv":
        data.to_csv("./data/herman-json-mode.csv", index=False)
    elif format == "json":
        data.to_json("./data/herman-json-mode.json", orient="records")
    else:
        raise ValueError("Format not supported")
    
def push_to_hub():
    from datasets import Dataset
    data = Dataset.from_pandas(data)
    data.push_to_hub("herman-json-mode-indo")
    
if __name__ == "__main__":
    data = read_data()
    data = transforms(data)
    write_data(data)
    push_to_hub()