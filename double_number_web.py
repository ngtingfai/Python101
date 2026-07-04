from flask import Flask, request, render_template_string

app = Flask(__name__)

#access the app at http://127.0.0.1:5000/

HTML_FORM = '''
<!doctype html>
<title>Double a Number</title>
<h2>Enter a number to double it:</h2>
<form method="post">
  <input type="number" name="number" required>
  <input type="submit" value="Double">
</form>
{% if result is not none %}
  <h3>Result: {{ result }}</h3>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def double_number():
    result = None
    if request.method == 'POST':
        try:
            num = float(request.form['number'])
            result = num * 20
        except (ValueError, KeyError):
            result = 'Invalid input.'
    return render_template_string(HTML_FORM, result=result)

if __name__ == '__main__':
    app.run(debug=True)
