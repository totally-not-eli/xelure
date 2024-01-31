from flask import Flask

import tabula
import pandas as pd

from models import *

from utils.general_utils import *
from utils.sql_utils import *

app = Flask(__name__)

general_utils = GeneralUtils()
db = Database()
logger = LogUtils().get_logger("flask-application")

@app.route("/scrape-and-check", methods=["POST"])
def get_data_and_check():
    all_pdf_data = general_utils.find_files_by_extension("pdf")
    
    if all_pdf_data:
        data_path = all_pdf_data[0]
        
        pdf_tables = tabula.read_pdf(data_path, pages='all', multiple_tables=True)
        
        for df in pdf_tables:
            search_label = "Total Principal Funds Available:"
            label_df = general_utils.find_row_with_label(df, search_label)
            total_principal = 0
            if label_df is not None:
                total_value = general_utils.get_value_from_label_df(label_df)
                if total_value:
                    total_value = float(total_value.replace(',',''))
                    query = db.query_table(LoanData)
                    df = pd.DataFrame(query)
                    total_principal = total_principal + df.select_dtypes(include='number').sum(axis=0).sum()
        
                    if total_value == total_principal:
                        return "Success, they're matched.", 200
                    
                    return "Principal are not matching", 200
                    
    return "Something went wrong.", 500

    
if __name__ == "__main__":
    app.run(debug=True)