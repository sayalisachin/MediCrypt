import logging

logging.basicConfig(filename='audit.log', level=logging.INFO)

def log_action(action, user):
    logging.info(f"{user} performed action: {action}")
