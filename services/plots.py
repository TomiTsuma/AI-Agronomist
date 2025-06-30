import pandas as pd
import io
import matplotlib.pyplot as plt
from services.google_drive import upload_image_to_drive
from services.gemini_interface import plot_summary, history_summary
import uuid
import json
import numpy as np


def createPlots(results, guides):
    results_df = pd.DataFrame(results)
    chemicals = results_df.columns[7:]
    output = []
    if len(results_df['Field Name']) > 0:
        for chemical in chemicals:
            chem_guides = [guide for guide in guides if guide['chemical_name'] == "ph"]
            plt.figure(figsize=(20, 16))
            plt.bar(results_df['Field Name'],results_df[chemical].astype(float) )
            plt.ylim(results_df[chemical].astype(float).min() - 0.2, results_df[chemical].astype(float).max() + 0.2)
            plt.gcf().set_size_inches(12, 6)
            plt.xticks(rotation=90)
           
            plt.tight_layout()
            plt.title(f"{chemical} Comparisons Across Different Fields")
            plt.ylabel(f"{chemical} Levels")
            plt.yticks([ i['class_upper_limit'] for i in chem_guides], [i['status_name'] for i in chem_guides])
            plt.axhline(y=[ i['class_upper_limit'] for i in chem_guides if i['status_name'] == "very low"][0], color='red', linestyle='--')
            plt.axhline(y=[ i['class_upper_limit'] for i in chem_guides if i['status_name'] == "very high"][0], color='blue', linestyle='--')
            plt.xlabel("Field Names")
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            image = buf.getvalue()
            buf.close()
            res = {}

            # res['image_url'] = upload_image_to_drive(image, str(uuid.uuid4())+".png")
            plt.savefig(f"{chemical}_plot.png", format='png')
            res['ai_summary'] = plot_summary(chemical, results=results_df[['Field Name', chemical]], guides=guides)
            output.append(res)
            return output

def plotHistory(history_dict, guides):
    data = history_dict

    df = pd.DataFrame(data)
    df['result'] = [ i.replace(">","").replace("<","").strip() for i in df['result']]
    df['result'] = df['result'].astype(float)
    df['batch_date'] = pd.to_datetime(df['batch_date'])

    pivot_df = df.pivot_table(
        index='batch_date',
        columns='chemical_name',
        values='result',
        aggfunc='mean' 
    ).fillna(0)

    chemicals = pivot_df.columns
    dates = pivot_df.index.strftime('%Y-%m-%d')
    x = np.arange(len(dates)) 
    bar_width = 0.1 
    fig, ax = plt.subplots(figsize=(14, 6))

    for i, chem in enumerate(chemicals):
        ax.bar(x + i * bar_width, pivot_df[chem], width=bar_width, label=chem)

    ax.set_xticks(x + bar_width * (len(chemicals) - 1) / 2)
    ax.set_xticklabels(dates, rotation=45)

    ax.set_xlabel("Batch Date")
    ax.set_ylabel("Chemical Result")
    ax.set_title("Grouped Chemical Results Over Time")
    ax.legend(title="Chemical", bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    # plt.show()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image = buf.getvalue()
    buf.close()
    res = {}

    # res['image_url'] = upload_image_to_drive(image, str(uuid.uuid4())+".png")
    plt.savefig("history_plot.png", format='png')
    res['ai_summary'] = history_summary(history=history_dict, guides=guides)

    return res
    

# def read_json_file(file_path):
#     with open(file_path, 'r') as f:
#         data = json.load(f)
#     return data

# json_path = "C://Users/tsuma.thomas/Documents/Cropnuts/DSML188/notebooks/test_report_input.json"
# json_data = read_json_file(json_path)
# results = json_data['results']
# guides = json_data['guides']
# createPlots(results, guides)