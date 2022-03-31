import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense
from cowait.tasks import Task


class ImdbTask(Task):
    async def run(self):
        # get the pre-processed data
        data_train, data_test = self.get_data()

        # train and evaluate model
        model = self.fit(data_train, data_test)

        # test model on example data point
        test_index = 500
        test_example = data_test[0][test_index]
        pred = model.predict(test_example.reshape(1, len(test_example)))
        pred = 1 if pred[0][0] > 0.5 else 0
        print("##### Test example #####")
        print("Correct class:", data_test[1][test_index])    # gt=1
        print("Predicted class:", pred)

        return int(pred)

    def get_data(self):
        # load the data
        # the text reviews have already been converted to numerical features
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.imdb.load_data()

        # pad all sequences to the same length
        pad_length = 1000
        x_train = pad_sequences(x_train, pad_length)
        x_test = pad_sequences(x_test, pad_length)

        return (x_train, y_train), (x_test, y_test)

    def create_model(self):
        # size of the vocabulary
        vocab_size = len(tf.keras.datasets.imdb.get_word_index().keys()) + 3
        # size of the embedding vectors learned by the model
        embedding_dim = 16

        # set up the model structure
        model = Sequential([
            Embedding(input_dim=vocab_size, output_dim=embedding_dim),    # embedding layer
            GlobalAveragePooling1D(),                                     # pooling layer
            Dense(1, activation='sigmoid')                                # single sigmoid output node
        ])

        # compile model with optimizer, loss function and evaluation metrics
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        return model

    def fit(self, data_train, data_test):
        # get the data
        (x_train, y_train), (x_test, y_test) = data_train, data_test

        # create the model
        model = self.create_model()

        # fit the model to the train set
        print("##### Train model #####")
        model.fit(
            x=x_train,
            y=y_train,
            epochs=2
        )

        # evaluate the model on the test set
        print("##### Evaluate model #####")
        model.evaluate(
            x=x_test,
            y=y_test
        )

        return model
