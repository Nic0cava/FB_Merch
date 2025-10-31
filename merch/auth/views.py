from flask import render_template, redirect, url_for, request, session, flash
import os
from . import auth
from merch.models import AppAuth
from merch import db
from .forms import LoginForm, ChangePasswordForm


def is_admin_password(pw: str) -> bool:
    admin_pw = os.getenv('ADMIN_BYPASS_PASSWORD')
    return bool(admin_pw) and pw == admin_pw


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next_url = request.args.get('next')

    if form.validate_on_submit():
        password = form.password.data
        # Admin bypass login
        if is_admin_password(password):
            session.clear()
            session['authed'] = True
            session['is_admin'] = True
            flash('Signed in (admin bypass)', 'warning')
            return redirect(next_url or url_for('core.index'))
        if AppAuth.verify_password(password):
            session['authed'] = True
            flash('Signed in', 'success')
            return redirect(next_url or url_for('core.index'))
        else:
            flash('Invalid password', 'danger')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    session.pop('authed', None)
    session.pop('is_admin', None)
    flash('Signed out', 'success')
    return redirect(url_for('auth.login'))


@auth.route('/change-password', methods=['GET', 'POST'])
def change_password():
    # Require a logged-in session
    if not session.get('authed'):
        return redirect(url_for('auth.login', next=url_for('auth.change_password')))

    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_ok = (
            session.get('is_admin')
            or is_admin_password(form.current_password.data)
            or AppAuth.verify_password(form.current_password.data)
        )
        if not current_ok:
            flash('Current password is incorrect', 'danger')
        else:
            AppAuth.set_password(form.new_password.data)
            flash('Password updated successfully', 'success')
            return redirect(url_for('core.index'))

    return render_template('auth/change_password.html', form=form)
