from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from demand_forcasting import process_data

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
PLOT_FOLDER = 'plots'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['PLOT_FOLDER'] = PLOT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'test.csv')
        file.save(filepath)
        process_data('train.csv', filepath, os.path.join(app.config['OUTPUT_FOLDER'], 'forecast_results.csv'), app.config['PLOT_FOLDER'])
        return redirect(url_for('results'))

@app.route('/results')
def results():
    # Check if the plot files exist
    sales_trend_exists = os.path.exists(os.path.join(app.config['PLOT_FOLDER'], 'sales_trend.html'))
    store_sales_exists = os.path.exists(os.path.join(app.config['PLOT_FOLDER'], 'store_sales.html'))

    return render_template('results.html', 
                           sales_trend_exists=sales_trend_exists, 
                           store_sales_exists=store_sales_exists)

@app.route('/download')
def download_file():
    return send_file(
        os.path.join(app.config['OUTPUT_FOLDER'], 'forecast_results.csv'),
        as_attachment=True,
        download_name='forecast_results.csv'
    )


@app.route('/plot/<plot_name>')
def display_plot(plot_name):
    return send_file(os.path.join(app.config['PLOT_FOLDER'], plot_name))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['OUTPUT_FOLDER']):
        os.makedirs(app.config['OUTPUT_FOLDER'])
    if not os.path.exists(app.config['PLOT_FOLDER']):
        os.makedirs(app.config['PLOT_FOLDER'])
    app.run(debug=True)
