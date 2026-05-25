import sys
import api_client
import parser
import visualizer_py
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def run_notebook(notebook_path):
    """Executes a Jupyter notebook from start to finish."""
    print(f"Executing notebook: {notebook_path}")
    
    # 1. Load the notebook file
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # 2. Set up the execution processor
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    
    # 3. Run the notebook code
    ep.preprocess(nb, {'metadata': {'path': './'}})
    
    # 4. Save the notebook back to disk so you can see the generated charts later
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)


def run_pipeline():
    print('====== Starting Automation ======')

    try:
        # 1. Run the api_client.py to get city lon and lat
        api_client.get_city_lan_lat()

        # 2. Run the parser.py to get the raw_city_temp and save it to a csv
        parser.get_raw_data()

        # 3. Run the visuzlier notebook to get the graphs
        visualizer_py.run_analysis()

    except Exception as e:
        print(f"❌ Pipeline failed due to error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    run_pipeline()