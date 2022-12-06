# product-importer
# Objective

Acme Inc needs to be able to import products from a CSV file and into their SQL database. Given there are half a million
products to be imported into the database, ACME Inc wants you to develop robust and scale APIs for the same
Specification

## STORY 1:
As an API user, I should be able to upload a large CSV file of 500K products (see here). If there are existing duplicates,
it should overwrite the data. Deduplication can be done using the SKU of the product. SKU is case insensitive.
Though not in the CSV file, some products should be active and others should be inactive. The SKU is expected to be
unique.
Develop API endpoint(s) for the same. Note that the API should consider scalability and be well optimized in terms
of resource consumption as well.

### STORY 1A:
There should be an endpoint to track the progress of the file upload. The most commonly used implementation is SSE
but feel free to explore other options as well.

### STORY 2:
As an API user, I should be able to perform all the CRUD operations for the products. This is preferably on a URL like
/products.
The GET endpoint should also support filtering the products by SKU, name, active and description. The endpoint should
also support pagination.

### STORY 3:
As an API user, it should be possible to delete ALL existing products

### STORY 4:
As an API user, it should be able to configure multiple webhooks which should be triggered when product is created
and updated using the endpoints developed in Story 2
Note: Design should be scalable and should not impact application performance.
