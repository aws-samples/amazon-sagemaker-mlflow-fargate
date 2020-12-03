# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os
import logging
import argparse
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import mlflow
import mlflow.sklearn

logging.basicConfig(level=logging.INFO)


if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    # MLflow related parameters
    parser.add_argument("--tracking_uri", type=str)
    parser.add_argument("--experiment_name", type=str)
    # hyperparameters sent by the client are passed as command-line arguments to the script.
    # to simplify the demo we don't use all sklearn RandomForest hyperparameters
    parser.add_argument('--n-estimators', type=int, default=10)
    parser.add_argument('--min-samples-leaf', type=int, default=3)

    # Data, model, and output directories
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))
    parser.add_argument('--test', type=str, default=os.environ.get('SM_CHANNEL_TEST'))
    parser.add_argument('--train-file', type=str, default='boston_train.csv')
    parser.add_argument('--test-file', type=str, default='boston_test.csv')
    parser.add_argument('--features', type=str)  # we ask user to explicitly name features
    parser.add_argument('--target', type=str) # we ask user to explicitly name the target

    args, _ = parser.parse_known_args()

    logging.info('reading data')
    train_df = pd.read_csv(os.path.join(args.train, args.train_file))
    test_df = pd.read_csv(os.path.join(args.test, args.test_file))

    logging.info('building training and testing datasets')
    X_train = train_df[args.features.split()]
    X_test = test_df[args.features.split()]
    y_train = train_df[args.target]
    y_test = test_df[args.target]

    
    # set remote mlflow server
    mlflow.set_tracking_uri(args.tracking_uri)
    mlflow.set_experiment(args.experiment_name)
    
    with mlflow.start_run():
        params = {
            "n-estimators": args.n_estimators,
            "min-samples-leaf": args.min_samples_leaf,
            "features": args.features
        }
        mlflow.log_params(params)
        
        # TRAIN
        logging.info('training model')
        model = RandomForestRegressor(
            n_estimators=args.n_estimators,
            min_samples_leaf=args.min_samples_leaf,
            n_jobs=-1
        )

        model.fit(X_train, y_train)

        # ABS ERROR AND LOG COUPLE PERF METRICS
        logging.info('evaluating model')
        abs_err = np.abs(model.predict(X_test) - y_test)

        for q in [10, 50, 90]:
            logging.info(f'AE-at-{q}th-percentile: {np.percentile(a=abs_err, q=q)}')
            mlflow.log_metric(f'AE-at-{str(q)}th-percentile', np.percentile(a=abs_err, q=q))

        # SAVE MODEL
        logging.info('saving model in MLflow')
        mlflow.sklearn.log_model(model, "model")