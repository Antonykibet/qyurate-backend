from Orders.models import OrderNotificationLog, Order
from business_partner.models import SiteConfigs
from common.utils import send_email
import logging

LOGGER = logging.getLogger(__name__)

def prepare_order_notification(order, shop):
    """
    Sends notification either via email or wozzap to admin.
    This function implements a SAGA pattern to gurantee reliable delivery of notifications
    
    :param order: Description
    """
    try:
        data = {}
        site_config = SiteConfigs.objects.filter(shop=shop).first()
        data['order'] = order
        data['notification_method'] = site_config.notification_method
        if site_config.notification_method == 'EMAIL':
            data['contact_info'] = site_config.email
        if site_config.notification_method == 'WOZZAP':
            data['contact_info'] = site_config.phone_contact
        data['message'] = f"New order received!\nOrder code: {order.code}\nCustomer: {order.customer_name}\nTotal Price: {order.total_price()}\nStatus: {order.status}"

        OrderNotificationLog.objects.create(**data)
    except Exception:
        LOGGER.error('Failed to prepare order notification',order.guid, exc_info=True)
        
def send_order_notification_via_wozzap(notification, to):
    pass

def send_order_notification_via_email(notification, to):
    subject = f"New Order Received - {notification.order.code}"
    body = f"ORDER:\n\n{notification.message}\n\nThis email was..."
    html_body = """
    <html>
        <body>
            <h1 style="color: #2e6c80;">ORDER:</h1>
            <p>This email was...</p>
        </body>
    </html>
    """

    send_email(subject, body, to, html=True, html_body=html_body)

def send_order_notification(order, contact):
    try:
        notification = OrderNotificationLog.objects.filter(order=order, status__in=['PENDING', 'FAILED']).first()
        if not notification:
            LOGGER.warning('No order notification for order found', order.guid)
            return
        
        if notification.notification_method == 'WOZZAP':
            send_order_notification_via_wozzap(notification, contact)
        else:
            send_order_notification_via_email(notification, contact)

        notification.status = 'SUCCESS'
        notification.save()
        LOGGER.info('Order notification sent successfully', order.guid)
    except Exception as e:
        notification.status = 'FAILED'
        notification.error_message = str(e)
        notification.save()
        LOGGER.error('Failed to send order notification', order.guid, exc_info=True)

def generate_order_code():
    import random
    import string
    length = 8
    characters = string.ascii_uppercase + string.digits
    order_code = ''.join(random.choice(characters) for _ in range(length))
    code_exists=Order.objects.filter(code=order_code).exists()
    if code_exists:
        return generate_order_code()
    return order_code