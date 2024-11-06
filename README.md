# Aerial Country Flags Detection and Classification

## Overview
This project demonstrates a pipeline for detecting country flags from aerial views using a YOLO pre-trained model. The model is trained in multiple stages using a combination of synthetic datasets generated through Python and Blender, and real-life flag images. The final model can effectively detect flags placed on the ground from a drone's perspective.

## Pipeline

The pipeline for detecting country flags consists of the following stages:
![image](https://github.com/user-attachments/assets/0450d79e-626c-4f0e-bc1a-981887ca8c4c)


1. **Pre-training**:
   - A synthetic dataset is generated using Python scripts to simulate the flags in a variety of environments and lighting conditions.
   - The YOLO pre-trained model is used to train on this synthetic dataset, providing an initial understanding of flag detection.

2. **Intermediate Training**:
   - After the initial training, we leveraged transfer learning by retraining the model on the real dataset collected from RoboFlow. This step fine-tuned the model, enabling it to adapt to the variations present in real-world images.
   
3. **Fine-tuning**:
   - A synthetic dataset is created using Blender, which simulates the flags from various angles and lighting conditions that may be encountered by drones in aerial footage.
   - The model is fine-tuned on this dataset to enhance its performance for the specific task of detecting flags in aerial views.

4. **Final Model**:
   - The final model is achieved after these stages of training and fine-tuning, resulting in a highly accurate detection system for country flags.

## Synthetic Dataset Generation (Blender)

The synthetic dataset is generated using Blender to create realistic 3D environments where flags are placed on the ground. This dataset is crucial for training the model to detect flags in various conditions such as different lighting, angles, and backgrounds.
### **Key Features**
- **Automated Dataset Generation**:
  - Synthetic images of 196 different flags.
  - Over 15,000 images generated with various augmentations.
  
- **Data Augmentation Techniques**:
  - **Random Positioning**: Flags are positioned randomly in the scene.
  - **Random Rotation**: Each flag is rotated at different angles to introduce variability.
  - **Random Camera Heights**: Simulated different camera angles and heights for a more diverse dataset.
  - **Random Backgrounds**: Varied and complex backgrounds to simulate real-world environments.

- **Auto-Annotation**:
  - Automated bounding box generation for object detection.
  - Annotations are formatted for training models using **YOLO**.

## Kaggle Notebook Link: https://www.kaggle.com/code/ahmedsaleh627/notebook24ac0bdae7 

## Evaluation Metrics
![results](https://github.com/user-attachments/assets/7f76c815-9e11-4e46-a5c7-2a9c891f65d6)  

![val_batch2_pred_50_639e1947b6fe9f7b15b9](https://github.com/user-attachments/assets/7439750b-bfa4-4b40-8577-90739c854309)




