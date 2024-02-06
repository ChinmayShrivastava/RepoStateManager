import pandas as pd
import numpy as np
import networkx as nx
import logging
from modules.actions.graph import add_unique_node

class Dataframe2Graph:

    def __init__(
            self,
            df: pd.DataFrame,
            G: nx.Graph = nx.DiGraph(),
            table_name: str = None,
            verbose: bool = True,
            ):
        self.verbose = verbose
        self.df = df
        self.table_name = table_name if table_name is not None else "table"
        self.G = G
        self.root_node_uid = 0
        # len(rows) x len(columns) np array
        self.col_tracker = np.zeros((len(self.df.values), len(self.df.columns)))
        self.cell_uid_tracker = np.zeros((len(self.df.values), len(self.df.columns)))
        self.meta_rows = []
        self.meta_columns = []
        # print the shape of the col tracker
        if self.verbose:
            print(f"col_tracker shape: {self.col_tracker.shape}")
        # log
        if self.verbose:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)
        logging.info('Dataframe2Graph initialized.')

    @classmethod
    def from_camelot_extracted_table(cls, table: pd.DataFrame, table_name: str, G: nx.Graph = nx.DiGraph(), verbose: bool = True):
        """Creates a Dataframe2Graph object from a camelot extracted table.

        ----------
        Unlike img2table, camelot doesn't fill the empty dataframe cells
        TODO: this might or might not be a problem, but it's something to keep in mind
        ----------

        Args:
            table (pd.DataFrame): The camelot extracted table.
            G (nx.Graph, optional): The networkx Graph to add the table to. Defaults to nx.DiGraph().
            verbose (bool, optional): Whether to print verbose logs. Defaults to True.

        Returns:
            Dataframe2Graph: The Dataframe2Graph object.
        """
        return cls(df=table, G=G, verbose=verbose)
    
    @classmethod
    def from_img2table_extracted_table(cls, table: dict, table_name: str, G: nx.Graph = nx.DiGraph(), verbose: bool = True):
        """Creates a Dataframe2Graph object from an img2table extracted table.

        Args:
            table (dict): The img2table extracted table.
            G (nx.Graph, optional): The networkx Graph to add the table to. Defaults to nx.DiGraph().
            verbose (bool, optional): Whether to print verbose logs. Defaults to True.

        Returns:
            Dataframe2Graph: The Dataframe2Graph object.
        """
        return cls(df=table, table_name=table_name, G=G, verbose=verbose)

    def __str__(self) -> str:
        _str = f"Dataframe2Graph for {self.df}"
        return _str
    
    def _init_rows(self):
        self.rows = self.df.values.tolist()
        return self.rows
    
    def _init_columns(self):
        self.columns = self.df.columns.tolist()
        return self.columns
    
    def _init_root_node(self):
        self.G, self.root_node_uid = add_unique_node(G=self.G, node_value=self.table_name, node_type="table", col_no=len(self.columns), row_no=len(self.rows))
        return self.G
    
    def _break_subtables(self, row_index: int, rows: list[list[str]]) -> list[list]:
        """Breaks a row into subtables.

        Args:
            row_index (int): The index of the row to break.

        Returns:
            list[list]: A list of subtables.
        """
        subtables = []
        row = rows[row_index]
        next_subtable = []
        for index, cell in enumerate(row):
            if cell == "":
                if len(next_subtable) > 0:
                    next_subtable.append(index)
                else:
                    subtables.append(None)
            else:
                if len(next_subtable) > 0:
                    # subtables.append(next_subtable)
                    # next_subtable = []
                    for col in next_subtable:
                        subtables.append(next_subtable[0])
                    next_subtable = []
                next_subtable.append(index)
        if len(next_subtable) > 0:
            for col in next_subtable:
                subtables.append(next_subtable[0])
        logging.info(f"subtables: {subtables}")
        return subtables
    
    def _populate_col_tracker(self):
        """Populates the column tracker with the subtables of each row."""
        for row_index in range(len(self.rows)):
            subtables = self._break_subtables(row_index=row_index, rows=self.rows)
            # update the numpy array
            self.col_tracker[row_index] = subtables
        return self.col_tracker
    
    def _get_connection_chains_column(self) -> list[list[int]]:
        # use the col_tracker to get the lists of each column
        col_lists = []
        for col_index in range(self.col_tracker.shape[1]):
            col_list = self.col_tracker[:, col_index].tolist()
            col_lists.append(col_list)
        return col_lists
    
    # TODO: this might not be working properly, as the wrong nan thing is being added as a graph edge - check this (I worked on a fix, but it might not be working properly) - okay for now
    def _add_row_connections(self):
        # needs to be run only after the column chains have been added
        for row_no, row in enumerate(self.cell_uid_tracker):
            for col_no, cell_uid in enumerate(row):
                if not np.isnan(cell_uid):
                    # add an edge between the cell_uid and the next cell_uid in the row
                    # if the next cell_uid is not nan or the last cell_uid in the row
                    if col_no + 1 < len(row):
                        if not np.isnan(row[col_no + 1]):
                            self.G.add_edge(cell_uid, row[col_no + 1], type="row")
                else:
                    # if the cell_uid is nan, and the next cell_uid is not nan
                    if col_no + 1 < len(row):
                        if row_no == 0:
                            continue
                        if not np.isnan(row[col_no + 1]):
                            # in the column col_no up until the row_no, get the non-nan cell_uid
                            col_data = self.cell_uid_tracker[:row_no, col_no]
                            col_data = col_data[~np.isnan(col_data)]
                            if len(col_data) > 0:
                                # get the last cell_uid
                                last_uid = col_data[-1]
                                # add an edge between the last_uid and the next cell_uid
                                self.G.add_edge(last_uid, row[col_no + 1], type="row")
        return self.G

    def _update_graph(self):
        # get the column lists
        col_lists = self._get_connection_chains_column()
        for col_no, chain in enumerate(col_lists):
            last_uid = self.root_node_uid
            for row_no, item in enumerate(chain):
                if not np.isnan(item):
                    # add the node
                    self.G, node_uid = add_unique_node(G=self.G, node_type="cell", node_value=self.rows[row_no][col_no], col_no=col_no, row_no=row_no)
                    # update the cell_uid_tracker
                    self.cell_uid_tracker[row_no][col_no] = node_uid
                    # add the edge
                    self.G.add_edge(last_uid, node_uid, type="column")
                    # update the last_uid
                    last_uid = node_uid
                else:
                    # update the cell uid tracker to be nan
                    self.cell_uid_tracker[row_no][col_no] = np.nan
        # add the row connections
        self.G = self._add_row_connections()
        return self.G
    
    def _get_meta(self):
        # if a row in col_tracker contains nan, it is a meta row, but they should be in succession
        last_row = 0
        for row_no, row in enumerate(self.col_tracker):
            if np.isnan(row).any() or last_row == 0:
                if row_no - last_row == 1 or last_row == 0:
                    self.meta_rows.append(row_no)
                    last_row = row_no
        # if a column in col_tracker contains nan, it is a meta column
        # first create a copy of the col tracker and remove the meta rows
        # new np array with the meta rows removed
        new_array = np.array([row for row_no, row in enumerate(self.col_tracker) if row_no not in self.meta_rows])
        last_col = 0
        for col_no, col in enumerate(new_array.T):
            if np.isnan(col).any():
                self.meta_columns.append(col_no)
                last_col = col_no
        # add the last_col + 1 as a meta column
        self.meta_columns.append(last_col + 1)
        return self.meta_rows, self.meta_columns
    
    def get_graph(self):
        self._init_rows()
        self._init_columns()
        self._init_root_node()
        self._populate_col_tracker()
        self._update_graph()
        self._get_meta()
        return
    
    # visualize the graph with node_value as the label
    def visualize(self):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos=pos, with_labels=True, node_size=500, font_size=10)
        plt.show()

    def __call__(self):
        self.get_graph()
        return self.G