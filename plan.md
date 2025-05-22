# Plan: CalmPOS - Modern POS SaaS Platform

## 1. Introduction

### 1.1. SaaS Name
CalmPOS (hereinafter referred to as "the Platform")

### 1.2. Vision
To be the leading cloud-based Point of Sale (POS) SaaS platform in Kenya and eventually East Africa, empowering businesses of all sizes with a versatile, modular, and user-friendly solution to streamline operations, manage sales and inventory efficiently, and foster growth.

### 1.3. Goals
*   Provide a comprehensive, yet customizable POS solution adaptable to various business types (retail, food & beverage, services).
*   Ensure ease of use through an intuitive interface and quick setup process.
*   Offer robust security features to protect sensitive business and customer data.
*   Enable seamless integration with essential Kenyan financial services (M-Pesa, local banks, KRA iTax).
*   Design a modular architecture allowing businesses to subscribe only to the functionalities they need.
*   Build an API-first platform to facilitate future integrations and scalability.
*   Support multi-location businesses effectively.
*   Provide reliable offline functionality for uninterrupted sales processing.

### 1.4. Target Audience
*   **Small and Medium Enterprises (SMEs) in Kenya:** Including retail shops, restaurants, cafes, bars, service providers (salons, repair shops), and sole proprietors.
*   **Multi-location businesses:** Chains requiring centralized management.
*   Businesses seeking to modernize from manual processes or outdated POS systems.
*   Enterprises needing KRA iTax compliance and integration with local payment methods.

### 1.5. Core Design Principles
*   **API-First:** The backend will be developed with a comprehensive API, allowing the frontend and any future applications (mobile, third-party integrations) to interact seamlessly. This promotes flexibility and scalability.
*   **Modularity:** The system is broken down into core and optional standalone functional modules. Clients subscribe to modules based on their needs, ensuring they only pay for what they use.
*   **User-Centric Design:** Emphasis on an intuitive, easy-to-learn, and efficient user interface (UI) and user experience (UX), including customizable layouts for different devices.
*   **Security:** Robust security measures at all levels (data, access, payment) are paramount.
*   **Scalability:** The architecture will be designed to handle growth in users, transactions, and data. While not using microservices initially, the modular design with Django allows for logical separation that can be scaled effectively.
*   **Kenyan Focus with Global Potential:** Prioritizing features critical for the Kenyan market (M-Pesa, KRA) while building a system flexible enough (e.g., currency, language) for future international expansion.
*   **Reliability:** Ensuring high availability and dependable offline capabilities.

### 1.6. Technology Stack
*   **Backend:** Django (Python framework)
*   **Database:** PostgreSQL
*   **Frontend:** HTML, CSS (Tailwind CSS), JavaScript
*   **Deployment:** Cloud-based (specific provider TBD, e.g., AWS, Google Cloud, Azure)

## 2. Core Modules (Included in Basic Subscriptions)

These modules form the foundational functionality of the Platform and will be available to all subscribers.

### 2.1. Point of Sale (POS) / Sales Module
*   **2.1.1. Description:** The primary interface for processing sales transactions quickly and efficiently, designed for speed, flexibility, and a superior user experience. It supports concurrent order handling and extensive customization to suit various business needs and user preferences.
*   **2.1.2. Key Features:**
    *   **Intuitive and Customizable Sales Interface:**
        *   Layout presets available (touchscreen, small screen, desktop), configurable system-wide and with potential for **user-specific preference overrides** (see User Preferences below).
        *   Clean design optimized for rapid transaction processing.
    *   **Concurrent Order Processing (Tabbed/Parallel Carts):**
        *   Ability to start and manage multiple orders simultaneously. Ideal for busy environments like supermarkets where a customer's payment delay shouldn't halt other sales.
        *   **UI/UX:** The interface will support a tab-like system or easily switchable cart instances. Each "active cart" maintains its own items, customer (if attached), discounts, and payment status, allowing cashiers to seamlessly switch between them.
    *   **Rapid Item Lookup & Addition:**
        *   **UI/UX for Lookup:** Prominent, always-accessible search bar with predictive text and instant filtering by name, SKU, or category. Visual cues for search results, including product thumbnails (size customizable by user).
        *   **High-Speed Scanning:**
            *   The POS interface will be in a constant "listening" mode for scanner input when the sales screen is active. **No need to click into a search field before scanning.**
            *   A single scan immediately adds the item to the current active cart.
            *   Multiple consecutive scans of the *same item's barcode/QR code* automatically increment its quantity in the cart.
    *   **Order Processing:**
        *   Quantity modification, item notes.
    *   **Discounts, Promotions, and Coupon Management:**
        *   Item-level (percentage/fixed amount) and order-level discounts.
        *   **UI Price Display:** Clearly shows original price, discounted price (e.g., strikethrough original), and amount saved for transparency.
        *   **Coupon Code Application:** Dedicated field to apply promotional coupon codes, with real-time validation and application of associated discounts.
        *   Discount rules, promotion validity, and coupon code generation/management are configured in a separate admin/system settings section.
    *   **Multiple Payment Methods:** (cash, mobile money, cards via integrated gateways).
    *   **Split Payments:** Across multiple methods or individuals.
    *   **Digital (email/SMS) and Printed Receipt Generation:** (customizable with logo).
    *   **Offline Mode:**
        *   Allows processing of essential sales functions (e.g., add to cart, manage concurrent carts, cash payments) during internet outages.
        *   Queues transactions locally and syncs automatically once connectivity is restored.
        *   Visual indicator for offline status.
    *   **Returns and Exchanges Management:** With inventory restock options.
    *   **Transaction Hold/Park Sale:** Allows temporarily saving an in-progress order to be recalled later (distinct from concurrent carts which are actively being worked on).
    *   **Customizable Quick Select Buttons:**
        *   For frequently sold items or categories.
        *   The general availability, configuration, and default layout of these buttons are managed as a **preference option in the global admin instance settings (System Settings Module)**. Individual POS stations/users might have some display flexibility based on these global settings and their role.
    *   **Support for Barcode & QR Code Scanning:** For item identification (as described under Rapid Item Lookup).
    *   **Tip Management:** Options to add pre-set or custom tip amounts.
    *   **End-of-shift/day reconciliation:** (Z-report generation).
    *   **User-Specific POS Preferences (within User Profile):**
        *   Users can (permissions allowing) customize certain aspects of their POS view, such as:
            *   Preferred default POS layout (if multiple are assigned to their role).
            *   Size of product images in search results or quick select buttons.
            *   Density of information displayed.
