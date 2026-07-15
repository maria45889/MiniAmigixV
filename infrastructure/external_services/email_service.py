"""
Email Service

Service for sending emails.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import os


class EmailServiceInterface(ABC):
    """Interface for email service."""
    
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str, html: bool = False) -> bool:
        """Send an email."""
        pass
    
    @abstractmethod
    def send_bulk_email(self, recipients: List[str], subject: str, body: str, html: bool = False) -> int:
        """Send bulk emails."""
        pass


class EmailService(EmailServiceInterface):
    """
    Concrete implementation of email service using Django's email backend.
    """
    
    def __init__(self):
        """Initialize the email service."""
        from django.core.mail import get_connection
        self.connection = get_connection()
    
    def send_email(self, to: str, subject: str, body: str, html: bool = False) -> bool:
        """
        Send an email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            html: Whether body is HTML
            
        Returns:
            True if sent successfully
        """
        try:
            from django.core.mail import EmailMessage, EmailMultiAlternatives
            
            if html:
                msg = EmailMultiAlternatives(subject, body, to=[to])
                msg.attach_alternative(body, "text/html")
            else:
                msg = EmailMessage(subject, body, to=[to])
            
            msg.send()
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_bulk_email(self, recipients: List[str], subject: str, body: str, html: bool = False) -> int:
        """
        Send bulk emails.
        
        Args:
            recipients: List of recipient email addresses
            subject: Email subject
            body: Email body
            html: Whether body is HTML
            
        Returns:
            Number of successfully sent emails
        """
        success_count = 0
        
        for recipient in recipients:
            if self.send_email(recipient, subject, body, html):
                success_count += 1
        
        return success_count
    
    def is_available(self) -> bool:
        """Check if the service is available."""
        return os.getenv('EMAIL_HOST') is not None
