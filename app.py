from flask import Flask, render_template, request, jsonify
from source.pneumonia_detection import detect_pneumonia
from source.handle_image import get_uri, read_image, open_image, UMatToPIL, ndarrayToPIL, convert_dcm
from source.image_enhancement_mamdani import FuzzyContrastEnhance
from source.image_enhancement import combineMamdani, combineSugeno, combineTsukamoto, combineHistogram
import io

app = Flask(__name__)


# @app.route('/convert_dcm', methods=['POST'])
# def convert_dcm_handler():
#     if 'file-image' in request.files:
#         file = request.files['file-image']
#         if file.filename.lower().endswith('.dcm'):
#             encoded_image = convert_dcm_to_jpeg(file.read())  # Pass the file content (byte data)
#             return jsonify({'encoded_image': encoded_image})

#     return jsonify({'error': 'Invalid file format. Only .dcm files are supported.'})

@app.route('/convert_dcm', methods=['POST'])
def convert_dcm_handler():
    if 'file-image' in request.files:
        file = request.files['file-image']
        if file.filename.lower().endswith('.dcm'):
            encoded_image = convert_dcm(file.read())  # Pass the file content (byte data)
            return jsonify({'encoded_image': encoded_image})

    return jsonify({'error': 'Invalid file format. Only .dcm files are supported.'})



@app.route('/', methods=['GET', 'POST'])
def index():
    pneumonia_percentage = None  # Initialize the variable

    if request.method == "POST":
        if 'file-image' in request.files:
            file = request.files['file-image']
            if file:
                output = detect_pneumonia(file)
                image_uri = get_uri(open_image(file))
                pneumonia_percentage = output[0]
                # return render_template('layout.html', pneumonia_percentage=pneumonia_percentage)
                # return str(pneumonia_percentage)
                return jsonify({"pneumonia_percentage": pneumonia_percentage})


    return render_template('layout.html', pneumonia_percentage=pneumonia_percentage)


@app.route("/process_image", methods=["POST"])
def process():
    if request.method == "POST":
        file = request.files["file-image"]

        # if file:
        #     enhanced_image = get_uri(UMatToPIL(FuzzyContrastEnhance(read_image(file))))
        #     return jsonify({"encoded_image": enhanced_image})

        if file:
            enhanced_image = get_uri(ndarrayToPIL(combineMamdani(read_image(file))))
            sugeno_enhanced_image = get_uri(ndarrayToPIL(combineSugeno(read_image(file))))
            tsukamoto_enhanced_image = get_uri(ndarrayToPIL(combineTsukamoto(read_image(file))))
            histogram_enhanced_image = get_uri(ndarrayToPIL(combineHistogram(read_image(file))))
            return jsonify({"encoded_image": enhanced_image, "sugeno_encoded_image": sugeno_enhanced_image, "tsukamoto_encoded_image": tsukamoto_enhanced_image, "histogram_encoded_image": histogram_enhanced_image})

    # Handle other cases or return an error message
    return "Invalid request"


# Menangani halaman 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('notFound.html'), 404


if __name__ == "__main__":
    app.run(debug=True)