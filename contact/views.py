import requests
from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactFormSerializer  # renamed for consistency

class ContactFormView(APIView):
    def post(self, request):
        serializer = ContactFormSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            sender_name = data.get("name")
            sender_email = data.get("email")
            phone = data.get("phone", "")
            service_type = data.get("serviceType", "")
            availability = data.get("availability", "")
            message = data.get("message", "").replace("\n", "<br>")

            payload = {
                "sender": {
                    "name": "New Appointment Alert – PricePersonalHealthcare",
                    "email": config("DEFAULT_FROM_EMAIL")
                },
                "to": [
                    {
                        "email": config("NOTIFY_EMAIL"),
                        "name": "pricepersonalhealthcare"
                    }
                ],
                "subject": "Appointment Request Submission 📩",
                "htmlContent": f"""
                    <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f9f9f9; border-radius: 5px;">
                        <h2 style="color: #333;">Someone Just Requested a Consultation</h2>
                        <p style="font-size: 16px; color: #555;">You have received a new appointment from your website contact form:</p>
                        <div style="background-color: #fff; border: 1px solid #ddd; padding: 20px; border-radius: 5px;">
                            <p><strong style="color: #333;">Name:</strong> {sender_name}</p>
                            <p><strong style="color: #333;">Email:</strong> {sender_email}</p>
                            <p><strong style="color: #333;">Phone:</strong> {phone}</p>
                            <p><strong style="color: #333;">Service Type:</strong> {service_type}</p>
                            <p><strong style="color: #333;">Availability:</strong> {availability}</p>
                            <p><strong style="color: #333;">Message:</strong></p>
                            <div style="background-color: #f1f1f1; border: 1px solid #ddd; padding: 18px; margin-top: 10px;">
                                {message}
                            </div>
                        </div>
                        <p style="margin-top: 20px; font-size: 14px; color: #999;">This message was sent via the website contact form.</p>
                    </div>
                """
            }

            headers = {
                "accept": "application/json",
                "api-key": config("BREVO_API_KEY"),
                "content-type": "application/json"
            }

            try:
                response = requests.post(
                    "https://api.brevo.com/v3/smtp/email",
                    json=payload,
                    headers=headers
                )

                if response.status_code == 201:
                    return Response({"message": "Message sent successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "error": "Failed to send email.",
                        "details": response.json()
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
