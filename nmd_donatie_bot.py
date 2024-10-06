import imaplib
import email
import sqlite3
import time
from lxml import html
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, IMAP_SERVER, IMAP_PORT
import re

# Connect to the IMAP server and select the inbox
def connect_to_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select('inbox')
        return mail
    except Exception as e:
        print(f"Error: {e}")
        return None

# Read and process emails
def read_email():
    mail = connect_to_email()
    if not mail:
        return

    print("Application is running... waiting for new emails.")

    try:
        # Search for all emails in the inbox
        status, messages = mail.search(None, 'ALL')
        if status != 'OK':
            return
        
        email_ids = messages[0].split()

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg['subject'].strip().lower()

                    match = re.search(r"nieuwe donatie nmd foundation - (\d{4})", subject)
                    if match:
                        email_id_number = match.group(1)  # Extract the 4 digits

                        if is_email_id_processed(email_id_number):
                            continue

                        extract_donation_info(msg, email_id_number)
    except Exception as e:
        print(f"Error: {e}")
        pass

# Extract donation information from the email using XPath
def extract_donation_info(msg, email_id_number):
    try:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/html':
                    email_body = part.get_payload(decode=True).decode()
                    tree = html.fromstring(email_body)

                    # Extract fields with refined XPath
                    voornaam = tree.xpath("//font[strong[contains(text(),'Voornaam')]]/following::font[1]/text()")
                    achternaam = tree.xpath("//font[strong[contains(text(),'Achternaam')]]/following::font[1]/text()")
                    telefoon = tree.xpath("//font[strong[contains(text(),'Telefoon')]]/following::font[1]/text()")

                    # Fix the product XPath to capture the entire product name
                    products = tree.xpath("//td[strong[contains(@style,'color:#bf461e')]]/strong/text()")
                    products = [' '.join(product.split()) for product in products]  # Clean whitespace
                    prices = tree.xpath("//td[strong[contains(@style,'color:#bf461e')]]/following::td[3]/text()")
                    prices = [price.replace("\n", "").replace(" ", "").strip() for price in prices]  # Clean up prices

                    if voornaam and achternaam and telefoon and products and prices:
                        # Iterate over each product and price, and log each product separately
                        for product, price in zip(products, prices):
                            product = product.strip()
                            price = price.replace("€", "").strip()  # Make sure there's no extra € symbol in price
                            
                            # Determine the channel based on the product type
                            if "met pomp" in product.lower():
                                channel = "Su Kuyusu"
                            elif "sadaqa" in product.lower():
                                channel = "Sadaqa"
                            else:
                                channel = "Donatie"  # Default channel

                            # Format the output for each product individually with the channel information
                            message = f"{voornaam[0]} {achternaam[0]} - {product} (€{price}) - {telefoon[0]} => Wordt verzonden naar kanaal \"{channel}\""
                            print(message)

                            # Save each product to the database
                            save_donation_to_db((voornaam[0], achternaam[0], product, f"€{price}", telefoon[0], email_id_number))
    except Exception as e:
        print(f"Error: {e}")
        pass

# Save donation and email ID to SQLite database
def save_donation_to_db(donation):
    try:
        connection = sqlite3.connect('donations.db')
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voornaam TEXT,
            achternaam TEXT,
            type TEXT,
            bedrag TEXT,
            telefoonnummer TEXT,
            email_id_number TEXT  -- This will store the unique email ID
        )
        ''')

        cursor.execute('''
        INSERT INTO donations (voornaam, achternaam, type, bedrag, telefoonnummer, email_id_number)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', donation)

        connection.commit()
        connection.close()
    except sqlite3.IntegrityError:
        print(f"Error: Email ID {donation[-1]} is already in the database.")
    except Exception as e:
        print(f"Error saving to database: {e}")
        pass

# Check if the email ID has already been processed
def is_email_id_processed(email_id_number):
    try:
        connection = sqlite3.connect('donations.db')
        cursor = connection.cursor()

        cursor.execute('''
        SELECT COUNT(*) FROM donations WHERE email_id_number = ?
        ''', (email_id_number,))

        result = cursor.fetchone()[0]
        connection.close()

        return result > 0  # Return True if the email ID exists, False otherwise
    except Exception as e:
        print(f"Error checking email ID: {e}")
        return False

# Main loop to continuously check for new emails
def main():
    print("Started application")  # Log when the application starts
    while True:
        read_email()
        time.sleep(10)  # Check every 10 seconds, This needs to be configured after discussion with stakeholders.

if __name__ == "__main__":
    main()
