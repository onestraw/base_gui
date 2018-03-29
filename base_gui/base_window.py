#!/usr/bin/python
# -*- coding: utf-8 -*-


import random
import traceback
import multiprocessing
import Tkinter
import tkFileDialog


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


class BaseWindow(object):

    align_center = Tkinter.EW
    align_EWN = Tkinter.EW + Tkinter.N
    align_right = Tkinter.E

    ROW_TYPE = ['FILE', 'TEXT']
    DEFAULT_RESULT_LABEL = 'unperformed'
    EXEC_LABEL = 'start'
    CLOSE_LABEL = 'close'
    row_pad = 16
    col_pad = 10
    main_bg_color = Color.BLUE
    btn_bgc, btn_fgc = Color.random_bg_fg_pair()

    row_items = {}

    def __init__(self, cfg):
        self.master = Tkinter.Tk()
        self.load_config(cfg)
        self.register_callback()
        self.init_ui()

        self.queue = multiprocessing.Queue()
        self.worker = None
        self.worker_args = ()
        self.query_delay = 50
        multiprocessing.freeze_support()

    def run(self):
        self.master.mainloop()

    def load_config(self, cfg):
        """
            cfg is instance of Config
        """
        self.title = cfg.title
        self.row_config = cfg.input_row['row']
        self.row_num = cfg.input_row['count']

    def init_ui(self):
        master = self.master
        master.title(self.title)
        pos = (300, 200)
        master.geometry('+%d+%d' % (pos))
        master.resizable(0, 0)
        master.config(background=self.main_bg_color)

        master.columnconfigure(0, pad=self.col_pad, minsize=100)
        master.columnconfigure(1, pad=self.col_pad, minsize=200)
        master.columnconfigure(2, pad=self.col_pad, minsize=100)

        for i in range(self.row_num + 1):
            master.rowconfigure(i, pad=self.row_pad)

        for i in range(self.row_num):
            cfg = self.row_config[i]
            self.row_items[i] = self.create_row(i,
                                                cfg['type'],
                                                cfg['label'],
                                                cfg['last_label'],
                                                cfg.get('callback'))

        # last row
        last_row_idx = self.row_num
        self.close_btn = Tkinter.Button(master,
                                        text=self.CLOSE_LABEL,
                                        command=master.quit,
                                        highlightbackground=self.main_bg_color)
        self.close_btn.grid(row=last_row_idx, column=0, sticky=self.align_EWN)

        self.exec_btn = Tkinter.Button(master,
                                       text=self.EXEC_LABEL,
                                       command=self.execute,
                                       highlightbackground=self.main_bg_color)
        self.exec_btn.grid(row=last_row_idx, column=1, sticky=self.align_EWN)

        bgc, fgc = Color.random_bg_fg_pair()
        self.result_lbl = Tkinter.Label(self.master,
                                        text=self.DEFAULT_RESULT_LABEL,
                                        background=bgc,
                                        foreground=fgc)
        self.result_lbl.grid(row=last_row_idx, column=2, sticky=self.align_EWN)

    def create_row(self, row_idx, row_type, input_label, last_label, callback):
        """
            input_label  input_box  button/label [by row_type]

            FILE type row must have callback
            TEXT type row does not need callback
        """
        bgc, fgc = Color.random_bg_fg_pair()

        lbl = Tkinter.Label(self.master,
                            text=input_label,
                            background=bgc,
                            foreground=fgc)
        lbl.grid(row=row_idx, column=0, sticky=self.align_right, padx=3)

        input_box = Tkinter.Entry(self.master, borderwidth='0')
        input_box.grid(row=row_idx, column=1, sticky=self.align_center)

        if row_type == 'FILE':
            item = Tkinter.Button(self.master,
                                  text=last_label,
                                  command=callback,
                                  background=self.btn_bgc,
                                  foreground=self.btn_fgc,
                                  highlightbackground=self.main_bg_color)
        elif row_type == 'TEXT':
            item = Tkinter.Label(self.master,
                                 text=last_label,
                                 background=bgc,
                                 foreground=fgc)
        else:
            raise Exception('unsupported row type')

        item.grid(row=row_idx, column=2, sticky=self.align_center)

        return [lbl, input_box, item]

    def on_open_file(self):
        """
            override the method if you want to set default filetype
        """
        return tkFileDialog.askopenfilename(
            filetypes=[('default', '*.txt'), ('All files', '*.*')])

    def on_open_directory(self):
        return tkFileDialog.askdirectory()

    def get_row_input_text(self, row_idx):
        """
            return the input_box data of row_idx
        """
        return self.row_items[row_idx][1].get()

    def set_row_input_text(self, row_idx, data):
        """
            set the input_box data of row_idx
        """
        input_box = self.row_items[row_idx][1]
        input_box.delete(0, 'end')
        input_box.insert(Tkinter.END, data)

    def set_row_callback(self, row_idx, callback):
        """
            register callback for button of row_idx
        """
        self.row_config[row_idx]['callback'] = callback

    def update_result(self, msg):
        """
            show processing status in result label
        """
        self.result_lbl.config(text=msg)

    def execute(self):
        """
            execute button action
            read data from self.row_items, check inputs,
            process it, show status in result_lbl
        """
        ok, msg = self.check_inputs()
        if not ok:
            self.update_result(msg)
        else:
            self.register_worker()
            try:
                self.exec_btn.config(state=Tkinter.DISABLED)
                self.p = multiprocessing.Process(
                     target=self.worker, args=self.worker_args)
                self.p.start()
                self.master.after(self.query_delay, self.on_get_result)
            except Exception:
                traceback.print_exc()

    def on_get_result(self):
        """
            check if the process is done
        """
        if not self.queue.empty():
            self.update_result(self.queue.get(0))
        if self.p.is_alive():
            self.master.after(self.query_delay, self.on_get_result)
            return
        else:
            self.exec_btn.config(state=Tkinter.NORMAL)

    def check_inputs(self):
        """
            check all input_box
            the return value is: True/Flase, message
        """
        for i in range(self.row_num):
            text = self.get_row_input_text(i)
            if not text.strip():
                return False, '{} is null'.format(self.row_config[i]['label'])
        return True, 'pass'

    def register_worker(self):
        """
            user should define one worker() to do all the work
            the first argument of worker is self.queue,
            which used to transmit task status, such as

            def f(queue, p1, p2):
                pass

            def register_worker(self):
                self.worker = f
                self.worker_args = (self.queue, p1, p2)
        """
        raise Exception('not implemented')

    def register_callback(self):
        """
            register callback for each data row, it's called before create_row
            currently only FILE type row need callback function,
            put the cb into self.row_config[]

            such as row2 = self.row_config[2], row2 items can be accessed from
            [lbl, input_box, item] = self.row_items[2]
            you can use the row_item in implementation of row2['callback']
        """
        raise Exception('not implemented')
