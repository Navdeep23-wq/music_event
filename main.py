from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Event, Genre, Booking, Comment, db
from forms import CreateEventForm
from utils import save_image
import os
import logging

main = Blueprint('main', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@main.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()
    form.genre_id.choices = [(g.id, g.name) for g in Genre.query.order_by('name')]
    
    if form.validate_on_submit():
        try:
            event = Event(
                name=form.name.data,
                genre_id=form.genre_id.data,
                date=form.date.data,
                location=form.location.data,
                price=form.price.data,
                capacity=form.capacity.data,
                description=form.description.data,
                user_id=current_user.id
            )
            
            if form.image.data:
                try:
                    filename = save_image(form.image.data)
                    event.image_url = filename
                except Exception as img_error:
                    logger.error(f"Failed to save image: {str(img_error)}")
                    flash('Error processing image. Please try again with a different file.', 'warning')
            
            db.session.add(event)
            db.session.commit()  # Fixed typo from 'comml' to 'commit'
            
            flash('Event created successfully!', 'success')
            return redirect(url_for('main.event_details', event_id=event.id))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating event: {str(e)}", exc_info=True)
            flash('Error creating event. Please try again.', 'danger')
    
    return render_template('create_event.html', form=form)

# Other routes would go here...
