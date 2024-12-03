from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        time = request.form['time']
        message = request.form['message']

        # Here you can save the form data to a database or send an email
        print(f"Appointment booked by {name}, {email}, {phone}, {date}, {time}, {message}")

        return redirect(url_for('thank_you'))  # Redirect to a thank you page

    return render_template('appointment.html')


@app.route('/thank-you')
def thank_you():
    return "<h2>Thank you for booking your appointment!</h2>"


if __name__ == '__main__':
    app.run(debug=True)
