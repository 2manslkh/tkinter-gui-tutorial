# from tkinter import Toplevel, Label, Message, Tk
# from components import frames
# from pages.StartPage import Start
# import utils


# class Base(Tk):
#     """主界面"""

#     def __init__(self, master=None):

#         self.root = master
#         utils.set_window_center(self.root, 800, 600)
#         # StartPage(self.root)

#         self.current_frame = None
#         self.page_frame = {
#             "start": StartPage
#         }
#         self.open_start()
#         self.win_about = None

#     def open_page(self, frame_name, title):
#         """Open any page"""
#         self.root.title(title)

#         if self.current_frame is not None and (hasattr(self.current_frame.destroy, '__call__')):
#             self.current_frame.destroy()

#         self.current_frame = self.page_frame[frame_name](self.root)
#         self.current_frame.pack()

#     def open_start(self):
#         """Open Start Page"""
#         self.open_page("start", "Start")
