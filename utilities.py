from json import JSONEncoder
from enum import Enum
import pydot

import datetime

class TimeEpochUnit(Enum):
    SECONDS=0
    MILLISECONDS=1
    MICROSECONDS=2
    NANOSECONDS=3

class TimeEpochFormat(Enum):
    UNIX_EPOCH=0
    ISO_8601_EPOCH=1

class HistoryEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


'''
Converts given date into POSIX timestamp in seconds, or into Win32 (LDAP) format
'''
def date_to_epoch(date_string: str, time_epoch_format: TimeEpochFormat) -> int:
    epoch = 0

    if (date_string == 'none'):
        return epoch;

    if (time_epoch_format == TimeEpochFormat.UNIX_EPOCH):
        epoch = int(datetime.datetime.strptime(date_string, "%Y-%m-%d").timestamp())
    elif (time_epoch_format == TimeEpochFormat.ISO_8601_EPOCH):
        unix_epoch_microsecs_frac = int(datetime.datetime.strptime(date_string, "%Y-%m-%d").timestamp()) * 1000 * 1000 * 10 # Unix time epoch expressed in 0,1 microsec precision
        base_unix_timestamp_as_ldap = 116444736000000000 # ...
        epoch = int((base_unix_timestamp_as_ldap + unix_epoch_microsecs_frac))
    return epoch

'''
Creates a WHERE search clause which filters out entries based on certain date column.
'''
def form_date_filter_query(visit_time_columnn_name: str, start_timestamp: int, end_timestamp: int, time_epoch_unit: TimeEpochUnit) -> str:
    where_filter = ""

    # Chromium stores timestamps as microseconds, while proper conversion to LDAP (or Win32, whatever) format is 10x from that.
    check_start_timestamp = start_timestamp / 10 #* 1000 ** time_epoch_unit.value
    check_end_timestamp = end_timestamp / 10 #* 1000 ** time_epoch_unit.value

    if (check_start_timestamp != 0):
        where_filter = " WHERE {} >= {}".format(visit_time_columnn_name, str(check_start_timestamp))

    if (check_end_timestamp != 0):
        if (where_filter != ""):
            where_filter += " AND {} <= {}".format(visit_time_columnn_name, str(check_end_timestamp))
        else:
            where_filter = " WHERE {} <= {}".format(visit_time_columnn_name, str(check_end_timestamp))
    
    return where_filter

# Render the dependency tree based on given array of nodes, sorted by the dependency between nodes
# node 0 is the root, node 1 depends on node 0 etc.
def plot_node_dependencies(nodes: [], path: str):
    stringified_graph = ""
    dot_string = "graph link_dependency_tree {\n"
    i = 0
    for node in nodes[::-1]:
        if (i != 0):
            stringified_graph += " -> \"{}\"".format(node)
        else:
            stringified_graph += "\"{}\"".format(node)
        i += 1
    dot_string += stringified_graph + "\n}"
    graphs = pydot.graph_from_dot_data(dot_string)
    graphs[0].write_png(path + ".png")