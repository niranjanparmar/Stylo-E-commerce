from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify

auth = Blueprint('auth', __name__)

# ---------------- LOGIN PAGE ----------------
@auth.route('/login')
def login():
    return render_template('login.html')


# ---------------- SIGNUP PAGE ----------------
@auth.route('/signup')
def signup():
    return render_template('signup.html')


# ---------------- FIREBASE → FLASK SESSION ----------------
@auth.route('/set_session', methods=['POST'])
def set_session():
    data = request.get_json()

    if not data or 'user_email' not in data:
        return jsonify({'status': 'error', 'message': 'Email missing'}), 400

    # save user in flask session
    session['user'] = data['user_email']

    return jsonify({'status': 'success'}), 200


# ---------------- LOGOUT ----------------
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.home'))
