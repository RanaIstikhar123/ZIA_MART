KONG_ADMIN_URL="http://localhost:8001"

# Wait for Kong to be ready
until $(curl --output /dev/null --silent --head --fail $KONG_ADMIN_URL); do
  printf '.'
  sleep 5
done

# Register Product Service
echo "Registering Product Service..."
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=product_service" \
  --data "url=http://host.docker.internal:8007"

# Product Service Routes
curl -i -X POST $KONG_ADMIN_URL/services/product_service/routes \
  --data "paths[]=/products" \
  --data "strip_path=true"  # API routes

# Swagger UI for Product Service (strip_path=false)
curl -i -X POST $KONG_ADMIN_URL/services/product_service/routes \
  --data "paths[]=/product/docs" \
  --data "strip_path=false"  # Swagger documentation

# CRUD Operations for Product Service
curl -i -X POST $KONG_ADMIN_URL/services/product_service/routes \
  --data "paths[]=/products" \
  --data "strip_path=true"  # POST
curl -i -X GET $KONG_ADMIN_URL/services/product_service/routes \
  --data "paths[]=/products" \
  --data "strip_path=true"  # GET
curl -i -X PUT $KONG_ADMIN_URL/services/product_service/routes \
  --data "paths[]=/products/{id}" \
  --data "strip_path=true"  # PUT
curl -i -X DELETE $KONG_ADMIN_URL/services/product_service/routes \
  --data "paths[]=/products/{id}" \
  --data "strip_path=true"  # DELETE

# Register Order Service
echo "Registering Order Service..."
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=order_service" \
  --data "url=http://host.docker.internal:8008"

# Order Service Routes
curl -i -X POST $KONG_ADMIN_URL/services/order_service/routes \
  --data "paths[]=/order" \
  --data "strip_path=true"  # API routes

# Swagger UI for Order Service (strip_path=false)
curl -i -X POST $KONG_ADMIN_URL/services/order_service/routes \
  --data "paths[]=/order/docs" \
  --data "strip_path=false"  # Swagger documentation

# CRUD Operations for Order Service
curl -i -X POST $KONG_ADMIN_URL/services/order_service/routes \
  --data "paths[]=/order" \
  --data "strip_path=true"  # POST
curl -i -X GET $KONG_ADMIN_URL/services/order_service/routes \
  --data "paths[]=/order" \
  --data "strip_path=true"  # GET
curl -i -X PUT $KONG_ADMIN_URL/services/order_service/routes \
  --data "paths[]=/order/{id}" \
  --data "strip_path=true"  # PUT
curl -i -X DELETE $KONG_ADMIN_URL/services/order_service/routes \
  --data "paths[]=/order/{id}" \
  --data "strip_path=true"  # DELETE

# Register Payment Service
echo "Registering Payment Service..."
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=payment_service" \
  --data "url=http://host.docker.internal:8003"

# Payment Service Routes
curl -i -X POST $KONG_ADMIN_URL/services/payment_service/routes \
  --data "paths[]=/payment" \
  --data "strip_path=true"  # API routes

# Swagger UI for Payment Service (strip_path=false)
curl -i -X POST $KONG_ADMIN_URL/services/payment_service/routes \
  --data "paths[]=/payment/docs" \
  --data "strip_path=false"  # Swagger documentation

# CRUD Operations for Payment Service
curl -i -X POST $KONG_ADMIN_URL/services/payment_service/routes \
  --data "paths[]=/payment" \
  --data "strip_path=true"  # POST
curl -i -X GET $KONG_ADMIN_URL/services/payment_service/routes \
  --data "paths[]=/payment" \
  --data "strip_path=true"  # GET
curl -i -X PUT $KONG_ADMIN_URL/services/payment_service/routes \
  --data "paths[]=/payment/{id}" \
  --data "strip_path=true"  # PUT
curl -i -X DELETE $KONG_ADMIN_URL/services/payment_service/routes \
  --data "paths[]=/payment/{id}" \
  --data "strip_path=true"  # DELETE

