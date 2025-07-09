import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
from services.google_drive import upload_image_to_drive
from services.dropbox import upload_image_to_dropbox
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

            res['image_url'] = upload_image_to_dropbox(image_stream=image, image_name=str(uuid.uuid4())+".png")
            # plt.savefig(f"{chemical}_plot.png", format='png')
            res['ai_summary'] = plot_summary(chemical, results=results_df[['Field Name', chemical]], guides=guides)
            output.append(res)
            return output

def plotHistory(history_dict, guides):
    data = history_dict
    chemicals = [ i['chemical_name'] for i in history_dict ]
    data = history_dict 
    df = pd.DataFrame(data)
    df['result'] = [ i.replace(">","").replace("<","").strip() for i in df['result']]
    df['result'] = df['result'].astype(float)
    df['batch_date'] = pd.to_datetime(df['batch_date'])

    df = df.sort_values('batch_date')

    chemicals = df['chemical_name'].unique()
    output = []
    for chem in chemicals:
        chem_guides = [guide for guide in guides if guide['chemical_name'] == "ph"]
        subset = df[df['chemical_name'] == chem]

        # Pivot: index = batch_date, columns = field_name, values = result
        pivot_df = subset.pivot_table(
            index='batch_date',
            columns='field_name',
            values='result'
        ).fillna(0)

        # Plotting setup
        fields = pivot_df.columns
        x = np.arange(len(pivot_df))  # positions for each date
        width = 0.8 / len(fields)     # dynamic width based on number of fields

        fig, ax = plt.subplots(figsize=(12, 5))
        
        for i, field in enumerate(fields):
            ax.bar(x + i*width, pivot_df[field], width=width, label=field)

        ax.set_xticks(x + width * (len(fields) - 1) / 2)
        ax.set_xticklabels(pivot_df.index.strftime('%Y-%m-%d'), rotation=45)
        ax.set_title(f'{chem} Levels Across Fields Over Time')
        ax.set_xlabel('Batch Date')
        ax.set_ylabel('Result')
        plt.yticks([ i['class_upper_limit'] for i in chem_guides], [i['status_name'] for i in chem_guides])
        plt.axhline(y=[ i['class_upper_limit'] for i in chem_guides if i['status_name'] == "very low"][0], color='red', linestyle='--')
        plt.axhline(y=[ i['class_upper_limit'] for i in chem_guides if i['status_name'] == "very high"][0], color='blue', linestyle='--')
        ax.legend(title='Field Name', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        # plt.show()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        image = buf.getvalue()
        buf.close()
        res = {}

        res['image_url'] = upload_image_to_dropbox(image_stream=image, image_name=str(uuid.uuid4())+".png")
        # plt.savefig(f"{chem}_plot.png", format='png')
        res['ai_summary'] = history_summary(history=history_dict, guides=guides)
        output.append(res)
        return output
    
def plotRecommendations(recommendations_dict):
    recommends_df = pd.DataFrame(recommendations_dict)
    numeric_cols = []
    for col in recommends_df.columns:
        try:
            pd.to_numeric(recommends_df[col], errors='raise')
            numeric_cols.append(col)
        except Exception:
            continue

    numeric_cols

    numeric_cols.append("Field")
    recommends_df = recommends_df[numeric_cols].replace("",np.nan).dropna(axis=1, how='all')

    # Convert to DataFrame
    df = recommends_df.copy(deep=True)

    # Melt the dataframe to long format
    df_melted = df.melt(id_vars="Field", var_name="Input Type", value_name="Input Amount")

    # Drop NaNs
    df_melted.dropna(subset=["Input Amount"], inplace=True)

    # Plot grouped bar chart
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_melted, x="Field", y="Input Amount", hue="Input Type")

    plt.title("Input Amount per Field (Grouped by Input Type)")
    plt.xlabel("Field")
    plt.ylabel("Amount (Kg/Ha)")
    plt.legend(title="Input Type", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.xticks(rotation=90)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image = buf.getvalue()
    buf.close()
    res = {}

    res['image_url'] = upload_image_to_dropbox(image_stream=image, image_name=str(uuid.uuid4())+".png")
    # plt.savefig(f"{chemical}_plot.png", format='png')
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