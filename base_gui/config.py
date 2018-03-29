#!/usr/bin/python
# -*- coding: utf-8 -*-


class Config(object):
    """
        Configurations for BaseWindow
        layout:
                label   input   button
                label   input   button
        default [close  exec    status]
    """

    _title = 'small tool'
    _input_row = {
        'count': 2,
        'row': [
            {'label': 'input I', 'last_label': 'select file', 'type': 'FILE'},
            {'label': 'output I', 'last_label': 'select dir', 'type': 'FILE'},
        ]
    }

    def __init__(self, title, data_row):
        self.title = title
        self.input_row = data_row

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError('title should not be null/None')
        if not isinstance(value, str):
            raise ValueError('title should be a string')

        self._title = value

    @property
    def input_row(self):
        return self._input_row

    @input_row.setter
    def input_row(self, value):
        if not isinstance(value, dict):
            raise ValueError('input_row should be a dict')
        for k in self._input_row.keys():
            if k not in value:
                raise ValueError('input_row should contain {}'.format(k))
        if len(value['row']) != value['count']:
            raise ValueError('row count should be the length of data_row list')

        data_row_keys = self._input_row['row'][0].keys()
        for row in value['row']:
            for k in data_row_keys:
                if k not in row:
                    raise ValueError('{} should contain {}'.format(row, k))

        self._input_row = value