*   **2.1.3. Target Industries:** Universal (Retail, Food & Beverage, Services, etc.).
*   **2.1.4. Functional Overview:** Users (cashiers, servers) log in to the POS interface. They can handle multiple customer orders concurrently, seamlessly switching between active carts. Items are added rapidly via scanning or intuitive lookup. Discounts and coupons are applied as per system configurations. The UI clearly reflects pricing. Users complete sales using various payment methods. The module updates inventory in real-time (when online, or syncs when reconnected) and records all transaction data for reporting. User preferences allow for a more personalized and efficient workspace.

### 2.2. Basic Inventory Management Module
*   **2.2.1. Description:** Manages product information and tracks stock levels.
*   **2.2.2. Key Features:**
    *   Product catalog: Add/edit products with details (name, SKU, category, supplier, purchase price, selling price, description, basic variants like size/color, images).
    *   Real-time stock level tracking: Automatically updated with each sale, return, and manual adjustment.
    *   Low stock alerts (notifications/dashboard warnings).
    *   Manual stock adjustments (e.g., for damages, discrepancies) with reason codes.
    *   **Barcode & QR Code Generation/Printing:**
        *   Generate unique barcodes (e.g., EAN-13, Code 128) for products, encoding an internal ID or SKU.
        *   Generate QR codes for products. User can choose to encode:
            *   Internal product ID/UUID (default).
            *   Product URL (for potential customer interaction).
            *   Custom defined data fields from the product model (e.g., name + price).
        *   Print barcode/QR code labels in various formats (requires compatible label printer).
    *   **Bulk CRUD Operations:**
        *   Download CSV/Excel templates for products.
        *   Upload CSV/Excel files to create, update, or delete multiple products at once.
        *   Error reporting for bulk operations (e.g., "SKU xxx already exists").
*   **2.2.3. Target Industries:** Universal, especially Retail and Food & Beverage.
*   **2.2.4. Functional Overview:** Users add their products and services into the system. As sales occur via the POS module, inventory levels are automatically decremented. Users receive alerts for low stock and can perform manual adjustments or bulk updates as needed.

### 2.3. User Management & Permissions Module
*   **2.3.1. Description:** Manages user accounts, roles, and access control throughout the Platform.
*   **2.3.2. Key Features:**
    *   **Account Types:**
        *   **Individual (Sole Proprietor):** Simplified setup, single user with full access (or predefined limited roles if they add staff).
        *   **Organization:** Hierarchical structure for multiple users, locations, and roles. Each user and organization will have a UUID field (in addition to the default Django PK) for secure, non-predictable identification.
    *   **Flexible Role Creation:** Admins can define custom roles (e.g., Cashier, Manager, Admin, Owner, Server, Stock Controller). Roles and permissions are managed via a custom Role model, with permissions as string constants (e.g., Permissions.ACCESS_BLAH_BLAH), and checked via user.has_permission(Permissions.ACCESS_BLAH_BLAH).
    *   **Granular Permissions:** Assign specific permissions to roles (e.g., view sales, process refunds, edit products, access specific reports, override prices, manage users). Permissions are tied to specific functions within modules and are easy to query.
    *   **User-Specific Overrides:** Option for an admin to grant or revoke specific permissions for an individual user, overriding their assigned role's defaults.
    *   **Secure Login Mechanisms:**
        *   Standard email and strong password authentication (email is the unique identifier).
        *   **X-digit PINs:** Configurable (e.g., 4-6 digits) for quick login/unlock at shared POS stations. Tied to a user account. PINs are securely hashed.
        *   **Multi-level Action Authorization:** Certain sensitive actions (e.g., voiding a completed transaction, applying high-value discounts, opening cash drawer without a sale) can be configured to require manager override (via PIN, password, or potentially RFID card scan).
        *   Optional Two-Factor Authentication (TFA/2FA, OTP via email or authenticator app) for admin accounts or sensitive operations. TFA can be enabled/disabled per user, and admins can require users to reset TFA or password (enforced via middleware on login).
        *   Potential for RFID card/fob scanner integration for login or quick user switching at POS stations.
    *   Basic employee clock-in/clock-out functionality (records timestamps).
    *   Comprehensive audit trails: Log significant user actions (logins, sales, voids, data changes) with timestamps and user details. Logging is detailed and handled via a dedicated model (e.g., UserActionLog).
    *   **Bulk User CRUD Operations:** Import/update users via CSV/Excel templates.
    *   **User Profile & Preferences:** Each user has a UserProfile model for additional info (avatar, preferences, etc.), and UserPreferences/OrganizationPreferences models for storing preferences.
    *   **Password Reset Tokens:** Password reset tokens/codes are tracked in a dedicated model, including expiry and usage status.
    *   **Custom User Manager:** All user creation and management is handled via a custom user manager.
    *   **Signals:** Django signals are used for post-save, post-delete, and other hooks (e.g., logging, notifications, updating related models).
    *   **Full Name:** Users have a single full_name field for flexibility (no splitting into first/middle/last names).
    *   **Superuser/Platform Admin:** Platform-level admins are handled using Django's is_staff and is_superuser fields (no extra is_platform_admin field).
