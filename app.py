import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

USERS = {
    'admin': 'password123',
    'user': 'demo123'
}

API_KEY = 'q5qsMRSkO4sqRrq+3acu9w==ZON0fjUFGYLBlBQj'  # your API Ninjas key

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['user'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out!', 'info')
    return redirect(url_for('home'))

# 🔷 Animal search route
@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        flash("Please enter an animal name to search.", "warning")
        return redirect(url_for('home'))
    
    api_url = f'https://api.api-ninjas.com/v1/animals?name={query}'
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    
    if response.status_code == 200:
        data = response.json()
        if not data:
            flash(f"No information found for '{query}'.", "info")
            return redirect(url_for('home'))
        return render_template('search_results.html', animal=data[0])
    else:
        flash(f"Error fetching data from API: {response.status_code}", "danger")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)
