import sys
import scanpy as sc
import anndata
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import subprocess

import os

import cell2location
import scvi

from matplotlib import rcParams
rcParams['pdf.fonttype'] = 42 # enables correct plotting of text
import seaborn as sns
from scipy.sparse import csr_matrix
from cell2location.utils.filtering import filter_genes

sc_file_path = sys.argv[1]
spatial_file_path = sys.argv[2]
celltype_key = sys.argv[3]
output_file_path = sys.argv[4]

adata_snrna_raw = sc.read_h5ad(sc_file_path)
adata_vis = sc.read_h5ad(spatial_file_path)
adata_snrna_raw.X = csr_matrix(adata_snrna_raw.X)
adata_vis.X = csr_matrix(adata_vis.X)

adata_snrna_raw = adata_snrna_raw[~adata_snrna_raw.obs[celltype_key].isin(np.array(adata_snrna_raw.obs[celltype_key].value_counts()[adata_snrna_raw.obs[celltype_key].value_counts() <=1].index))]

# remove cells and genes with 0 counts everywhere
sc.pp.filter_genes(adata_snrna_raw,min_cells=1)
sc.pp.filter_cells(adata_snrna_raw,min_genes=1)

adata_snrna_raw.obs[celltype_key] = pd.Categorical(adata_snrna_raw.obs[celltype_key])
adata_snrna_raw = adata_snrna_raw[~adata_snrna_raw.obs[celltype_key].isna(), :]

selected = filter_genes(adata_snrna_raw, cell_count_cutoff=5, cell_percentage_cutoff2=0.03, nonz_mean_cutoff=1.12)

# filter the object
adata_snrna_raw = adata_snrna_raw[:, selected].copy()

# scvi.data.setup_anndata(adata=adata_snrna_raw,labels_key=celltype_key)
cell2location.models.RegressionModel.setup_anndata(adata=adata_snrna_raw,
                        # 10X reaction / sample / batch
                        # batch_key='Sample',
                        # cell type, covariate used for constructing signatures
                        labels_key=celltype_key,
                        # multiplicative technical effects (platform, 3' vs 5', donor effect)
                        # categorical_covariate_keys=['Method']
                       )

# create and train the regression model
from cell2location.models import RegressionModel
mod = RegressionModel(adata_snrna_raw)

# Use all data for training (validation not implemented yet, train_size=1)
mod.train(max_epochs=250, batch_size=2500, train_size=1, lr=0.002, accelerator='gpu')

# plot ELBO loss history during training, removing first 20 epochs from the plot
#mod.plot_history(20)

# In this section, we export the estimated cell abundance (summary of the posterior distribution).
adata_snrna_raw = mod.export_posterior(
    adata_snrna_raw, sample_kwargs={'num_samples': 1000, 'batch_size': 2500, 'accelerator': 'gpu'}
)

# export estimated expression in each cluster
if 'means_per_cluster_mu_fg' in adata_snrna_raw.varm.keys():
    inf_aver = adata_snrna_raw.varm['means_per_cluster_mu_fg'][[f'means_per_cluster_mu_fg_{i}'
                                    for i in adata_snrna_raw.uns['mod']['factor_names']]].copy()
else:
    inf_aver = adata_snrna_raw.var[[f'means_per_cluster_mu_fg_{i}'
                                    for i in adata_snrna_raw.uns['mod']['factor_names']]].copy()
inf_aver.columns = adata_snrna_raw.uns['mod']['factor_names']
inf_aver.iloc[0:5, 0:5]

intersect = np.intersect1d(adata_vis.var_names, inf_aver.index)
adata_vis = adata_vis[:, intersect].copy()
inf_aver = inf_aver.loc[intersect, :].copy()

# prepare anndata for cell2location model
# scvi.data.setup_anndata(adata=adata_vis)
cell2location.models.Cell2location.setup_anndata(adata=adata_vis)

#scvi.data.view_anndata_setup(adata_vis)

# create and train the model
mod = cell2location.models.Cell2location(
    adata_vis, cell_state_df=inf_aver,
    # the expected average cell abundance: tissue-dependent
    # hyper-prior which can be estimated from paired histology:
    N_cells_per_location=30,
    # hyperparameter controlling normalisation of
    # within-experiment variation in RNA detection (using default here):
    detection_alpha=200
)

mod.train(max_epochs=30000,
          # train using full data (batch_size=None)
          batch_size=None,
          # use all data points in training because
          # we need to estimate cell abundance at all locations
          train_size=1,
          accelerator='gpu')

# plot ELBO loss history during training, removing first 100 epochs from the plot
# mod.plot_history(1000)
# plt.legend(labels=['full data training'])

adata_vis = mod.export_posterior(
    adata_vis, sample_kwargs={'num_samples': 1000, 'batch_size': mod.adata.n_obs, 'accelerator': 'gpu'}
)
print(adata_vis)
adata_vis.obsm['mean_cell_abundance_w_sf'].to_csv(output_file_path + '/Cell2location_result.txt')