*   **2.3.3. Target Industries:** Universal.
*   **2.3.4. Functional Overview:** Admins set up user accounts, assign them to predefined or custom roles, and manage their access permissions. Users log in using their credentials, and the system restricts their access and available actions based on their assigned permissions. All major models use UUIDs for secure identification. TFA, logging, and password reset enforcement are supported.

### 2.4. Basic Reporting & Analytics Module
*   **2.4.1. Description:** Provides essential insights into sales and business performance.
*   **2.4.2. Key Features:**
    *   Dashboard with key performance indicators (KPIs) like total sales, number of transactions, average transaction value.
    *   Sales Reports:
        *   Sales summary (daily, weekly, monthly, custom date range).
        *   Sales by product/category.
        *   Sales by payment type.
        *   Sales by employee/user (if applicable).
        *   Tax reports (summary of taxes collected).
    *   Basic Inventory Reports:
        *   Current stock levels.
        *   List of low-stock items.
    *   End-of-day/Shift reports (Z-reports).
    *   Data filtering and sorting options.
    *   Data export to CSV or PDF formats.
*   **2.4.3. Target Industries:** Universal.
*   **2.4.4. Functional Overview:** The module aggregates data from sales, inventory, and user activity. Authorized users can access various reports to understand business performance, identify trends, and make informed decisions.

### 2.5. System Settings & Customization Module
*   **2.5.1. Description:** Allows administrators to configure global settings and customize the Platform's appearance.
*   **2.5.2. Key Features:**
    *   Business profile setup: Business name, address, contact information, KRA PIN.
    *   **Currency Configuration:** Default to KES (Kenyan Shilling). Architecture designed to support multiple currencies for future expansion. Display formats for currency.
    *   Tax configuration: Define tax rates (e.g., VAT), apply them to products/services.
    *   Receipt template customization (add logo, custom header/footer text, terms & conditions).
    *   **Customizable Look & Feel (Whitelabeling):**
        *   Upload business logo (displayed on login screen, receipts, backend).
        *   Select from predefined color themes or set primary/accent colors.
        *   Choose from a selection of web-safe fonts for UI elements.
    *   **POS Interface Layout Customization:**
        *   Select from predefined layouts optimized for different screen sizes/orientations (e.g., compact for small tablets, grid for large touchscreens, list for desktops).
        *   Configure quick-select button grids on the POS screen.
    *   Hardware configuration: Printer settings (receipt, kitchen), barcode scanner behavior.
    *   Manage payment gateway configurations.
    *   Configure KRA iTax integration settings.
*   **2.5.3. Target Industries:** Universal.
*   **2.5.4. Functional Overview:** Admins use this module to tailor the Platform to their specific business needs, branding, and operational preferences. Settings here affect system-wide behavior.

### 2.6. Payment Gateway Integration Module
*   **2.6.1. Description:** Securely connects the POS to various third-party payment processors, enabling diverse payment acceptance. **The Platform will not store raw credit card numbers.**
*   **2.6.2. Key Features:**
    *   Secure, server-to-server integration with selected payment gateways.
    *   **Kenyan Payment Gateways:**
        *   **M-Pesa:**
            *   Lipa Na M-Pesa Online (STK Push) for customer-initiated payments.
            *   PayBill/Till Number integration for recording and verifying payments.
            *   Transaction status lookup API integration.
        *   **PesaPal:** Integration for card payments, mobile money.
        *   **Tingg:** Integration for various mobile money and bank payments.
        *   **Other popular Kenyan card processors/aggregators:** DPO Pay, Flutterwave, Pesaflow (evaluate based on market adoption and API capabilities).
    *   Tokenization (via payment gateway) for recurring payments or securely referencing customer payment methods if supported by the gateway.
    *   Handling different payment statuses (pending, success, failed).
    *   Configuration interface to add/manage gateway credentials securely.
    *   Architecture to facilitate adding international payment gateways in the future.
*   **2.6.3. Target Industries:** Universal.
*   **2.6.4. Functional Overview:** When a payment is initiated at the POS, this module securely communicates with the chosen payment gateway to process the transaction. It handles the request, response, and confirmation, ensuring payment data is handled according to security best practices (e.g., PCI DSS compliance through the gateway).

## 3. Optional/Subscribable Standalone Modules

These modules provide specialized functionalities and can be subscribed to by businesses based on their specific requirements and subscription tier. Each module is designed as a standalone functional unit.

### 3.1. Advanced Inventory Management Module
*   **3.1.1. Description:** Extends Basic Inventory with more sophisticated tracking and management features.
*   **3.1.2. Key Features:**
    *   All features of Basic Inventory Management.
    *   Purchase Order (PO) Management: Create, send, and track POs to suppliers.
    *   Supplier Management: Database of suppliers, contact details, products supplied.
    *   Stock Transfers: Manage inventory movement between different locations/branches (requires Multi-Location Module).
    *   Inventory Counts/Stock Takes: Tools for performing full or partial stock counts, with variance reporting.
    *   Product Bundling/Kits: Define products composed of other inventory items; sales of bundles auto-deduct components.
    *   Advanced Variant Management: More complex variant structures (e.g., size/color/material combinations).
    *   Serial Number/Batch Tracking: Track individual items by serial number or products by batch/lot number for traceability (e.g., electronics, perishables). Expiry date tracking for batches.
*   **3.1.3. Target Industries:** Retail (especially with diverse products), Wholesale, Multi-location businesses, Light Manufacturing, Pharmacies, Businesses dealing with perishables or high-value items.
*   **3.1.4. Functional Overview:** Provides tools for more in-depth control over the supply chain, stock accuracy, and product lifecycle, integrating closely with the POS for real-time updates.