# Register Notification Service
echo "Registering Notification Service..."
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=notification_service" \
  --data "url=http://host.docker.internal:8004"

# Notification Service Routes
curl -i -X POST $KONG_ADMIN_URL/services/notification_service/routes \
  --data "paths[]=/notification" \
  --data "strip_path=true"  # API routes

# Swagger UI for Notification Service (strip_path=false)
curl -i -X POST $KONG_ADMIN_URL/services/notification_service/routes \
  --data "paths[]=/notification/docs" \
  --data "strip_path=false"  # Swagger documentation

# CRUD Operations for Notification Service
curl -i -X POST $KONG_ADMIN_URL/services/notification_service/routes \
  --data "paths[]=/notification" \
  --data "strip_path=true"  # POST
curl -i -X GET $KONG_ADMIN_URL/services/notification_service/routes \
  --data "paths[]=/notification" \
  --data "strip_path=true"  # GET
curl -i -X PUT $KONG_ADMIN_URL/services/notification_service/routes \
  --data "paths[]=/notification/{id}" \
  --data "strip_path=true"  # PUT
curl -i -X DELETE $KONG_ADMIN_URL/services/notification_service/routes \
  --data "paths[]=/notification/{id}" \
  --data "strip_path=true"  # DELETE

# Register Inventory Service
echo "Registering Inventory Service..."
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=inventory_service" \
  --data "url=http://host.docker.internal:8005"

# Inventory Service Routes
curl -i -X POST $KONG_ADMIN_URL/services/inventory_service/routes \
  --data "paths[]=/inventory" \
  --data "strip_path=true"  # API routes

# Swagger UI for Inventory Service (strip_path=false)
curl -i -X POST $KONG_ADMIN_URL/services/inventory_service/routes \
  --data "paths[]=/inventory/docs" \
  --data "strip_path=false"  # Swagger documentation

# CRUD Operations for Inventory Service
curl -i -X POST $KONG_ADMIN_URL/services/inventory_service/routes \
  --data "paths[]=/inventory" \
  --data "strip_path=true"  # POST
curl -i -X GET $KONG_ADMIN_URL/services/inventory_service/routes \
  --data "paths[]=/inventory" \
  --data "strip_path=true"  # GET
curl -i -X PUT $KONG_ADMIN_URL/services/inventory_service/routes \
  --data "paths[]=/inventory/{id}" \
  --data "strip_path=true"  # PUT
curl -i -X DELETE $KONG_ADMIN_URL/services/inventory_service/routes \
  --data "paths[]=/inventory/{id}" \
  --data "strip_path=true"  # DELETE

# Register User Service
echo "Registering User Service..."
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=user_service" \
  --data "url=http://host.docker.internal:8006"

# User Service Routes
curl -i -X POST $KONG_ADMIN_URL/services/user_service/routes \
  --data "paths[]=/user" \
  --data "strip_path=true"  # API routes

# Swagger UI for User Service (strip_path=false)
curl -i -X POST $KONG_ADMIN_URL/services/user_service/routes \
  --data "paths[]=/user/docs" \
  --data "strip_path=false"  # Swagger documentation

# CRUD Operations for User Service
curl -i -X POST $KONG_ADMIN_URL/services/user_service/routes \
  --data "paths[]=/user" \
  --data "strip_path=true"  # POST
curl -i -X GET $KONG_ADMIN_URL/services/user_service/routes \
  --data "paths[]=/user" \
  --data "strip_path=true"  # GET
curl -i -X PUT $KONG_ADMIN_URL/services/user_service/routes \
  --data "paths[]=/user/{id}" \
  --data "strip_path=true"  # PUT
curl -i -X DELETE $KONG_ADMIN_URL/services/user_service/routes \
  --data "paths[]=/user/{id}" \
  --data "strip_path=true"  # DELETE

# Register kong-spec-expose plugin
curl -i -X POST http://localhost:8001/services/spec-server/plugins \
  --data "name=kong-spec-expose" \
  --data "config.spec_url=http://localhost:8000/merge/openapi.json"

echo "All services, routes, and Swagger UI have been registered successfully."
