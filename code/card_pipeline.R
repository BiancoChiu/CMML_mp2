library(CARD)
library(Matrix)
setwd('/Users/bianco/Documents/code/tmp/card')
org_st_count = read.csv('Out_gene_expressions_10000genes.csv',header = T, row.names = 1)
sc_exp = read.table('raw_somatosensory_sc_exp_sub10cells.txt',header = T,row.names = 1)
sc_anno = read.csv('somatosensory_sc_labels_sub.txt',header = F)
spatial_location = read.csv('Out_rect_locations.csv',header = T, row.names = 1)

colnames(spatial_location) = c('x','y')
sc_count = Matrix(as.matrix(sc_exp),sparse = TRUE)
sc_meta = data.frame(matrix(ncol = 3,nrow = ncol(sc_exp)))
colnames(sc_meta) = c('cellID','cellType','sampleInfo')
sc_meta$sampleInfo = "sample1"
sc_meta$cellType = sc_anno$V1
sc_meta$cellID = colnames(sc_count)
rownames(sc_meta) = sc_meta$cellID


colnames(org_st_count) <- as.character(colnames(org_st_count))
rownames(spatial_location) <- as.character(rownames(spatial_location))


rownames(spatial_location) <- paste0("X", rownames(spatial_location))
all(colnames(org_st_count) == rownames(spatial_location))

CARD_obj = createCARDObject(
  sc_count = as.matrix(sc_exp),
  sc_meta = sc_meta,
  spatial_count = as.matrix(org_st_count),
  spatial_location = spatial_location,
  ct.varname = "cellType",
  ct.select = unique(sc_meta$cellType),
  sample.varname = "sampleInfo",
  minCountGene = 100,
  minCountSpot = 5) 

CARD_obj = CARD_deconvolution(CARD_object = CARD_obj)
write.csv(CARD_obj@Proportion_CARD, 'card_sub10.csv')


