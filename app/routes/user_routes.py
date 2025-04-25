from flask import Blueprint, render_template, redirect, url_for, flash, session, request, current_app
from app.forms import UserForm, MessageForm, ContributionForm
from app.models import db, User, Message, Contribution
import requests
import base64
from datetime import datetime
import json

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET', 'POST'])
def landing_page():
    form = UserForm()
    if form.validate_on_submit():
        # Check if user exists, otherwise create new
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = User(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data
            )
            db.session.add(user)
            db.session.commit()
        
        # Store user_id in session
        session['user_id'] = user.id
        return redirect(url_for('user.message_page'))
    
    return render_template('landing.html', form=form)

@user_bp.route('/message', methods=['GET', 'POST'])
def message_page():
    if 'user_id' not in session:
        flash('Please register first.', 'warning')
        return redirect(url_for('user.landing_page'))
    
    form = MessageForm()
    user = User.query.get(session['user_id'])
    
    if form.validate_on_submit():
        message = Message(
            content=form.content.data,
            user_id=user.id
        )
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('user.contribute'))
    
    return render_template('message.html', form=form, user=user)

@user_bp.route('/contribute', methods=['GET', 'POST'])
def contribute():
    if 'user_id' not in session:
        flash('Please register first.', 'warning')
        return redirect(url_for('user.landing_page'))
    
    form = ContributionForm()
    user = User.query.get(session['user_id'])
    
    if form.validate_on_submit():
        # For demonstration, create a contribution record
        contribution = Contribution(
            amount=form.amount.data,
            transaction_id=f"DEMO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            status='pending',
            user_id=user.id
        )
        db.session.add(contribution)
        db.session.commit()
        
        # In a real app, initiate MPESA STK Push here
        try:
            # Add MPESA integration code here if available
            # For demo purposes, we'll just set the status to completed
            contribution.status = 'completed'
            db.session.commit()
            flash('Thank you for your contribution!', 'success')
        except Exception as e:
            flash(f'Error processing payment: {str(e)}', 'danger')
        
        return redirect(url_for('user.thank_you'))
    
    return render_template('contribute.html', form=form, user=user)

@user_bp.route('/thank-you')
def thank_you():
    if 'user_id' not in session:
        return redirect(url_for('user.landing_page'))
    
    user = User.query.get(session['user_id'])
    return render_template('thank_you.html', user=user)

# Helper function for MPESA integration (to be implemented with actual API)
def get_mpesa_access_token():
    consumer_key = current_app.config['MPESA_CONSUMER_KEY']
    consumer_secret = current_app.config['MPESA_CONSUMER_SECRET']
    api_url = f"{current_app.config['MPESA_API_URL']}/oauth/v1/generate?grant_type=client_credentials"
    
    # Encode credentials
    auth_string = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode('utf-8')
    
    headers = {
        'Authorization': f"Basic {auth_string}"
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response_data = response.json()
        return response_data.get('access_token')
    except:
        return None