# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 10:43:30 2022

@author: jwheel01
"""

import pandas as pd
import sqlite3
import numpy as np

def select_ir(c, p):
    con = sqlite3.connect('../metadata_database/repository_database.db')
    cur = con.cursor()
    res = cur.execute('SELECT repository_id, oairoot FROM repositories WHERE ' + c + ' = "' + p + '"')
    res_list = []
    for r in res.fetchall():
        res_list.append(r)
    res_df = pd.DataFrame(res_list, columns=['repository_id', 'oairoot'])
    return res_df


def get_meta(oairoot):
    con = sqlite3.connect('../metadata_database/repository_database.db')
    cur = con.cursor()
    res = cur.execute("SELECT * FROM records WHERE id LIKE '%" + oairoot + "%'")
    res_list = []
    for r in res.fetchall():
        res_list.append(r)
    res_df = pd.DataFrame(res_list, columns=['id', 'namespace', 'tag', 'value'])
    return res_df


def uid_lookup(oaipmh_id):
    con = sqlite3.connect('../metadata_database/repository_database.db')
    cur = con.cursor()
    res = cur.execute("SELECT unique_item_uri FROM uidlookup WHERE id=:oaipmh_id", {'oaipmh_id': oaipmh_id})
    uid = res.fetchone()[0]
    return uid


def get_ramp(repo_id):
    con = sqlite3.connect('../metadata_database/repository_database.db')
    cur = con.cursor()
    res = cur.execute('SELECT date, citablecontent, clicks, unique_item_uri FROM rampraw WHERE repository_id= :ir_identifier', {'ir_identifier': repo_id})
    res_list = []
    for r in res.fetchall():
        res_list.append(r)
    res_df = pd.DataFrame(res_list, columns=['date', 'citablecontent', 'clicks', 'unique_item_uri'])
    return res_df


dspace_ir = pd.read_csv('../supplementary_data/dspace_ir_w_qdc.csv')
ir_list = []
for i, r in dspace_ir.iterrows():
    ir = r['repository_id']
    ir_list.append(ir)
    

plt_dir = '../figures/'
df_dir = '../results/'

output_cols = ['ir', 'count_oaipmh_records', 'all_oaipmh_datestamp',
               'item_datestamp_ratio', 'count_all_ramp_uris', 
               'count_ancillary_ramp_uris', 'count_ramp_items_uris',
               'count_ramp_cc_uris', 'count_ramp_non_cc_uris',
               'item_ramp_ratio', 'ancillary_ramp_ratio', 
               'cc_meta_ratio', 'cc_ramp_ratio', 'cc_ramp_item_ratio',
               'non_cc_meta_ratio', 'non_cc_ramp_ratio', 
               'non_cc_ramp_item_ratio', 'cc_ratio', 'cc_occur_only',
               'non_cc_ratio', 'non_cc_only']

output_df = pd.DataFrame(columns=output_cols)

for ir in sorted(ir_list[:2]):
    try:
        print('\n' + ir)
        # get the repo_id and oaipmh root url
        ir_data = select_ir('repository_id', ir)
        ir_oairoot = ir_data['oairoot'].values[0]
        
        # get metadata for the IR
        # do some qa/qc checks
        ir_meta = get_meta(ir_oairoot)
        ir_meta['unique_item_uri'] = ir_meta['id'].apply(uid_lookup)

        # the number of unique ids and unique item uris should be the same
        print('counts after metadata retrieval and uri creation (should be equal)')
        print('count unique ids:', len(ir_meta['id'].unique()))
        print('count unique uris:', len(ir_meta['unique_item_uri'].unique()))

        # create date field - rows without date metadata will be coerced to NaT
        # then drop nulls - this should leave only rows with date metadata
        ir_meta['date'] = pd.to_datetime(ir_meta['value'], errors='coerce', utc=True).dt.date
        ir_meta.dropna(inplace=True)

        # more qa/qc - assuming all IR require at least one date field
        # the counts output below should be the same as above
        print('counts after adding date field and dropping NaT rows (should be equal to above)')
        print('count unique ids:', len(ir_meta['id'].unique()))
        print('count unique uris:', len(ir_meta['unique_item_uri'].unique()))
        count_oaipmh_records = len(ir_meta['unique_item_uri'].unique())

        # plot value counts for tags
        # save the plot for viewing
        ax2 = ir_meta.groupby('tag')['id'].count().plot.bar(title=ir + ": " + str(len(ir_meta['unique_item_uri'].unique())))

        # print to screen a table of value counts for metadata fields
        # this is another way to verify all but date metadata have been dropped
        print('\n')
        print(ir_meta.groupby('tag')['id'].count())
        fig2 = ax2.get_figure()
        fig2.savefig(plt_dir + ir + "_date_field_counts.png")

        # Is the a 1:1 (or close?) for item/datestamp? true across dspace IR?
        datestamped = ir_meta[ir_meta['tag'] == 'datestamp'].copy()
        datestamped_uri_set = set(datestamped['unique_item_uri'])
        # get the set of unique uris across all items
        ir_meta_unique_uris = set(ir_meta['unique_item_uri'])
        # cross reference w/ datestamped uris - bool and ratio
        all_oaipmh_datestamp = datestamped_uri_set == ir_meta_unique_uris
        item_datestamp_intersection = datestamped_uri_set & ir_meta_unique_uris
        # round to 6 places because otherwise ratios over 99% will still come out to 1
        item_datestamp_ratio = round(len(item_datestamp_intersection)/len(ir_meta_unique_uris), 6)

        # get RAMP data
        # get unique item uris for RAMP data and interesting subsets
        ir_ramp_data = get_ramp(ir)
        ir_ramp_data_uri_set = set(ir_ramp_data['unique_item_uri'])
        count_all_ramp_uris = len(ir_ramp_data_uri_set)
        # get the set of 'ancillary' uris
        # define here as any uri not included in the set of metadata uris
        # (which is a reasonable definition...)
        ir_ramp_ancillary_uris = ir_ramp_data[~ir_ramp_data['unique_item_uri'].isin(ir_meta_unique_uris)].copy()
        
        # subset RAMP to items (ie uris with metadata uris)
        # then subset by citablecontent and not citablecontent
        ir_ramp_item_uris = ir_ramp_data[ir_ramp_data['unique_item_uri'].isin(ir_meta_unique_uris)].copy()
        ir_ramp_non_cc_uris = ir_ramp_item_uris[ir_ramp_item_uris['citablecontent']== 'No'].copy()
        ir_ramp_cc_uris = ir_ramp_item_uris[ir_ramp_item_uris['citablecontent']== 'Yes'].copy()
        
        
        # get sets for ratios
        ir_ramp_ancillary_uris_set = set(ir_ramp_ancillary_uris['unique_item_uri'])
        count_ancillary_ramp_uris = len(ir_ramp_ancillary_uris_set)
        
        ir_ramp_item_uris_set = set(ir_ramp_item_uris['unique_item_uri'])
        count_ramp_items_uris = len(ir_ramp_item_uris_set)
        
        ir_ramp_cc_uris_set = set(ir_ramp_cc_uris['unique_item_uri'])
        count_ramp_cc_uris = len(ir_ramp_cc_uris_set)
        
        ir_ramp_non_cc_uris_set = set(ir_ramp_non_cc_uris['unique_item_uri'])
        count_ramp_non_cc_uris = len(ir_ramp_non_cc_uris_set)
        
        
        # ratios of iterest
        # ratio of metadata uris to ramp uris
        item_ramp_intersection = ir_meta_unique_uris & ir_ramp_data_uri_set
        item_ramp_ratio = round(len(item_ramp_intersection)/len(ir_ramp_data_uri_set), 3)
        # ratio of ancillary uris to ramp uris
        ancillary_ramp_intersection = ir_ramp_ancillary_uris_set & ir_ramp_data_uri_set
        ancillary_ramp_ratio = round(len(ancillary_ramp_intersection)/len(ir_ramp_data_uri_set), 3)
        
        # ratio of cc uris to meta uris
        cc_meta_intersection = ir_ramp_cc_uris_set & ir_meta_unique_uris
        cc_meta_ratio = round(len(cc_meta_intersection)/len(ir_meta_unique_uris), 3)
        # ratio of cc uris to all ramp uris
        cc_ramp_intersection = ir_ramp_cc_uris_set & ir_ramp_data_uri_set
        cc_ramp_ratio = round(len(cc_meta_intersection)/len(ir_ramp_data_uri_set), 3)
        # ratio of cc uris to ramp item uris
        cc_ramp_item_intersection = ir_ramp_cc_uris_set & ir_ramp_item_uris_set
        cc_ramp_item_ratio = round(len(cc_ramp_item_intersection)/len(ir_ramp_item_uris_set), 3)
        
        # ratio of non cc uris to meta uris
        non_cc_meta_intersection = ir_ramp_non_cc_uris_set & ir_meta_unique_uris
        non_cc_meta_ratio = round(len(non_cc_meta_intersection)/len(ir_meta_unique_uris), 3)
        # ratio of non cc uris to all ramp uris
        non_cc_ramp_intersection = ir_ramp_non_cc_uris_set & ir_ramp_data_uri_set
        non_cc_ramp_ratio = round(len(non_cc_meta_intersection)/len(ir_ramp_data_uri_set), 3)
        # ratio of cc uris to ramp item uris
        non_cc_ramp_item_intersection = ir_ramp_non_cc_uris_set & ir_ramp_item_uris_set
        non_cc_ramp_item_ratio = round(len(non_cc_ramp_item_intersection)/len(ir_ramp_item_uris_set), 3)
        
        # overlap of cc and non cc items
        cc_non_cc_intersection = ir_ramp_cc_uris_set & ir_ramp_non_cc_uris_set
        # ratio of cc items in intersection
        # that is - ratio of cc uris for which the corresponding item uri
        # also occurs in non cc form
        cc_ratio = round(len(cc_non_cc_intersection)/len(ir_ramp_cc_uris_set), 3)
        # so we might like to know
        cc_occur_only = 1 - cc_ratio
        # ratio of non cc items in intersection
        # ratio of non cc uris for which the corresponding item uri
        # also occurs in cc form
        non_cc_ratio = round(len(cc_non_cc_intersection)/len(ir_ramp_non_cc_uris_set), 3)
        # and also
        non_cc_only = 1 - non_cc_ratio
        # output to df
        d = [[ir, count_oaipmh_records, all_oaipmh_datestamp,
              item_datestamp_ratio, count_all_ramp_uris, 
              count_ancillary_ramp_uris, count_ramp_items_uris,
              count_ramp_cc_uris, count_ramp_non_cc_uris,
              item_ramp_ratio, ancillary_ramp_ratio,
              cc_meta_ratio, cc_ramp_ratio, cc_ramp_item_ratio,
              non_cc_meta_ratio, non_cc_ramp_ratio, 
              non_cc_ramp_item_ratio, cc_ratio, cc_occur_only,
              non_cc_ratio, non_cc_only]]
        ir_df = pd.DataFrame(d, columns=output_cols)
        output_df = pd.concat([output_df, ir_df])
        # now plot
        # set dt index for all dfs and drop cols
        # all ramp
        ir_ramp_data.set_index(pd.to_datetime(ir_ramp_data['date']), inplace=True)
        ir_ramp_data.drop(columns=['unique_item_uri', 'date', 'citablecontent'], inplace=True)
        # ancillary ramp
        ir_ramp_ancillary_uris.set_index(pd.to_datetime(ir_ramp_ancillary_uris['date']), inplace=True)
        ir_ramp_ancillary_uris.drop(columns=['unique_item_uri', 'date', 'citablecontent'], inplace=True)
        # all items
        ir_ramp_item_uris.set_index(pd.to_datetime(ir_ramp_item_uris['date']), inplace=True)
        ir_ramp_item_uris.drop(columns=['unique_item_uri', 'date', 'citablecontent'], inplace=True)
        # cc items
        ir_ramp_cc_uris.set_index(pd.to_datetime(ir_ramp_cc_uris['date']), inplace=True)
        ir_ramp_cc_uris.drop(columns=['unique_item_uri', 'date', 'citablecontent'], inplace=True)
        # non cc items
        ir_ramp_non_cc_uris.set_index(pd.to_datetime(ir_ramp_non_cc_uris['date']), inplace=True)
        ir_ramp_non_cc_uris.drop(columns=['unique_item_uri', 'date', 'citablecontent'], inplace=True)
        # resample
        resample_p = 'W'
        ir_ramp_resample = ir_ramp_data.resample(resample_p)
        ir_ramp_ancillary_resample = ir_ramp_ancillary_uris.resample(resample_p)
        ir_ramp_item_resample = ir_ramp_item_uris.resample(resample_p)
        ir_ramp_cc_resample = ir_ramp_cc_uris.resample(resample_p)
        ir_ramp_non_cc_resample = ir_ramp_non_cc_uris.resample(resample_p)
        # aggregate
        ir_ramp_clicksums = ir_ramp_resample.aggregate([np.sum])
        ir_ramp_ancially_clicksums = ir_ramp_ancillary_resample.aggregate([np.sum])
        ir_ramp_item_clicksums = ir_ramp_item_resample.aggregate([np.sum])
        ir_ramp_cc_clicksums = ir_ramp_cc_resample.aggregate([np.sum])
        ir_ramp_non_cc_clicksums =ir_ramp_non_cc_resample.aggregate([np.sum])
        ax = ir_ramp_clicksums.plot(legend=False)
        ax.set_title(ir + " clicksum comparison")
        ir_ramp_ancially_clicksums.plot(ax=ax)
        ir_ramp_item_clicksums.plot(ax=ax)
        ir_ramp_cc_clicksums.plot(ax=ax)
        ir_ramp_non_cc_clicksums.plot(ax=ax)
        ax.legend(['Total', 'Ancillary urls', 'Item urls', 'CC urls', 'Non CC urls'])
        fig = ax.get_figure()
        fig.savefig(plt_dir + ir + "_clicksums_comparison.png")
    except Exception as e:
        print(ir, str(e))
        pass

output_df.to_csv(df_dir + '_metadata_ramp_uri_stats.csv', index=False)










