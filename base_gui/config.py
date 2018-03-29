#!/usr/bin/python
# -*- coding: utf-8 -*-


import random


class Color(object):

    BLUE = '#8A2BE2'

    @classmethod
    def random_bg_fg_pair(cls):
        """
            generate random color pair (background, foreground)
        """
        ct = [random.randrange(256) for x in range(3)]
        brightness = int(round(0.299 * ct[0] + 0.587 * ct[1] + 0.114 * ct[2]))
        ct_hex = '%02x%02x%02x' % tuple(ct)
        bg_colour = '#' + "".join(ct_hex)
        fg_colour = 'White' if brightness < 120 else 'Black'
        return (bg_colour, fg_colour)


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

    # default configurations
    BTN_BGC, BTN_FGC = Color.random_bg_fg_pair()
    BACKGROUND_COLOR = Color.BLUE
    STATUS_LABEL = 'unperformed'
    EXEC_LABEL = 'start'
    CLOSE_LABEL = 'close'
    ROW_PAD = 16
    COL_PAD = 10
    POSITION = (300, 200)
    ROW_TYPE = ['FILE', 'TEXT']

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
            if row['type'] not in self.ROW_TYPE:
                raise ValueError('not supported type: {} '.format(row['type']))

        self._input_row = value
