import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactFormSerializer
from django.conf import settings

class ContactFormView(APIView):
    def post(self, request):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            # Send to Brevo API
            response = requests.post(
                "https://api.brevo.com/v3/smtp/email",
                headers={
                    "api-key": settings.BREVO_API_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "sender": {"name": "Your Company", "email": "you@yourdomain.com"},
                    "to": [{"email": "recipient@yourdomain.com"}],
                    "replyTo": {"email": data['email'], "name": data['name']},
                    "subject": "New Consultation Request",
                    "htmlContent": f"""
                        <h3>New Contact Form Submission</h3>
                        <p><strong>Name:</strong> {data['name']}</p>
                        <p><strong>Phone:</strong> {data['phone']}</p>
                        <p><strong>Email:</strong> {data['email']}</p>
                        <p><strong>Service Type:</strong> {data['serviceType']}</p>
                        <p><strong>Availability:</strong> {data['availability']}</p>
                        <p><strong>Message:</strong> {data['message']}</p>
                    """
                }
            )
            if response.status_code in [200, 201]:
                return Response({"message": "Sent successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
