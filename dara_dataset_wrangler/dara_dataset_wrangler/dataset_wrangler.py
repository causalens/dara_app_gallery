import io
import os
from typing import List

import pandas

from dara.core import DataVariable, UpdateVariable, Variable, DownloadContent, py_component
from dara.core.definitions import ComponentInstance
from dara.components import Stack, Table, Item, Spacer, Button, Text, Select, Heading, Card, UploadDropzone, DataSlicerModal

from dara_dataset_wrangler.plotting_utils import plot_column

# TODO this is empty dataframe for now but should be none
upload_data = DataVariable(pandas.DataFrame({}))

slicer_modal = DataSlicerModal(upload_data)
filtered_data = slicer_modal.get_output()

DATA_ROOT = os.environ.get('DATA_ROOT', './data')


def data_resolver(content: bytes, name: str) -> pandas.DataFrame:
    """Handle uploaded csv file"""
    file_object_csv = io.StringIO(content.decode('utf-8'))
    df = pandas.read_csv(file_object_csv, index_col=0)
    return df


def display_table(dataset: pandas.DataFrame) -> ComponentInstance:
    columns = list(dataset.columns)
    data_var = DataVariable(dataset)

    return Stack(
        Table(columns=columns, data=data_var),
        slicer_modal(),
    )


def get_columns(data: pandas.DataFrame) -> List[Item]:
    """A utility function to get dataset column names."""
    return [Item.to_item(symbol) for symbol in data.columns]


def path_resolver(ctx) -> str:
    data = ctx.extras[0]

    if data is None:
        raise Exception('Dataset does not exist')

    clean_name, _ext = os.path.splitext('filtered_data')

    # Write the dataset as a .csv temporarily, will be cleaned up after download
    csv_path = os.path.join(DATA_ROOT, clean_name + '.csv')

    data.to_csv(csv_path)
    return csv_path


def use_default_data(ctx) -> pandas.DataFrame:
    df = pandas.read_csv(os.path.join(DATA_ROOT, '401k.csv'), index_col=0)
    return df


def data_upload() -> ComponentInstance:
    return Stack(
        Heading("Upload data", level=3),
        Card(
            Stack(
                UploadDropzone(target=upload_data, resolver=data_resolver, height='170px', width='600px'),
                Button(
                    "Use Sample Dataset",
                    onclick=UpdateVariable(resolver=use_default_data, variable=upload_data),
                    styling='ghost'
                ),
                align='center',
                justify='center',
            )
        )
    )


@py_component
def visualize_data(data: pandas.DataFrame) -> ComponentInstance:
    if data is None or data.empty is True:
        return Stack(
                Text('Please upload data to visualize and download data.', bold=True, align='center'),
        )

    column_var = Variable()
    data_var = DataVariable(data)
    columns_var = get_columns(data)

    return Stack(
        Heading("Visualize & download data", level=3),
        Card(
            Stack(
                display_table(data),
                Stack(
                    Stack(
                        Text('Select column to plot:', width='20%'),
                        Select(value=column_var, items=columns_var),
                        direction='horizontal',
                        hug=True
                    ),
                    Stack(plot_column(data_var, column_var))
                ),
            ),
            Stack(
                Button(
                    'Download Data',
                    onclick=DownloadContent(resolver=path_resolver, extras=[filtered_data], cleanup_file=True),
                    width='20%',
                ),
                align='center',
                hug=True
            )
        ),
    )


def dataset_wrangler_page() -> ComponentInstance:
    return Stack(
        Stack(data_upload(), height='45%'),
        Stack(visualize_data(filtered_data), height='100%'),
    )
