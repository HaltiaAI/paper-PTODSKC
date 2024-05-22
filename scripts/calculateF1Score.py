import os
from rdflib import Graph

def calculate_metrics(TP, FP, FN):
    # Calculate Precision
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0

    # Calculate Recall
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0

    # Calculate F1 Score
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1_score

def evaluate_results(evaluation_output_path, ground_truth_output_path):
    # initialize the result variables
    triple_tp, triple_fp, triple_fn = 0, 0, 0
    triple_rec, triple_pre, triple_f1 = 0, 0, 0
    evaluation = {}

    # Iterate over all items in the directory
    for filename in os.listdir(ground_truth_output_path):
        file_eval = os.path.join(evaluation_output_path, filename)
        file_truth = os.path.join(ground_truth_output_path, filename)

        g_eval = Graph()
        g_truth = Graph()

        with open(file_truth, 'r') as file_gt:
            ground_truth_text = file_gt.readline().strip()
            if ''.join(ground_truth_text.split()).upper() == "NONE":
                print(f"Successfully parsed 1 triple from the ground truth file.")
                with open(file_eval, 'r') as file_mg:
                    generated_model_text = file_mg.readline().strip()
                    if ''.join(generated_model_text.split()).upper() == "NONE":
                        triple_tp += 1
                        print(f"Successfully parsed 1 triple from the evaluation file.")
                    else:
                        triple_fp += 1
                continue


        g_truth.parse(file_truth, format="turtle")
        print(f"Successfully parsed {len(g_truth)} triples from the ground truth file.")
        parset:bool = False
        try:
            g_eval.parse(file_eval, format="turtle")
            parset = True
            print(f"Successfully parsed {len(g_eval)} triples from the evaluation file.")
        except Exception as e:
            try: 
                generated_model_text = parse_rdf_data_from_brackets(generated_model_text)
                g_eval.parse(data=generated_model_text, format="turtle")
                print("IN EXCEPTION")
                print(f"Successfully parsed {len(g_truth)} triples from the ground truth file.")
                print(generated_model_text)
                print(ground_truth_text)
                print(f"Successfully parsed {len(g_eval)} triples from the evaluation file.")
                parset = True
                
            except Exception as e:
                triple_fn += len(g_truth)
        if parset:
            # Calculate the metrics
            g_truthOnly = g_truth - g_eval
            g_evalOnly = g_eval - g_truth
            triple_tp += len(g_truth) - len(g_truthOnly)
            fark_te = len(g_truthOnly) - len(g_evalOnly)
            if fark_te >= 0:
                triple_fp += len(g_evalOnly)
                triple_fn += fark_te
            else:
                triple_fp += len(g_truthOnly)

    triple_rec, triple_pre, triple_f1 = calculate_metrics(triple_tp, triple_fp, triple_fn)
    evaluation["eval_output"] = {
        'triple_matching': {'TP': triple_tp, 'FP': triple_fp, 'FN': triple_fn, "PRE": triple_pre, "REC": triple_rec, "F1": triple_f1},
    }

    return evaluation

def write_evaluation_to_file(evaluation, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for file_name, data in evaluation.items():
            file.write(f'Results for {file_name}:\n')
            for match_type, scores in data.items():
                file.write(f'  {match_type}:\n')
                for score_type, value in scores.items():
                    file.write(f'    {score_type}: {value}\n')
            file.write('\n')

# Replace these file paths with your actual file paths
evaluation_output_path = 'results/test_evaluation_output/'
ground_truth_output_path = 'results/test_ground_truth_output/'
evaluation_file = 'results/evaluation_results.txt'

evaluation = evaluate_results(evaluation_output_path, ground_truth_output_path)
write_evaluation_to_file(evaluation, evaluation_file)

print("Precision, recall and f1-score calculated. Results are written to 'evaluation_results.txt'")


