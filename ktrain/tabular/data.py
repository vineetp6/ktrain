from ..imports import *
from .. import utils as U
from . import preprocessor as pp

def table_from_df(train_df, label_columns=[], date_columns=[], val_df=None, val_pct=0.1, 
                  is_regression=False, random_state=None, verbose=1):

    # TODO: this code is similar to images_from_df: must refactor and cleaned up

    # check label_columns
    if label_columns is None or (isinstance(label_columns, (list, np.ndarray)) and len(label_columns) == 0):
        raise ValueError('label_columns is required')
    if isinstance(label_columns, (list, np.ndarray)) and len(label_columns) == 1:
        label_columns = label_columns[0]

    # define original predictor_columns
    predictor_columns = [col for col in train_df.columns.values if col not in label_columns]

    # create validation set
    if val_df is None:
        if val_pct:
            df = train_df.copy()
            prop = 1-val_pct
            if random_state is not None: np.random.seed(42)
            msk = np.random.rand(len(df)) < prop
            train_df = df[msk]
            val_df = df[~msk]

    procs = [pp.FillMissing, pp.Categorify, pp.Normalize]
    preproc = pp.TabularPreprocessor(predictor_columns, label_columns, date_columns=date_columns, 
                                     is_regression=is_regression, procs=procs)
    trn = preproc.preprocess_train(train_df, verbose=verbose)
    val = None if val_df is None else preproc.preprocess_test(val_df, verbose=verbose)
    return (trn, val, preproc)



def table_from_csv(train_csv, label_columns=[], date_columns=[], val_csv=None, val_pct=0.1, is_regression=False, random_state=None):
    """
    Loads tabular data from CSV file
    """

    # read in dataset
    train_df = pd.read_csv(train_csv, index_col=0)
    val_df = None
    if val_csv is not None:
        val_df = pd.read_csv(val_csv, index_col=0)
    return table_from_df(train_df, label_columns=label_columns, date_columns=date_columns, val_df=val_df, val_pct=val_pct, 
                         is_regression=is_regression, random_state=random_state)
 


