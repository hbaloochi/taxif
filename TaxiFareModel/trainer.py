# imports
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from TaxiFareModel.utils import *
from TaxiFareModel.data import get_data,clean_data
from TaxiFareModel.encoders import *

def compute_rmse(y_pred, y_true):
    return np.sqrt(((y_pred - y_true)**2).mean())

class Trainer():
    def __init__(self, X, y):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.pipeline = None
        self.X = X
        self.y = y

    def set_pipeline(self):
        """defines the pipeline as a class attribute"""
        dist_pipe = Pipeline([
                        ('dist_trans', DistanceTransformer()),
                        ('stdscaler', StandardScaler())
                        ])
        time_pipe = Pipeline([
                        ('time_enc', TimeFeaturesEncoder('pickup_datetime')),
                        ('ohe', OneHotEncoder(handle_unknown='ignore'))
                        ])
        preproc_pipe = ColumnTransformer([
                ('distance', dist_pipe, ["pickup_latitude", "pickup_longitude", 'dropoff_latitude', 'dropoff_longitude']),
                ('time', time_pipe, ['pickup_datetime'])
                ], remainder="drop")
        self.pipeline = Pipeline([
                ('preproc', preproc_pipe),
                ('linear_model', LinearRegression())
            ])
        return self



    def run(self):
        """set and train the pipeline"""
        self.set_pipeline()
        self.pipeline.fit(self.X,self.y)
        return self

    def evaluate(self, X_test, y_test):
        """evaluates the pipeline on df_test and return the RMSE"""
        y_pred = self.pipeline.predict(X_test)
        return compute_rmse(y_pred,y_test)


if __name__ == "__main__":
    df=get_data()
    df=clean_data(df)
    # set X and y
    X=df.drop(columns='fare_amount')
    y=df.fare_amount
    # hold out
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
    # train
    trainer=Trainer(X_train,y_train)
    trainer=trainer.set_pipeline()
    trainer=trainer.run()
    # evaluate

    print(trainer.evaluate(X_test,y_test))
