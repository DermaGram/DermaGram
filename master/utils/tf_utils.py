import trial

class TfUtils(object):

    @staticmethod
    def get_classifications(image_path):
        probabilities = get_probs(image_path)
        return [
                {"label":"Biopsy","probability":probabilities[2]},
                {"label":"No Biopsy","probability":probabilities[1]},
                {"label":"Unsure","probability":probabilities[0]}
                ]

    @staticmethod
    def get_top_classification(classification_data):
        max_label = ""
        max_prob = 0.0
        for classification in classification_data:
            for key, val in classification.iteritems():
                if key == "label":
                    label = val
                if key == "probability":
                    prob = val
            if prob > max_prob:
                max_prob = prob
                max_label = label
        return max_label
