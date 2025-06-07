from flask import render_template, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from models import Event, Genre, db
from forms import CreateEventForm

def create_event():
    form = CreateEventForm()
    
    # Populate genre choices
    form.genre_id.choices = [(g.id, g.name) for g in Genre.query.order_by('name')]
    
    if form.validate_on_submit():
        try:
            # Handle image upload
            image_filename = None
            if form.image.data:
                image = form.image.data
                filename = secure_filename(image.filename)
                unique_filename = f"{datetime.now().timestamp()}_{filename}"
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                image.save(image_path)
                image_filename = unique_filename
            
            # Create new event
            event = Event(
                name=form.name.data,
                genre_id=form.genre_id.data,
                date=form.date.data,
                location=form.location.data,
                price=form.price.data,
                capacity=form.capacity.data,
                description=form.description.data,
                image_url=image_filename,
                user_id=current_user.id,
                status='Open'  # Default status for new events
            )
            
            db.session.add(event)
            db.session.commit()
            
            flash('Your event has been created successfully!', 'success')
            return redirect(url_for('main.event_details', event_id=event.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating event: {str(e)}")
            flash('An error occurred while creating your event. Please try again.', 'danger')
    
    return render_template('create_event.html', form=form)