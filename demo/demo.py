#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import base_gui


class CustomWindow(base_gui.BaseWindow):

    def choose_file_1(self):
        file1 = self.on_open_file()
        self.set_row_input_text(0, file1)

    def choose_file_2(self):
        file2 = self.on_open_file()
        self.set_row_input_text(1, file2)

    def choose_path(self):
        path = self.on_open_directory()
        self.set_row_input_text(2, path)

    def register_callback(self):
        self.set_row_callback(0, self.choose_file_1)
        self.set_row_callback(1, self.choose_file_2)
        self.set_row_callback(2, self.choose_path)

    def register_worker(self):
        f1 = self.get_row_input_text(0)
        f2 = self.get_row_input_text(1)
        output_path = self.get_row_input_text(2)

        self.worker = worker
        self.worker_args = (self.queue, f1, f2, output_path)


def worker(queue, f1, f2, output_path):
    print f1, f2, output_path

    queue.put('converting phase...')
    time.sleep(1)
    queue.put('processing phase...')
    time.sleep(3)
    queue.put('merging phase...')
    time.sleep(5)
    queue.put('success')


if __name__ == '__main__':
    TITLE = 'small tool'
    INPUT_ROW = {
        'count': 3,
        'row': [
            {'label': 'input I', 'last_label': 'select file', 'type': 'FILE'},
            {'label': 'input II', 'last_label': 'select file', 'type': 'FILE'},
            {'label': 'output path', 'last_label': 'select dir', 'type': 'FILE'},
        ]
    }
    cfg = base_gui.Config(TITLE, INPUT_ROW)
    app = CustomWindow(cfg)
    app.run()
