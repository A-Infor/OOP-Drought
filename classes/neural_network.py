import tensorflow as tf
import json
import matplotlib.pyplot as plt

class NeuralNetwork:
    def __init__(self, file_name, data_processor):
        self.data_processor = data_processor
        self.configs_dict   = self._set_ml_model_parameters(file_name)        
        self.model          = self._create_ml_model()
        print(self.model.summary())
        self.train_ml_model()
    
    def _load_config_file(self, file_name):
        with open(file_name) as file:
            return json.load(file)
    
    def _set_ml_model_parameters(self, file_name):
        configs_dict                = self._load_config_file(file_name)
        configs_dict['input_shape'] = (configs_dict['total_points']-configs_dict['hidden_units'],1)
        configs_dict['activation' ] = ['relu','sigmoid']
        configs_dict['loss'       ] = 'mse'
        configs_dict['metrics'    ] = ['mae',
                                       tf.keras.metrics.RootMeanSquaredError(name='rmse'),
                                       'mse',
                                       tf.keras.metrics.R2Score(name="r2")]
        configs_dict['optimizer'  ] = 'adam'
        
        return configs_dict
    
    def _create_ml_model(self):
        print('Started: creation of ML model')
        model = tf.keras.Sequential()
        model.add(tf.keras.Input       (shape=self.configs_dict['input_shape']))
        model.add(tf.keras.layers.LSTM (     self.configs_dict['hidden_units'], activation=self.configs_dict['activation'][0]))
        model.add(tf.keras.layers.Dense(units=self.configs_dict['dense_units'], activation=self.configs_dict['activation'][1]))
        model.add(tf.keras.layers.Dense(units=self.configs_dict['dense_units'], activation=self.configs_dict['activation'][1]))
        model.add(tf.keras.layers.Dense(units=self.configs_dict['dense_units'], activation=self.configs_dict['activation'][1]))
        model.compile(loss=self.configs_dict['loss'], metrics=self.configs_dict['metrics'], optimizer=self.configs_dict['optimizer'])
        print('Ended: creation of ML model')
        
        return model
    
    def _print_loss_chart(self, history):
        plt.figure()
        plt.plot(history.history['loss'],'k')
        plt.ylabel('Mean Squared Error (MSE)')
        plt.legend(['loss'])
        plt.show()
    
    def train_ml_model(self):
        print('Started: training of ML model')
        trainData, testData, monthTrainData, monthTestData, split = self.data_processor._splitSpeiData('./Data/spei12_riopardodeminas.xlsx', self.configs_dict['parcelDataTrain'])
        trainDataForPrediction, trainDataTrueValues = self.data_processor._cria_IN_OUT(trainData, self.configs_dict['total_points'], self.configs_dict['dense_units']) # Treinamento
        history=self.model.fit(trainDataForPrediction, trainDataTrueValues, epochs=self.configs_dict['numberOfEpochs'], batch_size=1, verbose=0)
        self._print_loss_chart(history)
        print('Ended: training of ML model')
    
    # def apply_ml_model(self):
    #         #[0] = lista de dados do SPEI referentes à parcela de treinamento (80%)
    #         #[1] = lista de dados do SPEI referentes à parcela de teste (20%)
    #         #[2] = lista de datas referentes à parcela de treinamento (80%)
    #         #[3] = lista de datas referentes à parcela de teste (20%)
    #         #[4] = valor inteiro da posição que o dataset foi splitado
    #     trainData, testData, monthTrainData, monthTestData, split = splitSpeiData(xlsx)
    
    #         # Dataset que contém a parcela de dados que será utilizada para...
    #         #[0] = ... alimentar a predição da rede
    #         #[1] = ... validar se as predições da rede estão corretas
    #     trainDataForPrediction, trainDataTrueValues = cria_IN_OUT(trainData, totalPoints) # Treinamento
    #     testDataForPrediction , testDataTrueValues  = cria_IN_OUT(testData , totalPoints) # Teste
    
    #         # Dataset que contém a parcela dos meses nos quais...
    #         #[0] = ... os SPEIs foram utilizados para alimentar a predição da rede
    #         #[1] = ... os SPEIs foram preditos
    #     trainMonthsForPrediction, trainMonthForPredictedValues = cria_IN_OUT(monthTrainData, totalPoints) # Treinamento
    #     testMonthsForPrediction , testMonthForPredictedValues  = cria_IN_OUT(monthTestData , totalPoints) # Teste
    
    #     if training:
    #         model = trainNeuralNetwork(trainDataForPrediction, trainDataTrueValues)
    
    #         #faz previsões e calcula os erros
    #     trainPredictValues = model.predict(trainDataForPrediction)
    #     testPredictValues = model.predict(testDataForPrediction)
    
    #     trainErrors = getError(trainDataTrueValues, trainPredictValues)
    #     testErrors = getError(testDataTrueValues, testPredictValues)
    
    #     print("--------------Result for " + regionName +"---------------")
    #     print("---------------------Train-----------------------")
    #     print(trainErrors)
    
    #     print("---------------------Test------------------------")
    #     print(testErrors)
    
    #     showSpeiData(xlsx, testData, split, regionName)
        
    #     if training:
    #         showSpeiTest(xlsx, testData, split, regionName)
            
    #     showPredictionResults(trainDataTrueValues, testDataTrueValues, trainPredictValues, testPredictValues, trainMonthForPredictedValues, testMonthForPredictedValues, xlsx)
    #     showPredictionsDistribution(trainDataTrueValues, testDataTrueValues, trainPredictValues, testPredictValues, xlsx)
    
    #     return model
    
