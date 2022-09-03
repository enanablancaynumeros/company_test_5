# Phone billing system

Implement a very simple phone billing system as a microservice using python.
- The microservice must be able to:
- Receive number of minutes for each customer call
- Provide the call history by user
- Calculate the period total and generate the invoice for a customer
To keep it simple we will consider we are handling only postpaid monthly plans and a flat rate of US$
0.02 per minute.

Other requirements:
- The system must have a database where call history and invoices are stored (you can use any
database).
- You can use any framework you believe best fits to the solution.
- Keep your code as clean as possible and implement unit tests.
- Provide code base and instructions to build and run your microservice.

Use cases:
- As a phone operator I want all customer calls to be charged.
- As a customer I want to be able to see my phone call history.
- As a customer I want to receive my invoice every first day of the month.

Additional task:
Describe how you would extend the solution to be able to support different billing plans like prepaid and
fixed amount per month.

## How to run

Having docker and docker-compose (1.29.2) installed run `make build up` to get the API running in the forefront.
By default, it won't have any data, and there are no endpoints to create customers and phones associated.
To be able to interact with the API, you can run `make generate_fixtures` and then go to `http://localhost:8000/docs` and use
the swagger helpers or use the endpoints directly as follows:

```bash 
curl -X 'GET' \
'http://localhost:8000/phone/1/history' \
-H 'accept: application/json'
```

To run the tests execute `make tests_docker`

## DB models

![DB entity-relation diagram](./bin/db_entities.png)