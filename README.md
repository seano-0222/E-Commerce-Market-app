# E-Commerce Market App

A collaborative Django e-commerce web application built as a group project, where each team member is responsible for a specific app module.

---

## Group Members & Responsibilities

| Member | App Module | Models |
|--------|-----------|--------|
| **Tormes** | `accounts` | Person, Customer, Vendor |
| **Alipin** | `categories`, `products`, `reviews` | Category, Product, Discount, Review |
| **Malubay** | `cart` | Cart, CartItem |
| **Capendit** | `orders` | Platform, Order, OrderItem, Payment, Shipment |
| **Capuras** | `inventory` | Warehouse, Inventory |

---

## Tech Stack

- **Backend:** Django 6.0.4
- **Language:** Python 3.14
- **Database:** SQLite
- **Frontend:** HTML, CSS (Inter font via Google Fonts)

---

## Project Structure

```
E-Commerce Market app/
├── ecommerce/              # Project settings, root URLs, WSGI
├── accounts/               # Person, Customer, Vendor identity system
├── categories/             # Product categories
├── products/               # Products and discounts
├── reviews/                # Customer product reviews
├── cart/                   # Shopping cart and cart items
├── orders/                 # Orders, payments, and shipments
├── inventory/              # Warehouse and stock management
└── manage.py
```

---

## App Modules

### accounts (Tormes)
- **Person** — base identity (first name, last name, email, address)
- **Customer** — OneToOne → Person
- **Vendor** — OneToOne → Person (with store name)
- Includes registration forms and login/logout views
- Validation enforces a Person can only be a Customer OR a Vendor, not both

### categories & products (Alipin)
- **Category** — name, description
- **Product** — name, description, price, stock quantity, FK → Category
- **Discount** — ManyToMany → Product, with percentage and date range
- Views for product listing, detail, and filtering by category

### reviews (Alipin)
- **Review** — rating (1–5), comment, FK → Customer, FK → Product
- One review per customer per product enforced at model level

### cart (Malubay)
- **Cart** — OneToOne → Customer
- **CartItem** — FK → Cart, FK → Product, quantity
- Validates quantity against product stock level

### orders (Capendit)
- **Platform** — marketplace platform (e.g. web, mobile)
- **Order** — FK → Customer, FK → Platform, status, total amount
- **OrderItem** — FK → Order, FK → Product, quantity, price
- **Payment** — OneToOne → Order, method, amount
- **Shipment** — FK → Order, status, delivery address

### inventory (Capuras)
- **Warehouse** — name, location, capacity
- **Inventory** — OneToOne → Product, FK → Warehouse, stock level, reorder threshold
- Auto-flags items at or below reorder threshold as low stock

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/seano-0222/E-Commerce-Market-app.git
cd "E-Commerce Market app"
```

### 2. Install dependencies
```bash
pip install django
```

### 3. Apply migrations
```bash
python manage.py migrate
```

### 4. Create a superuser
```bash
python manage.py createsuperuser
```

### 5. Run the development server
```bash
python manage.py runserver
```

Then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## URL Routes

| URL | View |
|-----|------|
| `/` | Home / index |
| `/login/` | Login |
| `/logout/` | Logout |
| `/register/person/` | Register Person |
| `/register/customer/` | Register Customer |
| `/register/vendor/` | Register Vendor |
| `/categories/` | Category list |
| `/products/` | Product list |
| `/cart/` | View cart |
| `/orders/` | Order list |
| `/inventory/` | Inventory list |
| `/inventory/warehouses/` | Warehouse list |
| `/admin/` | Django admin panel |

---

## Admin Panel

All models are registered in the Django admin with appropriate list displays, filters, search fields, and inline views.

Default superuser (development only):
- **Username:** `admin`
- **Password:** `admin123`

---

## Git Branches

| Branch | Member | Status |
|--------|--------|--------|
| `main` | Tormes | Active — all apps integrated |
| `Alipin` | Alipin | Merged |
| `Malubay` | Malubay | Integrated |
| `Capendit` | Capendit | Integrated (manual extract) |
| `Capuras` | Capuras | Integrated (manual extract) |
