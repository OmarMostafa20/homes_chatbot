from flask import request, jsonify

from app.models import Customer, db
from localization import message_locale

# Route to create a new user
def create_user():
    """
    Create a new user if the phone number is not already in the database
    and return a JSON response with a success message and the new user's
    phone number and full name.
    """
    data = request.get_json()

    # Check that required fields are provided using set operations
    required_fields = {"device_id", "phone", "first_name", "last_name"}
    if not required_fields <= data.keys():
        return jsonify({"error": message_locale("MISSING_REQUIRED_FIELDS", "en")}), 400

    device_id = data.get('device_id')

    # Use optimized query filter instead of `get()`
    existing_customer = Customer.query.filter_by(device_id=device_id).first()

    if existing_customer:
        return jsonify({"message": "User Already Exists", 
                        "device_id": existing_customer.device_id, 
                        "phone": existing_customer.customer_number,
                        "username": f"{existing_customer.first_name} {existing_customer.last_name}"}), 200
    
    # Create a new customer if not exists
    customer = Customer(
        device_id=device_id,
        customer_number=data.get("phone"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
    )
    db.session.add(customer)
    db.session.commit()

    return jsonify({
        "message": "User Created", 
        "device_id": customer.device_id,
        "phone": customer.customer_number, 
        "username": f"{customer.first_name} {customer.last_name}"
    }), 201
