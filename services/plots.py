import pandas as pd
import io
import matplotlib.pyplot as plt
from services.google_drive import upload_image_to_drive
from services.gemini_interface import plot_summary
import uuid
import json
def createPlots(results, guides):
    results_df = pd.DataFrame(results)
    chemicals = results_df.columns[7:]
    output = []
    if len(results_df['Field Name']) > 0:
        for chemical in chemicals:
            plt.bar(results_df['Field Name'],results_df[chemical].astype(float) )
            plt.ylim(results_df[chemical].astype(float).min() - 0.2, results_df[chemical].astype(float).max() + 0.2)
            plt.gcf().set_size_inches(12, 6)
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.title(f"{chemical} Comparisons Across Different Fields")
            plt.ylabel(f"{chemical} Levels")
            plt.xlabel("Field Names")
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            image = buf.getvalue()
            buf.close()
            res = {}

            res['image_url'] = upload_image_to_drive(image, str(uuid.uuid4())+".png")
            res['ai_summary'] = plot_summary(chemical, results=results_df[['Field Name', chemical]], guides=guides)
            output.append(res)
    return output

    

# def read_json_file(file_path):
#     with open(file_path, 'r') as f:
#         data = json.load(f)
#     return data

# json_path = "C://Users/tsuma.thomas/Documents/Cropnuts/DSML188/notebooks/test_report_input.json"
# json_data = read_json_file(json_path)
# results = json_data['results']
# guides = json_data['guides']
# createPlots(results, guides)