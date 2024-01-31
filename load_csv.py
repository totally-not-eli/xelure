from utils.general_utils import *
from utils.csv_helper import *
from utils.sql_utils import *
from main import logger

from models import *

general_utils = GeneralUtils()
database = Database()

all_csv_data = general_utils.find_files_by_extension("csv")
csv_path = all_csv_data[0]
transformed_df = general_utils.read_csv_and_transform(csv_path)
transformed_df["id"] = transformed_df.index + 1
transformed_df = general_utils.convert_string_dates_to_datetime(transformed_df)
transformed_df = general_utils.convert_to_boolean(transformed_df)


with Session(database.engine) as session:
    csv_helper = HelperCSV(csv_path, LoanData, session)

    csv_helper.seed_data_from_csv(transformed_df.to_dict(orient="records"))