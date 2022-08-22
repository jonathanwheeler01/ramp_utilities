from zipfile import ZipFile
import pandas as pd
import re
from urllib.parse import urlparse


def extract_subset_ramp_data(zip_file, ir_repo_id):
    """This function tries to conserve memory by opening zipped RAMP monthly data
       files one at a time and subsetting the data to a single repository's data
       for that month, prior to further processing or aggregation.

    Parameters
    ----------

    zip_file:
        String. A file path pointing to a zip file.

    ir_repo_id:
        String. A locally unique repository identifier which will be used to
        subset the unzipped data.

    Returns
    -------

    ir_data:
        A Pandas dataframe. The subset of RAMP data for the specified repository and month.

    """
    with ZipFile(zip_file) as rampzip:
        with rampzip.open(rampzip.namelist()[0]) as rampfile:
            ramp_df = pd.read_csv(rampfile)
    ir_data = ramp_df[ramp_df["repository_id"] == ir_repo_id].copy()
    return ir_data


def make_dspace_item_uri(bitstream_url):
    p = urlparse(bitstream_url)
    handle = re.compile("\/[0-9\?\.]+\/[0-9][0-9]+\/*")
    h = handle.search(p.path)
    if h:
        return h.group()


def make_bepress_item_uri(pdf_url):
    p = urlparse(pdf_url)
    base_url = 'oai:' + p.netloc + ':'
    contextRe = re.compile(r'context=([a-z0-9_\-]*)')
    articleRe = re.compile(r'article=([0-9][0-9][0-9][0-9])')
    contextSearch = contextRe.search(pdf_url)
    articleSearch = articleRe.search(pdf_url)
    if contextSearch:
        if articleSearch:
            context = contextSearch.group().replace('context=', '')
            article = articleSearch.group().replace('article=', '')
            return base_url + str(context) + '-' + str(article)


def construct_item_uids(ir_data, platform):
    if platform == 'dspace':
        ir_data['unique_item_uri'] = ir_data['url'].apply(make_dspace_item_uri)
    if platform == 'digitalcommons':
        ir_data['unique_item_uri'] = ir_data['url'].apply(make_bepress_item_uri)
    return ir_data