### 3.2. Customer Management Module (CRM-Lite)
*   **3.2.1. Description:** Basic customer relationship management features to track customer interactions and foster loyalty. Not a full-fledged CRM but provides foundational capabilities.
*   **3.2.2. Key Features:**
    *   Customer Database: Store customer profiles (name, contact info, address, notes, custom fields).
    *   Purchase History Tracking: View all past transactions linked to a customer.
    *   Basic Customer Segmentation: Tag customers or group them based on purchase history or custom criteria (e.g., "VIP," "New Customer").
    *   Simple Loyalty Programs:
        *   Points-based system: Earn points per amount spent, redeemable for discounts or items.
        *   Tiered rewards (e.g., bronze, silver, gold based on spending).
    *   Gift Card Management: Issue, track balances, and redeem gift cards through the POS.
    *   **Bulk Customer CRUD Operations:** Import/update customer lists via CSV/Excel.
*   **3.2.3. Target Industries:** Retail, Services, Food & Beverage (especially those aiming to build repeat business).
*   **3.2.4. Functional Overview:** Allows businesses to collect customer information at the POS, track their spending habits, and implement simple loyalty initiatives to encourage repeat business.

### 3.3. Order Management Module
*   **3.3.1. Description:** Manages the lifecycle of orders, particularly useful for businesses with complex order fulfillment processes.
*   **3.3.2. Key Features:**
    *   Order status tracking (e.g., Pending, Confirmed, Preparing, Ready for Pickup, Out for Delivery, Completed, Cancelled).
    *   Order modification and history logging.
    *   Special instructions/notes per order or per item within an order.
    *   Order splitting/merging (e.g., splitting a large table's bill, merging take-out orders).
    *   Assignment of orders to staff members or stations.
    *   Real-time updates visible across relevant interfaces (POS, KDS).
*   **3.3.3. Target Industries:** Restaurants, Cafes, Bars, Quick Service Restaurants (QSRs), Cloud Kitchens, Retail with delivery or pick-up services, any business taking pre-orders.
*   **3.3.4. Functional Overview:** Centralizes order information, allowing staff to track and manage orders from initiation to fulfillment, ensuring smooth operations and communication.

### 3.4. Table Management Module
*   **3.4.1. Description:** Visual interface for managing tables and seating in hospitality environments.
*   **3.4.2. Key Features:**
    *   Customizable digital floor plan layout: Drag-and-drop interface to mimic the restaurant's actual layout.
    *   Table status indicators: Visual cues for table status (e.g., Available, Occupied, Reserved, Needs Cleaning, Bill Printed).
    *   Assigning orders/customers to tables.
    *   Tracking table occupancy and turn time.
    *   Merging/splitting tables.
    *   Reservation notes for tables.
*   **3.4.3. Target Industries:** Restaurants (dine-in), Cafes, Bars, Clubs, Hotels with dining facilities.
*   **3.4.4. Functional Overview:** Servers and hosts use the visual floor plan to manage seating, track table status, and link orders directly to tables, improving service efficiency.

### 3.5. Kitchen Display System (KDS) Module
*   **3.5.1. Description:** A digital display system that replaces paper tickets in the kitchen or other preparation areas.
*   **3.5.2. Key Features:**
    *   Real-time display of incoming orders or specific items on screens in the kitchen/bar.
    *   Order prioritization and color-coding (e.g., for new, delayed orders).
    *   Item status updates (e.g., Preparing, Ready) by kitchen staff, reflecting back to POS/Order Management.
    *   Item-level preparation tracking (mark individual items as prepared).
    *   Timers for order preparation duration.
    *   Support for multiple KDS screens for different preparation stations (e.g., hot line, cold line, bar).
    *   Order recall for completed orders.
    *   Sound/visual alerts for new orders.
*   **3.5.3. Target Industries:** Restaurants, Cafes, Bars, QSRs, Cloud Kitchens, Pizza Parlors.
*   **3.5.4. Functional Overview:** Orders from the POS (via the Order Management module) are sent directly to KDS screens. Kitchen staff view orders, manage preparation, and mark items/orders as ready, streamlining kitchen workflow and communication.

### 3.6. Menu Management Module
*   **3.6.1. Description:** Tools for creating, organizing, and customizing menus, especially for food and beverage establishments.
*   **3.6.2. Key Features:**
    *   Creating and organizing menu items into categories (e.g., Appetizers, Main Courses, Drinks).
    *   Modifiers and Add-ons: Define options for items (e.g., "extra cheese," "no onions," "medium-rare") with optional price adjustments.
    *   Combo Meal Creation: Bundle multiple items into a single menu offering.
    *   Scheduled Menus/Pricing: Set different menus or prices for specific times/days (e.g., breakfast menu, lunch specials, happy hour pricing).
    *   Item visibility control (show/hide items from POS quickly).
    *   Option to add item descriptions and images.
    *   Nutritional information and allergen tagging (optional advanced feature within this module).
*   **3.6.3. Target Industries:** Restaurants, Cafes, Bars, QSRs, Hotels, Food Trucks.
*   **3.6.4. Functional Overview:** Allows businesses to easily construct and update their offerings. When an item with modifiers is selected at the POS, the system prompts for choices, ensuring accurate order taking and pricing.

### 3.7. Communication Hub Module
*   **3.7.1. Description:** A centralized platform for sending and scheduling communications to customers.
*   **3.7.2. Key Features:**
    *   Channels:
        *   **SMS:** Integration with local Kenyan SMS gateways (e.g., Africa's Talking, Twilio) for sending messages.
        *   **Email:** Integration with email service providers (e.g., SendGrid, Mailgun) for sending transactional or marketing emails.
    *   Recipient List Management:
        *   Pull customer lists from the Customer Management module (if active).
        *   Upload recipient lists via CSV.
        *   Segment lists based on customer tags or purchase history.
    *   Message Templates: Create and save reusable SMS/Email templates.
    *   Personalization: Use placeholders (e.g., customer name) in messages.
    *   Scheduling: Send communications immediately or schedule for a future date/time.
    *   Basic Analytics: Track sent, delivered status for SMS; sent, delivered, opened for emails (depending on provider capabilities).
*   **3.7.3. Target Industries:** Any business wishing to engage customers through targeted communications (e.g., promotions, appointment reminders, order updates, event announcements).
*   **3.7.4. Functional Overview:** Users select a communication channel, choose recipients, compose or select a message template, and send/schedule the communication. This helps businesses stay connected with their customers.

### 3.8. Commission Management Module
*   **3.8.1. Description:** Calculates and tracks sales commissions for employees.
*   **3.8.2. Key Features:**
    *   Define commission rules:
        *   Percentage of sale value (overall or per item/category).
        *   Fixed amount per item/service sold.
        *   Tiered commissions based on sales targets.
    *   Assign commission rules to specific users/roles or products/services.
    *   Automatic calculation of commissions based on sales data from the POS module.
    *   Commission reports: View earned commissions per employee for a given period.
    *   Option to mark commissions as paid.
*   **3.8.3. Target Industries:** Retail with sales staff, Salons, Service businesses with commissioned employees, Direct sales.
*   **3.8.4. Functional Overview:** After sales are processed, the system automatically attributes sales to employees and calculates their earned commissions based on predefined rules, simplifying payroll and incentive management.

### 3.9. Basic Payroll Module/Export
*   **3.9.1. Description:** Assists with payroll preparation by consolidating relevant data. It is NOT a full payroll processing system.
*   **3.9.2. Key Features:**
    *   Calculates gross pay based on:
        *   Hours worked (from User Management clock-in/out data).
        *   Commissions earned (from Commission Management module, if active).
        *   Fixed salary data (manually entered).
    *   Basic deduction tracking (e.g., advances - manually entered).
    *   Generate payroll summaries/reports per employee for a specified period.
    *   Export payroll data to CSV/Excel format for use with dedicated payroll software or manual processing (e.g., for KRA PAYE, NHIF, NSSF calculations).
*   **3.9.3. Target Industries:** Any business with hourly or commissioned employees needing to simplify payroll data collation.
*   **3.9.4. Functional Overview:** Consolidates working hours and earned commissions to provide a gross pay figure and a structured export that can be fed into external payroll systems for final tax and deduction processing.

### 3.10. KRA iTax Integration Module
*   **3.10.1. Description:** Ensures compliance with Kenya Revenue Authority (KRA) requirements for electronic tax invoicing (e.g., eTIMS).
*   **3.10.2. Key Features:**
    *   Secure integration with KRA's eTIMS API (or relevant system).
    *   Automatic generation of fiscal receipts/invoices with KRA-required information (e.g., QR code, invoice number, Control Unit Serial Number if applicable).
    *   Real-time or batch submission of sales data to KRA systems as per regulations.
    *   Handling of KRA responses and error codes.
    *   Storage of fiscalization data for audit purposes.
    *   Configuration for different KRA device types if required (e.g., Type A, B, C control units – the module would integrate with the software aspect).
    *   Reporting on fiscalized transactions.
*   **3.10.3. Target Industries:** All VAT-registered businesses in Kenya.
*   **3.10.4. Functional Overview:** As sales are completed, this module communicates with KRA's systems to register the invoice, receive fiscal data, and include it on the customer receipt. It ensures that sales records are compliant with KRA regulations. *This requires ongoing attention to KRA's evolving technical specifications.*

### 3.11. Multi-Location Management Module
*   **3.11.1. Description:** Enables businesses with multiple branches or outlets to manage them centrally.
*   **3.11.2. Key Features:**
    *   Centralized dashboard: Overview of sales and performance across all locations.
    *   Consolidated reporting: Aggregate data or view reports per location.
    *   Location-specific settings: Configure some settings (e.g., specific printers, staff) per location while managing others (e.g., core product catalog) centrally.
    *   User access control: Assign users to specific locations or grant access to multiple locations.
    *   Centralized product management with per-location pricing/availability overrides (if needed).
    *   View consolidated inventory levels across locations (requires Advanced Inventory).
    *   Inter-location stock transfers (requires Advanced Inventory).
*   **3.11.3. Target Industries:** Retail chains, Restaurant groups, Service franchises, any business operating from multiple physical sites.
*   **3.11.4. Functional Overview:** Provides a top-level view and control for business owners/managers overseeing multiple outlets, while allowing individual locations to operate their POS and manage local tasks based on centrally defined policies and user permissions.

## 4. Key System-Wide Features & Functionalities

These are overarching features that enhance the usability and power of the Platform across various modules.

### 4.1. Multi-Location Support
*   **How it works:** The system is designed with a hierarchical data model where an "Organization" can have multiple "Locations." Users, products, inventory, sales, and reports can be associated with specific locations or be viewed centrally. Admins can define settings that apply to all locations or customize them per location. Data is segregated logically per location but can be aggregated for reporting and management.

### 4.2. Offline-First POS Operations & Offline Mode
*   **4.2.1. Design Philosophy for Speed and Resilience:**
    *   The Platform is architected with an **offline-first approach for core Point of Sale operations**. This means essential actions like adding items to a cart, modifying quantities, managing concurrent active carts, calculating totals, and processing certain payment types (e.g., cash) are designed to function instantaneously on the client-side (browser/PWA) regardless of internet connectivity status. This ensures a fast, fluid user experience and uninterrupted sales processing even during network outages.
*   **4.2.2. How Offline Mode Works:**
    *   The POS interface, ideally delivered as a **Progressive Web App (PWA)**, caches the essential application shell, user interface elements, and a relevant subset of data (e.g., frequently sold product catalog, user permissions, active cart data).
    *   If internet connectivity is lost (or for intentionally offline terminals):
        *   Core POS functionalities (as mentioned above) continue seamlessly.
        *   **Client-Side Database:** Transactions, cart modifications, and other pending operations are stored locally in the browser's robust storage (e.g., `IndexedDB`).
        *   Payment types requiring immediate online authorization (e.g., live STK push for M-Pesa, real-time card processing) will be clearly indicated as unavailable or will queue the request if the gateway supports deferred processing. Simple recording of "M-Pesa payment received" (to be verified later) would be an offline action.
        *   A clear UI indicator shows offline/online/syncing status.
    *   **Background Synchronization:**
        *   Once connectivity is restored, the application (potentially using Service Workers if a PWA) automatically and efficiently syncs pending transactions and updates with the central server in the background, minimizing disruption to the user.
        *   The backend API is designed to efficiently process these batched/queued essential transactions (sales, inventory updates).
*   **4.2.3. Architectural Approach for Optimal Offline Experience:**
    *   **Progressive Web App (PWA):** Strongly recommended for enabling reliable offline capabilities, installability (add to home screen), and efficient caching.
    *   **Client-Side State Management & Database:** Robust use of `IndexedDB` for storing product catalogs (potentially a "hot" subset for speed, with full lookup deferring to online if needed for obscure items), active transactions, user preferences, and a queue of operations to be synced with the backend.
    *   **Optimistic Updates:** The UI updates immediately upon user action (e.g., item added to cart, quantity changed), providing instant feedback. The system assumes the action is successful locally, and any discrepancies are handled during the backend synchronization process.
    *   **Backend API for Essential Processing:** Backend APIs are optimized for receiving and processing batches of core transactional data (sales, payments recorded offline, inventory adjustments) efficiently once the client syncs. Non-essential data processing or extensive computations can be deferred to reduce immediate load.
    *   **Conflict Resolution Strategy:** A clear strategy for handling data conflicts during synchronization will be implemented (e.g., for inventory levels if multiple offline terminals sell the same last item, it could be first-sync-wins, flagging for manual review, or a more sophisticated reservation system if feasible for critical items).

### 4.3. Customization & Whitelabeling
*   **How it works:**
    *   **Whitelabeling:** Admins can upload their business logo, select color themes (from presets or using a color picker for key UI elements), and choose from a selection of web-safe fonts. These are applied to the backend UI, login pages, and can be pulled into receipt templates.
    *   **POS Layout:** Admins can choose from predefined POS screen layouts (e.g., a compact list for smaller screens, a grid of quick-select buttons for large touchscreens). They can also customize the items and categories appearing on the quick-select buttons.

### 4.4. Bulk Data Operations
*   **How it works:** For entities like Products, Customers, and Users, the system provides:
    *   A feature to download a CSV/Excel template with predefined columns.
    *   Users fill this template with their data.
    *   An upload interface where users can submit the filled file.
    *   The backend parses the file, validates data row by row (e.g., checking for required fields, correct data types, uniqueness constraints).
    *   Successful rows are imported/updated. Errors are reported back to the user, often with row numbers and error descriptions, allowing them to correct and re-upload.

### 4.5. Barcode & QR Code Support
*   **How it works:**
    *   **Scanning:** The POS interface will be compatible with USB and Bluetooth barcode/QR code scanners (typically acting as keyboard input). When a code is scanned into a relevant field (e.g., product search), the system interprets the code to find the item or perform an action.
    *   **Generation (Products):** In the Inventory module, users can auto-generate barcodes (based on SKU or internal ID) or QR codes. For QR codes, users can select what information from the product's database record is encoded (e.g., just ID, or ID + Name + Price). These can then be printed on labels.
    *   **Generation (Receipts):** KRA module will generate specific QR codes on fiscal receipts as per regulations. Other QR codes (e.g., link to a feedback form, business website) can be added to receipt templates.

### 4.6. Secure Login & Authorization Mechanisms
*   **How it works:**
    *   **Standard Login:** Email and hashed passwords (using strong algorithms like Argon2 or bcrypt).
    *   **PIN Login:** Users can be assigned a shorter PIN. This PIN is also securely stored (hashed). Used for quick access at POS terminals. The terminal might first be "unlocked" by a manager, then cashiers can switch using PINs.
    *   **RFID:** If hardware is present (RFID reader), the system can be configured to read RFID tags assigned to users for login or authorization. The RFID tag ID is mapped to a user account.
    *   **Manager Overrides:** Certain actions (e.g., voiding a sale, applying a discount above a threshold) are flagged as requiring higher privileges. If a user without the privilege attempts it, a prompt appears asking for a manager's PIN, password, or RFID scan to authorize that specific action.

### 4.7. API-First Design Approach
*   **How it works:** The entire backend functionality will be exposed through a well-documented RESTful API. The primary web frontend (built with Tailwind CSS) will be a consumer of this API. This means:
    *   Clear separation between frontend and backend logic.
    *   Easier development of alternative frontends (e.g., native mobile apps) in the future.
    *   Ability to offer the API to third-party developers or for custom integrations by clients.
    *   Better testability of backend logic.

## 5. User SaaS Flow

### 5.1. Onboarding & Account Setup
*   **5.1.1. Sign-up (Individual Account):**
    1.  User visits the Platform's website and chooses "Sign Up."
    2.  Selects "Individual/Sole Proprietor" account type.
    3.  Provides basic details: Name, email, password, phone number.
    4.  Agrees to Terms of Service and Privacy Policy.
    5.  Verifies email address via a confirmation link.
    6.  Proceeds to Business Profile Creation.
*   **5.1.2. Sign-up (Organization Account):**
    1.  User visits the Platform's website and chooses "Sign Up."
    2.  Selects "Organization" account type.
    3.  Provides organization name, primary admin user details (name, email, password, phone number).
    4.  Agrees to Terms of Service and Privacy Policy.
    5.  Verifies email address.
    6.  Proceeds to Business Profile Creation.
*   **5.1.3. Business Profile Creation:**
    1.  Logs into the newly created account.
    2.  Enters business name, business type (e.g., Retail, Restaurant, Cafe, Salon - this helps with quick setup).
    3.  Specifies primary location details (address, city).
    4.  Confirms primary currency (KES default).
    5.  Enters KRA PIN.
*   **5.1.4. Module Selection & Quick Setup:**
    1.  Core modules (POS, Basic Inventory, User Management, Basic Reporting, System Settings, Payment Gateway Integration) are enabled by default.
    2.  Based on the selected "Business Type," the system suggests relevant optional modules (e.g., Restaurant -> Table Mgmt, Order Mgmt, KDS, Menu Mgmt).
    3.  User reviews suggested modules and can select/deselect optional modules based on their needs and initial subscription plan (a trial period might grant access to more modules).
    4.  Confirms module selection.
*   **5.1.5. Initial Data Import (Optional but Recommended):**
    1.  Navigate to Inventory > Products. Option to "Add Product" manually or "Import Products."
    2.  Download CSV/Excel template for products.
    3.  Populate template and upload. System validates and imports.
    4.  Similar process for existing Customers (if Customer Management module is active).
*   **5.1.6. Payment Gateway & KRA Configuration:**
    1.  Navigate to System Settings > Payment Gateways.
    2.  Select desired gateways (M-Pesa, PesaPal, etc.).
    3.  Enter secure API credentials/account details for each gateway. Test connection.
    4.  Navigate to System Settings > KRA iTax Configuration.
    5.  Enter relevant KRA device/integration details. Test connection with KRA sandbox (if available).
*   **5.1.7. Branding Customization:**
    1.  Navigate to System Settings > Appearance/Branding.
    2.  Upload business logo.
    3.  Select color theme and fonts.
    4.  Preview changes. Save settings.

### 5.2. Day-to-Day Operations
*   **5.2.1. User Login:**
    *   **Cashier/Staff at POS:** Enters X-digit PIN on the POS terminal screen or swipes RFID card.
    *   **Manager/Admin:** Logs in via email/password (potentially with OTP) on a desktop or tablet.
*   **5.2.2. POS Operations (Cashier Role Example):**
    1.  Start Shift (if clock-in/out is used).
    2.  Access POS screen.
    3.  Add items to cart by:
        *   Tapping quick-select buttons.
        *   Scanning barcode/QR code.
        *   Searching by name/SKU.
    4.  Apply discounts if applicable (may require manager override).
    5.  Select payment method(s) (cash, M-Pesa STK push, card via terminal integrated with gateway).
    6.  Process payment through the integrated gateway.
    7.  Issue receipt (print/email/SMS).
    8.  Handle returns/exchanges as needed.
    9.  End Shift (Z-report might be auto-generated or manually run).
*   **5.2.3. Inventory Management Tasks (Stock Controller Role Example):**
    1.  Receive new stock: Update quantities for products (manually or via PO receiving if Advanced Inventory is active).
    2.  Perform spot checks or scheduled stock counts.
    3.  Add new products or update existing product details.
    4.  Monitor low stock alerts and plan reordering.
*   **5.2.4. Order Management (Restaurant Server/Kitchen Example - requires relevant modules):**
    1.  **Server:** Takes order at table (via tablet POS), selects items, modifiers. Order sent to Order Management & KDS.
    2.  **Kitchen (KDS):** Sees new order on KDS screen. Marks items as "Preparing," then "Ready."
    3.  **Server:** Gets notification (or sees on POS) that order is ready. Delivers to table.
    4.  Updates order status in Order Management if needed.
*   **5.2.5. Table Management (Restaurant Host/Server Example - requires Table Management module):**
    1.  **Host:** Views floor plan, assigns arriving guests to an available table, updates table status to "Occupied."
    2.  **Server:** Selects their table on the POS to add items to that table's order.
    3.  Table status changes as order progresses (e.g., "Bill Printed").
*   **5.2.6. Accessing Reports (Manager/Owner Role Example):**
    1.  Logs into the backend.
    2.  Navigates to the Reporting module.
    3.  Views dashboard KPIs.
    4.  Runs specific reports (e.g., daily sales, product performance, employee sales).
    5.  Exports reports for further analysis or record-keeping.
*   **5.2.7. Using the Communication Hub (Marketing/Manager Role Example - requires Communication Hub):**
    1.  Navigates to Communication Hub.
    2.  Selects channel (SMS/Email).
    3.  Chooses recipient list (e.g., "All Customers," "VIPs," or uploads a list).
    4.  Composes message or selects a template. Personalizes.
    5.  Sends immediately or schedules for later.
    6.  Reviews basic delivery/open analytics.

### 5.3. Management & Configuration (Admin/Manager Roles)
*   **5.3.1. User & Role Management:**
    1.  Navigate to User Management.
    2.  Add new users, assign roles, set PINs/passwords.
    3.  Modify existing user details or permissions.
    4.  Create/edit custom roles and their associated permissions.
    5.  View audit trails.
*   **5.3.2. Module Subscription Management:**
    1.  Navigate to Account Settings > Subscriptions/Modules.
    2.  View currently active modules.
    3.  Option to subscribe to additional available modules or unsubscribe (downgrade) from optional modules, subject to billing cycle and plan.
*   **5.3.3. System & Business Settings Configuration:**
    1.  Access System Settings.
    2.  Update business profile, tax rates, receipt templates, branding.
    3.  Manage payment gateway configurations.
    4.  Adjust KRA integration settings.
    5.  Configure POS layout presets.
*   **5.3.4. Managing Commissions & Payroll Data (requires relevant modules):**
    1.  **Commissions:** Navigate to Commission Management. Define/update commission rules. View calculated commissions for staff. Mark as paid.
    2.  **Payroll:** Navigate to Payroll Export. Select period and employees. Review gross pay summaries (hours, commissions). Export data for external payroll system.

### 5.4. Platform Subscription Management (Account Owner)
*   **5.4.1. Viewing Current Plan:**
    1.  Log in as Account Owner.
    2.  Navigate to Account Settings > Billing/Subscription.
    3.  View current subscription tier, included modules, renewal date, and pricing.
*   **5.4.2. Upgrading/Downgrading Subscription:**
    1.  From Billing/Subscription page, select "Change Plan."
    2.  View available subscription tiers and their features/pricing.
    3.  Select new plan. Confirm changes. Billing will be prorated or adjusted at the next cycle as per policy.

## 6. Kenyan Market Focus & Future Expansion

### 6.1. Localization
*   **Currency:** KES is the default and primary supported currency. All financial transactions and reports will be in KES. The system architecture will store currency codes and allow for the addition of other currencies if/when expanding.
*   **Language:** English.
*   **Date/Time Formats:** Default to Kenyan standard formats.

### 6.2. Payment Gateways for Kenya
As detailed in section 2.6.2, deep integration with M-Pesa (STK Push, Paybill/Till reconciliation), PesaPal, Tingg, and other relevant local card processors is a priority.

### 6.3. KRA iTax Compliance
As detailed in section 3.10, the KRA iTax Integration Module is crucial for ensuring businesses can meet their fiscal reporting obligations seamlessly. This includes generating compliant eTIMS invoices/receipts.

### 6.4. Architecture for Future Market Expansion
*   **Modular Design:** Allows for region-specific modules (e.g., different tax systems, payment gateways) to be developed and plugged in.
*   **API-First:** Facilitates integration with country-specific services.
*   **Configurable Localization:** Currency, language, date formats, and tax rules designed to be configurable.
*   **Cloud Infrastructure:** Choose a cloud provider with global reach to ease deployment in new regions.

## 7. Security Considerations

### 7.1. Data Encryption
*   **In Transit:** All communication between the client (browser) and the server, and between the server and third-party services (payment gateways, KRA), will use HTTPS with strong TLS encryption.
*   **At Rest:** Sensitive data in the PostgreSQL database (e.g., user credentials, business financial data) will be encrypted using industry-standard encryption mechanisms (e.g., AES-256). Particular attention to encrypting personally identifiable information (PII).
*   **UUIDs:** All major models (User, Organization, Role, etc.) will include a UUID field (models.UUIDField) in addition to the default Django primary key, to ensure secure, non-predictable identifiers for API and external references.

### 7.2. User Authentication & Authorization
*   Strong password policies enforced (complexity, length).
*   Secure hashing of passwords and PINs (e.g., Argon2, bcrypt).
*   Role-based access control (RBAC) to ensure users can only access data and functions relevant to their roles.
*   Session management with timeouts and secure cookie handling.
*   Protection against common web vulnerabilities (OWASP Top 10), including SQL Injection, XSS, CSRF, through Django's built-in protections and best practices.

### 7.3. Payment Security
*   **No local storage of raw cardholder data.** All card processing will be handled by PCI DSS compliant third-party payment gateways.
*   Secure transmission of payment information to gateways.
*   If tokenization is used, tokens are stored securely, not the actual PAN.

### 7.4. Audit Trails
*   Comprehensive logging of significant events: user logins (success/failure), access to sensitive data, changes to critical settings, financial transactions, administrative actions.
*   Audit logs should be immutable or have strong integrity checks and be regularly reviewed.

### 7.5. Regular Security Audits & Updates
*   Plan for regular security code reviews and penetration testing (manual and automated).
*   Keep all system components, libraries (Django, PostgreSQL, etc.), and server software up to date with security patches.
*   Implement intrusion detection/prevention systems (IDS/IPS) at the network level.
*   Data backup and disaster recovery plan.

## 8. Suggested Project Structure

```
Calm-POS/
├── core/                 
│   ├── asgi.py           
│   ├── settings.py       
│   ├── urls.py           
│   ├── wsgi.py           
│   └── __init__.py       
├── accounts/             
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── sales/                
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── inventory/            
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── reports/              
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── core_settings/        
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── payments/             
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── advanced_inventory/   
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── crm/                  
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── orders/               
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── hospitality/          
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── kds/                  
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── menu/                 
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── communications/       
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── commissions/          
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── payroll/              
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── kra_integration/      
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── logs/                 
│   └── django.log        
├── static/               
├── .env                  
├── .env.example          
├── .gitignore            
├── manage.py             
├── plan.md               
├── README.md             
└── requirements.txt      
```

## 9. Project Rules & Technical Guidelines

*   All forms and validation will be handled via Django views and HTTP methods (POST, etc.), not Django forms. No use of Django's form classes in this project.
*   All major models must include a UUID field for secure, non-sequential identification.
*   Use Django signals for post-save, post-delete, and other event hooks (e.g., logging, notifications, updating related models).
*   All authentication and user management must use a custom user model and custom user manager from the start.
*   User and organization preferences must be stored in dedicated models (UserPreferences, OrganizationPreferences).
*   All permissions must be string constants and easily queryable via user.has_permission(Permissions.SOME_PERMISSION).
*   TFA/2FA must be supported and enforceable by admin, with middleware to require resets as needed.
*   Detailed logging and audit trails are required for all significant user and system actions.
*   Password reset tokens/codes must be tracked in a dedicated model.
*   Use a single full_name field for user names.
*   Superuser/platform admin is handled using Django's is_staff and is_superuser fields only.