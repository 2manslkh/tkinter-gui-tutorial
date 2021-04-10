from tkinter import (
    Button,
    Label,
    Frame,
    Entry,
    LabelFrame,
    StringVar,
    messagebox,
    scrolledtext,
    ttk,
    Listbox,
)


class Ladder(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.root = parent
        # self.list = []
        # self.selected_item = None
        # self.selected_name = StringVar()
        # self.win_content_info = None
        # self.win_content_edit = None
        self.init_page()

    def init_page(self):

        # Tree View
        self.tree_view = ttk.Treeview(self, show="headings", height=600)

        # Column Names
        self.tree_view["columns"] = ("#", "Name")

        self.tree_view.column("#", width=25)
        self.tree_view.column("Name", width=175)

        self.tree_view.heading("#", text="#")
        self.tree_view.heading("Name", text="Name")

        # # 选中行
        # self.tree_view.bind("<<TreeviewSelect>>", self.select)

        # 排序
        # for col in self.tree_view["columns"]:  # 给所有标题加
        #     self.tree_view.heading(
        #         col,
        #         text=col,
        #         command=lambda _col=col: treeview_sort_column(
        #             self.tree_view, _col, False
        #         ),
        #     )

        vbar = ttk.Scrollbar(self, orient="vertical", command=self.tree_view.yview)
        self.tree_view.configure(yscrollcommand=vbar.set)
        self.tree_view.grid(row=1, column=0, sticky="nsew")
        vbar.grid(row=1, column=1, sticky="ns")

        # Display ladder data into tree view

    def loadLadderData(self, ladder_data):
        for pos, name in enumerate(ladder_data):
            self.tree_view.insert(
                "",
                "end",
                text="",
                values=(pos + 1, name),
            )
