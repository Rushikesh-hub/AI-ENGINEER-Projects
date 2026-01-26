from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

def build_preprocessor(numeric_features,categorical_features):

    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler",StandardScaler())
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_pipeline,numeric_features),
        ("cat",categorical_pipeline,categorical_features)
    ])

    return preprocessor


from sklearn.model_selection import train_test_split

X_train, X_test,y_train,y_test = train_test_split(
    X, y, test_size=0.2,random_state=42,stratify=y
)