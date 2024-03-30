from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify, send_from_directory
import fitz

app = Flask(__name__)
app.secret_key = b'\xd8`\xc0+\x95,\xdcO\xddQ8\xab\xf6\x06\x9f\x86\x1fl\xe1\x94\xba\x90;H'

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/unlock', methods=['POST'])
def unlock_pdf():
    if 'pdf_file' not in request.files:
        flash('No file part')
        return jsonify({'flash': get_flashed_messages()})
    file = request.files['pdf_file']
    password = request.form['password']
    if file.filename == '':
        flash('No selected file')
        return jsonify({'flash': get_flashed_messages()})
    try:
        file_bytes = file.read()
        doc = fitz.open("pdf", file_bytes)
        if doc.is_encrypted and not doc.authenticate(password):
            flash("Incorrect password")
            return jsonify({'flash': get_flashed_messages()})
        
        unlocked_pdf_path = "/tmp/unlocked.pdf"
        doc.save(unlocked_pdf_path)
        doc.close()
        return jsonify({'redirect': url_for('download_file', filename='unlocked.pdf')})
    except Exception as e:
        flash(str(e))
        return jsonify({'flash': get_flashed_messages()})

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory('/tmp', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


