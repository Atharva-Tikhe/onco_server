import papermill as pm
import os
from subprocess import Popen
# print(pm.inspect_notebook(r'ML\Untitled.ipynb'))


def run_regression(input_file: str, target: str) -> None:

    pm.execute_notebook(rf'ML\Regression.ipynb',
                        r'ML\Regression_output.ipynb',
                        parameters=dict(file=rf'{input_file}', target='info'))

    conversion_cmd = "jupyter nbconvert --TemplateExporter.exclude_input=True --to html ML\\Regression_output.ipynb "

    process = Popen(conversion_cmd, shell=True)

    process.wait()

    print('execution and conversion complete...')

    move_cmd = r"copy E:\MIT\OncoOmics_portal\ML\Regression_output.html E:\MIT\OncoOmics_portal\templates"

    process = Popen(move_cmd, shell=True)
    process.wait()
    print('template moved...')


def run_classification(input_file: str, target: str) -> None:
    pm.execute_notebook(rf'ML\Classification.ipynb',
                        r'ML\Classification_output.ipynb',
                        parameters=dict(file=rf'{input_file}', target='info'))

    conversion_cmd = "jupyter nbconvert --TemplateExporter.exclude_input=True --to html ML\\Classification_output.ipynb"

    process = Popen(conversion_cmd, shell=True)

    process.wait()

    print('execution and conversion complete...')

    move_cmd = r"copy E:\MIT\OncoOmics_portal\ML\Classification_output.html E:\MIT\OncoOmics_portal\templates"

    process = Popen(move_cmd, shell=True)
    process.wait()
    print('template moved...')
