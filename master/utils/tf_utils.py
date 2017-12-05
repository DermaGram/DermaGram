

class TfUtils(object):

    @staticmethod
    def get_classifications():
        return [
                {"label":"Biopsy","probability":0.6},
                {"label":"No Biopsy","probability":0.3},
                {"label":"Unsure","probability":0.1}
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
