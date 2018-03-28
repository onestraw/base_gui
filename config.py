#!/usr/bin/python
# -*- coding: utf-8 -*-

TITLE = u'small tool'


"""layout:
        label   input   button
        label   input   button
        label   input   button
default [close  exec    status]
"""
INPUT_ROW = {
    'count': 3,
    'row': [
        {'label': 'input I', 'last_label': 'select file', 'type': 'FILE'},
        {'label': 'input II', 'last_label': 'select file', 'type': 'FILE'},
        {'label': 'output path', 'last_label': 'select dir', 'type': 'FILE'},
    ]
}
