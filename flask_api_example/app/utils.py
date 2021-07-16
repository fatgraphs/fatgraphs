import pandas as pd

def to_pd_frame(raw_result):
    """
    :param raw_result: the object returned from executing a raw query with sqlAlchemy
    :return: a pandas frame where the column names are the DB column names and the rows are DB records
    """
    df = pd.DataFrame(raw_result.fetchall())
    if df.empty:
        return df
    df.columns = raw_result.keys()
    return df



def wkt_to_x_y_list(wkt):
    """

    :param wkt: well known text representation of a 2D POINT (a point in GIS).
            e.g. POINT(34234 42)
    :return: a python list where the first element is the x and the second is the y
    """
    p = wkt.split('(')[-1].split(')')[0].split(' ')
    return [float(p[0]), float(p[1])]