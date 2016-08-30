def message_order_device(data):
    """Prepare message to send in email."""
    msg = "<h1>NEW ORDER DEVICE</h1>" \
          "Email: {0}<br/>" \
          "First Name: {1}<br/>" \
          "Last Name: {2}<br/>" \
          "address: {3}<br/>" \
          "Phone Number: {4}<br/>" \
          "Payment Type: {5}<br/>" \
          "paid: {6}<br/>" \
          "Date Request: {7}<br/>".format(data.user.email,
                                          data.user.first_name,
                                          data.user.last_name,
                                          data.address,
                                          data.phone_number,
                                          data.get_payment_display(),
                                          data.get_paid_display(),
                                          data.date_request.strftime('%Y-%m-%d'))

    return msg


def send_application_email(msg, subject):  # pragma: no cover
    """send email."""
    return True
