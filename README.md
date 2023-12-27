# Product Importer System

# Objective:
A comprehensive product importing system is needed to seamlessly import products from a CSV file into an SQL database. With a substantial volume of half a million products, the challenge is to develop robust and scalable APIs to handle this data migration efficiently.

## System Requirements:

    1. CSV File Import:
        Implement an API endpoint that allows users to upload a large CSV file containing 500K products.
        Ensure that the system can handle duplicates by overwriting existing data, with deduplication based on the SKU of the product (SKU is case insensitive).
        Assign activity status (active or inactive) to products, even if this information is not explicitly present in the CSV file.
        Design the API with a focus on scalability and resource optimization.

    2. Upload Progress Tracking:
        Create an endpoint to track the progress of the file upload.
        Consider various options for implementation, such as Server-Sent Events (SSE) or other alternatives.

    3. CRUD Operations for Products:
        Enable API users to perform all CRUD (Create, Read, Update, Delete) operations for products.
        Design the API to be accessible through a URL like /products.
        Implement a GET endpoint that supports filtering products by SKU, name, activity status, and description.
        Provide support for pagination to enhance user experience.

    4. Bulk Deletion of Products:
        Implement functionality that allows users to delete ALL existing products through the API.

    5. Webhook Configuration:
        Enable API users to configure multiple webhooks that trigger when a product is created or updated using the endpoints developed in Requirement 3.
        Emphasize a scalable design that does not negatively impact application performance.


