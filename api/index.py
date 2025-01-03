from defect_finder.wsgi import application
from mangum import Mangum

# Configure Mangum handler with WSGI application
handler = Mangum(application, lifespan="off")

# Main handler function for Vercel
def main(event, context):
    """
    Main handler for Vercel serverless function
    """
    return handler(event, context)