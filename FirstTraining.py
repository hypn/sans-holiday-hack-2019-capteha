from imageai.Prediction.Custom import ModelTraining

model_trainer = ModelTraining()
model_trainer.setModelTypeAsResNet()
model_trainer.setDataDirectory(".")
model_trainer.trainModel(num_objects=6, num_experiments=200, enhance_data=True, batch_size=4, show_network_summary=True)

