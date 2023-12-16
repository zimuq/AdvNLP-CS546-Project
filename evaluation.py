import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

def result_preprocess(predict_dataset, real_dataset):

    y_true = []
    y_pred = []    
    
    # for url in predict_dict:
        # predict_dict[url] = predict_dict[url].replace("\n", " ")
        # print(predict_dict)
        # predict_str = predict_dict[url]
    dict_predict_one_url = {}
    for line in predict_dataset.strip().split("\n"):
            # print(predict_dataset)
            if ": " in line:
                brand, rest = line.split(": ", 1)
                # print(rest)
                try:
                    score, sentiment = rest.split(",", 1)
                except ValueError:
                    score = rest
                brand_no_space = brand.replace(" ", "")
                # if isinstance(score, int):
                dict_predict_one_url[brand_no_space.lower()] = {"score": int(score)}

    # real_str = real_dict[url]

    for key in dict_predict_one_url:
            for correct_brand, remain in real_dataset.items():
                for model, score in remain.items():
                    brand_str_no_space = str(correct_brand).replace(" ", "").lower()
                    model_no_space = str(model).replace(" ", "").lower()
                    if key == brand_str_no_space + model_no_space:
                        y_true.append(int(score))
                        y_pred.append(dict_predict_one_url[key]["score"])
                    elif key == model_no_space:
                        y_true.append(int(score))
                        y_pred.append(dict_predict_one_url[key]["score"])    

    return y_true, y_pred

def calculate_weighted_metrics(y_true, y_pred):

    # Create the confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    # True positives, false positives, false negatives for each class
    tp = np.diag(cm)
    fp = np.sum(cm, axis=0) - tp
    fn = np.sum(cm, axis=1) - tp

    # Calculate MSE
    mse = sum((true - pred) ** 2 for true, pred in zip(y_true, y_pred)) / len(y_true)

    # Precision, Recall, and F1 for each class
    # precision = np.nan_to_num(tp / (tp + fp))
    precision = np.array([tp / (tp + fp) if (tp + fp) > 0 else 0 for tp, fp in zip(tp, fp)])
    # recall = np.nan_to_num(tp / (tp + fn))
    recall = np.array([tp / (tp + fn) if (tp + fn) > 0 else 0 for tp, fn in zip(tp, fn)])    
    # print(precision + recall)
    f1 = np.array([2 * p * r / (p + r) if (p + r) > 0 else 0 for p, r in zip(precision, recall)])

    # Total instances in each class
    total_instances = np.sum(cm, axis=1)

    # Weighted metrics
    weighted_precision = np.sum(precision * total_instances) / np.sum(total_instances)
    weighted_recall = np.sum(recall * total_instances) / np.sum(total_instances)
    weighted_f1 = np.sum(f1 * total_instances) / np.sum(total_instances)

    return weighted_precision, weighted_recall, weighted_f1, mse

# def main():
# #     dataset_predict = """
# # OnePlus Open: 1 (positive)
# # Pixel Fold: 1 (positive)
# # iPhone 14 Pro: 0 (neutral)
# # iPhone 15: 0 (neutral)
# # Samsung Z Fold 5: 0 (neutral)
# # HONOR Magic V2: 0 (neutral)
# # LG: -1 (negative)
# # Sony: -1 (negative)
# #     """
#     predict_dict = {'https://www.youtube.com/watch?v=jD9n01Mck0Q': 'OnePlus Open: 1\nPixel Fold: 1\niPhone 14 Pro: 1\niPhone 15: 0\niPhone 13 Pro: 0\nSamsung Z Fold 5: 0\nOPPO Find N3: 0\nHONOR Magic V2: 0\nSamsung: -1\nLG: -1\nSony: -1\nAsus ZenFones: -1\nMotorola Razr 40: 0', 'https://www.youtube.com/watch?v=BS8x2TicxQ8': 'Google Pixel: 1\niPhone: 0\nSamsung: 0', 'https://www.youtube.com/watch?v=0X0Jm8QValY': 'iPhone 15: www.youtube.com/watch?v=WuljKartv2U': 'Z Flip 5: 1\nSamsung: 1', 'https://www.youtube.com/watch?v=6aK407STsGA': 'Asus Zenfone 10: 1', 'https://www.youtube.com/watch?v=PhFwDJCEhBg': 'Pixel Fold: 1\nSamsung: 0\niPhone: -1', 'https://www.youtube.com/watch?v=lRUtHtqfCGA': 'Nothing Phone 2: 1', 'https://www.youtube.com/watch?v=PCp1BmME6QA': 'Sony Xperia 1 Mark V: 1\niPhone 13 Pro: 0\nSamsung: -1\nGoogle Pixel 3: 0'} 
#     real_dict = 
#     rs =exp.readManuallyLabels('std_manual_label.csv') # rs is a dictionary
#     videos_dict = rs['mkbhd']
#     # link = 'https://www.youtube.com/watch?v=jD9n01Mck0Q'
#     y_true, y_pred = result_preprocess(predict_dict, videos_dict, link)
#     y_true = [1, 0, 0, -1, 0, 1]
#     y_pred = [1, 0, 0, 0, -1, 1]
#     # precision, recall, f1, mse = calculate_weighted_metrics(y_true, y_pred)
#     # print(f"Precision: {precision}, Recall: {recall}, F1: {f1}, MSE: {mse}")

# if __name__ == '__main__':
#     main()